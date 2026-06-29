"""Version information."""
import importlib.metadata

try:
    __version__ = importlib.metadata.version("salvajson")
except importlib.metadata.PackageNotFoundError:
    # Package is not installed, e.g., when running from source directory
    # or during build process before metadata is available.
    # Fallback or indicate development version.
    # Hatch-vcs might replace this file content during build.
    # For local editable installs, `hatch version` or git describe can be sources.
    # This placeholder is fine if hatch-vcs correctly populates it at build time.
    __version__ = "0.0.0.dev0"
