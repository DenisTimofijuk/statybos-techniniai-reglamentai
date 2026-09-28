#!/usr/bin/env python3
"""Small offline router over data/str-catalog.json."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", value.lower()).strip()


def score(item: dict, terms: list[str]) -> int:
    code = norm(item["code"])
    title = norm(item["title"])
    topics = norm(" ".join(item.get("topics", [])))
    haystack = f"{code} {title} {topics}"
    value = 0
    for term in terms:
        if term in code:
            value += 8
        if term in title:
            value += 5
        if term in topics:
            value += 3
        if term in haystack:
            value += 1
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="+")
    parser.add_argument("--catalog", default="data/str-catalog.json")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    data = json.loads(Path(args.catalog).read_text(encoding="utf-8"))
    terms = [norm(x) for x in args.query if norm(x)]

    ranked = []
    for item in data["regulations"]:
        points = score(item, terms)
        if points:
            ranked.append((points, item))
    ranked.sort(key=lambda x: (-x[0], x[1]["code"]))

    for points, item in ranked[: args.limit]:
        validity = item["status"]
        if "valid_until" in item:
            validity += f"; valid_until={item['valid_until']}"
        if "effective_from" in item:
            validity += f"; effective_from={item['effective_from']}"
        print(f"{points:>3}  {item['code']}  {item['title']}  [{validity}]")
        print(f"     {item['source_url']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
