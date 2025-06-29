# SalvaJSON: Robust JSON Repair and Processing

SalvaJSON is a powerful Python library designed to seamlessly repair and process corrupted or malformed JSON data. It intelligently fixes common syntax errors, making it an essential tool for developers working with unreliable JSON sources, such as LLM outputs, APIs, or user-generated content. Beyond repair, SalvaJSON offers high-performance JSON serialization and deserialization.

## Part 1: User-Facing Documentation

### What is SalvaJSON?

SalvaJSON ("salvage JSON") is your go-to Python toolkit for handling imperfect JSON. It excels at:

1.  **Repairing Corrupted JSON:** Automatically fixes many common JSON syntax issues like missing quotes, trailing commas, incorrect quoting, and comments.
2.  **High-Performance Parsing:** Provides fast and efficient JSON loading.
3.  **Flexible Serialization:** Offers robust Python object to JSON string conversion.

It leverages the lenient `jsonic` JavaScript parser via the PythonMonkey bridge for its powerful repair capabilities and the high-speed `orjson` library for standard JSON operations.

### Who is it For?

SalvaJSON is designed for:

*   **Python Developers** integrating with external APIs that might return slightly malformed JSON.
*   **Data Scientists and Analysts** cleaning JSON data from various, sometimes unreliable, sources.
*   **AI/ML Engineers** working with Large Language Models (LLMs) that can produce JSON-like output with minor syntax errors.
*   Anyone who needs to reliably parse JSON data that doesn't strictly adhere to the JSON specification.

### Why is it Useful?

*   **Resilience:** Makes your applications more robust by gracefully handling common JSON errors instead of crashing.
*   **Simplicity:** Offers a straightforward API (`salvaj`, `loads`, `dumps`) that is easy to learn and use.
*   **Performance:** Utilizes `orjson` for fast parsing and serialization of valid JSON.
*   **Versatility:** Provides both a Python library and a command-line interface (CLI) for flexible usage.
*   **Fixes Many Common Errors:**
    *   Missing or mismatched quotes around keys and string values.
    *   Use of single quotes instead of double quotes.
    *   Trailing commas in objects and arrays.
    *   Missing commas between elements or key-value pairs.
    *   JavaScript-style comments (`//`, `/* */`).
    *   Unquoted keys or string values where unambiguous.

### Installation

To install SalvaJSON, ensure you have Python 3.10 or higher. Then, run the following command:

```bash
pip install salvajson
```

This will also install its dependencies, including `pythonmonkey` (for JavaScript interoperability) and `orjson` (for fast JSON processing).

### Usage

SalvaJSON can be used as a Python library in your projects or as a command-line tool.

#### Python API

The library provides three main functions:

1.  **`salvaj(json_str: str) -> str`**:
    This is the core repair function. It takes a potentially corrupted JSON string, uses the `jsonic` parser (via JavaScript) to fix it, and returns a valid JSON string.

    ```python
    from salvajson import salvaj

    corrupted_json = """{
        name: "John Doe", // Name is unquoted, comment present
        age: 30,
        'city': 'New York', // Single quotes for key and value
        interests: ["coding" "reading",], // Missing comma, trailing comma
    }"""

    try:
        fixed_json_string = salvaj(corrupted_json)
        print(f"Fixed JSON string: {fixed_json_string}")
        # Output: Fixed JSON string: {"name":"John Doe","age":30,"city":"New York","interests":["coding","reading"]}
    except Exception as e:
        print(f"Failed to salvage JSON: {e}")
    ```

2.  **`loads(s: bytes | str, **kw) -> Any`**:
    This function parses a JSON string (or bytes) into a Python object. It first attempts to parse using the fast `orjson` library. If that fails due to malformed JSON, it automatically falls back to using `salvaj()` to repair the string and then parses the result.

    ```python
    from salvajson import loads

    # Example with valid JSON
    valid_json = '{"id": 1, "status": "active"}'
    data = loads(valid_json)
    print(f"Parsed valid JSON: {data}")
    # Output: Parsed valid JSON: {'id': 1, 'status': 'active'}

    # Example with corrupted JSON (automatically fixed by salvaj)
    corrupted_json_for_loads = "{'item': 'gadget', price: 49.99,}" # Single quotes, unquoted key, trailing comma
    data_from_corrupted = loads(corrupted_json_for_loads)
    print(f"Parsed corrupted JSON: {data_from_corrupted}")
    # Output: Parsed corrupted JSON: {'item': 'gadget', 'price': 49.99}
    ```

