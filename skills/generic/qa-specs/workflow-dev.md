# Dev Mode Workflow

## Stages

### Stage 0: Align with Spec

- Confirm understanding of intent
- List any ASSUMPTIONs needed

### Stage 1: Find Issues (Solutions-First)

**Division of labor:** Report is candidate input; re-derive and tag every finding yourself; present your own findings, never the report's verbatim; alignment flows through you. The delegate never presents findings, asks the developer questions, or edits the spec.

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
- Claiming "implementation-ready" or queueing the developer's next gates

## Example

Given: Spec for API endpoint
When: I find missing error handling
Then: I propose solution (return 400 with error message)
And: I edit plan to include it

## Status Claims

- **Dev 3:** "QA-clean" is a scoped claim — no residuals against QA-mode audit criteria. It is not implementation-readiness.
- **Dev 4:** The one-line summary states **the spec is ready for QA review**; "implementation-ready" / "Ready for Development" are forbidden in Dev mode — that status belongs to QA-mode Stage 4 after triage; gates after handoff are the developer's sequence, never declared or queued by the agent.
