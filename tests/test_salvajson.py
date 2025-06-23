"""Tests for salvajson package."""

import json
import re
from pathlib import Path

import orjson  # For testing loads fallback
import pytest
from pythonmonkey import SpiderMonkeyError  # Import the specific error

from salvajson import __version__, dumps, loads, salvaj  # Import dumps and loads
from salvajson.__main__ import cli

# Test data
VALID_JSON = """{"name": "John", "age": 30}"""

CORRUPTED_CASES = [
    # Missing quotes around property names
    ("""{name: "John", age: 30}""", """{"name":"John","age":30}"""),
    # Single quotes instead of double quotes
    ("""{'name': 'John', 'age': 30}""", """{"name":"John","age":30}"""),
    # Trailing commas
    ("""{"name": "John", "age": 30,}""", """{"name":"John","age":30}"""),
    # Missing commas
    ("""{"name": "John" "age": 30}""", """{"name":"John","age":30}"""),
    # Unquoted string values
    ("""{"name": John, "age": 30}""", """{"name":"John","age":30}"""),
    # Comments in JSON
    (
        """{"name": "John", // This is a comment
        "age": 30}""",
        """{"name":"John","age":30}""",
    ),
]

# Cases that should raise errors
ERROR_CASES = [
    # Reversed braces
    "}{",
    # Mismatched brackets
    "{[}]",
]


@pytest.mark.parametrize("corrupted,expected", CORRUPTED_CASES)  # noqa: PT006
def test_salvaj_corrupted_json(corrupted: str, expected: str):
    """Test salvaging various forms of corrupted JSON."""
    result = salvaj(corrupted)
    # Verify the result can be parsed as valid JSON
    parsed = json.loads(result)
    expected_parsed = json.loads(expected)
    assert parsed == expected_parsed


def test_salvaj_valid_json():
    """Test that valid JSON passes through unchanged."""
    result = salvaj(VALID_JSON)
    assert json.loads(result) == json.loads(VALID_JSON)


@pytest.mark.parametrize("invalid_json", ERROR_CASES)
def test_salvaj_error_cases(invalid_json: str):
    """Test that appropriate errors are raised for invalid JSON."""
    # Expect salvaj to raise SpiderMonkeyError directly
    with pytest.raises(SpiderMonkeyError) as excinfo:
        salvaj(invalid_json)
    # Check if the error message contains typical Jsonic error parts.
    # Jsonic error messages, when wrapped by SpiderMonkeyError, will contain
    # identifiable substrings.
    error_message = str(excinfo.value)
    # Examples from Jsonic: "[jsonic/unexpected]: unexpected character(s): }"
    # or "[jsonic/unterminated]: unterminated string"
    assert "[jsonic/" in error_message or "SyntaxError:" in error_message


def test_cli_with_file(tmp_path: Path):
    """Test CLI functionality with a file input."""
    # Create a test file
    test_file = tmp_path / "test.json"
    test_file.write_text(CORRUPTED_CASES[0][0])

    # Test CLI
    result = cli(str(test_file))
    assert json.loads(result) == json.loads(CORRUPTED_CASES[0][1])


def test_cli_file_not_found():
    """Test CLI handles missing files appropriately."""
    with pytest.raises(FileNotFoundError):
        cli("nonexistent.json")


def test_cli_with_invalid_json(tmp_path: Path):
    """Test CLI with invalid JSON file."""
    test_file = tmp_path / "invalid.json"
    test_file.write_text(ERROR_CASES[0])

    with pytest.raises(SpiderMonkeyError) as excinfo:
        cli(str(test_file))
    # Check if the error message contains typical Jsonic error parts.
    error_message = str(excinfo.value)
    # Examples from Jsonic: "[jsonic/unexpected]: unexpected character(s): }"
    # or "[jsonic/unterminated]: unterminated string"
    assert "[jsonic/" in error_message or "SyntaxError:" in error_message


def test_version():
    """Test that version is properly formatted."""
    assert isinstance(__version__, str)
    assert re.match(
        r"^\d+\.\d+\.\d+$",
        __version__,
    ), "Version should be in format X.Y.Z"


# Tests for salvajson.dumps
def test_dumps_basic():
    """Test basic serialization with dumps."""
    data = {"name": "Alice", "age": 30}
    expected_json = """{"name":"Alice","age":30}"""
    assert json.loads(dumps(data)) == json.loads(expected_json)


def test_dumps_with_indent():
    """Test dumps with indentation."""
    data = {"name": "Bob", "age": 25}
    # orjson.OPT_INDENT_2 produces two spaces
    expected_json = """{\n  "name": "Bob",\n  "age": 25\n}"""
    assert dumps(data, indent=2) == expected_json


def test_dumps_with_sort_keys():
    """Test dumps with sorted keys."""
    data = {"b": 1, "a": 2, "c": {"z": 0, "x": 1}}
    # Note: orjson sorts keys at all levels
    expected_json_sorted = """{"a":2,"b":1,"c":{"x":1,"z":0}}"""
    # With indent for visual comparison and combined testing
    expected_json_sorted_indented = (
        """{\n  "a": 2,\n  "b": 1,\n  "c": {\n    "x": 1,\n    "z": 0\n  }\n}"""
    )
    assert json.loads(dumps(data, sort_keys=True)) == json.loads(expected_json_sorted)
    assert dumps(data, sort_keys=True, indent=2) == expected_json_sorted_indented


