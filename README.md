# SalvaJSON

[`salvajson`](https://github.com/twardoch/salvajson) is a Python package for fixing corrupted JSON files using. It uses the lenient [`jsonic`](https://github.com/rjrodger/jsonic) parser and the [`pythonmonkey`](https://github.com/Distributive-Network/PythonMonkey) Python-JS bridge.

- Seamlessly corrects invalid JSON from LLMs, APIs, and other sources
- Handles missing/single quotes, trailing commas, missing commas, unquoted strings, JSON comments, and more
- Simple Python API and command-line interface

## Installation

```bash
uv pip install --system salvajson
```

### Requirements

- Python 3.10 or higher
- PythonMonkey 1.1.0 or higher (automatically installed)

## Usage

### Python API

```python
from salvajson import salvaj

# Fix a corrupted JSON string
corrupted_json = """{
    name: "John",
    age: 30,
    'hobbies': ['reading' 'coding'],
}"""

fixed_json = salvaj(corrupted_json)
print(fixed_json)
```

The package provides three main functions:

#### `salvaj(json_str: str) -> str`

Fixes corrupted JSON strings using the lenient jsonic parser. This is the core function that handles:
- Missing or single quotes
- Trailing commas
- Missing commas
- Unquoted property names
- JSON comments
- And more syntax issues

#### `dumps(obj, *, indent=None, sort_keys=False, **kw) -> str`

High-performance JSON serialization using orjson:
- Faster than the standard json.dumps()
- Compatible with json.dumps() parameters
- Supports pretty-printing with indent=2
- Optional key sorting with sort_keys=True
- Handles numpy arrays and UTC datetimes
- Non-string dictionary keys are converted to strings

```python
from salvajson import dumps

data = {"b": 2, "a": 1}
# Pretty-printed with sorted keys
print(dumps(data, indent=2, sort_keys=True))
```

#### `loads(s: bytes | str, **kw) -> Any`

High-performance JSON parsing with automatic corruption recovery:
- Uses orjson for fast parsing
- Falls back to jsonic (salvaj) if standard parsing fails
- Compatible with json.loads() parameters
- Accepts both string and bytes input
- Returns Python objects (dict, list, str, int, float, None)

```python
from salvajson import loads

# Standard JSON parsing
valid_json = '{"name": "John", "age": 30}'
data = loads(valid_json)

# Automatic recovery of corrupted JSON
corrupted_json = '{name: John, age: 30}'
data = loads(corrupted_json)  # Still works!
```

### Command Line Interface

Salvajson comes with a CLI for processing JSON files directly:

```bash
# Process a single file
python -m salvajson path/to/corrupted.json

# Process and save to a new file
python -m salvajson input.json > output.json
```

## Development

### Setup Development Environment

1. Clone the repository:

```bash
git clone https://github.com/twardoch/salvajson.git; cd salvajson
```

2. Install development dependencies:

```bash
uv venv && source .venv/bin/activate; uv pip install -e ".[dev,test]"
```

3. Install JavaScript dependencies:
```bash
cd js_src; npm install
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

Salvajson uses PythonMonkey to create a bridge between Python and JavaScript, allowing it to leverage the powerful jsonic parser. When you pass a JSON string to `salvaj()`:

1. The string is passed to the JavaScript runtime
2. jsonic attempts to parse and fix the JSON
3. The fixed JSON is returned to Python as a string

## License

Apache License 2.0 - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Credits

- **Adam Twardoch** [@twardoch](https://github.com/twardoch)
- **Anthropic Claude**
- [jsonic](https://github.com/rjrodger/jsonic) - The lenient JSON parser in JavaScript
- [PythonMonkey](https://github.com/Distributive-Network/PythonMonkey) - Python-JavaScript bridge

## Rationale

This project serves as an exercise demonstrating how to effectively bridge Python and JavaScript ecosystems. It showcases:

- Integration of mature JavaScript libraries into Python applications using PythonMonkey
- Clean architecture for JavaScript-Python interoperability
- Proper packaging of JavaScript dependencies within a Python package
- Modern build system configuration using hatchling and esbuild
- Automated workflows for dependency management and publishing

While the project solves a specific problem (fixing malformed JSON), its architecture and build setup can be adapted for integrating other JavaScript libraries into Python projects.

## About the `jsonic` lenient JSON parser

[`jsonic`](https://github.com/rjrodger/jsonic) is a JavaScript library that provides a more lenient and extensible JSON parser. Unlike the standard `JSON.parse`, `jsonic` allows for a more flexible syntax, making it easier to work with human-written JSON-like data. This article provides a detailed technical overview of how `jsonic` works, exploring its architecture, parsing process, and extensibility features.

### Core Architecture

At its core, `jsonic` is built around two primary components:

1. **Lexer (Tokenizer):** The lexer's role is to break down the input string into a stream of tokens. Each token represents a meaningful unit of the input, such as a string, number, keyword, or punctuation. The lexer in `jsonic` is highly configurable, allowing users to define custom token types and matching rules.

2. **Parser:** The parser takes the token stream generated by the lexer and constructs an Abstract Syntax Tree (AST) based on a predefined grammar. This grammar defines the rules of the `jsonic` syntax, including how tokens can be combined to form valid JSON structures.

The parser utilizes a recursive descent parsing strategy. This approach involves defining a set of functions, each responsible for parsing a specific grammar rule. These functions recursively call each other to parse nested structures.

### Parsing Process

The parsing process in `jsonic` can be summarized as follows:

1. **Initialization:** When `Jsonic()` is called, it initializes a new parser instance with the default or user-provided options. The options control various aspects of the parsing process, including the allowed syntax, error handling, and plugin configurations.
2. **Lexing:** The input string is passed to the lexer, which scans the string character by character. The lexer uses regular expressions and custom matching functions (as defined in the options) to identify and extract tokens. Each token is represented by an object containing its type, value, and location in the source string.
3. **Parsing:** The parser receives the stream of tokens from the lexer. It uses a set of parsing rules, defined by the `jsonic` grammar, to construct an AST. The parser starts with a top-level rule (typically 'val') and recursively applies other rules based on the current token and the grammar.
4. **AST Construction:** As the parser applies the rules, it builds an AST that represents the structure of the input data. The AST is a hierarchical tree structure where each node corresponds to a grammar rule or a token.
5. **Result:** Once the entire input has been parsed, the parser returns the root node of the AST. This node represents the parsed JSON value, which can be a primitive value, an object, or an array.

### Grammar Definition

The grammar of `jsonic` is defined using a set of rules. Each rule specifies how a particular syntactic construct can be recognized and parsed. Rules are defined using the `jsonic.rule()` method, which takes a rule name and a rule definer function.

A rule definer function takes a `RuleSpec` object and modifies it to define the rule's behavior. It primarily uses the `open` and `close` methods to specify the token sequences that mark the beginning and end of a rule, respectively.

Let's illustrate this with a simplified example:

```javascript
jsonic.rule('map', (rs: RuleSpec) => {
  rs.bo((r: Rule) => {
    // Create a new empty map.
    r.node = {}
  })
  .open([
    // An empty map: {}.
    { s: [OB, CB], b: 1, n: { pk: 0 }, g: 'map,json' },
    // Start matching map key-value pairs: a:1.
    // Reset counter n.pk as new map (for extensions).
    { s: [OB], p: 'pair', n: { pk: 0 }, g: 'map,json,pair' },
  ])
  .close([
    // End of map.
    { s: [CB], g: 'end,json' },
  ])
});
```

In this example, the `map` rule is defined to match a JSON object. The `bo` method sets up the initial node for the rule as an empty object. The `open` method specifies two possible starting token sequences:

1. `OB, CB`: Matches an empty object `{}`.
2. `OB`: Matches the opening brace of a non-empty object, and pushes the `pair` rule onto the stack to parse the key-value pairs.

The `close` method specifies that a closing brace `CB` marks the end of the map.

### Extensibility

`jsonic` is designed to be extensible, allowing users to customize the parsing process and add support for new syntax features. This extensibility is achieved through several mechanisms:

1. **Options:** `jsonic` provides a wide range of options that control various aspects of the parsing process. These options can be used to modify the behavior of the lexer and parser, enabling users to fine-tune the parsing process to their specific needs.

2. **Plugins:** Plugins are a powerful mechanism for extending `jsonic`. A plugin is a function that takes a `jsonic` instance as an argument and can modify its behavior by:

    *   Adding new lexer matchers using `jsonic.lex()`.
    *   Defining new parsing rules or modifying existing ones using `jsonic.rule()`.
    *   Adding custom options to the `jsonic.options` object.

3. **Custom Lexer Matchers:** Users can define custom lexer matchers to recognize new token types. These matchers are functions that take the current lexer state and return a token object if a match is found.

4. **Custom Rule Actions:** Rule definitions can include custom actions that are executed when a rule matches. These actions can be used to modify the parsed data, perform validation, or trigger other custom logic.

### Error Handling

`jsonic` includes robust error handling capabilities. When the parser encounters an unexpected token or a syntax error, it throws a `JsonicError` exception. This exception provides detailed information about the error, including the error code, a descriptive message, and the location of the error in the source string.

The error messages are customizable through the `error` option, and hints can be provided using the `hint` option.

### Example: Adding Support for Comments

Let's illustrate how to extend `jsonic` with a simple example. We'll add support for single-line comments starting with `//`.

1. **Define a Lexer Matcher:**

    ```javascript
    function makeCommentMatcher(cfg, _opts) {
      return function matchComment(lex) {
        let pnt = lex.pnt
        let src = lex.src
        let sI = pnt.sI

        if (src.substring(sI).startsWith('//')) {
          let end = src.indexOf('\n', sI)
          if (-1 === end) {
            end = src.length
          }
          let comment = src.substring(sI, end)
          let tkn = lex.token('#CM', comment, comment, pnt)
          pnt.sI += comment.length
          pnt.cI += comment.length
          return tkn
        }
      }
    }
    ```

2. **Register the Matcher:**

    ```javascript
    let j = Jsonic.make({
      lex: {
        match: {
          comment: { order: 1e5, make: makeCommentMatcher },
        },
      },
    })
    ```

    We add a new lexer matcher named `comment` with a high order to ensure it runs before other matchers. The `makeCommentMatcher` function creates a matcher that recognizes `//` comments and generates a `#CM` token.

3. **Ignore the Comment Token:**

    ```javascript
    j.options({
      tokenSet: {
        IGNORE: ['#SP', '#LN', '#CM'], // Add #CM to IGNORE
      },
    })
    ```

    We add the `#CM` token to the `IGNORE` token set, so the parser ignores it.

Now, `jsonic` will correctly parse JSON with single-line comments:

```javascript
let result = j(`
{
  // This is a comment
  "a": 1,
  "b": 2 // Another comment
}
`)

console.log(result) // Output: { a: 1, b: 2 }
```

This example demonstrates how to extend `jsonic` with custom lexing and parsing logic to support new syntax features. By defining custom lexer matchers and modifying the parsing rules, you can tailor `jsonic` to your specific needs.

### Conclusion

`jsonic` is a powerful and flexible JSON parser that offers a more lenient syntax and extensive customization options. Its modular architecture, based on a configurable lexer and a rule-based parser, makes it highly extensible. By understanding how `jsonic` works, developers can leverage its capabilities to parse a wide range of JSON-like data formats and even define their own custom JSON dialects.

This detailed overview provides a solid foundation for understanding the inner workings of `jsonic`. For further exploration, refer to the official documentation and the source code of the library and its plugins.

## About `pythonmonkey`

[`pythonmonkey`](https://github.com/Distributive-Network/PythonMonkey) is a powerful tool that embeds the SpiderMonkey JavaScript engine into the Python runtime, enabling seamless interoperability between JavaScript and Python. This article will delve into the technical details of how `pythonmonkey` achieves this integration, covering its core mechanisms and design choices.

### Architecture Overview

At its heart, `pythonmonkey` has two main components:

1. **SpiderMonkey Integration**: The library embeds the SpiderMonkey JavaScript engine, providing the capability to execute JavaScript code within the Python process.
2. **Python-JavaScript Bridge**: This component facilitates communication and data exchange between the two language runtimes. It handles object wrapping, type coercion, and function calls across the boundary.

### SpiderMonkey Embedding

`pythonmonkey` statically links to a specific version of SpiderMonkey. During the build process, the SpiderMonkey source code (obtained from mozilla-central repository) is compiled and linked with the `pythonmonkey` library. This creates a single library that contains both the Python extension and the JavaScript engine.

The build process uses `CMake` as the build system, and `build.py` is the main Python script that orchestrates the build process.

### Python-JavaScript Bridge

The bridge is the crucial part that enables interoperability. It consists of several key mechanisms:

1. **Context Creation**: When `pythonmonkey` is initialized, it creates a JSContext. This context represents an isolated instance of the SpiderMonkey engine.
2. **Global Object**: A JavaScript global object is created within the context. This object serves as the global namespace for JavaScript code executed by `pythonmonkey`.
3. **Object Wrapping**: `pythonmonkey` employs a system of proxy objects to enable interaction between Python and JavaScript objects:

    *   **JSObjectProxy**: This Python class acts as a proxy for JavaScript objects. It overrides methods like `__getattr__`, `__setattr__`, and `__delattr__` to delegate operations to the underlying JavaScript object using the SpiderMonkey API.
    *   **JSArrayProxy**: This is similar to `JSObjectProxy` but specifically handles JavaScript arrays, also conforming to Python's list interface.
    *   **JSFunctionProxy**: This wraps JavaScript functions, allowing them to be called from Python.
    *   **JSMethodProxy**: This wraps JavaScript functions that are expected to act as methods (i.e., have a 'this' context) when called from Python.
4. **Type Coercion**: `pythonmonkey` automatically coerces data types when values cross the language boundary. It handles intrinsic types (numbers, booleans, strings, `None`, `null`, `undefined`), as well as more complex structures like lists/arrays and dictionaries/objects.

    *   **From JS to Python**:
        *   JavaScript strings are represented by Python's `JSStringProxy` type (String).
        *   JavaScript numbers are represented by Python floats or integers (depending on the size).
        *   JavaScript bigints are represented by `pythonmonkey.bigint` (Integer).
        *   JavaScript booleans are represented by Python bools.
        *   JavaScript functions are represented by `pythonmonkey.JSFunctionProxy`.
        *   JavaScript Date objects are represented by Python `datetime.datetime` objects.
        *   JavaScript Arrays are represented by `pythonmonkey.JSArrayProxy` (List).
        *   JavaScript Objects are represented by `pythonmonkey.JSObjectProxy` (Dict).
        *   JavaScript TypedArrays are represented by Python Buffer, sharing the same memory.
        *   JavaScript Promises are awaitable.
        *   JavaScript Error objects are represented by `pythonmonkey.SpiderMonkeyError` (Error).
        *   JavaScript `null` and `undefined` are represented by `pythonmonkey.null` and `None` respectively.
    *   **From Python to JS**:
        *   Python strings are converted to JS strings, with the possibility of sharing the underlying string buffer for immutable strings.
        *   Python integers are converted to JS numbers or bigints, depending on their size.
        *   Python floats are converted to JS numbers.
        *   Python booleans are converted to JS booleans.
        *   Python lists are represented by JS true arrays and support all Array methods through a JS API Proxy.
        *   Python dictionaries are represented by JS objects.
        *   Python `None` is converted to JS `undefined`.
        *   Python functions are wrapped so they can be called from JS.
        *   Python awaitables are converted to JS Promises.
        *   Python `Buffer` objects are converted to JS `ArrayBuffer` and share the same memory.
        *   Python `datetime.datetime` objects are converted to JS Date objects.
        *   Python Errors are converted to JS Error objects.
5. **Function Calls**: When a Python function is called from JavaScript (e.g., through a callback), `pythonmonkey` creates a wrapper that:

    *   Converts JS arguments to their Python equivalents.
    *   Calls the Python function.
    *   Converts the Python return value to a JavaScript value.
    *   Handles Python exceptions by converting them to JavaScript errors.
    Similarly, when a JavaScript function is called from Python, a `JSFunctionProxy` handles the call by:
    *   Converting Python arguments to their JavaScript equivalents.
    *   Calling the JavaScript function.
    *   Converting the JavaScript return value to a Python object.
    *   Handles JavaScript exceptions by converting them to Python exceptions.
6. **Garbage Collection**: `pythonmonkey` integrates with both Python's and SpiderMonkey's garbage collectors. Proxy objects hold references to their underlying objects in the other runtime, ensuring that they are not prematurely collected.
7. **Event Loop**: `pythonmonkey` utilizes the Python asyncio event loop to manage asynchronous operations in JavaScript. It provides APIs to schedule tasks on the event loop and to await JavaScript promises from Python.

### Internal Bindings

`pythonmonkey` provides a special function called `internalBinding`. This function allows JavaScript code to access certain built-in modules that are implemented in C++ for performance or to expose platform-specific functionality. These internal bindings are analogous to Node.js's internal modules.

### Example: `eval`

The `pythonmonkey.eval` function is a good example of how the bridge works:

```python
import pythonmonkey as pm

result = pm.eval("1 + 1")
print(result)
```

In this example:

1. The Python string `"1 + 1"` is passed to the `pm.eval` function.
2. `pm.eval` uses the SpiderMonkey API to parse and compile the JavaScript code.
3. The compiled code is executed within the SpiderMonkey context.
4. The result (the number 2) is returned as a JavaScript value.
5. `pythonmonkey` automatically coerces the JavaScript number to a Python float.
6. The Python code then prints the result.

### Example: Calling Python from JS

```javascript
// In JavaScript
const python = require('pythonmonkey').python;
const result = python.eval('1 + 1');
console.log(result);
```

Here:

1. The JavaScript code uses the `require` function (provided by `pythonmonkey`'s CommonJS implementation) to import the `python` object.
2. The `python.eval` function is called, which internally calls the corresponding Python function in `pythonmonkey`.
3. The Python code evaluates the expression and returns the result.
4. The result is automatically converted to a JavaScript number and printed to the console.

### Conclusion

`pythonmonkey` provides a sophisticated integration between Python and JavaScript, enabling developers to leverage the strengths of both languages within a single application. The library carefully manages object lifetimes, handles type conversions, and provides mechanisms for asynchronous operations, making it a powerful tool for building hybrid applications. Understanding its internal workings can help developers make the most of its capabilities and write efficient and robust interoperable code.


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

## Versioning

This project uses semantic versioning. To create a new release:

1. Commit your changes
2. Create a new git tag following semantic versioning principles:
   ```bash
   # For a patch release
   git tag v0.1.1

   # For a minor release
   git tag v0.2.0

   # For a major release
   git tag v1.0.0
   ```
3. Push the tag to trigger the PyPI publishing workflow:
   ```bash
   git push origin v0.1.1
   ```

