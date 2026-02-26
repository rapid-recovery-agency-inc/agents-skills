# Agent Skills Specification Brief

## Initial Instruction

If deeper specification detail is needed beyond this document, agents SHOULD review the full specification at <https://agentskills.io/specification>.

## Recommendation

Yes. A consolidated `skills-spec.md` in `references/` is appropriate for this workflow.

Why:

- Agent Skills spec explicitly supports optional `references/` resources for deeper documentation.
- This workflow already separates implementation (`SKILL.md`) from reference material (`references/technical-writing.md`).
- A spec summary prevents repetitive re-reading of external docs during future edits.

Source reviewed: <https://agentskills.io/specification>

## Minimal Skill Directory Contract

A valid skill must include:

- `SKILL.md` (required)

Optional but recommended:

- `scripts/` for executable helpers
- `references/` for in-depth docs and standards
- `assets/` for templates, diagrams, static data

## `SKILL.md` Structure Requirements

`SKILL.md` contains:

1. Frontmatter (required)
1. Body content (instructions)

### Frontmatter fields

Required:

- `name`
- `description`

Optional:

- `license`
- `compatibility`
- `metadata`
- `allowed-tools` (experimental support)

### Field constraints to remember

#### `name`

- Lowercase alphanumeric plus hyphen only
- No leading or trailing hyphen
- No consecutive hyphens
- Must match parent directory name

#### `description`

- Should explain both what skill does and when to use it
- Should include specific keywords that help routing and activation

#### `compatibility`

- Include only when environment constraints matter (tooling, network, runtime expectations)

#### `metadata`

- String key-value map for implementation-specific extensions

#### `allowed-tools`

- Space-delimited pre-approved tool list
- Treated as experimental across agent runtimes

## Body Content Expectations

Body should include:

- Ordered execution instructions
- Input/output examples
- Edge-case handling guidance

## Optional Directory Guidance

### `scripts/`

- Keep scripts self-contained or document dependencies
- Emit clear error messages
- Handle edge cases explicitly

### `references/`

Typical files include:

- `REFERENCE.md` for technical depth
- `FORMS.md` for structured templates
- Domain-specific references (for example, standards, policy, or protocol notes)

### `assets/`

Use for:

- Templates
- Diagrams and images
- Static data files and schema-like artifacts

## Progressive Disclosure Model

Loading behavior is designed for efficiency:

1. Metadata loads broadly for discovery and routing
1. Full `SKILL.md` loads on skill activation
1. `scripts/`, `references/`, and `assets/` load on demand

Implication: keep top-level description highly discriminative, and keep deep details in references.

## File Reference Pattern

In `SKILL.md`, explicitly reference supporting files when needed.

Example pattern:

- Point to `references/...` for detailed rules
- Point to `scripts/...` for executable mechanics

This keeps `SKILL.md` concise while preserving depth.

## Validation

Spec references `skills-ref` validation tooling.

Suggested command pattern from spec:

```bash
skills-ref validate ./my-skill
```

For this repository workflow, run markdown lint and format checks alongside spec validation where possible.

## Practical Guidance for This Skill

For `create-agents-files`:

- Keep execution flow in `SKILL.md`.
- Keep writing standards in `references/technical-writing.md`.
- Keep spec-facing constraints and interoperability notes in this file.
- Link references from `SKILL.md` when behavior depends on spec nuance.

## Quick Compliance Checklist

Use this checklist when updating the skill:

- `SKILL.md` exists and frontmatter is valid.
- `name` and directory naming are aligned.
- `description` clearly encodes activation cues.
- Optional fields are present only when needed.
- Deep guidance lives in `references/` (not bloating core instructions).
- Scripts and assets are referenced only where necessary.
- Validation path is documented and runnable.
