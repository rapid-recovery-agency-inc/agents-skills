# cli/: CLI tool for consuming skills

> **Purpose:** Source code and configuration for the `agents-skills` CLI tool.

## Scope

Applies to: `cli/` and all nested code.
Excludes: skill definitions (`skills/`), root documentation.

## Authority & Precedence

Precedence:

1. Root AGENTS.md
1. This file
1. Task-specific user/developer instructions

## CLI Development

See root `AGENTS.md` for local installation and testing instructions.

### Running Locally

```bash
cd cli
pip install -e .
```

Test with:

```bash
agents-skills list --local
```

## Dependencies

- `typer` - CLI framework
- `httpx` - HTTP client
- `jsonschema` - Registry validation
- `pyyaml` - YAML parsing

## Commands

- `list` - List available skills
- `add` - Install skill(s)

## Versioning

Single source of truth: `cli/pyproject.toml` `version` field.

```bash
pip install -e .  # version comes from pyproject.toml
agents-skills --version
```

To bump version: edit the `version` field in the `[project]` section of `cli/pyproject.toml`.
