#!/usr/bin/env bash
# run_css.sh
#
# Runs sync_critical_css.py, minify_style_css.py and inline_critical_css.py once, in order.
#
# USAGE:
#   ./run_css.sh assets/css/style.css assets/css/critical.css assets/css/style_min.css index.html
#
# (First run: chmod +x run_css.sh)

set -e

STYLE_CSS="$1"
CRITICAL_CSS="$2"
STYLE_MIN_CSS="$3"
INDEX_HTML="$4"
if [[ -z "$STYLE_CSS" || -z "$CRITICAL_CSS" || -z "$STYLE_MIN_CSS" || -z "$INDEX_HTML" ]]; then
echo "Usage: $0 <style.css> <critical.css> <style_min.css> <index.html>"
exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# The style-to-critical sync step is currently disabled.
# Uncomment the line below to restore syncing from style.css into critical.css.
# python3 "$SCRIPT_DIR/assets/py/sync_critical_css.py" "$STYLE_CSS" "$CRITICAL_CSS"
python3 "$SCRIPT_DIR/assets/py/minify_style_css.py" "$STYLE_CSS" "$STYLE_MIN_CSS"
python3 "$SCRIPT_DIR/assets/py/inline_critical_css.py" "$CRITICAL_CSS" "$INDEX_HTML"