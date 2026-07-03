#!/usr/bin/env python3

import argparse
import csv
import json
import os
from typing import Iterable, Optional


SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_WATCHED_CSV = os.path.join(SKILL_ROOT, "references", "watched.csv")


def normalize_title(value: Optional[str]) -> str:
    if not value:
        return ""
    return value.strip().strip('"').lower()


def load_watched_titles(csv_path: str) -> set[str]:
    with open(csv_path, encoding="utf-8") as handle:
        rows = list(csv.reader(handle, delimiter="\t"))

    watched_titles: set[str] = set()
    for row in rows[1:]:
        if len(row) > 3:
            watched_titles.add(normalize_title(row[3]))
        if len(row) > 4:
            watched_titles.add(normalize_title(row[4]))
    watched_titles.discard("")
    return watched_titles


def iter_candidates(values: Iterable[str]) -> list[dict[str, str]]:
    candidates: list[dict[str, str]] = []
    for value in values:
        parts = [part.strip() for part in value.split("|", 1)]
        if len(parts) == 2:
            title_ru, title_orig = parts
        else:
            title_ru = parts[0]
            title_orig = ""
        candidates.append({
            "title_ru": title_ru,
            "title_orig": title_orig,
        })
    return candidates


def is_watched(watched_titles: set[str], title_ru: str = "", title_orig: str = "") -> bool:
    return normalize_title(title_ru) in watched_titles or normalize_title(title_orig) in watched_titles


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check whether movie or TV titles already exist in Kinorium watched.csv.",
    )
    parser.add_argument(
        "titles",
        nargs="+",
        help="Candidate title as 'Russian Title|Original Title' or just 'Title'.",
    )
    parser.add_argument(
        "--csv",
        default=DEFAULT_WATCHED_CSV,
        help="Path to watched.csv.",
    )
    args = parser.parse_args()

    watched_titles = load_watched_titles(args.csv)
    results = []
    for candidate in iter_candidates(args.titles):
        results.append({
            **candidate,
            "watched": is_watched(
                watched_titles,
                title_ru=candidate["title_ru"],
                title_orig=candidate["title_orig"],
            ),
        })

    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())