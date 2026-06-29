# SalvaJSON: repair and parse malformed JSON

SalvaJSON fixes broken JSON that standard parsers reject, then parses it into Python objects. It's a drop-in upgrade for `json.loads()` when your input comes from LLMs, scraped pages, hand-edited configs, or any source that doesn't guarantee strict JSON.

## What it fixes

SalvaJSON uses [jsonic](https://github.com/rjrodger/jsonic) — a lenient JavaScript JSON parser — to handle:

- **Unquoted keys** — `{name: "Alice"}` instead of `{"name": "Alice"}`
- **Single quotes** — `{'key': 'value'}` instead of `{"key": "value"}`
- **Trailing commas** — `[1, 2, 3,]` and `{"a": 1,}`
- **Missing commas** — `[1 2 3]` parsed as `[1, 2, 3]`
- **JavaScript comments** — `// line comments` and `/* block comments */`
- **Unquoted string values** — `{status: active}` where `active` is unambiguous

Valid JSON is parsed at full speed by [orjson](https://github.com/ijl/orjson) without touching the repair path.

## Install

```bash
pip install salvajson
```

Requires Python 3.10+. Pulls in `pythonmonkey` (embeds SpiderMonkey JS engine) and `orjson`.

## Usage

### Python API

```python
from salvajson import salvaj, loads, dumps

# Repair a broken JSON string → returns valid JSON string
salvaj('{name: "Alice", age: 30,}')
# → '{"name":"Alice","age":30}'

# Parse JSON → Python object (auto-repairs on failure)
loads('{"id": 1}')                       # fast path via orjson
loads("{id: 1, tags: ['a', 'b'],}")      # repair path via jsonic
# → {'id': 1, 'tags': ['a', 'b']}

# Serialize Python → JSON string (via orjson, fast)
dumps({"name": "Alice", "scores": [1, 2]})
dumps({"b": 2, "a": 1}, sort_keys=True, indent=2)
```

`loads()` and `dumps()` accept the same keyword arguments as `json.loads()` / `json.dumps()` for compatibility, though most are no-ops (orjson handles them natively).

### CLI

```bash
# Repair a file and print to stdout
python -m salvajson broken.json

# Repair and save
python -m salvajson broken.json > fixed.json

# Pipe
echo '{key: "value"}' | python -m salvajson
```

## How it works

```
loads(s)
  ├── orjson.loads(s)          → fast path if valid JSON
  └── on JSONDecodeError:
        salvaj(s)              → jsonic via PythonMonkey SpiderMonkey engine
          └── JSON.stringify() → valid JSON string
        orjson.loads(repaired) → Python object
```

The JavaScript engine is embedded in-process via PythonMonkey — no Node.js required, no subprocess overhead.

## API reference

| Function | Signature | Description |
|----------|-----------|-------------|
| `salvaj` | `(json_str: str) -> str` | Repair broken JSON; return valid JSON string |
| `loads` | `(s: bytes \| str, **kw) -> Any` | Parse JSON with automatic repair fallback |
| `dumps` | `(obj, *, indent=None, sort_keys=False, **kw) -> str` | Serialize to JSON string |

## Performance notes

- Valid JSON: `orjson` is used directly — among the fastest Python JSON parsers.
- Invalid JSON: repair path invokes SpiderMonkey JS engine via PythonMonkey; adds latency (~ms).
- The JS bundle is loaded once at import time.

## Development

```bash
git clone https://github.com/twardoch/salvajson && cd salvajson
./dev.sh setup     # creates venv, installs Python + JS deps, pre-commit hooks
./dev.sh test      # pytest
./dev.sh lint      # ruff + mypy + bandit + prettier
./dev.sh build     # hatch build
```

The JS source lives in `js_src/salvajson.src.js` and is bundled into `src/salvajson/salvajson.js` by esbuild during build.

## License

Apache License 2.0. See `LICENSE`.
