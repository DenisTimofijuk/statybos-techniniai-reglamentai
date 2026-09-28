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

DEFAULT_SOURCE = "https://vtpsi.lrv.lt/lt/teisine-informacija/teises-aktai-2/statybos-techniniai-reglamentai/"
DATE_RE = re.compile(r"Atnaujinimo data:\s*(\d{4}-\d{2}-\d{2})")
STR_RE = re.compile(r"STR\s+\d\.\d{2}\.\d{2}(?:\(\d\))?:\d{4}")


def unique_in_order(values):
    seen = set()
    result = []
    for value in values:
        value = " ".join(value.split())
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def fetch_live(source: str, timeout: int = 30) -> tuple[str, list[str]]:
    headers = {
        "User-Agent": "statybos-techniniai-reglamentai-monitor/1.0 (+GitHub repository freshness check)"
    }
    response = requests.get(source, headers=headers, timeout=timeout)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(" ", strip=True)

    date_match = DATE_RE.search(text)
    if not date_match:
        raise RuntimeError("Could not find 'Atnaujinimo data' on VTPSI page")

    codes = unique_in_order(STR_RE.findall(text))
    if not codes:
        raise RuntimeError("Could not find any STR codes on VTPSI page")

    return date_match.group(1), codes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", default="data/str-catalog.json")
    parser.add_argument("--source", default=DEFAULT_SOURCE)
    parser.add_argument("--report", default="freshness-report.json")
    args = parser.parse_args()

    catalog = json.loads(Path(args.catalog).read_text(encoding="utf-8"))
    stored_date = catalog["vtpsi_update_date"]
    stored_codes = [item["code"] for item in catalog["regulations"]]

    live_date, live_codes = fetch_live(args.source)

    added = [code for code in live_codes if code not in stored_codes]
    removed = [code for code in stored_codes if code not in live_codes]

    report = {
        "source": args.source,
        "stored_update_date": stored_date,
        "live_update_date": live_date,
        "stored_count": len(stored_codes),
        "live_count": len(live_codes),
        "added_codes": added,
        "removed_codes": removed,
        "fresh": live_date == stored_date and not added and not removed,
    }

    Path(args.report).write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))

    if report["fresh"]:
        return 0

    print(
        "VTPSI STR index differs from the committed baseline. Review and update the catalog.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
