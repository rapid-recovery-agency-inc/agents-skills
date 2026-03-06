# AGENTS.md

> **Purpose:** Project-level agent instructions and conventions for this repository.

## Scope

This file provides guidance for agents working on the entire repository.
For skill-specific guidance, see `skills/AGENTS.md`.

## Repository Structure

- `skills/` - Source-of-truth skill definitions (organized by category)
- `skills/registry.yaml` - Skill index with embedded schema and tags_vocab
- `cli/` - CLI tool for consuming skills

## Categories

Skills are organized under `skills/` by category:

- `generic/` - Cross-project, language-agnostic skills
- `python/` - Python-specific skills
- `javascript/` - JavaScript/TypeScript-specific skills

## Adding New Skills

1. Create skill directory: `skills/<category>/<skill-name>/SKILL.md`
1. Add required frontmatter: `name`, `description`
1. Add entry to `skills/registry.yaml` with:
   - `id`, `name`, `description`, `category`, `primary_language`
   - `source_path`, `entrypoint`, `version`
   - `install` section with `target_path` and `link_mode`
   - `tags` from `tags_vocab` in registry.yaml

## Adding New Tags

If a new skill needs tags not in `tags_vocab`:

1. Add the tag to `tags_vocab` in `skills/registry.yaml` (alphabetical order)
1. Use the tag in the skill's entry

All tags must be lowercase kebab-case.

## Running Locally

- Validate: `just lint`
- Stage skill: `just stage-skill <skill-name>`

### CLI Development

You can install the CLI locally without committing:

```bash
cd cli
pip install -e .
```

Test with:

```bash
agents-skills list --local
```

The `--local` flag will use the local `skills/registry.yaml` file. Without `--local`, it tries to fetch from GitHub (which won't work until you commit/push since the remote URL changed to `/skills/registry.yaml`).

## Authority

Precedence:

1. This file
1. `cli/AGENTS.md` for CLI-specific guidance
1. `skills/AGENTS.md` for skill-specific guidance
1. Task-specific user/developer instructions

## Child AGENTS

> **Agent Directive:** Read child AGENTS files for domain-specific guidance.

- [cli/AGENTS.md](cli/AGENTS.md) - CLI tool development
- [skills/AGENTS.md](skills/AGENTS.md) - Skill definitions and management
