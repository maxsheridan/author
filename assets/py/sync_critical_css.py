#!/usr/bin/env python3
"""
sync_critical_css.py

Keeps a "borrowed" section of critical.css in sync with a marked
block of rules in shared.css (e.g. @font-face, resets, body styles).

SETUP (one-time):

1. In shared.css, wrap the rules you've duplicated into critical.css
with a single start/end marker pair:

    /* @critical-sync:start */
    @font-face {
        font-family: 'MyFont';
        src: url('/fonts/main.woff2') format('woff2');
        font-display: swap;
    }

    *, *::before, *::after {
        box-sizing: border-box;
        margin: 0;
    }

    body {
        font-family: 'MyFont', sans-serif;
    }
    /* @critical-sync:end */

Everything between those two comments is copied as-is — no need
to tag individual rules. You can have more than one wrapped block
in shared.css if the borrowed rules aren't contiguous; all blocks
are concatenated in order.

2. In critical.css, add markers where the synced rules should land:

    /* AUTO-SYNCED FROM shared.css — DO NOT EDIT BELOW — START */
    /* AUTO-SYNCED FROM shared.css — END */

(Anything between these two lines gets overwritten on every run,
so don't hand-edit that block.)

USAGE:

    python sync_critical_css.py shared.css critical.css

    # Or watch for changes and auto-sync on save:
    python sync_critical_css.py shared.css critical.css --watch
"""

import argparse
import re
import sys
import time
from pathlib import Path

DEST_START = "/* AUTO-SYNCED FROM shared.css — DO NOT EDIT BELOW — START */"
DEST_END = "/* AUTO-SYNCED FROM shared.css — END */"
SRC_START = "/* @critical-sync:start */"
SRC_END = "/* @critical-sync:end */"


def extract_wrapped_blocks(css_text: str) -> list[str]:
    """Return the raw contents of every SRC_START...SRC_END block in
    shared.css, in order, with the markers themselves stripped out."""
    pattern = re.compile(
        re.escape(SRC_START) + r"(.*?)" + re.escape(SRC_END), re.DOTALL
    )
    blocks = [m.strip() for m in pattern.findall(css_text)]
    return blocks


def sync(shared_path: Path, critical_path: Path) -> bool:
    shared_css = shared_path.read_text(encoding="utf-8")
    critical_css = critical_path.read_text(encoding="utf-8")

    if DEST_START not in critical_css or DEST_END not in critical_css:
        print(
            f"ERROR: {critical_path} is missing the sync markers.\n"
            f"Add these two lines where the synced rules should go:\n\n"
            f"  {DEST_START}\n  {DEST_END}\n",
            file=sys.stderr,
        )
        sys.exit(1)

    blocks = extract_wrapped_blocks(shared_css)
    if not blocks:
        print(
            f"WARNING: no {SRC_START} ... {SRC_END} block found in {shared_path}."
        )

    synced_block = "\n\n".join(blocks)
    new_section = f"{DEST_START}\n{synced_block}\n{DEST_END}"

    pattern = re.compile(
        re.escape(DEST_START) + r".*?" + re.escape(DEST_END),
        re.DOTALL,
    )
    updated_css, count = pattern.subn(new_section, critical_css)

    if updated_css == critical_css:
        return False  # no change needed

    critical_path.write_text(updated_css, encoding="utf-8")
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("shared_css", type=Path)
    parser.add_argument("critical_css", type=Path)
    parser.add_argument(
        "--watch", action="store_true", help="Re-sync automatically on save"
    )
    args = parser.parse_args()

    if not args.shared_css.exists():
        sys.exit(f"File not found: {args.shared_css}")
    if not args.critical_css.exists():
        sys.exit(f"File not found: {args.critical_css}")

    if not args.watch:
        changed = sync(args.shared_css, args.critical_css)
        print("critical.css updated." if changed else "Already in sync — no changes.")
        return

    print(f"Watching {args.shared_css} for changes... (Ctrl+C to stop)")
    last_mtime = args.shared_css.stat().st_mtime
    try:
        while True:
            time.sleep(1)
            mtime = args.shared_css.stat().st_mtime
            if mtime != last_mtime:
                last_mtime = mtime
                changed = sync(args.shared_css, args.critical_css)
                if changed:
                    print("shared.css changed — critical.css re-synced.")
    except KeyboardInterrupt:
        print("\nStopped watching.")


if __name__ == "__main__":
    main()