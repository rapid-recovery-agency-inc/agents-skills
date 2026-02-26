# skills/generic: reusable, cross-project skill catalog

> **Purpose:** This directory contains skills that are not tied to a specific project, product, or programming language. Use it for general utility or hard-to-classify skills that should be reusable by any team (including Insightt, Foundd, and other consumers).

## Scope

Applies to: `skills/generic/` and all child skill directories.
Excludes: project-specific or language-specific skill families when those are split into dedicated categories.

## Authority & Precedence

Inherits: ../AGENTS.md

Precedence:

1. `skills/AGENTS.md`
1. This file
1. Task-specific user/developer instructions

## How to Run Locally

- Validate changes: `just lint`
- Stage one generic skill for runtime usage: `just stage-skill <skill-name>`

## Key Entry Points

- `skills/generic/create-agents-files/SKILL.md`: skill for creating and maintaining AGENTS hierarchies.
- `skills/generic/skill-creator/SKILL.md`: skill for authoring, evaluating, and iterating on other skills.

## Common Changes

- Add a generic skill under `skills/generic/<skill-name>/SKILL.md` and register it in `registry.json`.
- Keep frontmatter concise and portable (`name`, `description`, optional compatibility metadata).
- Move a skill out of `generic/` if it becomes product- or language-specific.

## Gotchas

- Do not bake in Insightt- or Foundd-only assumptions unless explicitly required.
- Keep instructions broadly reusable and tool-agnostic.

## Runtime Path

Skills authored in `skills/generic/*` are materialized for agents under `.agents/skills/generic/*`.
