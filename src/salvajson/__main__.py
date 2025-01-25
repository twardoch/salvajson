"""Command-line interface for salvajson."""

import sys
from pathlib import Path

from fire import Fire  # type: ignore

from . import salvage


def cli(path: str | Path) -> str:
    """Parse potentially corrupted JSON file using jsonic.

    Args:
        path: Path to the JSON file to parse

    Returns:
        Fixed JSON string that can be parsed by standard JSON parsers

    Raises:
        FileNotFoundError: If the input file doesn't exist
    """
    input_path = Path(path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    return salvage(input_path.read_text())


def main():
    """Main entry point for the CLI."""
    try:
        result = Fire(cli)
        print(result)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
