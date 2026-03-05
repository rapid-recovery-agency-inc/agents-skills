"""agents-skills CLI package."""

from __future__ import annotations

from importlib.metadata import version as get_version

__all__ = ["__version__"]

try:
    __version__: str = get_version("agents-skills")
except Exception:
    __version__ = "0.0.0"
