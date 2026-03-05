#!/usr/bin/env python3
"""Validate that all skills in skills/ are registered in registry.yaml."""

import sys
from pathlib import Path

import yaml


def find_skills() -> set[str]:
    """Find all skills by scanning for SKILL.md files."""
    skills_dir = Path("skills")
    if not skills_dir.exists():
        return set()

    skills = set()
    for category_dir in skills_dir.iterdir():
        if category_dir.is_dir() and not category_dir.name.startswith("."):
            for skill_dir in category_dir.iterdir():
                if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                    skills.add(f"{category_dir.name}/{skill_dir.name}")
    return skills


def get_registered_skills(registry_path: Path) -> set[str]:
    """Extract skill IDs from registry.yaml."""
    if not registry_path.exists():
        return set()

    try:
        with open(registry_path) as f:
            registry = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML in {registry_path}: {e}")
        return set()

    if not isinstance(registry, dict):
        print(f"Error: Registry must be a dictionary, got {type(registry).__name__}")
        return set()

    skills = registry.get("skills")
    if not isinstance(skills, list):
        print(f"Error: Registry 'skills' must be a list, got {type(skills).__name__}")
        return set()

    registered = set()
    for i, skill in enumerate(skills):
        if not isinstance(skill, dict):
            print(
                f"Error: Skill at index {i} must be a dictionary, got {type(skill).__name__}"
            )
            continue

        skill_id = skill.get("id")
        if not isinstance(skill_id, str):
            print(f"Error: Skill at index {i} missing or invalid 'id' field")
            continue

        registered.add(skill_id)

    return registered


def main() -> int:
    # Detect and change to repository root
    repo_root = Path(__file__).parent.parent
    if not (repo_root / "skills" / "registry.yaml").exists():
        print(f"Error: Could not find repository structure at {repo_root}")
        print("This script must be run from within the agents-skills repository")
        return 1

    registry_path = repo_root / "skills" / "registry.yaml"

    all_skills = find_skills()
    registered_skills = get_registered_skills(registry_path)

    unregistered = all_skills - registered_skills

    if not unregistered:
        print("OK: All skills are registered in registry.yaml")
        return 0

    print("Error: The following skills are not registered in skills/registry.yaml:")
    for skill_id in sorted(unregistered):
        print(f"  - {skill_id}")
    print()
    print("To register a skill, add an entry to skills/registry.yaml.")
    print("See skills/AGENTS.md for more info on adding skills.")

    return 1


if __name__ == "__main__":
    sys.exit(main())
