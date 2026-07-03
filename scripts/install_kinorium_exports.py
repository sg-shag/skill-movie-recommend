#!/usr/bin/env python3

import argparse
import glob
import os
from datetime import date


SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DOWNLOADS_DIR = os.path.expanduser("~/Downloads")
DEFAULT_REFERENCES_DIR = os.path.join(SKILL_ROOT, "references")


def install_export(downloads_dir: str, references_dir: str, pattern: str, destination_name: str) -> bool:
    matches = sorted(glob.glob(os.path.join(downloads_dir, pattern)))
    if not matches:
        print(f"Not found: {pattern}")
        return False

    source_path = matches[-1]
    destination_path = os.path.join(references_dir, destination_name)
    with open(source_path, "rb") as source_handle:
        text = source_handle.read().decode("utf-16")
    with open(destination_path, "w", encoding="utf-8") as destination_handle:
        destination_handle.write(text)
    print(f"Written: {destination_name} <- {os.path.basename(source_path)}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install Kinorium CSV exports into this skill's references directory.",
    )
    parser.add_argument(
        "--downloads-dir",
        default=DEFAULT_DOWNLOADS_DIR,
        help="Directory containing Kinorium backup CSV attachments.",
    )
    parser.add_argument(
        "--references-dir",
        default=DEFAULT_REFERENCES_DIR,
        help="Destination references directory.",
    )
    args = parser.parse_args()

    os.makedirs(args.references_dir, exist_ok=True)
    mappings = [
        ("backup_*_votes.csv", "watched.csv"),
        ("backup_*_movie_list.csv", "watchlist.csv"),
    ]

    install_results = []
    for pattern, destination_name in mappings:
        install_results.append(install_export(args.downloads_dir, args.references_dir, pattern, destination_name))

    if all(install_results):
        date_path = os.path.join(args.references_dir, "kinorium_date.txt")
        with open(date_path, "w", encoding="utf-8") as handle:
            handle.write(f"{date.today():%Y-%m-%d}\n")
        print("Updated: kinorium_date.txt")
        return 0

    print("Refresh incomplete: kinorium_date.txt not updated.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())