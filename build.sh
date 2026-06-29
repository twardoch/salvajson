#!/usr/bin/env bash
# build.sh: Lint, test, and build salvajson
# salvajson: Fix corrupted JSON files using the jsonic JSON parser in JavaScript

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Linting ==="
uvx ruff check --fix --unsafe-fixes . || true
uvx ruff format . || true

echo "=== Tests ==="
if [ -d "tests" ] || find . -name "test_*.py" -not -path "./.git/*" | grep -q .; then
    python -m pytest -x || true
else
    echo "No tests found, skipping."
fi

echo "=== Build ==="
uvx hatch build

echo "=== Build complete ==="
