#!/usr/bin/env python3
"""
inline_critical_css.py

Takes critical.css, strips out the AUTO-SYNCED marker comments, minifies
the rest, and writes it into a specific <style> tag in index.html.

SETUP (one-time):

In index.html, give the critical <style> tag an id so this script
targets exactly the right one:

    <style id="critical-css">
      /* this content gets replaced automatically */
    </style>

USAGE:

    python inline_critical_css.py critical.css index.html

    # Watch mode:
    python inline_critical_css.py critical.css index.html --watch
"""

import argparse
import re
import sys
import time
from pathlib import Path

MARKER_START = "/* AUTO-SYNCED FROM shared.css — DO NOT EDIT BELOW — START */"
MARKER_END = "/* AUTO-SYNCED FROM shared.css — END */"
STYLE_ID = "critical-css"


def minify_css(css: str) -> str:
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{}:;,])\s*", r"\1", css)
    css = re.sub(r";}", "}", css)
    return css.strip()


def strip_markers(css: str) -> str:
    css = css.replace(MARKER_START, "")
    css = css.replace(MARKER_END, "")
    return css


def sync(critical_path: Path, html_path: Path) -> bool:
    critical_css = critical_path.read_text(encoding="utf-8")
    html = html_path.read_text(encoding="utf-8")

    cleaned = strip_markers(critical_css)
    minified = minify_css(cleaned)

    pattern = re.compile(
        r'(<style\s+id=["\']' + re.escape(STYLE_ID) + r'["\'][^>]*>)(.*?)(</style>)',
        re.DOTALL,
    )

    if not pattern.search(html):
        print(
            f'ERROR: no <style id="{STYLE_ID}"> tag found in {html_path}.\n'
            f'Add one, e.g.:\n\n  <style id="{STYLE_ID}"></style>\n',
            file=sys.stderr,
        )
        sys.exit(1)

    updated_html, count = pattern.subn(
        lambda m: f"{m.group(1)}{minified}{m.group(3)}", html
    )

    if updated_html == html:
        return False

    html_path.write_text(updated_html, encoding="utf-8")
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("critical_css", type=Path)
    parser.add_argument("index_html", type=Path)
    parser.add_argument("--watch", action="store_true")
    args = parser.parse_args()

    if not args.critical_css.exists():
        sys.exit(f"File not found: {args.critical_css}")
    if not args.index_html.exists():
        sys.exit(f"File not found: {args.index_html}")

    if not args.watch:
        changed = sync(args.critical_css, args.index_html)
        print(f"{args.index_html} updated." if changed else "Already in sync — no changes.")
        return

    print(f"Watching {args.critical_css} for changes... (Ctrl+C to stop)")
    last_mtime = args.critical_css.stat().st_mtime
    try:
        while True:
            time.sleep(1)
            mtime = args.critical_css.stat().st_mtime
            if mtime != last_mtime:
                last_mtime = mtime
                changed = sync(args.critical_css, args.index_html)
                if changed:
                    print(f"{args.critical_css} changed — {args.index_html} re-synced.")
    except KeyboardInterrupt:
        print("\nStopped watching.")


if __name__ == "__main__":
    main()
