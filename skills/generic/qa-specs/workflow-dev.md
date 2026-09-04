# Dev Mode Workflow

## Stages

### Stage 0: Align with Spec

- Confirm understanding of intent
- List any ASSUMPTIONs needed

### Stage 1: Find Issues (Solutions-First)

- Identify gaps in spec
- Propose solutions
- Edit plan if needed

### Stage 2: Implement

- Hard stop before Dev 2 if gaps exist
- Implement only after gaps resolved

## Common Dev Mistakes

- Implementing before clarifying gaps
- Not listing ASSUMPTIONs
- Skipping solutions-first approach

## Example

Given: Spec for API endpoint
When: I find missing error handling
Then: I propose solution (return 400 with error message)
And: I edit plan to include it
