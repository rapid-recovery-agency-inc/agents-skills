#!/usr/bin/env python3
"""Update version.json from pyproject.toml version field.

This script is intended to be run as a pre-push hook to keep version.json
in sync with the version defined in cli/pyproject.toml.
"""

import re
import json
from pathlib import Path

def main() -> None:
    repo_root = Path(__file__).parent.parent
    pyproject = repo_root / "cli" / "pyproject.toml"
    version_file = repo_root / "cli" / "version.json"

    if not pyproject.exists():
        raise FileNotFoundError(f"pyproject.toml not found at {pyproject}")

    content = pyproject.read_text(encoding="utf-8")
    match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
    if not match:
        raise ValueError("Version not found in pyproject.toml")

    version = match.group(1)
    version_file.write_text(
        json.dumps({"version": version}, indent=2) + "\n",
        encoding="utf-8"
    )
    print(f"Updated version.json to {version}")

if __name__ == "__main__":
    main()
