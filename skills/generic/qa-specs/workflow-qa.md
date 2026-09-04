# QA Mode Workflow

## Stages

### Stage 0: Intent Check

- Ask: "What behavior should this enable?"
- If unclear → stop, clarify intent
- If clear → proceed to Stage 1

### Stage 1: Spec Audit

- Check for: acceptance criteria, edge cases, error handling, ownership
- Find gaps → list as `NEEDS FURTHER REFINEMENT`
- No gaps → proceed to Stage 2

### Stage 2: Final Audit

- Verify all gaps addressed
- If complete → `APPROVED`
- If incomplete → `NEEDS FURTHER REFINEMENT`

## Common QA Mistakes

- Skipping intent check
- Assuming spec is complete
- Not listing gaps explicitly

## GWT Example

Given: Feature spec for user login
When: I audit the spec
Then: I find missing edge cases (password reset, account lockout)
And: I list them as NEEDS FURTHER REFINEMENT
