# Changelog

## v2.7.6 (unreleased)

### Improvements
- Migrated pytest configuration from `pytest.ini` to `pyproject.toml` (`[tool.pytest.ini_options]`) — eliminates duplicate config and resolves `hatch test` argument conflict
- Fixed version-format test patterns to accept hatch-vcs dev/dirty suffixes (e.g. `2.7.6.dev11+gec76a4218.d20260629`)
- Added Jekyll docs site under `docs/` with full API reference, what-it-fixes matrix, and comparison table vs. `demjson3`/`hjson`/`json5`/`pyjson5`

## v2.7.5 (2025-06-29)

### Features
- `src/` layout with `hatchling` + `hatch-vcs` build system
- Three public functions: `salvaj()`, `loads()`, `dumps()`
- Fast path via `orjson` for valid JSON; repair path via jsonic/SpiderMonkey (PythonMonkey)
- CLI: `python -m salvajson [file]`
- Full type annotations and docstrings on public API
- `ruff` + `mypy` configuration in `pyproject.toml`
- GitHub Actions CI with build, test (Python 3.10 + 3.12), and PyPI publish jobs

## v2.7.0 — v2.7.4

- Incremental improvements to JS bundle bundling via esbuild
- Switch from flat layout to `src/` layout
- Added `pytest-timeout`, `pytest-sugar`, `pytest-xdist` to test dependencies

## v2.0.0 — v2.6.x

- Rewrite using PythonMonkey (SpiderMonkey in-process) instead of Node.js subprocess
- `orjson` fast path added for valid JSON
- `dumps()` function added for high-performance serialization
- `loads()` function added as drop-in `json.loads()` replacement

## v1.x

- Initial versions using Node.js subprocess for jsonic
- Basic `salvaj()` function only
