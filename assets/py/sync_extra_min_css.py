#!/usr/bin/env python3
"""
sync_extra_min_css.py

Extracts the minified rules starting from the `.flex` selector from a
minified style stylesheet and writes them into extra.min.css.
"""

import argparse
import re
import sys
from pathlib import Path


def sync(source_path: Path, output_path: Path, start_selector: str) -> bool:
    css = source_path.read_text(encoding="utf-8")
    match = re.search(re.escape(start_selector) + r"\{", css)
    if match is None:
        raise ValueError(
            f"Start selector {start_selector!r} not found in {source_path}"
        )
    extracted = css[match.start():].strip()

    if output_path.exists() and output_path.read_text(encoding="utf-8") == extracted:
        return False

    output_path.write_text(extracted, encoding="utf-8")
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_css", type=Path, help="Minified style.css file")
    parser.add_argument("output_css", type=Path, help="extra.min.css output file")
    parser.add_argument(
        "--selector",
        default=".flex",
        help="Starting selector to extract from the minified file",
    )
    args = parser.parse_args()

    if not args.source_css.exists():
        sys.exit(f"File not found: {args.source_css}")

    changed = sync(args.source_css, args.output_css, args.selector)
    print(f"{args.output_css} updated." if changed else "Already in sync — no changes.")


if __name__ == "__main__":
    main()
