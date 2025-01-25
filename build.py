"""Build script for salvajson package."""

import subprocess
from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


def get_version_from_git_tag() -> str:
    """Extract version from the latest git tag.

    Returns:
        str: Version string, or '0.0.0' if no tag is found
    """
    try:
        # Get the latest tag that starts with 'v'
        tag = subprocess.check_output(
            ["git", "describe", "--tags", "--abbrev=0"], text=True
        ).strip()

        # Remove the 'v' prefix if present
        return tag[1:] if tag.startswith("v") else tag
    except subprocess.CalledProcessError:
        # Fallback to a default version if no tag is found
        return "0.0.0"


class CustomBuildHook(BuildHookInterface):
    """Build hook to compile JS assets and set version during package build."""

    def initialize(self, version, build_data):
        """Run during the initialization phase of the build.

        Args:
            version: The version of the build
            build_data: Build configuration data
        """
        # Only build JS during sdist builds
        if not self.target_name == "sdist":
            return

        root_dir = Path(__file__).parent
        js_src_dir = root_dir / "js_src"
        pkg_dir = root_dir / "src" / "salvajson"

        # Create package directory if it doesn't exist
        pkg_dir.mkdir(parents=True, exist_ok=True)

        # Install npm dependencies
        subprocess.run(["npm", "install"], cwd=js_src_dir, check=True)

        # Build the JS bundle
        cmd = ["node", "build.esbuild.js"]
        subprocess.run(cmd, cwd=js_src_dir, check=True)

    def get_version(self):
        """Override version extraction to use git tags."""
        return get_version_from_git_tag()
