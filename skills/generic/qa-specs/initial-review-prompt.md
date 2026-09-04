# Initial Review Prompt (QA)

## Purpose

Audit spec for completeness before implementation. Provide a bulleted list of gaps, then rewrite or suggest fixes using the Given-When-Then format.

## Contract

- Ambiguity & Determinism Check: identify vague language that could lead to multiple valid implementations; ask the author to choose one path explicitly.
- Requirements Traceability: map each requirement to acceptance criteria; flag orphaned requirements.
- Testability Analysis: ensure every criterion can be verified deterministically.
- Gap Categories (5): acceptance criteria, edge cases, error handling, ownership/roles, test matrix.
- Test Matrix: 6 rows × 4 columns (happy/edge/error × input/output).

## Format

```
## Findings
- [Gap 1]
- [Gap 2]

## Status
NEEDS FURTHER REFINEMENT / APPROVED
```
