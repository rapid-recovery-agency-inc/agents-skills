# Technical Writing Principles for Development Documentation

## Purpose

This reference defines writing standards for technical documentation in software development contexts: code comments, API documentation, runbooks, specifications, architecture documents, and READMEs.

## Core Principles

Technical documentation MUST be:

- **Evidence-driven** - Based on observed behavior, not assumptions
- **Measurable** - Constraints are testable and enforceable
- **Non-duplicative** - No repeated information across documents
- **Token-efficient** - Concise without sacrificing clarity
- **Clarity-focused** - Simple language, active voice, present tense

No narrative. No filler. No fabrication.

______________________________________________________________________

## Evidence-Driven Content

### Verification Requirements

Before writing documentation:

- Verify system behavior through direct observation
- Confirm implementation details against source code
- Validate assumptions through testing or runtime inspection
- Document what exists, not what should exist or might exist

Content MUST reflect observed reality.

### When Evidence is Insufficient

If evidence confidence is low:

- STOP writing
- Gather missing information through code review, testing, or profiling
- Request clarification from subject matter experts
- Mark uncertain areas explicitly if documentation must proceed

Never fabricate functionality, behavior, or constraints.

### Applicability

Applies to all technical documentation: code comments, docstrings, API docs, runbooks, specifications, architecture decision records, READMEs, troubleshooting guides.

______________________________________________________________________

## Declarative Language

### RFC 2119 Keywords

Use RFC 2119 keywords for precision:

- **MUST** / **MUST NOT** - Absolute requirements
- **SHOULD** / **SHOULD NOT** - Strong recommendations with valid exceptions
- **MAY** - Truly optional behavior

### Writing Rules

- One requirement per bullet point
- No adjectives unless technically necessary
- No rationale or justification (separate section if needed)
- No narrative or conversational tone
- No compound requirements

**Pattern - Avoid:**

```text
Validate and sanitize all user inputs before processing.
```

**Pattern - Prefer:**

```text
- All user inputs MUST be validated.
- All user inputs MUST be sanitized before processing.
```

### Voice and Tense

- Use active voice (Google, Microsoft standards)
- Use present tense for current behavior
- Use second person for instructions ("you configure" not "the user configures")

______________________________________________________________________

## Measurability and Enforceability

### Testable Constraints

Constraints SHOULD be measurable when applicable.

**Pattern - Avoid:**

```text
Code must be clean and maintainable.
```

**Pattern - Prefer:**

```text
- Linter MUST pass with zero warnings.
- Code coverage MUST be ≥ 80%.
- Cyclomatic complexity MUST be ≤ 10 per function.
```

### Structural Constraints

If not directly measurable, use structural language:

```text
- Functions MUST be stateless.
- Dependencies MUST be injected, not instantiated.
- Configuration MUST be immutable after initialization.
```

______________________________________________________________________

## Token Efficiency

### Conciseness Patterns

Write the minimum viable documentation:

- Omit empty sections
- Remove redundant explanations
- Eliminate filler words ("basically", "simply", "just")
- Use bulleted lists over paragraphs
- Front-load critical information

### Smart Omission

MUST omit:

- Sections with no content
- Obvious information derivable from code
- Repeated information available elsewhere
- Generic boilerplate unsupported by evidence
- Symmetrical sections added for visual balance

### Information Hierarchy

Structure by importance:

- Critical constraints first
- Common use cases before edge cases
- Required information before optional details
- Breaking changes before enhancements

______________________________________________________________________

## Duplication Control

### Anti-Duplication Rules

Before writing:

- Check if information exists elsewhere
- Link to canonical source instead of duplicating
- If duplication necessary, mark one as canonical

If information appears in multiple places:

- Designate one source as authoritative
- Others MUST link to canonical source
- Update canonical source only

### Cross-Reference Pattern

**Pattern - Avoid:**

```text
File A: "The API uses OAuth2 with PKCE flow..."
File B: "Authentication uses OAuth2 with PKCE flow..."
```

**Pattern - Prefer:**

```text
File A: "See authentication.md for OAuth2 PKCE flow details."
File B (authentication.md): "OAuth2 PKCE flow: [detailed content]"
```

______________________________________________________________________

## Scope Precision

### Boundary Definition

Every document MUST define scope:

```markdown
**Applies to:** [specific systems, modules, or contexts]
**Excludes:** [out-of-scope items to avoid confusion]
```

If boundaries are unclear:

- STOP writing
- Clarify scope with stakeholders
- Document scope explicitly before proceeding

### Audience Specification

Define intended audience:

- End users
- API consumers
- System operators
- Internal developers
- External contributors

Adjust technical depth accordingly.

______________________________________________________________________

## Validation and Quality Gates

### Pre-Publication Checks

Before finalizing documentation:

**Accuracy:**

- All statements verified against implementation
- No fabricated or assumed behavior
- Code examples tested and functional

**Clarity:**

- No ambiguous requirements
- All declarative statements enforceable
- Technical terms defined or linked

**Completeness:**

- Scope clearly defined
- Critical paths documented
- Error conditions covered

**Format:**

- Markdown linter passes
- Links resolve correctly
- Code blocks have language identifiers

### Failure Conditions

MUST NOT publish if:

- Scope is undefined or ambiguous
- Evidence is insufficient for claims
- Duplicates existing documentation without justification
- Contains fabricated information

______________________________________________________________________

## Industry References

This document incorporates principles from:

- **Google Technical Writing Guide** - Active voice, present tense, second person
- **Google Developer Documentation Style Guide** - Clarity and consistency standards
- **Microsoft Writing Style Guide** - Conciseness and measurability
- **Write the Docs** - Community best practices for software documentation

For detailed style guidance, consult:

- Google Technical Writing: <https://developers.google.com/tech-writing>
- Microsoft Style Guide: <https://learn.microsoft.com/en-us/style-guide/welcome/>
- Write the Docs: <https://www.writethedocs.org/guide/>

______________________________________________________________________

## Final Quality Check

Documentation is complete when:

- Every statement is enforceable or verifiable
- Every section exists for a specific purpose
- No information is duplicated across documents
- No narrative or filler text remains
- No fabricated or assumed behavior is documented
- Scope and audience are explicitly defined

If interpretation is required to understand a requirement, rewrite for clarity.
