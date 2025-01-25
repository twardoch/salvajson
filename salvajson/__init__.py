"""JSON Salvation - Parse corrupted JSON files using jsonic."""

import pathlib

from pythonmonkey import require  # type: ignore

# Get the directory containing this file
salvajson_dir = pathlib.Path(__file__).parent.absolute()
# Load the bundled JS file
salvajson_js = require(str(salvajson_dir / "salvajson.js"))


def salvage(json_str: str) -> str:
    """Re-parse potentially corrupted JSON string using jsonic.

    Args:
        json_str: The JSON string to parse

    Returns:
        Fixed JSON string
    """
    return salvajson_js(json_str)


if __name__ == "__main__":
    from pathlib import Path

    from fire import Fire  # type: ignore

    def cli(path: str | Path):
        return salvage(Path(path).read_text())

    Fire(cli)
