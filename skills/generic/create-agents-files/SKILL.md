---
name: create-agents-files
description: Create and maintain hierarchical AGENTS.md documentation from real package structure, dependencies, and call-site evidence. Use for any request to create or update an agents file, AGENTS.md, agents.md, or AGENTS hierarchy.
compatibility: Designed for agent runtimes that support Agent Skills and repository file editing.
---

# Create AGENTS Hierarchy

For AGENTS.md specification guidance, read `references/agents-spec.md` first.

If additional AGENTS specification details are needed, review the official documentation at <https://agents.md/>.

## Invocation Routing and Use Cases

### Routing Priority (Mandatory)

- If user intent mentions `agents` and file/doc creation, this skill MUST be selected before generic file creation flows.
- If request is ambiguous between “generic markdown file” and “AGENTS guidance file”, resolve ambiguity in favor of this skill, then clarify scope.
- Agent MUST NOT satisfy AGENTS requests by directly creating markdown files without invoking this skill workflow.
- When confidence is moderate and request includes any AGENTS-like token, invoke this skill in clarification mode.

### Trigger Phrases (Case-Insensitive)

Treat these as direct activation cues:

- `need an agents file`
- `create agents file`
- `make agents.md`
- `add AGENTS.md`
- `create agents`
- `set up AGENTS hierarchy`
- `we need AGENTS docs`

Also activate for close variants including punctuation/plurals (for example `agents doc`, `agents docs`, `agents guidance file`).

- If user asks to create an `AGENTS.md` file, use this skill.
- If user asks to create an `agents` file or `agents.md` (case-insensitive), use this skill.
- If user request is broad (for example, "we need an agents file") and no target path is provided, still invoke this skill in clarification mode.
- In clarification mode, ask exactly where the file is needed before creation. Preferred prompt:
  - `Where should I create or update AGENTS.md? (project root, specific module path, or only missing files)`
- If intent includes creating AGENTS docs, missing AGENTS, or hierarchy creation, use this skill.
- If entering package that has no AGENTS.md, use this skill.
- If onboarding to project lacking AGENTS hierarchy, use this skill.
- If creating new sub-package that needs local agent guidance, use this skill.
- If user asks to update, refresh, or recreate AGENTS hierarchy after refactors, use this skill.
- If AGENTS.md exists but is stale, run in update mode and preserve manual intent while refreshing structure and links.
- If evidence confidence remains low, stop and ask for clarification.

### Clarification Mode (Default Fallback)

If path/scope is missing, do not write files yet. Ask:

- `Where should I create or update AGENTS.md? (project root, specific module path, or only missing files)`

If user answers with a directory, treat it as scoped mode.
If user answers `project`, treat it as full-tree mode.

## Purpose

Create AGENTS.md hierarchy for nested packages in a project while preserving parent-child authority semantics and evidence-first content quality.

## Scope Input

Accepted scope values:

- `project` for whole repository
- Relative directory path for focused creation

If scope is missing, ask for scope before creation.

When asking for missing scope, ask for target location in concrete terms (path/module/root) and do not start file edits until scope is confirmed.

## Evidence-First Creation (Required)

Before writing any AGENTS.md, collect evidence for each target package:

1. Get package overview (for example, `tree` or equivalent repository map).
1. List all files in package directory.
1. Analyze file purposes by reading representative files.
1. Identify architectural patterns (for example, service, repository, adapter).
1. Determine package scope and boundaries.
1. Trace upstream dependencies.
1. Trace downstream consumers.
1. Examine call sites to confirm real usage.

If evidence is insufficient, stop and request clarification.

After collecting evidence, run a synthesis pass before writing:

- Think deeply about the package's practical role in end-to-end project behavior.
- If MCP `sequential-thinking` is available, use it to structure this reasoning.
- If `sequential-thinking` is unavailable, use an equivalent agent thinking mode.
- Produce one refined practical package description grounded in observed call sites and dependencies.

## Hierarchy Semantics (Required)

Each non-root AGENTS.md includes:

- `Inherits: <relative parent AGENTS.md>`
- `Overrides:` (optional)
- `Additions:` (optional)

Each parent AGENTS.md includes:

- Child AGENTS list with relative links
- Agent directive to read child AGENTS for domain specifics

Lower levels may narrow scope and must not weaken parent constraints.

## Token Discipline by Depth

- Root AGENTS.md: authority, policy, global invariants.
- Mid-level AGENTS.md: package responsibilities and key patterns.
- Leaf AGENTS.md: implementation-focused constraints and local invariants.

Do not duplicate parent policy unless narrowing or overriding.

## Title Heuristic

- Title MUST start with package path or package name.
- Title MUST state primary runtime role of the package.
- Title MUST be concrete and operational, not generic.
- Title SHOULD avoid vague labels like "utils" without role context.

