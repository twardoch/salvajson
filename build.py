"""Build script for salvajson package."""

import subprocess
from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    """Build hook to compile JS assets during package build."""

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
