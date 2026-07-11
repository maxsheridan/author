#!/usr/bin/env python3
"""
minify_shared_css.py

Regenerates shared.min.css from shared.css whenever shared.css changes.

Note: this is a full regeneration, not a patch. Minifiers always work
this way (cssnano, clean-css, esbuild, etc.) — they re-minify the whole
source rather than trying to patch just the changed rules inside an
already-minified file, which would be fragile and error-prone.

USAGE:

    python minify_shared_css.py shared.css shared.min.css

    # Or watch for changes and auto-regenerate on save:
    python minify_shared_css.py shared.css shared.min.css --watch

LIMITATIONS:

    This uses a lightweight regex-based minifier (comment stripping +
    whitespace collapsing), which covers standard CSS well but can
    mishandle edge cases like braces or semicolons inside quoted
    string values (e.g. content: "a;b"). If your CSS relies on that,
    consider swapping in a proper minifier library (e.g. `rcssmin` or
    `csscompressor` via pip, or Node's `clean-css-cli`) — the sync/
    watch logic below would stay the same either way.
"""

import argparse
import re
import sys
import time
from pathlib import Path


def minify_css(css: str) -> str:
    # Strip comments
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
    # Collapse all whitespace (including newlines) to single spaces
    css = re.sub(r"\s+", " ", css)
    # Remove whitespace around punctuation that doesn't need it
    css = re.sub(r"\s*([{}:;,])\s*", r"\1", css)
    # Remove the now-redundant trailing semicolon before a closing brace
    css = re.sub(r";}", "}", css)
    return css.strip()


def sync(source_path: Path, output_path: Path) -> bool:
    source_css = source_path.read_text(encoding="utf-8")
    minified = minify_css(source_css)

    if output_path.exists() and output_path.read_text(encoding="utf-8") == minified:
        return False

    output_path.write_text(minified, encoding="utf-8")
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_css", type=Path, help="e.g. shared.css")
    parser.add_argument("output_css", type=Path, help="e.g. shared.min.css")
    parser.add_argument(
        "--watch", action="store_true", help="Re-minify automatically on save"
    )
    args = parser.parse_args()

    if not args.source_css.exists():
        sys.exit(f"File not found: {args.source_css}")

    if not args.watch:
        changed = sync(args.source_css, args.output_css)
        print(f"{args.output_css} updated." if changed else "Already in sync — no changes.")
        return

    print(f"Watching {args.source_css} for changes... (Ctrl+C to stop)")
    last_mtime = args.source_css.stat().st_mtime
    try:
        while True:
            time.sleep(1)
            mtime = args.source_css.stat().st_mtime
            if mtime != last_mtime:
                last_mtime = mtime
                changed = sync(args.source_css, args.output_css)
                if changed:
                    print(f"{args.source_css} changed — {args.output_css} re-minified.")
    except KeyboardInterrupt:
        print("\nStopped watching.")


if __name__ == "__main__":
    main()