# Non-Root AGENTS.md Patterns

Non-root AGENTS.md files document individual modules and packages. The goal is to provide **scoped domain understanding** and **technical depth** appropriate to the module's complexity, using patterns rather than rigid templates.

This document describes patterns observed in effective module AGENTS files. These are **patterns, not requirements** - adapt based on module characteristics and evidence.

## Core Philosophy

Effective module AGENTS files:

- **Explain the module's domain** (scoped to this package, not project-wide)
- **Provide mental models** for understanding the module's role
- **Include technical depth** appropriate to complexity
- **Adapt flexibly** - simple modules stay concise, complex modules get richer treatment
- **Balance reference and context** - practical utility with domain understanding

## Key Patterns

### 1. Module Purpose & Domain Context

**Pattern**: Lead with the module's scoped domain context before diving into implementation details.

**Consider including**:

- What this module does in the larger system (its role)
- Mental model for the module ("think of this as a transformer", "acts as a coordinator")
- Why this module exists (business/technical rationale)
- Key domain concepts specific to this module
- Boundaries: what's in scope, what's excluded

**Why this works**: Scoped domain context helps contributors understand the module's purpose and make decisions aligned with its intent.

### 2. Scoped Architecture & Data Flow

**Pattern**: Show how data moves through the module and how it integrates with the system.

**Consider including**:

- Module's role in the larger system
- Data flow within the module (ASCII/text diagrams)
- Integration points with other modules
- Key architectural patterns used here

**Why this works**: Visual flow and integration points clarify the module's place in the system architecture.

### 3. Technical Depth

**Pattern**: Provide concrete technical details appropriate to module complexity.

**Consider including**:

- Entry points with signatures and purposes
- Data contracts and schemas
- Technical constraints specific to this module
- Key patterns with code examples
- Implementation details that matter

**Why this works**: Technical depth enables effective work without constant code diving.

### 4. "Why?" Explanations

**Pattern**: Explain rationale for non-obvious module decisions.

**Consider including**:

- Design decisions that might seem counterintuitive
- Trade-offs made in this module
- Constraints that shape implementation
- Why certain patterns were chosen over alternatives

**Why this works**: Prevents future contributors from "fixing" intentional design decisions.

### 5. Practical Guidance

**Pattern**: Provide actionable playbooks for common tasks.

**Consider including**:

- Common changes ("To add X, modify Y")
- Gotchas and sharp edges
- Testing strategies for this module
- Debugging tips

**Why this works**: Practical guidance accelerates common tasks and prevents mistakes.

## Adapting to Module Complexity

**Pattern**: Adjust depth based on evidence, not arbitrary rules.

**Simple modules** (utilities, helpers, simple adapters):

- Typically 50-100 lines
- Focus on entry points, contracts, common changes
- Minimal domain context (purpose is often obvious)
- Skip patterns that don't add value

**Moderate modules** (services, repositories, domain logic):

- Typically 100-200 lines
- Include module purpose and mental model
- Data flow diagram, key patterns
- Technical constraints and gotchas

**Complex modules** (core domain, orchestration, algorithms):

- Typically 200-400 lines (but < root files)
- Rich domain context scoped to module
- Multiple "why?" subsections
- Detailed patterns with examples
- Comprehensive data flow and integration points

**Remember**: These are guidelines, not rules. Let evidence guide depth.

## Contrast with Root AGENTS.md

**Root AGENTS.md**:

- Project-wide domain and mental models
- Onboarding-focused narrative
- Pedagogical structure (numbered sections, learning path)
- 400-600+ lines

**Non-Root AGENTS.md**:

- Module-scoped domain and patterns
- Task-focused with domain context
- Balanced reference + understanding
- 50-400 lines based on complexity
- Inherits from parent, adds module-specific guidance

## When to Use These Patterns

Consider these patterns when:

- Module has meaningful domain logic (not just utilities)
- Non-obvious design decisions need explanation
- Integration points are complex
- Module is frequently modified
- Onboarding to the module takes time

**Use lighter patterns when**:

- Module is simple and self-explanatory
- Purpose is obvious from code
- No complex integration points
- Evidence suggests concise reference is better

## Application Guidance

1. **Assess the module**: Understand its complexity and domain significance
1. **Select relevant patterns**: Choose patterns that add value for this module
1. **Adapt flexibly**: Modify patterns to fit module characteristics
1. **Preserve intent**: Documentation serves understanding, not completeness
1. **Follow evidence**: Let module characteristics guide depth, not templates
