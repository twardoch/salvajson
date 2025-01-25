"""JSON Salvation - Parse corrupted JSON files using jsonic.

This package provides tools for parsing and fixing corrupted JSON files using
the powerful jsonic parser. It bridges Python and JavaScript through
PythonMonkey to leverage jsonic's flexible parsing capabilities.

The package provides three main functions:

    salvaj(json_str: str) -> str
        Parse potentially corrupted JSON strings using jsonic and return
        valid JSON.

    dumps(obj, *, indent=None, sort_keys=False, **kw) -> str
        Serialize Python objects to JSON strings using orjson for high
        performance. Supports standard json.dumps() parameters for
        compatibility.

    loads(s: bytes | str, **kw) -> Any
        Parse JSON strings into Python objects using orjson for high
        performance, with fallback to jsonic (salvaj). Supports standard
        json.loads() parameters for compatibility.

Example:
    >>> from salvajson import salvaj, dumps, loads
    >>> corrupted = '{name: "John", age: 30}'
    >>> fixed = salvaj(corrupted)
    >>> print(fixed)
    {"name":"John","age":30}
    >>> data = loads(fixed)
    >>> print(dumps(data, indent=2))
    {
      "name": "John",
      "age": 30
    }

The package also provides a command-line interface:
    $ python -m salvajson input.json
"""

from ._version import __version__
from .salvajson import dumps, loads, salvaj

__all__ = ["__version__", "dumps", "loads", "salvaj"]