Preferred pattern:

`# <package_path>: <primary runtime role>`

## Content Template

Use this baseline template and include ALL required sections. Omit only if genuinely not applicable to the module.

For non-root AGENTS files, `Scope` and `Authority & Precedence` MUST appear before the operational sections (see `references/technical-writing.md` Section 3).

```markdown
# <package_path>: <primary runtime role>

> **Purpose:** <what the module does in 2–5 lines>

## Scope

Applies to: <path and brief description>
Excludes: <what is out of scope>

## Authority & Precedence

Inherits: <relative path to parent AGENTS.md>

Precedence:
1. Root AGENTS.md
2. This file
3. Task instructions

## How to Run Locally

- **Install:** `<command>`
- **Build:** `<command>`
- **Start:** `<command>`
- **Test:** `<command>`

## Key Entry Points

- **<file>.py**: <main files, routes/handlers, jobs, consumers, or UI roots>

## Config

| Variable | Meaning | Default | Where Set |
| --- | --- | --- | --- |
| <env_var> | <description> | <default> | <location> |

## Dependencies & Integrations

- **DBs:** <databases used>
- **Queues:** <queues/topics>
- **External APIs:** <external services>
- **Events:** <events emitted/consumed>

## Data & Contracts

- **Schemas:** <schema definitions>
- **Endpoints:** <API endpoints>
- **Payloads:** <payload shapes>
- **Versioning:** <versioning rules>

## Logging & Observability

- **Log format:** <log structure>
- **Correlation IDs:** <how to trace>
- **Metrics:** <key metrics>
- **Dashboards/Alerts:** <monitoring links>

## Common Changes

- **"If you want to add X, do Y"**: <short playbook>

## Gotchas

- <sharp edges, performance traps, known flaky tests, local pitfalls>

## Security Notes

- **Secrets:** <how secrets are handled>
- **Permissions:** <permission assumptions>
- **PII/Retention:** <PII considerations>

## Release/Deploy

- **Pipeline:** <CI/CD pipeline>
- **Migrations:** <migration strategy>
- **Feature Flags:** <feature flag usage>

## Inherits

Inherits: ../AGENTS.md

> **Agent Directive:** Read child AGENTS.md files in subdirectories for domain-specific context.

## Child AGENTS

- [<relative_path>/AGENTS.md](<relative_path>/AGENTS.md) - <description>
```

## Smart Omission Rules

- Omit empty sections.
- Omit Child AGENTS for leaf packages.
- Omit Key Patterns if no recurring pattern exists.
- **Omit co-located `tests/` directories**: Test-specific details belong in the parent package's AGENTS.md. Only create a separate tests AGENTS.md if the test conventions are substantially different from the project baseline.
- Keep files concise and avoid policy bloat.
- Keep `Purpose` practical, concrete, and evidence-backed.

## Creation Workflow

1. Resolve scope.
1. Discover candidate packages.
1. Build hierarchy map.
1. Introspect each package (structure, dependencies, call sites).
1. Synthesize package role and refine practical Purpose description.
1. Create AGENTS.md top-down.
1. Add inheritance and child references.
1. Lint/format created markdown when tooling exists.
1. Run validation pass and report summary.

## Polishing Step (Required)

After initial creation, revise each AGENTS.md with technical depth:

1. **Add Entry Points table**: Document key public functions with signature, file location, and one-line purpose
1. **Add Data Flow diagram**: Show input → transformation → output pipeline in ASCII/text diagram
1. **Add Technical Constraints**: Document critical rules (e.g., "MUST run in threadpool", "Identity via spatial match")
1. **Add nuanced guidance**: Include domain-specific invariants, gotchas, and behavioral details

Then fix any Markdown errors:

1. Run `mdformat` for consistent formatting
1. Run `markdownlint` or project hooks to catch structural issues
1. Fix table alignment, code fence languages, heading hierarchy, link targets

If lint tooling is unavailable, manually verify:

- Tables have consistent column widths
- Code fences specify language (for example: python, text)
- Heading levels don't skip (H1 → H2 → H4 is invalid)
- Relative links resolve correctly

## Validation Pass (Required)

Run these checks after creation:

1. Hierarchy checks
   - Parent/child links resolve
   - No orphan AGENTS in scoped tree
1. Quality checks
   - No contradiction with parent
   - No duplicated policy
   - Declarative rules (MUST/SHOULD/MAY)
1. Markdown checks
   - Run `mdformat`, `markdownlint`, or project hooks when available

If lint tooling is unavailable, continue without failing creation.

## References

- [AGENTS.md Specification Brief](references/agents-spec.md)
- [Technical Writing Standard](references/technical-writing.md)
- [Agent Skills Specification Brief](references/skills-spec.md) and <https://agentskills.io/specification>
