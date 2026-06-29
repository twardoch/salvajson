#!/usr/bin/env bash
# install.sh: Install salvajson in editable mode
# salvajson: Fix corrupted JSON files using the jsonic JSON parser in JavaScript

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Installing salvajson (editable) ==="
uv pip install -e .
echo "=== Install complete ==="