def test_dumps_compatibility_params():
    """Test that dumps ignores unhandled standard json.dumps params."""
    data = {"key": "value"}
    # These params are listed as ignored in the docstring
    assert (
        dumps(
            data,
            skipkeys=True,
            ensure_ascii=False,
            check_circular=False,
            allow_nan=False,
            cls=None,
            separators=(",", ":"),
            default=None,
        )
        == """{"key":"value"}"""
    )


# Placeholder for numpy/datetime tests if numpy/datetime objects are easily available
# import numpy as np
# from datetime import datetime, timezone
# def test_dumps_numpy_datetime():
#     """Test dumps with numpy array and datetime object."""
#     data = {
#         "array": np.array([1, 2, 3]),
#         "timestamp": datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
#     }
#     expected_json = """{"array":[1,2,3],"timestamp":"2023-01-01T12:00:00Z"}"""
#     # This requires numpy to be installed. If it's not a direct dependency,
#     # this test might need to be conditional or numpy added to test deps.
#     # For now, will assume orjson handles it if the options are passed.
#     # The key is that options OPT_SERIALIZE_NUMPY and OPT_NAIVE_UTC are used.
#     # We can't directly verify the output without these libs.
#     # A simpler check is that it doesn't FAIL with these options set by default.
#     # For now, this test will be commented out unless numpy is added to test deps.
#     pass


def test_package_version():
    """Test that the package version is available and correctly formatted."""
    assert isinstance(__version__, str)
    # Basic semver check (X.Y.Z)
    # This regex also allows for dev versions like 0.1.dev2+gc06f597
    version_pattern = r"^\d+\.\d+\.\d+(?:\.dev\d+\+g[a-f0-9]+)?$"
    assert re.match(version_pattern, __version__), (
        f"Version {__version__} does not match semantic versioning pattern."
    )

    # Check consistency with importlib.metadata
    # This might fail if the package is not installed in editable mode
    # or if hatch-vcs hasn't built the metadata yet.
    # It's more of an integration check for the build/install process.
    try:
        import importlib.metadata
        installed_version = importlib.metadata.version("salvajson")
        assert __version__ == installed_version
    except importlib.metadata.PackageNotFoundError:
        # This is acceptable if running tests directly from source without installation
        # or if `_version.py` fallback is active.
        # In a CI environment after install, this should ideally not be hit.
        pass # Or print a warning: warnings.warn("salvajson not installed, skipping metadata version check")


# Tests for salvajson.loads
def test_loads_valid_json():
    """Test loads with valid JSON string and bytes."""
    valid_json_str = """{"name": "Charlie", "score": 100}"""
    valid_json_bytes = valid_json_str.encode("utf-8")
    expected_data = {"name": "Charlie", "score": 100}

    assert loads(valid_json_str) == expected_data
    assert loads(valid_json_bytes) == expected_data


def test_loads_corrupted_json_fallback():
    """Test loads fallback mechanism for corrupted JSON."""
    # This JSON is one of the CORRUPTED_CASES that salvaj can fix
    corrupted_json_str = """{name: "David", 'details': [1 2]}"""
    # Expected after salvaj fixes it and orjson parses that
    expected_data_after_salvaj = {"name": "David", "details": [1, 2]}

    # orjson alone would fail on this
    with pytest.raises(orjson.JSONDecodeError):
        orjson.loads(corrupted_json_str)

    # salvajson.loads should fix it using salvaj and then parse
    assert loads(corrupted_json_str) == expected_data_after_salvaj

    # Test with bytes input as well
    corrupted_json_bytes = corrupted_json_str.encode("utf-8")
    assert loads(corrupted_json_bytes) == expected_data_after_salvaj


def test_loads_error_case_after_fallback():
    """Test loads with JSON so corrupted that even salvaj fails."""
    # This JSON is one of the ERROR_CASES
    very_corrupted_json_str = ERROR_CASES[0]  # e.g., "}{"

    # Expect SpiderMonkeyError as salvaj will be called and fail
    with pytest.raises(SpiderMonkeyError) as excinfo:
        loads(very_corrupted_json_str)

    error_message = str(excinfo.value)
    assert "[jsonic/" in error_message or "SyntaxError:" in error_message

    # Test with bytes input as well
    very_corrupted_json_bytes = very_corrupted_json_str.encode("utf-8")
    with pytest.raises(SpiderMonkeyError) as excinfo_bytes:
        loads(very_corrupted_json_bytes)

    error_message_bytes = str(excinfo_bytes.value)
    assert "[jsonic/" in error_message_bytes or "SyntaxError:" in error_message_bytes


def test_loads_compatibility_params():
    """Test that loads ignores unhandled standard json.loads params."""
    valid_json_str = """{"key": "value"}"""
    expected_data = {"key": "value"}
    # These params are listed as ignored in the docstring
    assert (
        loads(
            valid_json_str,
            cls=None,
            object_hook=None,
            parse_float=None,
            parse_int=None,
            parse_constant=None,
            object_pairs_hook=None,
        )
        == expected_data
    )
