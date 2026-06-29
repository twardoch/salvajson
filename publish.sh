#!/usr/bin/env bash
# publish.sh: Build, install, version, and publish salvajson to PyPI
# salvajson: Fix corrupted JSON files using the jsonic JSON parser in JavaScript

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Build ==="
bash "$SCRIPT_DIR/build.sh"

echo "=== Install ==="
bash "$SCRIPT_DIR/install.sh"

echo "=== Version bump ==="
uvx gitnextver@latest

echo "=== Final build & publish ==="
uvx hatch build
uv publish

echo "=== Publish complete ==="
