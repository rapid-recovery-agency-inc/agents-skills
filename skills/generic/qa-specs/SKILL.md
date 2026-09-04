---
name: qa-specs
description: Use when aligning feature specs before QA handoff, or when specs need QA/implementation-driven development validation. Triggers: vague acceptance criteria, missing edge cases, undefined error handling, implicit role/ownership rules, untestable rules.
---

# QA Specs

## Overview

QA specs ensures specifications are testable, complete, and aligned with implementation before handoff.

## When to Use

**Use when:**

- Writing or reviewing feature specs before implementation
- Acceptance criteria feel vague or incomplete
- Edge cases aren't explicitly defined
- Error handling isn't specified
- Role/ownership rules are implicit
- Rules can't be tested deterministically

**Not for:**

- Already-testable specs (use regular review)
- Code review (use code-review skill)

## Core Workflow

### Stage 0: Intent Check (QA Mode)

- Ask: "What behavior should this enable?"
- If unclear → stop, clarify intent
- If clear → proceed to Stage 1

### Stage 1: Spec Audit (QA Mode)

- Check for: acceptance criteria, edge cases, error handling, ownership
- Find gaps → list as `NEEDS FURTHER REFINEMENT`
- No gaps → proceed to Stage 2

### Stage 2: Final Audit (QA Mode)

- Verify all gaps addressed
- If complete → `APPROVED`
- If incomplete → `NEEDS FURTHER REFINEMENT`

### Dev Mode (when implementing)

- Stage 0: Align with spec
- Stage 1: Find issues (solutions-first)
- Stage 2: Edit plan if needed
- Stage 3: Implement (hard stop before Dev 2 if gaps)

## Contracts

### DEV-RESOLVABLE

Used when finding can be fixed by code changes.

### ASSUMPTION

Used when spec is unclear but implementation can proceed with assumption.

### APPROVED / NEEDS FURTHER REFINEMENT

Final status after audit.

## Common Mistakes

**Without skill:**

- Skip intent check → build wrong thing
- Assume spec is complete → miss edge cases
- Implement before clarifying → rework

**With skill:**

- Always check intent first
- List gaps explicitly
- Stop before implementing if gaps exist

## Real-World Impact

- Reduces rework from unclear specs
- Catches edge cases before implementation
- Ensures testable acceptance criteria
