"""Core functionality for salvaging corrupted JSON files using jsonic."""

from pathlib import Path
from typing import Final

from pythonmonkey import require  # type: ignore

_SALVAJSON_DIR: Final[Path] = Path(__file__).parent.absolute()
_salvajson_js = require(str(_SALVAJSON_DIR / "salvajson.js"))


def salvaj(json_str: str) -> str:
    """Re-parse potentially corrupted JSON string using jsonic.

    Args:
        json_str: The JSON string to parse

    Returns:
        Fixed JSON string that can be parsed by standard JSON parsers
    """
    return _salvajson_js(json_str)
