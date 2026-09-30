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
DATE_RE = re.compile(r"Atnaujinimo data:\s*(\d{4}-\d{2}-\d{2})")
STR_RE = re.compile(r"STR\s+\d\.\d{2}\.\d{2}(?:\(\d\))?:\d{4}")

EXIT_FRESH = 0
EXIT_STALE = 2
EXIT_CHECK_ERROR = 3

# The LRV frontend has rejected obvious bot-style requests from GitHub-hosted
# runners. These are ordinary browser-compatible request headers for a public
# HTML page; the repository identity is still exposed separately below.
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
    "X-Automation-Source": "github.com/DenisTimofijuk/statybos-techniniai-reglamentai",
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
    session.headers.update(BROWSER_HEADERS)
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session


def fetch_live(source: str, timeout: int = 30) -> tuple[str, list[str]]:
    with build_session() as session:
        response = session.get(source, timeout=timeout)
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
        live_date, live_codes = fetch_live(args.source)
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
    fresh = live_date == stored_date and not added and not removed

    report = {
        "status": "fresh" if fresh else "stale",
        "source": args.source,
        "stored_update_date": stored_date,
        "live_update_date": live_date,
        "stored_count": len(stored_codes),
        "live_count": len(live_codes),
        "added_codes": added,
        "removed_codes": removed,
        "fresh": fresh,
    }
    write_report(args.report, report)

    if fresh:
        return EXIT_FRESH

    print(
        "VTPSI STR index differs from the committed baseline. Review and update the catalog.",
        file=sys.stderr,
    )
    return EXIT_STALE


if __name__ == "__main__":
    raise SystemExit(main())
