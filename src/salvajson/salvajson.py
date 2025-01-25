"""Core functionality for salvaging corrupted JSON files using jsonic."""

from pathlib import Path
from typing import Final, NoReturn

from pythonmonkey import require  # type: ignore


class SalvajsonError(Exception):
    """Base exception for salvajson errors."""

    def __init__(self, message: str, original_error: Exception | None = None):
        """Initialize error with message and optional original error.

        Args:
            message: Error message
            original_error: Original exception that caused this error
        """
        super().__init__(message)
        self.original_error = original_error


class ParseError(SalvajsonError):
    """Raised when JSON parsing fails."""

    pass


_SALVAJSON_DIR: Final[Path] = Path(__file__).parent.absolute()
_salvajson_js = require(str(_SALVAJSON_DIR / "salvajson.js"))

# Cache for repeated operations
_parse_cache: dict[str, str] = {}


def salvage(json_str: str) -> str:
    """Re-parse potentially corrupted JSON string using jsonic.

    Args:
        json_str: The JSON string to parse

    Returns:
        Fixed JSON string that can be parsed by standard JSON parsers

    Raises:
        ParseError: If the JSON cannot be salvaged
        SalvajsonError: For other errors
    """
    if not json_str:
        raise ParseError("Empty JSON string")

    # Check cache first
    if json_str in _parse_cache:
        return _parse_cache[json_str]

    try:
        result = _salvajson_js(json_str)
        # Cache successful results
        _parse_cache[json_str] = result
        return result
    except Exception as e:
        if "SyntaxError" in str(e):
            raise ParseError(f"Invalid JSON syntax: {str(e)}") from e
        raise SalvajsonError(f"Failed to parse JSON: {str(e)}") from e
