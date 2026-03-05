#!/usr/bin/env python3
"""Validate skills/registry.yaml against its embedded schema."""

import sys
from pathlib import Path
from typing import Any

import jsonschema
import yaml


def main() -> int:
    # Detect and change to repository root
    repo_root = Path(__file__).parent.parent
    if not (repo_root / "skills" / "registry.yaml").exists():
        print(f"Error: Could not find repository structure at {repo_root}")
        print("This script must be run from within the agents-skills repository")
        return 1

    registry_path = repo_root / "skills" / "registry.yaml"

    if not registry_path.exists():
        print(f"Error: {registry_path} not found")
        return 1

    try:
        with open(registry_path) as f:
            registry = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML in {registry_path}: {e}")
        return 1

    if not isinstance(registry, dict):
        print(f"Error: Registry must be a dictionary, got {type(registry).__name__}")
        return 1

    schema = registry.get("schema")
    if not schema:
        print("Error: No embedded schema found in registry.yaml")
        return 1

    validator = jsonschema.Draft202012Validator(schema)
    errors = list(validator.iter_errors(registry))

    if errors:
        print(f"Error: registry.yaml failed schema validation:")
        for err in errors[:5]:
            path = "/".join(str(p) for p in err.path) or "<root>"
            context = f" (got: {err.instance!r})" if hasattr(err, "instance") else ""
            print(f"  - {path}: {err.message}{context}")
        if len(errors) > 5:
            print(f"  ... and {len(errors) - 5} more errors")
        return 1

    print("OK: registry.yaml is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
