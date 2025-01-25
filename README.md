# Salvajson

A Python package for parsing and fixing corrupted JSON files using the powerful [jsonic](https://github.com/rjrodger/jsonic) parser. Salvajson provides a bridge between Python and the JavaScript jsonic library through PythonMonkey.

## Features

- Parse corrupted or malformed JSON strings
- Fix common JSON syntax errors
- Command-line interface for processing JSON files
- Simple Python API
- Built on the battle-tested jsonic parser

## Installation

```bash
pip install salvajson
```

### Requirements

- Python 3.8 or higher
- PythonMonkey 0.5.0 or higher (automatically installed)

## Usage

### Python API

```python
from salvajson import salvage

# Fix a corrupted JSON string
corrupted_json = """{
    name: "John",
    age: 30,
    'hobbies': ['reading' 'coding'],
}"""

fixed_json = salvage(corrupted_json)
print(fixed_json)
```

### Command Line Interface

Salvajson comes with a CLI for processing JSON files directly:

```bash
python -m salvajson path/to/corrupted.json
```

## Common JSON Issues Salvajson Can Fix

- Missing quotes around property names
- Single quotes instead of double quotes
- Trailing commas
- Missing commas between elements
- Unquoted string values
- And more...

## Development

### Setup Development Environment

1. Clone the repository:
```bash
git clone https://github.com/yourusername/salvajson.git
cd salvajson
```

2. Install development dependencies:
```bash
pip install -e ".[dev]"
```

3. Install JavaScript dependencies:
```bash
cd js_src
npm install
```

### Project Structure

```
salvajson/
├── src/
│   └── salvajson/
│       ├── __init__.py      # Main package interface
│       └── salvajson.js     # Bundled JavaScript code
├── js_src/
│   ├── package.json     # JavaScript dependencies
│   └── index.js         # JavaScript source
├── tests/
│   └── test_salvajson.py
├── build.py             # Build script
└── pyproject.toml       # Python package configuration
```

### Building

The project uses `hatchling` as its build backend. The `build.py` script handles bundling the JavaScript code before package building.

```bash
python build.py
pip install -e .
```

## How It Works

Salvajson uses PythonMonkey to create a bridge between Python and JavaScript, allowing it to leverage the powerful jsonic parser. When you pass a JSON string to `salvage()`:

1. The string is passed to the JavaScript runtime
2. jsonic attempts to parse and fix the JSON
3. The fixed JSON is returned to Python as a string

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Credits

- [jsonic](https://github.com/rjrodger/jsonic) - The JavaScript library that powers the JSON parsing
- [PythonMonkey](https://github.com/Distributive-Network/PythonMonkey) - Python-JavaScript bridge

## Notes for Maintainers

### Automated Workflows

The package uses GitHub Actions for automation:

1. **JS Dependencies Update** (weekly + manual trigger)
   - Updates JS dependencies and rebuilds the bundle
   - Creates a PR for review
   - Trigger manually: Go to Actions → "Update JS Dependencies" → "Run workflow"

2. **PyPI Publishing** (on tag)
   - Builds and publishes to PyPI when a version tag is pushed
   - To release a new version:
     ```bash
     git tag v0.1.1  # Use appropriate version
     git push origin v0.1.1
     ```
   - The workflow will automatically build and publish to PyPI

### Required Secrets

Set up these secrets in your GitHub repository:

- `PYPI_API_TOKEN`: API token from PyPI for publishing

### License

This project is licensed under the Apache License, Version 2.0.
