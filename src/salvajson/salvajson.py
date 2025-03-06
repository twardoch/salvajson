"""Core functionality for salvaging corrupted JSON files using jsonic."""

from collections.abc import Callable
from pathlib import Path
from typing import Final

import orjson
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


def dumps(
    obj: dict | list | int | float | str | None,
    *,
    skipkeys: bool = False,
    ensure_ascii: bool = True,
    check_circular: bool = True,
    allow_nan: bool = True,
    cls: type | None = None,
    indent: int | None = None,
    separators: tuple[str, str] | None = None,
    default: Callable | None = None,
    sort_keys: bool = False,
    **kw,
) -> str:
    """Serialize Python object to JSON string using orjson.

    Args:
        obj: Python object to serialize
        skipkeys: Ignored, for compatibility with json.dumps()
        ensure_ascii: Ignored, for compatibility with json.dumps()
        check_circular: Ignored, for compatibility with json.dumps()
        allow_nan: Ignored, for compatibility with json.dumps()
        cls: Ignored, for compatibility with json.dumps()
        indent: If not None, pretty-print with 2-space indentation
        separators: Ignored, for compatibility with json.dumps()
        default: Ignored, for compatibility with json.dumps()
        sort_keys: If True, sort dictionary keys
        **kw: Additional keyword arguments ignored for compatibility

    Returns:
        JSON string representation of the input object
    """
    options = (
        orjson.OPT_NAIVE_UTC | orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_NON_STR_KEYS
    )
    if sort_keys:
        options |= orjson.OPT_SORT_KEYS
    if indent is not None:
        options |= orjson.OPT_INDENT_2

    return orjson.dumps(obj, option=options).decode("utf-8")


def loads(
    s: bytes | str,
    *,
    cls: type | None = None,
    object_hook: Callable | None = None,
    parse_float: Callable | None = None,
    parse_int: Callable | None = None,
    parse_constant: Callable | None = None,
    object_pairs_hook: Callable | None = None,
    **kw,
) -> dict | list | int | float | str | None:
    """Parse JSON string into Python object, with fallback to jsonic parser.

    Args:
        s: JSON string or bytes to parse
        cls: Ignored, for compatibility with json.loads()
        object_hook: Ignored, for compatibility with json.loads()
        parse_float: Ignored, for compatibility with json.loads()
        parse_int: Ignored, for compatibility with json.loads()
        parse_constant: Ignored, for compatibility with json.loads()
        object_pairs_hook: Ignored, for compatibility with json.loads()
        **kw: Additional keyword arguments ignored for compatibility

    Returns:
        Python object parsed from the JSON input

    Raises:
        JSONDecodeError: If parsing fails even after jsonic fallback
    """
    try:
        return orjson.loads(s)
    except orjson.JSONDecodeError:
        if isinstance(s, bytes):
            s = s.encode("utf-8")
        return orjson.loads(str(salvaj(s)))
