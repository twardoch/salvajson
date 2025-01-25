"""JSON Salvation - Parse corrupted JSON files using jsonic.

This package provides tools for parsing and fixing corrupted JSON files using
the powerful jsonic parser. It bridges Python and JavaScript through
PythonMonkey to leverage jsonic's flexible parsing capabilities.

Example:
    >>> from salvajson import salvage
    >>> corrupted = '{name: "John", age: 30}'
    >>> fixed = salvage(corrupted)
    >>> print(fixed)
    {"name":"John","age":30}

The package also provides a command-line interface:
    $ python -m salvajson input.json
"""

__version__ = "0.1.0"

from .salvajson import salvage

__all__ = ["salvage", "__version__"]
