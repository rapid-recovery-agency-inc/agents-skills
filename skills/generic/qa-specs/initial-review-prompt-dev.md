# Initial Review Prompt (Dev)

## Purpose

Align with spec before implementation. Provide a bulleted list of gaps, then rewrite or suggest fixes using the Given-When-Then format.

## Contract

- Ambiguity & Determinism Check: identify vague language that could lead to multiple valid implementations; ask the author to choose one path explicitly.
- Requirements Traceability: map each requirement to acceptance criteria; flag orphaned requirements.
- Testability Analysis: ensure every criterion can be verified deterministically.
- Gap Categories (5): acceptance criteria, edge cases, error handling, ownership/roles, test matrix.
- Test Matrix: 6 rows × 4 columns (happy/edge/error × input/output).

## Format

```
## Understanding
- [Intent summary]

## Assumptions
- [ASSUMPTION 1]
- [ASSUMPTION 2]

## Issues Found
- [Issue 1]
- [Issue 2]

## Status
APPROVED / NEEDS FURTHER REFINEMENT
```
