#!/usr/bin/env python

from pathlib import Path

from fire import Fire  # type: ignore

from . import salvaj


def cli(path: str | Path) -> str:
    """Parse potentially corrupted JSON file using jsonic.

    Args:
        path: Path to the JSON file to parse

    Returns:
        Fixed JSON string that can be parsed by standard JSON parsers
    """
    return salvaj(Path(path).read_text())


if __name__ == "__main__":
    Fire(cli)
