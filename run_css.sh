#!/usr/bin/env bash
# run_css.sh
#
# Runs sync_critical_css.py, minify_shared_css.py and inline_critical_css.py once, in order.
#
# USAGE:
#   ./run_css.sh assets/css/shared.css assets/css/critical.css assets/css/shared.min.css index.html
#
# (First run: chmod +x run_css.sh)

set -e

SHARED_CSS="$1"
CRITICAL_CSS="$2"
MIN_CSS="$3"
INDEX_HTML="$4"
if [[ -z "$SHARED_CSS" || -z "$CRITICAL_CSS" || -z "$MIN_CSS" || -z "$INDEX_HTML" ]]; then
echo "Usage: $0 <shared.css> <critical.css> <shared.min.css> <index.html>"
exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python3 "$SCRIPT_DIR/assets/py/sync_critical_css.py" "$SHARED_CSS" "$CRITICAL_CSS"
python3 "$SCRIPT_DIR/assets/py/minify_shared_css.py" "$SHARED_CSS" "$MIN_CSS"
python3 "$SCRIPT_DIR/assets/py/inline_critical_css.py" "$CRITICAL_CSS" "$INDEX_HTML"