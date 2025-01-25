"""JSON Salvation - Parse corrupted JSON files using jsonic.

This package provides tools for parsing and fixing corrupted JSON files using the
powerful jsonic parser. It bridges Python and JavaScript through PythonMonkey to
leverage jsonic's flexible parsing capabilities.

Example:
    >>> from salvajson import salvage
    >>> corrupted = '{name: "John", age: 30}'
    >>> fixed = salvage(corrupted)
    >>> print(fixed)
    {"name":"John","age":30}

The package also provides a command-line interface:
    $ python -m salvajson input.json
"""

import sys
from importlib.metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

from .salvajson import salvage

__all__ = ["salvage", "__version__"]
