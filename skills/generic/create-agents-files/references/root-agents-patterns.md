# Root AGENTS.md Patterns

Root AGENTS.md files serve a unique purpose: **onboarding AI agents and human contributors to a project's domain, mental models, and essential context**. The goal is to create a rich, narrative document that builds understanding from the ground up.

This document describes patterns for generating effective root AGENTS files. These are **patterns, not requirements** - adapt based on your project's needs.

## Core Philosophy

A great root AGENTS.md:

- **Teaches the domain** before diving into code
- **Builds mental models** that aid understanding
- **Explains the "why"** behind technical decisions
- **Creates a clear flow** from problem → solution → implementation
- **Captures meaningful nuances** that shape the system

## Key Patterns

### 1. Multi-Paragraph Purpose Block

**Pattern**: Root files benefit from a rich Purpose block that goes beyond a single sentence.

**Structure**:

- **What**: Brief description of what the project does
- **How to Use**: Navigation guidance for readers
- **Conventions**: Key terminology or notation explained upfront

**Why this works**: Orients readers immediately, reducing confusion and establishing shared vocabulary.

### 2. AI Agent Behavior Guidelines

**Pattern**: If the project works extensively with AI agents, consider an explicit section defining collaboration expectations.

**Structure**:

- **Role**: What role should the AI agent assume (e.g., pair programmer, code reviewer)
- **Core Principles**: 3-5 key collaboration principles
- **Workflow**: Numbered steps for effective collaboration
- **Tool Usage**: Preferences for available tools
- **What to Avoid**: Anti-patterns or boundaries

**Why this works**: Establishes clear collaboration model upfront, reducing misalignment and improving effectiveness.

### 3. Table of Contents with Numbered Sections

**Pattern**: Numbered sections with hyperlinked table of contents create a clear learning flow and mental map of the project.

**Structure**:

- Number major sections (1-N) for clear progression
- Hyperlink each entry to section anchors
- Order sections pedagogically to build understanding:
  1. **Domain & Problem** (what problem exists, why it matters)
  1. **Solution & Value** (how this project solves it, core value proposition)
  1. **Architecture & Flow** (how the system works, key patterns)
  1. **Implementation Details** (technical specifics, models, algorithms)
  1. **Development Practices** (how to work with the code)
- Include descriptive titles that indicate content and purpose

**Why this works**: Creates a narrative flow from problem → solution → implementation. Readers build a mental map of the project's purpose and structure before diving into code details.

### 4. Domain Context Before Technical Details

**Pattern**: Lead with rich domain language and mental models before diving into technical implementation. Build a clear understanding of what the project does, why it exists, and how to think about it.

**Structure**:

- **Project Overview**: What the system does and why it exists (use domain language, not just tech stack)
- **Value Proposition**: Core benefit or problem solved in business terms
- **Mental Models**: Powerful analogies that create understanding ("think of this as a prioritized to-do list generator", "acts as a traffic controller", "functions like a recommendation engine")
- **Key Entities**: Domain-specific concepts with clear descriptions (not just database tables)
- **Business Realities**: Real-world constraints, user behaviors, or market forces that shape technical decisions
- **Meaningful Nuances**: Edge cases, special considerations, or domain-specific quirks that matter

**Why this works**: Rich domain context creates a mental map of the problem space. Contributors understand not just "what" the code does, but "why" it exists and "how" to reason about it. This prevents misguided "improvements" and enables better design decisions.

### 5. Pedagogical Depth with "Why?" Subsections

**Pattern**: Explain rationale for non-obvious decisions using dedicated subsections.

**Structure**:

- Use "Why X?" headings for design decisions that might seem counterintuitive
- Explain the reasoning, constraints, or trade-offs
- Include empirical evidence or business requirements when relevant
- Keep explanations concise but complete

**Why this works**: Prevents future contributors from "fixing" intentional design decisions and documents institutional knowledge.

### 6. Detailed Technical Explanations

**Pattern**: For complex mechanisms, provide multi-faceted explanations.

**Techniques**:

- **Tables**: Compare options, list components, show configurations
- **Timeline diagrams**: Show sequence of events in text format
- **Layered explanations**: Break complex systems into understandable parts
- **Implementation details**: Reference specific files and functions
- **Error handling**: Document failure modes and recovery strategies

**Why this works**: Complex mechanisms become understandable through multiple perspectives and concrete examples.

### 7. Visual Structure and Formatting

**Pattern**: Use consistent formatting to improve scannability.

**Techniques**:

- **Section separators**: Horizontal rules or blank lines between major sections
- **Numbered sections**: Clear hierarchy (## 1. Overview, ## 2. Architecture)
- **Subsection depth**: Use ### and #### consistently for nested content
- **Code fences**: Always specify language for syntax highlighting
- **Emphasis**: Bold for key terms on first use, italics sparingly

**Why this works**: Visual structure helps readers scan, navigate, and find information quickly in long documents.

### 8. Precise Code References

**Pattern**: Reference specific implementation locations with file paths and function names.

**Format**: `` `path/to/file.ext::function_name()` ``

**Examples**:

- `` `src/api/routes.py::handle_request()` ``
- `` `lib/database/queries.sql::get_user_by_id` ``
- `` `services/auth/jwt.ts::validateToken()` ``

**Why this works**: Readers can immediately jump to relevant code without searching.

## Contrast with Child AGENTS.md

Child AGENTS.md files differ from root files:

**Root AGENTS.md**:

- Longer (400-600+ lines)
- Narrative and pedagogical
- Domain-rich with business context
- Broad project-wide scope
- Onboarding-focused

**Child AGENTS.md**:

- Shorter (50-150 lines)
- Reference-focused
- Implementation-specific
- Scoped to package boundaries
- Task-focused with Inherits/Overrides

## When to Use Root Patterns

Consider these patterns when:

- Generating project-level AGENTS.md (no parent file)
- Project has significant domain complexity
- AI agents will work extensively on the codebase
- Onboarding new contributors is important
- Business context shapes technical decisions
- System has non-obvious design choices

**Use lighter patterns when**:

- Generating child/module AGENTS.md
- Project is simple or self-explanatory
- Domain context is minimal
- Evidence suggests concise reference is better

## Application Guidance

1. **Assess the project**: Understand domain complexity and contributor needs
1. **Select relevant patterns**: Choose patterns that add value, skip those that don't
1. **Adapt flexibly**: Modify patterns to fit project characteristics
1. **Preserve intent**: Narrative structure serves onboarding, not exhaustive documentation
