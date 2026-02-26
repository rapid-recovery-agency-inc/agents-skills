# skills/: skill definitions for agent runtime consumption

> **Purpose:** Define and maintain the canonical `SKILL.md` content that agent runtimes consume from `.agents/skills`. Keep this tree focused on skill behavior, trigger quality, and validation-friendly metadata.

## Scope

Applies to: `skills/` and all nested skill directories (for example `skills/generic/*`).
Excludes: repository-wide tooling/docs outside this tree (`cli/`, root README, hook setup).

## Authority & Precedence

Precedence:

1. This file
1. Task-specific user/developer instructions

If a parent `AGENTS.md` is added later, it takes precedence over this file.

## Directory Contract

- Each skill directory MUST contain `SKILL.md`.
- `SKILL.md` frontmatter MUST include:
  - `name`
  - `description`
- Allowed top-level frontmatter keys are constrained to:
  - `name`, `description`, `license`, `allowed-tools`, `metadata`, `compatibility`
- Skill `name` SHOULD be kebab-case.

## Runtime Path Contract (`.agents/skills`)

- Skills are authored in this source tree (`skills/...`).
- Registry-driven consumers materialize skills under `.agents/skills/...`.
- Keep skill paths stable; moving directories requires registry updates.

## How to Run Locally

- **Validate repo hooks:** `just lint`
- **Stage a skill to runtime path:** `just stage-skill <skill-name>`
  - Example: `just stage-skill create-agents-files`
- **Validate one skill frontmatter quickly:**
  - `python skills/generic/skill-creator/scripts/quick_validate.py skills/generic/<skill-name>`

## Common Changes

- **Add a new skill:** create `skills/<category>/<skill-name>/SKILL.md`, then register it in `registry.json`.
- **Update a skill:** edit `SKILL.md`, keep frontmatter valid, then run `just lint`.
- **Rename/move a skill:** update both filesystem path and matching `registry.json` `source_path`/install mapping in one change.

## Gotchas

- Do not add unrelated files to skill directories unless they are part of the skill package.
- `check-added-large-files` runs in pre-commit; keep new assets reasonably small.
- If commit is blocked because `.pre-commit-config.yaml` changed, stage that file before committing.

## Security Notes

- Do not place secrets or credentials in `SKILL.md` or example files.
- Keep examples generic and non-sensitive.
