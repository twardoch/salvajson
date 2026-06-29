---
layout: default
title: Home
nav_order: 1
---

# SalvaJSON

**A drop-in upgrade for `json.loads()` that repairs malformed JSON.**

SalvaJSON uses [jsonic](https://github.com/rjrodger/jsonic) — a lenient JavaScript JSON parser running in-process via [PythonMonkey](https://pythonmonkey.io) (SpiderMonkey engine) — to fix broken JSON that standard parsers reject. Valid JSON takes a fast path through [orjson](https://github.com/ijl/orjson) and never reaches the repair engine.

```python
pip install salvajson
```

---

## What SalvaJSON fixes

| Problem | Broken input | Fixed output |
|---------|-------------|--------------|
| Unquoted keys | `{name: "Alice"}` | `{"name":"Alice"}` |
| Single quotes | `{'key': 'value'}` | `{"key":"value"}` |
| Trailing commas (object) | `{"a": 1,}` | `{"a":1}` |
| Trailing commas (array) | `[1, 2, 3,]` | `[1,2,3]` |
| Missing commas | `[1 2 3]` | `[1,2,3]` |
| JS line comments | `{"a": 1 // note\n}` | `{"a":1}` |
| JS block comments | `{"a": /* x */ 1}` | `{"a":1}` |
| Unquoted string values | `{status: active}` | `{"status":"active"}` |
| Mixed quote styles | `{name: 'Jo', "age": 30}` | `{"name":"Jo","age":30}` |
| Deeply nested quirks | Any combination of the above | Valid JSON |

## What SalvaJSON does NOT fix

| Problem | Example | Reason |
|---------|---------|--------|
| Reversed / mismatched brackets | `}{` or `{[}]` | Structurally ambiguous — jsonic raises an error |
| Truncated / incomplete JSON | `{"key":` | No way to infer missing value |
| Binary or non-UTF-8 data | `\xff\xfe...` | Not JSON at any layer |
| Numbers with leading zeros | `{"n": 01}` | Invalid in JSON and most JS engines |

When jsonic cannot repair the input, a `pythonmonkey.SpiderMonkeyError` is raised containing the jsonic error tag (e.g. `[jsonic/unexpected]`).

---

## API reference

### `salvaj(json_str: str) -> str`

Repair a potentially malformed JSON string using jsonic. Returns a valid JSON string.

```python
from salvajson import salvaj

salvaj('{name: "Alice", age: 30,}')
# → '{"name":"Alice","age":30}'

salvaj('["a" "b" "c"]')
# → '["a","b","c"]'

salvaj('/* config */ {debug: true, host: localhost}')
# → '{"debug":true,"host":"localhost"}'
```

**Raises:** `pythonmonkey.SpiderMonkeyError` if jsonic cannot parse the input.

---

### `loads(s: bytes | str, **kw) -> Any`

Parse JSON into a Python object. Uses `orjson` for the fast path; falls back to `salvaj` on `JSONDecodeError`. Accepts the same keyword arguments as `json.loads()` for drop-in compatibility (most are no-ops).

```python
from salvajson import loads

# Fast path — valid JSON, orjson only
loads('{"id": 1}')
# → {'id': 1}

# Repair path — malformed, goes through jsonic
loads("{id: 1, tags: ['a', 'b'],}")
# → {'id': 1, 'tags': ['a', 'b']}

# Bytes input supported
loads(b'{"ok": true}')
# → {'ok': True}
```

**Raises:**
- `orjson.JSONDecodeError` if valid JSON parsing of the repaired string fails.
- `pythonmonkey.SpiderMonkeyError` if jsonic cannot repair the input.

---

### `dumps(obj, *, indent=None, sort_keys=False, **kw) -> str`

Serialize a Python object to a JSON string using `orjson`. Accepts the same keyword arguments as `json.dumps()` for drop-in compatibility.

```python
from salvajson import dumps

dumps({"name": "Alice", "scores": [1, 2]})
# → '{"name":"Alice","scores":[1,2]}'

dumps({"b": 2, "a": 1}, sort_keys=True, indent=2)
# → '{\n  "a": 1,\n  "b": 2\n}'
```

`indent` always produces 2-space indentation (orjson behaviour). `sort_keys` sorts at all nesting levels. Parameters `skipkeys`, `ensure_ascii`, `check_circular`, `allow_nan`, `cls`, `separators`, and `default` are accepted but ignored.

---

## How it works

```
loads(s)
  ├── orjson.loads(s)          → fast path (valid JSON)
  └── on JSONDecodeError:
        salvaj(s)
          └── PythonMonkey → SpiderMonkey → jsonic.make()(s) → JSON.stringify()
        orjson.loads(repaired)  → Python object
```

The SpiderMonkey JS engine is embedded in-process via PythonMonkey — no Node.js subprocess, no network call.

---

## Comparison with alternatives

| Library | Approach | Unquoted keys | Single quotes | Comments | Trailing commas | Speed (valid JSON) |
|---------|----------|:---:|:---:|:---:|:---:|---|
| **SalvaJSON** | jsonic/SpiderMonkey | ✅ | ✅ | ✅ | ✅ | Fast (orjson fast-path) |
| `json` (stdlib) | C parser | ❌ | ❌ | ❌ | ❌ | Fast |
| `orjson` | Rust parser | ❌ | ❌ | ❌ | ❌ | Fastest |
| `demjson3` | Pure Python | ✅ | ✅ | ✅ | ✅ | Slow (pure Python) |
| `hjson` | Python/JS | ✅ | ✅ | ✅ | ✅ | Moderate |
| `json5` | Pure Python | ✅ | ✅ | ✅ | ✅ | Slow (pure Python) |
| `pyjson5` | C extension | ✅ | ✅ | ✅ | ✅ | Fast |

SalvaJSON's distinguishing traits:
- **Fast path for valid JSON** — orjson is used directly; the JS engine is never invoked.
- **In-process JS engine** — no subprocess, no Node.js install required.
- **jsonic's permissive grammar** — handles more malformed inputs than most pure-Python parsers (missing commas, unquoted values).

---

## Installation notes

SalvaJSON pulls in `pythonmonkey` which embeds the SpiderMonkey JS engine. Pre-built wheels are available for Linux x86_64/ARM64 and macOS ARM64/x86_64. Windows ARM64 wheels may not be available for all versions — check [pythonmonkey releases](https://github.com/Distributive-Network/PythonMonkey/releases) if installation fails on Windows.

The JS bundle (`salvajson.js`, ~46 KB) is included in the wheel and loaded once at import time.

---

## CLI

```bash
# Repair a file and print to stdout
python -m salvajson broken.json

# Pipe from stdin
echo '{key: "value"}' | python -m salvajson
```

---

## License

Apache License 2.0. See [LICENSE](https://github.com/twardoch/salvajson/blob/main/LICENSE).
