#!/usr/bin/env python3
"""Check whether the VTPSI STR index is newer/different than our committed catalog."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

DEFAULT_SOURCE = "https://vtpsi.lrv.lt/lt/teisine-informacija/teises-aktai-2/statybos-techniniai-reglamentai/"
READER_PREFIX = "https://r.jina.ai/"
DATE_RE = re.compile(r"Atnaujinimo data:\s*(\d{4}-\d{2}-\d{2})")
STR_RE = re.compile(r"STR\s+\d\.\d{2}\.\d{2}(?:\(\d\))?:\d{4}")

EXIT_FRESH = 0
EXIT_STALE = 2
EXIT_CHECK_ERROR = 3

BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "lt-LT,lt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
}


def unique_in_order(values):
    seen = set()
    result = []
    for value in values:
        value = " ".join(value.split())
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def build_session() -> requests.Session:
    retry = Retry(
        total=3,
        connect=3,
        read=3,
        status=3,
        backoff_factor=1.0,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET"}),
        raise_on_status=False,
    )
    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session


def normalize_text(content: str) -> str:
    return BeautifulSoup(content, "html.parser").get_text(" ", strip=True)


def extract_codes(text: str) -> list[str]:
    codes = unique_in_order(STR_RE.findall(text))
    if not codes:
        raise RuntimeError("Could not find any STR codes on VTPSI content")
    return codes


def extract_full(content: str) -> tuple[str, list[str]]:
    text = normalize_text(content)
    date_match = DATE_RE.search(text)
    if not date_match:
        raise RuntimeError("Could not find 'Atnaujinimo data' on VTPSI content")
    return date_match.group(1), extract_codes(text)


def fetch_live(source: str, timeout: int = 30) -> tuple[str | None, list[str], str, str, str | None]:
    """Return date, codes, transport, scope, and direct-fetch error if degraded."""
    direct_error: Exception | None = None

    with build_session() as session:
        try:
            response = session.get(source, headers=BROWSER_HEADERS, timeout=timeout)
            response.raise_for_status()
            live_date, live_codes = extract_full(response.text)
            return live_date, live_codes, "direct", "full", None
        except (requests.RequestException, RuntimeError) as exc:
            direct_error = exc

        reader_url = f"{READER_PREFIX}{source}"
        try:
            response = session.get(
                reader_url,
                headers={
                    "Accept": "text/plain",
                    "X-No-Cache": "true",
                    "DNT": "1",
                },
                timeout=timeout,
            )
            response.raise_for_status()
            text = normalize_text(response.text)
            live_codes = extract_codes(text)
            date_match = DATE_RE.search(text)
            live_date = date_match.group(1) if date_match else None
            scope = "full" if live_date else "code_set_only"
            return live_date, live_codes, "jina_reader_no_cache", scope, str(direct_error)
        except (requests.RequestException, RuntimeError) as fallback_error:
            raise RuntimeError(
                f"Direct VTPSI fetch failed ({type(direct_error).__name__}: {direct_error}); "
                f"fresh rendering fallback also failed ({type(fallback_error).__name__}: {fallback_error})"
            ) from fallback_error


def write_report(path: str, report: dict) -> None:
    Path(path).write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", default="data/str-catalog.json")
    parser.add_argument("--source", default=DEFAULT_SOURCE)
    parser.add_argument("--report", default="freshness-report.json")
    args = parser.parse_args()

    catalog = json.loads(Path(args.catalog).read_text(encoding="utf-8"))
    stored_date = catalog["vtpsi_update_date"]
    stored_codes = [item["code"] for item in catalog["regulations"]]

    try:
        live_date, live_codes, transport, check_scope, direct_error = fetch_live(args.source)
    except Exception as exc:
        report = {
            "status": "check_error",
            "source": args.source,
            "stored_update_date": stored_date,
            "error_type": type(exc).__name__,
            "error": str(exc),
        }
        write_report(args.report, report)
        print(
            "Could not complete the VTPSI freshness check. This is not evidence that the catalog is stale.",
            file=sys.stderr,
        )
        return EXIT_CHECK_ERROR

    added = [code for code in live_codes if code not in stored_codes]
    removed = [code for code in stored_codes if code not in live_codes]
    code_set_changed = bool(added or removed)
    date_changed = live_date is not None and live_date != stored_date
    stale = code_set_changed or date_changed

    if stale:
        status = "stale"
    elif check_scope == "full":
        status = "fresh"
    else:
        status = "partial_fresh"

    report = {
        "status": status,
        "source": args.source,
        "transport": transport,
        "check_scope": check_scope,
        "stored_update_date": stored_date,
        "live_update_date": live_date,
        "stored_count": len(stored_codes),
        "live_count": len(live_codes),
        "added_codes": added,
        "removed_codes": removed,
        "fresh": status == "fresh",
    }
    if direct_error:
        report["direct_fetch_error"] = direct_error
    write_report(args.report, report)

    if stale:
        print(
            "VTPSI STR index differs from the committed baseline. Review and verify the official source before updating the catalog.",
            file=sys.stderr,
        )
        return EXIT_STALE

    if status == "partial_fresh":
        print(
            "WARNING: GitHub runner could not verify the VTPSI page update date directly. "
            "The no-cache fallback confirmed only that the STR code set is unchanged; same-code amendments may not be detected.",
            file=sys.stderr,
        )

    return EXIT_FRESH


if __name__ == "__main__":
    raise SystemExit(main())