3.  **`dumps(obj, *, indent=None, sort_keys=False, **kw) -> str`**:
    This function serializes a Python object into a JSON string using `orjson` for high performance. It supports common parameters like `indent` for pretty-printing and `sort_keys` for ordering dictionary keys.

    ```python
    from salvajson import dumps

    python_object = {'name': 'Jane Doe', 'age': 28, 'hobbies': ['skiing', 'music']}

    # Standard serialization
    json_string = dumps(python_object)
    print(f"Serialized JSON: {json_string}")
    # Output: Serialized JSON: {"name":"Jane Doe","age":28,"hobbies":["skiing","music"]}

    # Pretty-printed serialization with sorted keys
    pretty_json_string = dumps(python_object, indent=2, sort_keys=True)
    print(f"Pretty JSON:\n{pretty_json_string}")
    # Output:
    # Pretty JSON:
    # {
    #   "age": 28,
    #   "hobbies": [
    #     "skiing",
    #     "music"
    #   ],
    #   "name": "Jane Doe"
    # }
    ```

#### Command-Line Interface (CLI)

SalvaJSON also provides a simple CLI to fix JSON files directly from your terminal. The CLI uses the `salvaj` function to process the input.

*   **Process a JSON file and print the fixed JSON to standard output:**

    ```bash
    python -m salvajson /path/to/your/corrupted_file.json
    ```

*   **Process a JSON file and save the fixed output to a new file:**

    ```bash
    python -m salvajson input.json > output_fixed.json
    ```

    If `input.json` contains, for example:
    `{name: "Test", value: 123, // A comment}`
    Then `output_fixed.json` will contain:
    `{"name":"Test","value":123}`

## Part 2: Technical Documentation

### How it Works

SalvaJSON cleverly combines Python and JavaScript technologies to achieve its robustness and performance:

