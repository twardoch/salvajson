"""Tests for salvajson package."""

import json
import re
from pathlib import Path

import pytest

from salvajson import __version__, salvaj
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


@pytest.mark.parametrize("corrupted,expected", CORRUPTED_CASES)
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
    result = salvaj(invalid_json)
    with pytest.raises(json.JSONDecodeError):
        json.loads(result)


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

    result = cli(str(test_file))
    with pytest.raises(json.JSONDecodeError):
        json.loads(result)


def test_version():
    """Test that version is properly formatted."""
    assert isinstance(__version__, str)
    assert re.match(r"^\d+\.\d+\.\d+$", __version__), (
        "Version should be in format X.Y.Z"
    )
