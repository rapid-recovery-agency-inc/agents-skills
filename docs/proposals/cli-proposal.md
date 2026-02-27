# agents-skills CLI Proposal (Finished-State User Flow)

This proposal defines a production-ready `agents-skills` CLI with a minimal Typer API (`list`, `add`) that prioritizes speed, clarity, and low-friction skill installation.

## 1) User outcome first

Users SHOULD be able to do three things quickly:

1. Discover skills.
1. Install or update one skill.
1. Sync all skills when needed.

Everything else is secondary.

## 2) CLI shape (KISS)

### Primary commands

- `agents-skills list [term ...]`
- `agents-skills add <skill-id|skill-name|all>`

### Compatibility aliases (hidden from main help)

- `agents-skills install <skill-id>` -> `add <skill-id>`
- `agents-skills sync` -> `add all`
- `agents-skills update` -> `add all`

### Global options (v1)

- `--registry <path>`: override `registry.json` location.
- `--target-root <path>`: override destination root (default `.agents`).
- `--dry-run`: show planned actions without writes.
- `--json`: machine-readable output.

## 3) Install and run (progressive disclosure)

Canonical CLI source:

- `https://github.com/rapid-recovery-agency-inc/agents-skills/tree/main/cli`

### Quick start (most users)

```bash
pip install "git+https://github.com/rapid-recovery-agency-inc/agents-skills.git@main#subdirectory=cli"
agents-skills list
agents-skills add generic/create-agents-files
```

### If using Poetry

```bash
# install Poetry
curl -sSL https://install.python-poetry.org | python3 -

poetry self add "git+https://github.com/rapid-recovery-agency-inc/agents-skills.git@main#subdirectory=cli"
agents-skills list
```

### If using uv / uvx

```bash
# install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

uv tool install "git+https://github.com/rapid-recovery-agency-inc/agents-skills.git@main#subdirectory=cli"
agents-skills list

# ephemeral run
uvx --from "git+https://github.com/rapid-recovery-agency-inc/agents-skills.git@main#subdirectory=cli" agents-skills list
```

## 4) Core user flows

### Flow A: Find the right skill

```bash
agents-skills list
agents-skills list fastapi
agents-skills list python fastapi backend
```

Behavior:

- CLI reads `registry.json`.
- CLI validates registry against `registry.schema.json`.
- CLI accepts mixed terms (language, tag, category, or keyword) after `list`.
- CLI narrows results by intersection across all supplied terms.
- CLI returns concise results with id, language, category, and one-line description.

### Flow B: Add one skill (idempotent)

```bash
agents-skills add skill-creator
```

Behavior:

- CLI checks `git` availability.
- CLI ensures submodule exists and is updated.
- CLI resolves a unique short skill name (for example `skill-creator`) to its full id.
- If a short name is ambiguous, CLI asks for the full id (for example `generic/skill-creator`).
- CLI materializes skill into `.agents/skills/<target_path>/SKILL.md`.
- If skill already exists, CLI updates it in place.

### Flow C: Sync all skills

```bash
agents-skills add all
# or compatibility alias:
agents-skills sync
```

Behavior:

- CLI updates submodule once.
- CLI re-materializes all registry skills.

## 5) Registry contract visible to users

Each skill entry MUST include:

- `id`
- `primary_language` (enum: `python`, `node`, `bash`, `go`, `ruby`, `typescript`, `na`)
- `category`
- `description` (single sentence)
- `tags` (one or more, controlled vocabulary)
- `added_at` (datetime)
- `updated_at` (datetime)

Tag examples:

- `node`, `frontend`
- `python`, `backend`, `fastapi`, `global-exceptions`

## 6) Error UX (low cognitive load)

Errors MUST follow this pattern:

1. What failed.
1. Why it failed.
1. Exact next action.

Examples:

- `git is required. Install git and retry.`
- `Unknown skill id: generic/foo. Run 'agents-skills list'.`
- `registry.json failed schema validation: skills/1/primary_language must be one of ...`

## 7) Typer best-practice constraints

Implementation SHOULD follow Typer conventions:

- Single `typer.Typer()` app.
- Typed arguments and options.
- Concise command docstrings for help.
- `typer.echo`/`typer.secho` for output.
- Non-zero exits through `typer.Exit(code=1)`.
- Completion support enabled and documented (`--install-completion`).

## 8) Success criteria

The CLI is successful when a new user can:

1. Install the tool from the remote GitHub `cli` source.
1. Run `agents-skills list` and understand results.
1. Run `agents-skills add <id>` without reading internal docs.
1. Recover from common errors using printed guidance only.
