"""Tests for salvajson package."""

import json
from pathlib import Path

import pytest

from salvajson import salvage
from salvajson.__main__ import cli, main

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

ERROR_CASES = [
    # Empty input
    "",
    # Invalid syntax that can't be recovered
    "{{",
    # Incomplete object
    '{"name":',
]


@pytest.mark.parametrize("corrupted,expected", CORRUPTED_CASES)
def test_salvage_corrupted_json(corrupted: str, expected: str):
    """Test salvaging various forms of corrupted JSON."""
    result = salvage(corrupted)
    # Verify the result can be parsed as valid JSON
    parsed = json.loads(result)
    expected_parsed = json.loads(expected)
    assert parsed == expected_parsed


def test_salvage_valid_json():
    """Test that valid JSON passes through unchanged."""
    result = salvage(VALID_JSON)
    assert json.loads(result) == json.loads(VALID_JSON)


@pytest.mark.parametrize("invalid_json", ERROR_CASES)
def test_salvage_error_cases(invalid_json: str):
    """Test that appropriate errors are raised for invalid JSON."""
    with pytest.raises(Exception):
        salvage(invalid_json)


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


def test_main_success(capsys, tmp_path: Path):
    """Test main function success path."""
    # Create a test file
    test_file = tmp_path / "test.json"
    test_file.write_text(CORRUPTED_CASES[0][0])

    # Mock sys.argv
    import sys

    original_argv = sys.argv
    sys.argv = ["salvajson", str(test_file)]
    try:
        exit_code = main()
        assert exit_code == 0
        captured = capsys.readouterr()
        assert json.loads(captured.out.strip()) == json.loads(CORRUPTED_CASES[0][1])
    finally:
        sys.argv = original_argv


def test_main_error(capsys):
    """Test main function error path."""
    import sys

    original_argv = sys.argv
    sys.argv = ["salvajson", "nonexistent.json"]
    try:
        exit_code = main()
        assert exit_code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err
    finally:
        sys.argv = original_argv
