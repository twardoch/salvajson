"""Build script for salvajson package."""

import subprocess
from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


def get_version_from_git_tag() -> str:
    """Extract version from the latest git tag.

    Returns:
        str: Version string from git tag, or "0.0.0" if not available
    """
    try:
        # Get the latest tag that starts with 'v'
        tag = subprocess.check_output(
            ["git", "describe", "--tags", "--abbrev=0"],
            text=True,
            stderr=subprocess.DEVNULL,  # Suppress stderr
        ).strip()

        # Remove the 'v' prefix if present and return
        return tag[1:] if tag.startswith("v") else tag
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "0.0.0"


# This variable is required by Hatch for version detection
VERSION = get_version_from_git_tag()


class CustomBuildHook(BuildHookInterface):
    """Custom build hook for hatchling."""

    def initialize(self, version: str, build_data: dict) -> None:
        """Initialize the build process.

        Args:
            version: The version of the build
            build_data: Build configuration data
        """
        super().initialize(version, build_data)

        # Build JS for both sdist and wheel
        root_dir = Path(self.root)
        js_src_dir = root_dir / "js_src"
        pkg_dir = root_dir / "src" / "salvajson"

        # Create package directory if it doesn't exist
        pkg_dir.mkdir(parents=True, exist_ok=True)

        # Build JS bundle
        build_js_bundle(js_src_dir, pkg_dir)


def build_js_bundle(js_src_dir: Path, pkg_dir: Path) -> None:
    """Build the JavaScript bundle.

    Args:
        js_src_dir: Directory containing JavaScript source files
        pkg_dir: Directory where the bundle should be placed

    Raises:
        subprocess.CalledProcessError: If npm build fails
        RuntimeError: If bundle is not created in correct location
    """
    # Ensure node_modules exists
    if not (js_src_dir / "node_modules").exists():
        subprocess.run(["npm", "ci"], cwd=js_src_dir, check=True)

    # Build the bundle
    subprocess.run(["npm", "run", "build"], cwd=js_src_dir, check=True)

    # Verify bundle exists in correct location
    bundle_path = pkg_dir / "salvajson.js"
    if not bundle_path.exists():
        msg = f"JS bundle not found at expected location: {bundle_path}"
        raise RuntimeError(msg)


if __name__ == "__main__":
    # For manual builds
    root_dir = Path(__file__).parent
    js_src_dir = root_dir / "js_src"
    pkg_dir = root_dir / "src" / "salvajson"

    # Ensure package directory exists
    pkg_dir.mkdir(parents=True, exist_ok=True)

    # Build JS bundle
    build_js_bundle(js_src_dir, pkg_dir)

    print("JavaScript bundle built successfully!")
