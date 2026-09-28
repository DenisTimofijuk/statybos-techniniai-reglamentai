#!/usr/bin/env python3
"""Mechanical knowledge-base hygiene checks.

This script deliberately checks structure, not legal meaning. It should flag
candidates for human/AI review rather than mutate repository knowledge.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from urllib.parse import urlparse


EXPECTED_PATHS = [
    "AGENTS.md",
    "PROJECT_GUIDE.md",
    "data/str-catalog.json",
    "knowledge/REGULATION_MAP.md",
    "knowledge/COMMON_DECISION_PATHS.md",
    "knowledge/TRANSITIONS_2027.md",
    "maintenance/KNOWLEDGE_AUDIT.md",
    "maintenance/audit-state.json",
]

CATALOG_REQUIRED_FIELDS = [
    "code",
    "title",
    "status",
    "source_url",
    "source_registry",
    "vtpsi_listed",
    "vtpsi_snapshot_date",
    "topics",
]

REPO_PATH_RE = re.compile(
    r"(?<![A-Za-z0-9_.-])"
    r"((?:knowledge|data|scripts|maintenance)/[A-Za-z0-9_.\-/]+)"
)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)


@dataclass
class Finding:
    severity: str
    check: str
    message: str
    path: str | None = None


def add(findings, severity, check, message, path=None):
    findings.append(Finding(severity, check, message, path))


def load_json(path: Path, findings: list[Finding]):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        add(findings, "error", "json", "File does not exist", str(path))
    except json.JSONDecodeError as exc:
        add(
            findings,
            "error",
            "json",
            f"Invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}",
            str(path),
        )
    return None


def check_expected_paths(root: Path, findings: list[Finding]) -> None:
    for rel in EXPECTED_PATHS:
        if not (root / rel).exists():
            add(findings, "error", "expected-path", "Expected file is missing", rel)


def check_catalog(root: Path, findings: list[Finding]) -> None:
    path = root / "data/str-catalog.json"
    catalog = load_json(path, findings)
    if not isinstance(catalog, dict):
        return

    regs = catalog.get("regulations")
    if not isinstance(regs, list):
        add(findings, "error", "catalog", "'regulations' must be a list", str(path))
        return

    declared_count = catalog.get("regulation_count")
    if declared_count != len(regs):
        add(
            findings,
            "error",
            "catalog-count",
            f"regulation_count={declared_count!r}, actual={len(regs)}",
            str(path),
        )

    codes = []
    source_urls = defaultdict(list)

    for index, item in enumerate(regs):
        label = f"regulations[{index}]"
        if not isinstance(item, dict):
            add(findings, "error", "catalog-item", "Entry must be an object", label)
            continue

        missing = [field for field in CATALOG_REQUIRED_FIELDS if field not in item]
        if missing:
            add(
                findings,
                "error",
                "catalog-fields",
                f"Missing required fields: {', '.join(missing)}",
                label,
            )

        code = item.get("code")
        if isinstance(code, str) and code.strip():
            codes.append(code)
        else:
            add(findings, "error", "catalog-code", "Missing/empty STR code", label)

        url = item.get("source_url")
        if isinstance(url, str) and url:
            parsed = urlparse(url)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                add(findings, "error", "source-url", f"Malformed URL: {url}", label)
            source_urls[url].append(code or label)

        topics = item.get("topics")
        if "topics" in item and (
            not isinstance(topics, list)
            or not topics
            or any(not isinstance(topic, str) or not topic.strip() for topic in topics)
        ):
            add(
                findings,
                "warning",
                "catalog-topics",
                "topics should be a non-empty list of non-empty strings",
                label,
            )

    for code, count in Counter(codes).items():
        if count > 1:
            add(
                findings,
                "error",
                "duplicate-code",
                f"Regulation code occurs {count} times: {code}",
                str(path),
            )

    for url, labels in source_urls.items():
        if len(labels) > 1:
            add(
                findings,
                "warning",
                "duplicate-source-url",
                f"Source URL is shared by multiple entries: {', '.join(labels)} -> {url}",
                str(path),
            )


def clean_repo_reference(raw: str) -> str:
    return raw.rstrip(".,;:!?)]}'\"")


def check_repo_references(root: Path, findings: list[Finding]) -> None:
    text_files = list(root.glob("*.md"))
    for folder in ("knowledge", "maintenance"):
        if (root / folder).exists():
            text_files.extend((root / folder).rglob("*.md"))

    seen = set()
    for path in text_files:
        text = path.read_text(encoding="utf-8")

        for match in REPO_PATH_RE.finditer(text):
            rel = clean_repo_reference(match.group(1))
            key = (str(path.relative_to(root)), rel)
            if key in seen:
                continue
            seen.add(key)
            if not (root / rel).exists():
                add(
                    findings,
                    "warning",
                    "repo-reference",
                    f"Referenced repository path does not exist: {rel}",
                    str(path.relative_to(root)),
                )

        for target in MARKDOWN_LINK_RE.findall(text):
            target = target.strip()
            if (
                not target
                or target.startswith(("#", "http://", "https://", "mailto:"))
            ):
                continue
            target = target.split("#", 1)[0]
            candidate = (path.parent / target).resolve()
            try:
                candidate.relative_to(root.resolve())
            except ValueError:
                continue
            if not candidate.exists():
                add(
                    findings,
                    "warning",
                    "markdown-link",
                    f"Broken local markdown link: {target}",
                    str(path.relative_to(root)),
                )


def check_duplicate_headings(root: Path, findings: list[Finding]) -> None:
    for folder in ("knowledge", "maintenance"):
        base = root / folder
        if not base.exists():
            continue
        for path in base.rglob("*.md"):
            headings = [h.strip().lower() for h in HEADING_RE.findall(path.read_text(encoding="utf-8"))]
            for heading, count in Counter(headings).items():
                if count > 1:
                    add(
                        findings,
                        "warning",
                        "duplicate-heading",
                        f"Heading occurs {count} times: {heading}",
                        str(path.relative_to(root)),
                    )


def check_audit_state(root: Path, findings: list[Finding]) -> None:
    path = root / "maintenance/audit-state.json"
    state = load_json(path, findings)
    if not isinstance(state, dict):
        return

    if state.get("schema_version") != 1:
        add(
            findings,
            "warning",
            "audit-state",
            f"Unexpected schema_version: {state.get('schema_version')!r}",
            str(path.relative_to(root)),
        )

    for field in ("last_full_audit", "last_mechanical_audit", "last_vtpsi_check"):
        if field not in state:
            add(findings, "warning", "audit-state", f"Missing field: {field}", str(path.relative_to(root)))

    if not isinstance(state.get("open_issues", []), list):
        add(findings, "error", "audit-state", "open_issues must be a list", str(path.relative_to(root)))


def build_report(root: Path) -> dict:
    findings: list[Finding] = []
    check_expected_paths(root, findings)
    check_catalog(root, findings)
    check_repo_references(root, findings)
    check_duplicate_headings(root, findings)
    check_audit_state(root, findings)

    counts = Counter(f.severity for f in findings)
    return {
        "root": str(root),
        "summary": {
            "errors": counts.get("error", 0),
            "warnings": counts.get("warning", 0),
            "findings": len(findings),
        },
        "findings": [asdict(f) for f in findings],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--report", default="knowledge-audit-report.json")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return non-zero when any error or warning is found.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    report = build_report(root)

    Path(args.report).write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))

    summary = report["summary"]
    if summary["errors"]:
        return 2
    if args.strict and summary["warnings"]:
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
