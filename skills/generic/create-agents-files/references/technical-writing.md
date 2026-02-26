# AGENTS.md Writing Standard (For Hierarchy Skill)

## 0. Writing Objective

Created AGENTS.md files MUST be:

- Evidence-derived
- Hierarchically consistent
- Non-duplicative
- Enforceable
- Token-efficient

No narrative. No filler.

______________________________________________________________________

## 1. Evidence-Driven Content Rules

Before writing, the Skill MUST confirm:

- Package structure
- Upstream dependencies
- Downstream consumers
- Real call-site usage patterns

Content MUST reflect observed behavior, not assumptions.

If evidence confidence is low:

- STOP
- Ask for clarification

Never fabricate responsibilities.

______________________________________________________________________

## 2. Hierarchy Semantics (Mandatory)

### Root AGENTS.md

Contains:

- Global invariants
- Authority model
- Cross-cutting constraints
- Child AGENTS list

MUST NOT contain:

- Package-level implementation details

______________________________________________________________________

### Non-Root AGENTS.md

MUST include:

```md
Inherits: <relative path to parent AGENTS.md>
Overrides: (optional)
Additions: (optional)
```

Rules:

- MAY narrow scope
- MUST NOT weaken parent constraints
- MUST NOT duplicate parent policy unless narrowing

______________________________________________________________________

## 3. Deterministic File Structure

### Root AGENTS.md Structure

Root files MUST follow this 5-section structure:

1. Scope
1. Authority & Precedence
1. Package Responsibilities
1. Constraints
1. Child AGENTS (omit for leaf)

No additional sections unless justified by evidence.

### Non-Root Operational AGENTS.md

Non-root module AGENTS files MUST include `Scope` and `Authority & Precedence` blocks at the top (see Section 2), then MAY use the operational template defined in `SKILL.md` for the remaining sections. The operational template sections (`Key Entry Points`, `Config`, `Constraints`, `Gotchas`, etc.) serve as an expanded form of Package Responsibilities and Constraints.

Accepted non-root structure:

```text
Scope block
Authority & Precedence block (with Inherits:)
[Operational template sections from SKILL.md]
```

No additional sections beyond the operational template unless justified by evidence.

______________________________________________________________________

## 4. Writing Constraints

### Language

- Use MUST / MUST NOT / SHOULD / MAY
- One rule per bullet
- No adjectives
- No rationale
- No narrative
- No compound rules

Bad:

- Validate and sanitize inputs.

Good:

- All inputs MUST be validated.
- All outputs MUST be sanitized.

______________________________________________________________________

### Measurability

Constraints SHOULD be testable when applicable.

Bad:

- Code must be clean.

Good:

- Lint MUST pass.
- Coverage MUST be ≥ 80%.

If not measurable, keep it structural (e.g., "MUST be stateless").

______________________________________________________________________

### Scope Precision

Scope section MUST define:

```markdown
Applies to:
Excludes:
```

If boundary unclear → STOP.

______________________________________________________________________

## 5. Token Discipline by Depth

### Root

Only:

- Authority
- Global invariants
- Cross-cutting security/architecture/quality

No repetition downstream.

______________________________________________________________________

### Mid-Level

Only:

- Real responsibilities (from evidence)
- Key usage patterns (if recurring)
- Narrowed constraints (if applicable)

______________________________________________________________________

### Leaf

Only:

- Implementation-focused constraints
- Local invariants

No child section.

______________________________________________________________________

## 6. Smart Omission Rules

The Skill MUST omit:

- Empty sections
- Child AGENTS in leaf packages
- "Key Patterns" if no recurring pattern exists
- Generic boilerplate not supported by evidence

No filler for symmetry.

______________________________________________________________________

## 7. Duplication Control

Before writing each file:

- Compare with parent

- Remove inherited policy

- Keep only:

  - Narrowing
  - Additions
  - Overrides

If a rule is identical to parent → delete it.

______________________________________________________________________

## 8. Authority & Precedence Block

Each file MUST declare precedence:

```markdown
Precedence:
1. Root AGENTS.md
2. Domain AGENTS.md
3. Feature AGENTS.md
4. Task instructions
```

Non-root files MUST reference parent via `Inherits:`.

______________________________________________________________________

## 9. Child Linking Contract (Parents Only)

Parent files MUST:

- List child AGENTS with relative paths
- Instruct agents to read child AGENTS for specifics

Example:

```markdown
Child AGENTS:
- ./payments/AGENTS.md
- ./ledger/AGENTS.md

Agents MUST read child AGENTS before modifying those directories.
```

______________________________________________________________________

## 10. Validation Requirements (Pre-Commit of Generation)

Before finalizing:

### Hierarchy

- All `Inherits:` paths resolve
- No orphan AGENTS in scoped tree
- Parent lists match actual children

### Quality

- No weakening of parent constraints
- No duplicated policy
- All rules declarative

### Markdown

- Run formatter/linter if available
- Do not fail generation if tooling absent

______________________________________________________________________

## 11. Failure Rules

The Skill MUST STOP if:

- Scope is missing
- Package boundaries ambiguous
- Evidence insufficient
- Conflicting inheritance detected

Ask clarification before generation.

______________________________________________________________________

## 12. Acceptance Compliance Mapping

The Skill output is valid only if:

- Scope was confirmed
- Evidence informed responsibilities
- Inheritance semantics exist in non-root files
- Parent lists child AGENTS
- No policy duplication
- Files remain concise
- Validation pass completed

______________________________________________________________________

## Final Compression Check

A created AGENTS.md is correct if:

- Every bullet is enforceable
- Every section exists for a reason
- No repetition across hierarchy
- No narrative text
- No fabricated responsibility
- No weakening of parent constraints

If interpretation is required, rewrite.
