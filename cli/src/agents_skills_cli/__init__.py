"""agents-skills CLI package."""

from __future__ import annotations

import json
from pathlib import Path

import httpx


__all__ = ["__version__"]

_FALLBACK_VERSION = "0.1.0"
_HTTP_OK = 200


def _load_version() -> str:
    """Load version from version.json, with fallback to remote and hardcoded default."""
    pkg_dir = Path(__file__).parent.parent.parent

    local_version_file = pkg_dir / "cli" / "version.json"
    if local_version_file.exists():
        try:
            data = json.loads(local_version_file.read_text(encoding="utf-8"))
            if isinstance(data, dict) and "version" in data:
                return data["version"]
        except (json.JSONDecodeError, OSError):
            pass

    try:
        resp = httpx.get(
            "https://raw.githubusercontent.com/rapid-recovery-agency-inc/agents-skills/refs/heads/main/cli/version.json",
            timeout=5.0,
        )
        if resp.status_code == _HTTP_OK:
            data = resp.json()
            if isinstance(data, dict) and "version" in data:
                return data["version"]
    except Exception:
        pass

    return _FALLBACK_VERSION


__version__: str = _load_version()
