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
# Show version
agents-skills --version

# List available skills (fetches from remote by default)
agents-skills list

# Use local registry instead
agents-skills list --local

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

# Install for specific IDE
agents-skills add skill-creator --ide c  # Claude
agents-skills add skill-creator --ide a  # Antigravity/Gemini
```

#### IDE-Specific Installation

By default, skills are installed to `.agents/skills/` which is supported by Windsurf, Copilot, Codex, and Cursor. For other IDEs, you can specify a target directory:

```bash
# Interactive prompt (default)
agents-skills add create-agents-files
# Prompts:
#   Which system are you installing skills for?
#     w. Windsurf/Copilot/Codex/Cursor -> .agents/skills/<skill>/
#     c. Claude                        -> .claude/skills/<skill>/
#     a. Antigravity/Gemini            -> .gemini/skills/<skill>/
#   Choice [w]:

# Non-interactive with --ide flag
agents-skills add create-agents-files --ide w  # .agents/skills/ (default)
agents-skills add create-agents-files --ide c  # .claude/skills/
agents-skills add create-agents-files --ide a  # .gemini/skills/

# Skip confirmation prompt
agents-skills add create-agents-files --ide c --yes
```

### Hidden Aliases

- `install <skill-id>` → `add <skill-id>`
- `sync` → `add all`
- `update` → `add all`

## Global Flags

- `--version`, `-v`: Show version information
- `--remote` / `--local`: Use remote registry (default) or local files
- `--registry <path>`: Override registry.json location (forces local mode)
- `--target-root <path>`: Override destination root (default: `.agents`)
- `--ide <choice>`: IDE choice: `w` (Windsurf/Copilot/Codex/Cursor), `c` (Claude), `a` (Antigravity/Gemini)
- `--dry-run`: Show actions without writing
- `--yes`, `-y`: Skip confirmation prompts
- `--json`: Machine-readable output

## Registry

By default, the CLI fetches the registry from GitHub. This means you can run `agents-skills list` from any directory without needing local registry files.

### Remote Registry (Default)

The CLI fetches registry files from:

- `https://raw.githubusercontent.com/rapid-recovery-agency-inc/agents-skills/main/cli/registry.json`
- `https://raw.githubusercontent.com/rapid-recovery-agency-inc/agents-skills/main/cli/registry.schema.json`
- `https://raw.githubusercontent.com/rapid-recovery-agency-inc/agents-skills/main/cli/tags.vocab.json`

### Local Registry

Use `--local` to use local registry files instead:

```bash
agents-skills list --local
agents-skills add create-agents-files --local
```

Or specify a custom registry path:

```bash
agents-skills list --registry /path/to/registry.json
```

**Note**: Using remote registry requires network access.

## How It Works

1. Fetches registry from GitHub (or uses local files with `--local`)
1. Validates registry against schema
1. Ensures git submodule exists and is updated
1. Resolves skill by ID or short name
1. Prompts for IDE selection (if not using `--ide` flag or `--yes`)
1. Materializes skill to IDE-specific directory:
   - `.agents/skills/<target_path>/` (Windsurf/Copilot/Codex/Cursor)
   - `.claude/skills/<target_path>/` (Claude)
   - `.gemini/skills/<target_path>/` (Antigravity/Gemini)
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
