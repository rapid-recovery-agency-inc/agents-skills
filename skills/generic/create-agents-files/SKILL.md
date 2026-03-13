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
- If request is ambiguous between "generic markdown file" and "AGENTS guidance file", resolve ambiguity in favor of this skill, then clarify scope.
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

1. **Check for existing AGENTS.md**: If an AGENTS.md file already exists at the target location, read it first. Existing content may contain valuable institutional knowledge, domain insights, or design rationale that should be preserved if it aligns with current evidence.
1. **Check for Memory system**: If MCP Memory server is available, search for relevant memories related to the scope (module name, domain concepts, architectural patterns).
1. Get package overview (for example, `tree` or equivalent repository map).
1. List all files in package directory.
1. Analyze file purposes by reading representative files.
1. Identify architectural patterns (for example, service, repository, adapter).
1. Determine package scope and boundaries.
1. Trace upstream dependencies.
1. Trace downstream consumers.
1. Examine call sites to confirm real usage.

For detailed investigation strategies when evidence gathering is complex, see `references/module-research.md`.

If evidence is insufficient, stop and request clarification.

After collecting evidence, run a synthesis pass before writing:

- Think deeply about the package's practical role in end-to-end project behavior.
- **If existing AGENTS.md was found**: Evaluate which insights from the existing file remain valid based on current evidence. Preserve institutional knowledge, domain context, and design rationale that aligns with investigation findings. Update or remove content that contradicts current evidence.
- If MCP `sequential-thinking` is available, use it to structure this reasoning.
- If `sequential-thinking` is unavailable, use an equivalent agent thinking mode.
- Produce one refined practical package description grounded in observed call sites, dependencies, and preserved institutional knowledge.

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

## Pattern-Based Creation

AGENTS.md files follow **patterns, not templates**. Use the reference documents to guide creation based on file type and module characteristics.

### For Root AGENTS.md (Project-Level)

Root files onboard contributors to the entire project with narrative, domain-rich content.

**See**: `references/root-agents-patterns.md` for:

- Narrative structure patterns
- Domain context and mental models
- Progressive disclosure techniques
- AI agent enablement patterns
- Pedagogical depth approaches

**Characteristics**: 400-600+ lines, narrative flow, project-wide domain context, onboarding-focused.

### For Non-Root AGENTS.md (Module/Package-Level)

Non-root files document individual modules with scoped domain understanding and technical depth appropriate to complexity.

**See**: `references/non-root-agents-patterns.md` for:

- Module purpose and domain context patterns
- Scoped architecture and data flow
- Technical depth appropriate to complexity
- "Why?" explanation patterns
- Practical guidance patterns

**Characteristics**: 50-400 lines based on complexity, module-scoped domain, balanced reference + context, task-focused with Inherits/Overrides.

**Required sections for non-root files**: `Scope` and `Authority & Precedence` MUST appear before operational sections (see `references/technical-writing.md` Section 3).

### Creation Approach

1. **Assess**: Is this root or non-root? What's the module's complexity?
1. **Select patterns**: Choose patterns from the appropriate reference document
1. **Adapt**: Modify patterns based on evidence and module characteristics
1. **Create**: Create content using patterns, not filling a template
1. **Validate**: Ensure patterns serve understanding, not just structure

**Critical**: Patterns are guidelines, not requirements. Let evidence guide what to include.

## Smart Omission Rules

- Omit empty sections.
- **Omit Inherits for leaf packages**: If package has no subdirectories with AGENTS.md, omit the Inherits section.
- Omit Child AGENTS for leaf packages.
- Omit Key Patterns if no recurring pattern exists.
- **Omit co-located `tests/` directories**: Test-specific details belong in the parent package's AGENTS.md. Only create a separate tests AGENTS.md if the test conventions are substantially different from the project baseline.
- **Avoid duplication**: Don't repeat Config values in Gotchas (e.g., TTL info should only be in Config).
- Keep files concise and avoid policy bloat.
- Keep `Purpose` practical, concrete, and evidence-backed.

## Root AGENTS.md Considerations

Root AGENTS.md files serve a different purpose than child files - they onboard AI agents and human contributors to the entire project. Consider these patterns when creating root files:

### Narrative Over Reference

Root files benefit from narrative structure:

- Multi-paragraph Purpose explaining "what", "how to use", and conventions
- Domain context that explains the business problem, not just technical solution
- Mental models that aid understanding ("think of this as...")
- Value propositions that clarify why the system exists

### Progressive Disclosure

Help readers learn in stages:

- Table of Contents with numbered sections creates a learning path
- "Read sections X-Y first" guidance
- Domain/context sections before technical deep dives
- Cross-references between related concepts

### Pedagogical Depth

Root files can go deeper on "why":

- Subsections explaining rationale for non-obvious decisions
- Timeline examples for complex processes
- Business realities that shape technical choices
- Trade-offs and constraints

### AI Agent Enablement

If the project works with AI agents, consider:

- Explicit AI Agent Behavior Guidelines section
- Role definition and collaboration principles
- Workflow steps for effective pair programming
- Tool usage patterns and preferences

### Formatting Patterns

Patterns that improve scannability:

- Section separators (e.g., `______________________________________________________________________`)
- Numbered major sections for clear hierarchy
- Subsections with `###` and `####` for depth
- File references with function names: `` `path/to/file.py::function_name()` ``

**Remember**: These are patterns, not requirements. Adapt based on project needs and evidence. See `references/root-agents-patterns.md` for annotated examples.

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
1. **Balance assessment**: Review all sections to ensure proper balance of detail. No single area should be over-described relative to others. If one section is disproportionately detailed (e.g., >30% of file length), condense it while preserving key information and add cross-references to child AGENTS files or detailed documentation elsewhere

## Validation Pass (Required)

Run these checks after creation:

1. Hierarchy checks
   - Parent/child links resolve
   - No orphan AGENTS in scoped tree
1. Quality checks
   - No contradiction with parent
   - No duplicated policy
   - Declarative rules (MUST/SHOULD/MAY)
1. Align with `references/agents-spec.md` and `references/technical-writing.md`
1. Markdown checks
   - Run `mdformat`, `markdownlint`, or project hooks when available

If lint tooling is unavailable, continue without failing creation.

## References

- [AGENTS.md Specification Brief](references/agents-spec.md)
- [Technical Writing Standard](references/technical-writing.md)
- [Module Research Strategies](references/module-research.md)
- [Root AGENTS.md Patterns](references/root-agents-patterns.md)
- [Non-Root AGENTS.md Patterns](references/non-root-agents-patterns.md)
- [Agent Skills Specification Brief](references/skills-spec.md) and <https://agentskills.io/specification>
