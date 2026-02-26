# agents-skills CLI

Lightweight CLI for consuming skills from this registry with a low-friction workflow.

## DevEx goals

- Fast happy path (one command to add a skill)
- Predictable commands/flags
- Safe defaults + clear error messages
- Human-readable output by default, `--json` for automation

## Command surface (v0)

```bash
agents-skills list [query]
agents-skills add <skill-id> [--mode symlink|copy]
agents-skills remove <skill-id>
agents-skills sync
agents-skills doctor
```

Aliases:

- `install` -> `add`
- `update` -> `sync`

## Quick start

```bash
# 1) See available skills
agents-skills list

# 2) Install one skill into your project
agents-skills add generic/skill-creator

# 3) Pull latest registry submodule updates and re-materialize links/copies
agents-skills sync
```

## Install contract (submodule mode)

When running `agents-skills add <skill-id>`, the CLI should:

1. Read `registry.json` and validate against `registry.schema.json`.
1. Resolve top-level `source` (`repo`, `default_ref`, `submodule_path`, `skills_root`).
1. Ensure submodule exists/updated at `source.submodule_path`.
1. Resolve skill by exact `skills[].id`.
1. Build source from `<submodule_path>/<skills[].source_path>/<skills[].entrypoint>`.
1. Materialize to `.agents/skills/<skills[].install.target_path>` via `skills[].install.link_mode`.

## Recommended global flags

- `--project-root <path>`: run from any directory
- `--registry <path>`: override registry location
- `--dry-run`: show actions without writing
- `--json`: machine-readable output
- `--yes`: non-interactive confirmation

## Error model

- Non-zero exit code on failure.
- Clear reason + next action (for example, missing skill id, invalid schema, git/submodule failure).
- `doctor` should diagnose common setup issues and print exact fix commands.
