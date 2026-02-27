# agents-skills CLI

Ergonomic CLI for installing and updating agent skills from a centralized registry.

## Installation

### Using pip

```bash
pip install "git+https://github.com/rapid-recovery-agency-inc/agents-skills.git@main#subdirectory=cli"
```

### Using Poetry

```bash
poetry self add "git+https://github.com/rapid-recovery-agency-inc/agents-skills.git@main#subdirectory=cli"
```

### Using uv

```bash
# Install as a tool
uv tool install "git+https://github.com/rapid-recovery-agency-inc/agents-skills.git@main#subdirectory=cli"

# Or run ephemerally
uvx --from "git+https://github.com/rapid-recovery-agency-inc/agents-skills.git@main#subdirectory=cli" agents-skills list
```

## Quick Start

```bash
# List available skills
agents-skills list

# Search for skills
agents-skills list python fastapi

# Add a skill to your project
agents-skills add create-agents-files

# Add all skills
agents-skills add all

# Use hidden aliases
agents-skills sync  # same as: agents-skills add all
```

## Commands

### `list [term ...]`

List skills from the registry with optional filtering.

```bash
# List all skills
agents-skills list

# Filter by multiple terms (intersection)
agents-skills list create agents

# Filter by tag
agents-skills list --tag documentation

# JSON output
agents-skills list --json
```

### `add <skill-id|short-name|all>`

Add or update skills. Supports short names (e.g., `skill-creator` instead of `generic/skill-creator`).

```bash
# Add by full ID
agents-skills add generic/create-agents-files

# Add by short name
agents-skills add create-agents-files

# Add all skills
agents-skills add all

# Dry run
agents-skills add skill-creator --dry-run
```

### Hidden Aliases

- `install <skill-id>` → `add <skill-id>`
- `sync` → `add all`
- `update` → `add all`

## Global Flags

- `--registry <path>`: Override registry.json location
- `--target-root <path>`: Override destination root (default: `.agents`)
- `--dry-run`: Show actions without writing
- `--json`: Machine-readable output

## How It Works

1. Reads `registry.json` and validates against schema
1. Ensures git submodule exists and is updated
1. Resolves skill by ID or short name
1. Materializes skill to `.agents/skills/<target_path>/SKILL.md`
1. Uses symlink or copy based on registry configuration

## Development

```bash
# Install dev dependencies
cd cli
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e .
pip install ruff black mypy pytest

# Run linting
ruff check src/
mypy src/agents_skills_cli/

# Format code
ruff format src/
```

## License

Apache-2.0
