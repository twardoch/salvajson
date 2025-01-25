"""Command-line interface for salvajson."""

import sys
from pathlib import Path
from typing import NoReturn

from fire import Fire  # type: ignore

from . import salvage
from .salvajson import ParseError, SalvajsonError


def cli(path: str | Path) -> str:
    """Parse potentially corrupted JSON file using jsonic.

    Args:
        path: Path to the JSON file to parse

    Returns:
        Fixed JSON string that can be parsed by standard JSON parsers

    Raises:
        FileNotFoundError: If the input file doesn't exist
        ParseError: If the JSON cannot be salvaged
        SalvajsonError: For other errors
    """
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if not file_path.is_file():
        raise ValueError(f"Not a file: {path}")

    try:
        return salvage(file_path.read_text())
    except (ParseError, SalvajsonError) as e:
        # Re-raise these errors for proper error messages
        raise
    except Exception as e:
        # Wrap unexpected errors
        raise SalvajsonError(f"Unexpected error while processing {path}") from e


def main() -> int:
    """Main entry point for the CLI.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        # Don't print the result here since Fire will print it
        Fire(cli)
        return 0
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ParseError as e:
        print(f"Parse Error: {e}", file=sys.stderr)
        return 1
    except SalvajsonError as e:
        print(f"Error: {e}", file=sys.stderr)
        if e.original_error:
            print(f"Caused by: {e.original_error}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
