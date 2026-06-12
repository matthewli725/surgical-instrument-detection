#!/usr/bin/env bash
set -euo pipefail

# Ensure SSH key is loaded in agent for forwarding
if ! ssh-add -l &>/dev/null; then
  ssh-add ~/.ssh/id_rsa
fi

SRC="/home/matthewli/surgical-instrument-detection/"
DST="matthew@obiwan.ee.ucla.edu:/home3/matthew/surgical-instrument-detection/"
EXCLUDES="--exclude=.venv --exclude=weights --exclude=runs --exclude=__pycache__ --exclude='*.pyc'"

echo "=== Dry run ==="
ssh -A jarjar "rsync -av --dry-run $EXCLUDES '$SRC' '$DST'"

echo ""
read -p "Looks good? Press Enter to run for real, Ctrl-C to abort."

echo "=== Real transfer ==="
ssh -A jarjar "rsync -av --progress $EXCLUDES '$SRC' '$DST'"

echo "=== Done. Run 'uv sync' on obiwan to recreate venv ==="
