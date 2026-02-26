# skills/: source-of-truth skill catalog for agent runtimes

> **Purpose:** Define and maintain canonical `SKILL.md` content used by registry-aware agent runtimes. Keep this tree focused on reusable behavior, valid frontmatter, and stable skill paths.

## Scope

Applies to: `skills/` and all nested skill directories.
Excludes: repository tooling and docs outside this subtree (`cli/`, root README, hook configuration).

## Authority & Precedence

Precedence:

1. This file
1. Child AGENTS files under `skills/*/AGENTS.md`
1. Task-specific user/developer instructions

## How to Run Locally

- Validate formatting + checks: `just lint`
- Stage one skill to runtime path: `just stage-skill <skill-name>`
- Validate one skill frontmatter quickly:
  - `python skills/generic/skill-creator/scripts/quick_validate.py skills/generic/<skill-name>`

## Directory Contract

- Each skill directory MUST contain `SKILL.md`.
- Required frontmatter: `name`, `description`.
- Allowed top-level frontmatter keys:
  - `name`, `description`, `license`, `allowed-tools`, `metadata`, `compatibility`
- Skill names SHOULD be kebab-case.

## Runtime Path Contract

- Source authoring path: `skills/...`
- Runtime materialization path: `.agents/skills/...`
- Any move/rename in `skills/` MUST be paired with `registry.json` updates.

## Common Changes

- Add a skill: create `skills/<category>/<skill-name>/SKILL.md`, then add/update entry in `registry.json`.
- Update a skill: edit content + frontmatter, then run `just lint`.
- Rename/move a skill: update filesystem path and matching registry `source_path`/install mapping in the same change.

## Gotchas

- Keep guidance portable; avoid hardcoding product-specific assumptions unless intended.
- Do not commit secrets or private data in skill examples.

## Child AGENTS

> **Agent Directive:** Read child AGENTS files for category-specific guidance before editing nested skills.

- [generic/AGENTS.md](generic/AGENTS.md) - Rules for cross-project, language-agnostic generic skills.