1.  **PythonMonkey Bridge:** At its core, SalvaJSON uses [`PythonMonkey`](https://github.com/Distributive-Network/PythonMonkey). This library embeds a JavaScript engine (SpiderMonkey, the engine used in Firefox) within the Python process. This allows Python code to execute JavaScript code and exchange data seamlessly.

2.  **`jsonic` for Lenient Parsing:** The actual JSON repair magic is handled by [`jsonic`](https://github.com/rjrodger/jsonic), a mature and lenient JavaScript JSON parser. When `salvaj(json_str)` is called:
    *   The input `json_str` (Python string) is passed to the embedded JavaScript environment.
    *   A small JavaScript wrapper (`js_src/salvajson.src.js`, bundled into `src/salvajson/salvajson.js`) calls `Jsonic(json_str)`.
    *   `jsonic` parses the string, correcting common syntax errors according to its lenient rules.
    *   The result from `jsonic` (a JavaScript object/array) is then stringified using `JSON.stringify()` in JavaScript to ensure it's a valid JSON string.
    *   This valid JSON string is returned to the Python environment.
    *   If `jsonic` cannot parse the input even with its lenient rules, it throws an error in JavaScript, which PythonMonkey propagates as a `pythonmonkey.SpiderMonkeyError` in Python.

3.  **`orjson` for Performance:** For standard JSON operations (`loads` and `dumps`), SalvaJSON uses [`orjson`](https://github.com/ijl/orjson). `orjson` is a high-performance Python JSON library known for its speed.
    *   **`dumps(obj, ...)`:** Directly uses `orjson.dumps()` for fast Python object to JSON string serialization.
    *   **`loads(s, ...)`:** First attempts to parse the input string/bytes using `orjson.loads()`. If this succeeds (meaning the JSON is already valid), the result is returned quickly.

4.  **Fallback Mechanism in `loads`:** If the initial `orjson.loads()` attempt fails (e.g., due to a `orjson.JSONDecodeError`), it indicates malformed JSON. The `loads` function then automatically:
    *   Takes the input string (decoding from bytes if necessary).
    *   Calls `salvaj()` on this string to get a repaired JSON string.
    *   Finally, calls `orjson.loads()` again on this repaired string.

This layered approach ensures that valid JSON is processed with maximum speed, while corrupted JSON gets a chance to be repaired and then parsed.

### Project Structure

The project is organized as follows:

```
salvajson/
├── .github/workflows/    # GitHub Actions CI/CD workflows (ci.yml, update-js.yml)
├── src/
│   └── salvajson/
│       ├── __init__.py       # Main package interface, exports salvaj, loads, dumps
│       ├── _version.py       # Version info (managed by hatch-vcs & python-semantic-release)
│       ├── salvajson.py      # Core Python logic for salvaj, loads, dumps
│       └── salvajson.js      # Bundled JavaScript code (generated by esbuild from js_src/)
├── js_src/                 # JavaScript source code and build tools
│   ├── package.json        # npm package definition, lists JS dependencies (jsonic)
│   ├── package-lock.json   # npm lockfile for reproducible JS builds
│   ├── salvajson.src.js    # Main JavaScript source file wrapping jsonic
│   └── build.esbuild.js    # esbuild configuration for bundling salvajson.src.js
├── tests/                  # Pytest tests
│   └── test_salvajson.py   # Unit tests for salvajson functionalities
├── .pre-commit-config.yaml # Configuration for pre-commit hooks
├── build.py                # Hatchling build hook for bundling JS during package build
├── commitlint.config.js    # Configuration for commitlint (Conventional Commits)
├── pyproject.toml          # Python project configuration (PEP 621, Hatch, Ruff, Mypy, etc.)
├── README.md               # This file
├── CHANGELOG.md            # Changelog (managed by python-semantic-release)
└── LICENSE                 # Apache 2.0 License
```

### Development Environment Setup

To set up a development environment for SalvaJSON:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/twardoch/salvajson.git
    cd salvajson
    ```

2.  **Create and Activate a Virtual Environment** (recommended):
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install Python Dependencies:**
    Install the package in editable mode along with development and test dependencies:
    ```bash
    pip install -e ".[dev,test]"
    ```
    This also triggers the initial JavaScript build (see `build.py`).

4.  **Install JavaScript Dependencies:**
    Navigate to the `js_src` directory and install npm dependencies:
    ```bash
    cd js_src
    npm ci  # Or npm install for a fresh setup
    cd ..
    ```

5.  **Install Pre-commit Hooks:**
    This ensures your contributions adhere to the project's coding standards and commit message format.
    ```bash
    pre-commit install
    pre-commit install --hook-type commit-msg # For commit message linting (commitlint)
    ```

### Building the Package

SalvaJSON uses [`Hatch`](https://hatch.pypa.io/) as its build backend, configured in `pyproject.toml`.

*   **JavaScript Bundling:** A custom Hatchling build hook defined in `build.py` is responsible for bundling the JavaScript code.
    *   It uses `npm run build` within the `js_src` directory (which in turn uses `esbuild` as configured in `js_src/build.esbuild.js`).
    *   This bundles `js_src/salvajson.src.js` and its dependencies (like `jsonic`) into a single file: `src/salvajson/salvajson.js`.
    *   This bundle is then included in the Python package.
*   **Building the Python Package:** To build the wheel and source distribution:
    ```bash
    hatch build
    ```
    The distributable files will be placed in the `dist/` directory.
*   **Manual JS Rebuild (for development):** If you modify files in `js_src/` after the initial editable install, the JavaScript bundle `src/salvajson/salvajson.js` needs to be rebuilt. You can do this by:
    *   Running `python build.py` directly.
    *   Or, reinstalling the editable package: `pip install -e .[dev,test]`

### Coding and Contribution Rules

We welcome contributions! Please adhere to the following guidelines:

*   **Code Style & Quality:**
    *   **Pre-commit:** Always run `pre-commit run --all-files` before committing. This tool automatically formats code and checks for issues using:
        *   `Ruff`: For linting and formatting Python code.
        *   `Prettier`: For formatting JavaScript, JSON, and Markdown.
        *   `Mypy`: For static type checking in Python.
        *   `Bandit`: For finding common security issues in Python code.
    *   Configurations for these tools are in `pyproject.toml` and `.pre-commit-config.yaml`.
*   **Commit Messages:**
    *   Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification (e.g., `feat: ...`, `fix: ...`, `docs: ...`, `chore: ...`).
    *   `commitlint` (via pre-commit hook) enforces this.
*   **Testing:**
    *   Write `pytest` tests for any new features or bug fixes.
    *   Ensure all tests pass by running `pytest` in the project root.
    *   Aim for high test coverage. Current settings require >=80% coverage (`pytest.ini`).
*   **Branching and Pull Requests:**
    *   Work on feature branches.
    *   Submit Pull Requests (PRs) to the `main` branch for review.
    *   Ensure your PR passes all CI checks.
*   **Versioning and Releasing:**
    *   The project uses `python-semantic-release` for automated versioning, changelog generation, and tagging.
    *   The version is derived from Git tags (e.g., `v1.2.3`) managed by `hatch-vcs` during build time.
    *   `CHANGELOG.md` is automatically updated based on Conventional Commit messages when a release is made.
    *   **Release Process (for Maintainers):**
        1.  Ensure `main` branch is up-to-date and all desired commits are present.
        2.  Run `semantic-release publish`. This command:
            *   Determines the next semantic version based on commit history.
            *   Updates `CHANGELOG.md`.
            *   Commits these changes with a `chore(release): ...` message.
            *   Creates and pushes a new Git tag (e.g., `v0.2.1`).
        3.  Pushing this tag triggers the "PyPI Publishing" job in the `ci.yml` GitHub Actions workflow. This job builds the package and uploads it to PyPI, then creates a GitHub Release.
*   **Automated Workflows (GitHub Actions):**
    *   **`ci.yml`:**
        *   Triggered on pushes, pull requests, and manual dispatch.
        *   Sets up Python and Node.js environments.
        *   Installs dependencies (Python and JS).
        *   Runs `pre-commit` checks.
        *   Runs `pytest`.
        *   Builds the package.
        *   On new version tags, publishes to PyPI and creates a GitHub Release.
    *   **`update-js.yml`:**
        *   Runs weekly or manually.
        *   Updates JavaScript dependencies in `js_src/package-lock.json` using `npm update`.
        *   Runs `npm audit --audit-level=critical`.
        *   Rebuilds the JS bundle (`src/salvajson/salvajson.js`).
        *   Creates a Pull Request with these updates for review.

### Key Technologies

*   **Python 3.10+:** The core language.
*   **PythonMonkey:** Embeds a JavaScript engine, enabling the use of JavaScript libraries like `jsonic`.
*   **jsonic:** A lenient JavaScript JSON parser used for repairing malformed JSON.
*   **orjson:** A fast Python JSON library used for serializing and deserializing valid JSON.
*   **Fire:** For creating the command-line interface (`__main__.py`).
*   **Hatch / Hatchling:** Modern Python build system and backend.
*   **esbuild:** Extremely fast JavaScript bundler, used to package `jsonic` and the wrapper script.
*   **npm / Node.js:** For managing JavaScript dependencies and running build scripts for the JS part.
*   **Pre-commit Framework:** Manages Git hooks for code quality checks.
    *   **Ruff:** Linter and formatter for Python.
    *   **Mypy:** Static type checker for Python.
    *   **Prettier:** Code formatter for JS, JSON, MD.
    *   **Bandit:** Security linter for Python.
    *   **commitlint:** Linter for commit messages (Conventional Commits).
*   **Pytest:** Testing framework for Python.
*   **python-semantic-release:** For automating versioning, changelog generation, and release tagging.
*   **GitHub Actions:** For CI/CD and other automated workflows.

### License

SalvaJSON is licensed under the Apache License 2.0. See the `LICENSE` file for details.

### Credits and Acknowledgements

*   **Adam Twardoch** ([@twardoch](https://github.com/twardoch)): Original author and maintainer.
*   **Anthropic Claude:** Contributed to development and documentation.
*   **Dependencies:** This project relies on the excellent work of the maintainers of:
    *   [jsonic](https://github.com/rjrodger/jsonic)
    *   [PythonMonkey](https://github.com/Distributive-Network/PythonMonkey)
    *   [orjson](https://github.com/ijl/orjson)
    *   And all other tools and libraries listed under "Key Technologies".

This project also serves as a demonstration of effective Python-JavaScript interoperability, modern Python packaging, and CI/CD best practices.
