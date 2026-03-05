# AGENTS.md as the Universal Standard for AI Agent Context

## Abstract

AI coding assistants face a critical fragmentation problem: each tool requires its own memory file (CLAUDE.md, .cursorrules, copilot-instructions.md), forcing teams to maintain identical content across multiple formats. This paper argues that AGENTS.md will achieve README.md-level ubiquity as the universal standard for AI agent context. The evidence is compelling: Linux Foundation governance through the Agentic AI Foundation (founded December 2025), co-founding by OpenAI, Anthropic, Google, Microsoft, and AWS, adoption by 60,000+ open-source projects, and a pragmatic design that prioritizes interoperability over feature richness. We propose a KISS-compliant strategy using shim files rather than symlinks for cross-tool consistency, demonstrating that AGENTS.md replicates the exact success pattern that made README.md ubiquitous.

______________________________________________________________________

## 1. Introduction: The Stateless Problem

Every AI coding assistant session starts blank. Three months into using Claude Code on a production codebase, developers find themselves correcting the same mistakes every session: "No, we use pnpm, not npm." "No, the test command is `make test-integration`, not `pytest`." "No, we don't use default exports here." Every correction vanishes when the session ends.[^1]

This is the stateless problem. Large language models are stateless functions—they have no memory between conversations. Similarly, coding agent harnesses like Claude Code, Cursor, GitHub Copilot, and Windsurf start each session without knowledge of your project's conventions, build commands, or architectural patterns.[^7]

The solution seemed simple: create a memory file. Drop it in your project root, and the AI reads it at the start of every session. One developer created a CLAUDE.md file—forty lines of project context. The corrections stopped overnight.[^1]

But this solution created a new problem: fragmentation.

### The Fragmentation Crisis

If you use more than one AI coding assistant (and most teams do), you've encountered the mess:

- Claude Code wants `CLAUDE.md`
- Cursor wants `.cursorrules` or `.cursor/rules/`
- GitHub Copilot wants `.github/copilot-instructions.md`
- Windsurf wants `.windsurf/rules`
- Google's Jules wants `JULES.md`

The content is almost identical across all of them: your coding standards, your build commands, your test setup, your architectural patterns. But you're copying and pasting the same instructions into five different files.[^1]

This fragmentation imposes real costs on development teams:

- **Maintenance overhead**: Every change to coding standards must be propagated to multiple files
- **Configuration drift**: Copy-paste errors lead to inconsistent instructions across tools
- **Cognitive burden**: Developers must remember which file controls which tool
- **Onboarding friction**: New team members must learn multiple file formats

### Research Question

What standard will unify this chaos, and how should teams adapt?

This paper argues that AGENTS.md will achieve the same ubiquity as README.md because it mirrors README.md's success pattern: Linux Foundation governance ensuring neutral stewardship, broad cross-industry backing from major AI vendors (OpenAI, Anthropic, Google, Microsoft, AWS), and pragmatic design that prioritizes interoperability over feature richness.

This paper examines the current landscape of AI agent memory files, analyzes AGENTS.md's architecture and governance, and proposes practical strategies for teams to adopt this emerging standard while maintaining compatibility with existing tools.

______________________________________________________________________

## 2. The Landscape: Competing Standards

To understand why AGENTS.md is positioned to become the universal standard, we must first examine the fragmented ecosystem it aims to unify.

### 2.1 CLAUDE.md: The Pioneer

CLAUDE.md is Claude Code's memory file. Drop it in your project root, and Claude reads it at the start of every session.[^1]

**Location and Hierarchy**:

```text
~/.claude/CLAUDE.md                    # Enterprise policies
~/.claude/CLAUDE.md                    # Personal preferences
/project/CLAUDE.md                     # Project-level
/project/subdirectory/CLAUDE.md        # Subdirectory-level
```

The hierarchy loads bottom-up. Enterprise policies load first, then personal preferences, then project-level, then subdirectory-level. More specific instructions override broader ones.[^1]

**Key Features**:

**1. @imports system**: CLAUDE.md supports importing other files with `@path/to/file` syntax:

```markdown
See @README.md for project overview
See @docs/api-patterns.md for API conventions
See @package.json for available npm scripts
```

Imports can be recursive (referenced files can reference other files, up to 5 levels deep). This solves the "one giant file" problem—keep your CLAUDE.md lean, move detailed guidance into separate files.[^1]

**2. /init workflow**: The `/init` command generates a starter file based on your project structure and detected tech stack.[^1]

**3. Auto-memory system**: Claude Code now has an auto-memory system where Claude writes notes to itself during sessions. It lives in `~/.claude/projects/<project>/memory/`:

```text
memory/
├── MEMORY.md          # Index file, loaded every session
├── debugging.md       # Notes on debugging patterns
├── api-conventions.md # API design decisions
└── ...
```

The key difference: you write CLAUDE.md, Claude writes MEMORY.md. You provide the instructions; Claude captures the learnings.[^1]

**Limitations**:

CLAUDE.md is Claude-only. If your team uses Cursor or Copilot alongside Claude Code, they won't read this file. This is the fundamental limitation that AGENTS.md was created to solve.[^1]

### 2.2 Cursor Rules: Granular Control

Cursor supports two formats for memory files:

**Legacy format**: `.cursorrules` in repo root—simple Markdown file.[^1]

**Modern format**: `.cursor/rules/*.mdc`—Markdown files with YAML frontmatter supporting:

- **Activation modes**: Always, Auto Attached, Agent Requested, Manual
- **Glob patterns**: Apply rules to specific file types or directories
- **Multiple focused rules**: Different rule files for different contexts[^9]

Example `.cursor/rules/api.mdc`:

```text
---
description: API development rules
glob: src/api/**/*
activation: Auto Attached
---

# API Rules

All API routes must:
- Follow REST conventions
- Include error handling
- Return consistent error payloads
```

**Strengths**: Granular, context-aware rules that activate based on file location.

**Limitations**: Cursor-only. The YAML schema creates friction for teams wanting simple, portable instructions. However, Cursor also reads AGENTS.md, so teams can use both—shared rules in AGENTS.md, Cursor-specific behaviors in `.cursor/rules/`.[^1]

### 2.3 GitHub Copilot Instructions

GitHub Copilot reads instructions from `.github/copilot-instructions.md`. The file lives in the `.github/` folder and supports path-scoped instruction files.[^8]

**Strengths**: Integrated with GitHub ecosystem; natural location for GitHub-centric teams.

**Limitations**: Until recently, ignored by other tools. GitHub-centric placement feels arbitrary for projects not hosted on GitHub.

Copilot now also reads AGENTS.md, reducing the need for a separate copilot-instructions.md file.[^1]

### 2.4 Other Tool-Specific Files

**Windsurf** (`.windsurfrules`): Dual structure with `global_rules.md` for workspace-wide instructions. Windsurf supports AGENTS.md too.[^1]

**CLAUDE.local.md**: Personal, project-specific preferences that don't get committed to git. Auto-added to `.gitignore`. Use it for sandbox URLs, preferred test data, or personal workflow quirks.[^1]

### 2.5 The Ecosystem Map

| Tool                  | File                      | Location                 | Format         | Tool-Specific Features      |
| --------------------- | ------------------------- | ------------------------ | -------------- | --------------------------- |
| **Universal**         | `AGENTS.md`               | Repo root                | Plain Markdown | Closest wins precedence     |
| **Claude Code**       | `CLAUDE.md`               | Repo root                | Markdown       | @imports, 5-level recursion |
| **Cursor**            | `.cursor/rules/*.mdc`     | `.cursor/rules/`         | Markdown+YAML  | Activation modes, globs     |
| **GitHub Copilot**    | `copilot-instructions.md` | `.github/`               | Markdown       | Path-scoped files           |
| **Windsurf**          | `.windsurfrules`          | Repo root                | Markdown       | Dual structure              |
| **Claude (personal)** | `CLAUDE.local.md`         | Repo root                | Markdown       | Git-ignored                 |
| **Claude (auto)**     | `MEMORY.md`               | `~/.claude/projects/...` | Markdown       | AI-written                  |

**Key Observation**: Content is nearly identical across all files—coding standards, build commands, test setup, architectural patterns. The only differences are file location and format. This duplication is the fragmentation problem that AGENTS.md solves.[^1][^11]

______________________________________________________________________

## 3. The Standard: AGENTS.md Architecture

### 3.1 Governance: The README.md Parallel

On December 9, 2025, the Linux Foundation announced the formation of the Agentic AI Foundation (AAIF), describing it as "a neutral home for building agentic AI."[^2]

**Co-founders**:

- OpenAI
- Anthropic
- Block

**Supporting organizations**:

- Google
- Microsoft
- AWS
- Bloomberg
- Cloudflare[^2][^3]

The AAIF provides neutral stewardship for open, interoperable infrastructure for agentic AI systems. Among its anchor projects is AGENTS.md—"a simple, universal standard that gives AI coding agents a consistent source of project-specific guidance needed to operate reliably across different repositories and toolchains."[^2]

**Why This Mirrors README.md's Success**:

README.md didn't become universal because it was technically superior to alternatives. It succeeded because of three factors:

1. **Neutral Governance**: No single vendor controlled the standard. It emerged organically and was maintained by the community.

1. **Broad Backing**: Every major code hosting platform (GitHub, GitLab, Bitbucket) and development tool adopted it.

1. **Simple Design**: Plain text or Markdown. No schema, no special syntax. Works in every text editor.

AGENTS.md replicates this exact pattern:

1. **Neutral Governance**: Linux Foundation AAIF ensures no single vendor controls the standard.[^2]

1. **Broad Backing**: Co-founding by OpenAI, Anthropic, Google, Microsoft, AWS creates industry consensus.[^2][^3]

1. **Simple Design**: Plain Markdown, no required schema—just like README.md.[^4]

This is not speculation. This is the deliberate strategy of the AAIF: create a neutral, open standard with broad industry support to prevent fragmentation.[^2]

### 3.2 Technical Design: KISS Principle

**Specification**:[^4]

- **Format**: Standard Markdown
- **Schema**: None required
- **Location**: Repo root (and subdirectories via "closest wins")
- **Precedence**: Explicit user prompt > closest AGENTS.md > broader scope

**Design Philosophy**:

AGENTS.md prioritizes interoperability over feature richness. It's human-readable first, machine-readable by default. No YAML frontmatter, no special syntax. Works in every text editor and IDE.[^4]

Example AGENTS.md:

```markdown
# AGENTS.md

## Project Overview

E-commerce platform built with Next.js 14, Postgres, and Stripe.

## Build & Test

- Install: `pnpm install`
- Dev: `pnpm dev`
- Test: `pnpm test`
- Lint: `pnpm lint:fix`

## Code Standards

- Use TypeScript strict mode
- Prefer named exports over default exports
- API routes follow REST conventions in /src/api/

## Testing Requirements

- All PRs must include tests
- Use vitest for unit tests, playwright for e2e
```

This simplicity is a feature, not a limitation. Complex schemas create adoption friction. AGENTS.md removes that friction.[^1][^4]

### 3.3 Adoption Metrics

As of early 2026, AGENTS.md is used by **over 60,000 open-source projects**.[^4]

**Supported by**:

- Claude Code
- Cursor
- GitHub Copilot
- Gemini CLI
- Windsurf
- Aider
- Zed
- Warp
- RooCode
- Growing list of others[^1][^4]

The adoption curve is accelerating. Six months ago, you needed five different files for five different tools. Today, most tools read AGENTS.md. The fragmentation problem isn't solved yet, but convergence is happening.[^1]

### 3.4 Hierarchical Layout Strategy

AGENTS.md supports a "closest wins" precedence model. Drop AGENTS.md files in subdirectories, and the closest file to the edited file takes precedence.[^4][^11]

**Recommended structure**:[^11]

```text
repo/
├── AGENTS.md                    # Root: invariants across whole repo
│                                 # - Build/test entrypoints
│                                 # - Repo-wide conventions
│                                 # - Security invariants
│                                 # - Pointers to deeper docs
├── docs/
│   └── agent/
│       ├── architecture.md      # System design patterns
│       ├── conventions.md       # Coding standards
│       └── testing.md           # Testing requirements
├── frontend/
│   └── AGENTS.md                # UI conventions, component patterns
└── backend/
    └── AGENTS.md                # API architecture, contracts
```

**Content Strategy**:[^11]

- **Root AGENTS.md**: Only the invariants across the whole repo

  - Build/test entrypoints (top-level)
  - Repo-wide conventions (formatting, error payload shape, logging)
  - Security invariants (secrets, auth boundaries)
  - Pointers to deeper docs under `docs/agent/*`

- **Frontend AGENTS.md**: UI conventions, component patterns, frontend test commands

- **Backend AGENTS.md**: API architecture, contracts, migrations, service-local commands

This gives you locality ("closest wins") without relying on symlinks, and keeps each file short enough to stay high-signal.[^11]

______________________________________________________________________

## 4. The Transition Strategy: Bridging to Universal Adoption

While AGENTS.md adoption is accelerating, the transition period requires a practical approach: maintain AGENTS.md as your single source of truth while ensuring compatibility with tools that haven't fully adopted the standard yet.

### 4.1 Why Symlinks Fail

The naive solution to the fragmentation problem is symlinks. Create one canonical AGENTS.md and symlink tool-specific files to it:

```bash
ln -sfn AGENTS.md .github/copilot-instructions.md
mkdir -p .cursor/rules && ln -sfn ../../AGENTS.md .cursor/rules/main.mdc
```

This works on a single developer's macOS or Linux machine. But it fails as a team strategy.[^1][^11]

**Symlink Pros**:

- Single source of truth
- Works on macOS/Linux

**Symlink Cons** (Critical for Teams):[^11]

1. **Windows compatibility**: Symlinks on Windows require Developer Mode enabled AND `git config core.symlinks true`. Without proper configuration, Windows clones silently materialize symlinks as small text files containing the symlink path—not the actual content.

1. **Tool resolution issues**: Some tools resolve symlinks differently. The "closest file wins" precedence can behave unexpectedly when a symlink points elsewhere in the directory tree.

1. **CI/CD fragility**: ZIP downloads break symlinks. Some CI policies disallow symlinks entirely. Artifacts may not preserve symlink relationships.

1. **Operational friction**: Every new developer needs a symlink-compatible environment. This adds onboarding overhead and creates "works on my machine" scenarios.

**Verdict**: Symlinks are a local deduplication hack, not a robust team strategy.[^11]

### 4.2 The Recommended Approach: Pointer Files

**Strategy**: Maintain AGENTS.md as your source of truth. Create lightweight pointer files at tool-expected locations.[^11]

**Implementation**:

For each tool your team uses, create a minimal file that references AGENTS.md:

**For GitHub Copilot** (`.github/copilot-instructions.md`):

```markdown
# GitHub Copilot Instructions

See `AGENTS.md` at the repository root for all project guidance.
```

**For Cursor** (`.cursor/rules/base.mdc`):

```text
---
description: Base project rules
glob: **/*
---

# Cursor Rules

See `AGENTS.md` at the repository root for all project guidance.
```

**Why This Works**:[^11]

- Works identically on Windows, macOS, Linux
- AGENTS.md remains the single source of truth—no drift
- Each tool finds its expected file
- No build steps, no symlink configuration
- Version-controlled and auditable

The minimal duplication (one pointer per tool) is an acceptable trade-off for cross-platform reliability and simplicity.[^11]

### 4.3 Alternative: Automated Generation

Teams requiring zero duplication can generate tool-specific files from AGENTS.md:[^11]

```bash
#!/bin/bash
# scripts/generate-agent-configs.sh
# Reads AGENTS.md → writes tool-specific files

cat AGENTS.md > .github/copilot-instructions.md
cat AGENTS.md > .cursor/rules/base.mdc
# Add tool-specific frontmatter if needed
```

Run this in a pre-commit hook or CI pipeline.

**Trade-off**: Eliminates duplication but adds build complexity.

**Recommendation**: Start with pointer files. Add generation only if needed.[^11]

### 4.4 Security Consideration: Instruction Injection

Recent security research has identified instruction injection attack vectors in AI coding assistants. Specifically, GitHub Issues have been abused in Copilot attacks leading to repository takeover.[^10]

The attack vector: malicious instructions embedded in issue comments, PR descriptions, or other external sources that AI tools pull into their context.

**Mitigation strategy**:[^10][^11]

- Keep canonical agent instructions in version-controlled repo files (AGENTS.md)
- Avoid pulling instructions from untrusted external sources
- Version-controlled AGENTS.md is auditable, reviewable, and stable

This is another advantage of the shim file strategy: all instructions live in version-controlled files, not external sources or dynamically generated content.

______________________________________________________________________

## 5. The Implementation: Comprehensive AGENTS.md

### 5.1 Structure: The Four Essential Sections

A good AGENTS.md has four core sections:[^1]

**1. Project Overview** (one line):

```markdown
## Project Overview

Next.js e-commerce app with Stripe integration and Postgres.
```

**2. Build & Test** (exact commands):

```markdown
## Build & Test

- Install: `pnpm install`
- Dev: `pnpm dev`
- Test: `pnpm test`
- Lint: `pnpm lint:fix`
- Build: `pnpm build`
```

AI agents use these verbatim. Precision matters.[^1]

**3. Code Standards** (specific rules, not generalities):

```markdown
## Code Standards

- Use ES modules
- Prefer named exports over default exports
- 2-space indentation
- Max line length: 100 characters
- Use TypeScript strict mode
```

Not "format code properly"—that's too vague. Specific, actionable rules.[^1]

**4. Architecture** (patterns and conventions):

```markdown
## Architecture

- API routes go in /src/api/[resource]/route.ts
- We use the repository pattern for database access
- All database queries go through repositories in /src/repositories/
- Business logic lives in service classes in /src/services/
```

This is where Claude would get things wrong without guidance.[^1]

### 5.2 Content Strategy: What Goes Where

**Target**: Under 300 lines for root AGENTS.md. Focus on what the AI would get wrong without the file.[^1]

**Root AGENTS.md** (invariants only):

- Build commands
- Security rules
- Formatting standards
- Pointers to detailed docs

**docs/agent/\*.md** (detailed guidance):

- Architecture patterns
- Testing requirements
- API conventions
- Security policies

**Subdirectory AGENTS.md** (context-specific):

- Frontend: Component patterns, UI conventions
- Backend: API contracts, migration patterns
- Worker: Async semantics, idempotency rules

**What NOT to include**:[^1]

- Obvious information ("this is a TypeScript project"—the AI can see package.json)
- Redundant information already in README.md
- Implementation details that change frequently

Every line in AGENTS.md competes for attention with the actual work. Keep it lean.[^1]

### 5.3 The /init Then Delete Workflow

For Claude Code users, the fastest way to bootstrap AGENTS.md:[^1]

1. Run `/init` in your project directory
1. Claude generates a starter CLAUDE.md based on your project structure
1. **Delete most of what it generates**

Step 3 is where most people go wrong. The generated file is a starting point, not a finished product. It often includes filler that doesn't add value.[^1]

The delete-first approach is faster than writing from scratch. You're editing down from a reasonable draft instead of staring at a blank file.

After the initial setup, build your memory file organically. When Claude makes a wrong assumption, don't just correct it once—tell Claude: "add to my AGENTS.md: always import from @company/utils-v2, not @company/utils." The instruction persists for future sessions.[^1]

### 5.4 Multi-Tool Integration Example

**Recommended structure**:

```text
repo/
├── AGENTS.md                    # Universal standard (comprehensive)
├── .github/
│   └── copilot-instructions.md  # Shim: "See AGENTS.md"
├── .cursor/
│   └── rules/
│       └── base.mdc             # Shim: "See AGENTS.md"
├── docs/
│   └── agent/
│       ├── architecture.md      # Detailed patterns
│       └── testing.md           # Test requirements
└── CLAUDE.md                    # Optional: Claude-specific @imports
```

**Benefits**:

- Any IDE/agent entering the repo finds guidance
- AGENTS.md serves as the universal brief
- Claude users get enhanced features via CLAUDE.md (optional)
- No symlinks, no fragility
- Version-controlled, auditable, portable

This structure works on Windows, macOS, Linux. It works in CI. It works when someone downloads a ZIP of your repo. It just works.[^11]

### 5.5 Template

```markdown
# [Project Name]

## Project Overview

[One-sentence description: tech stack + project type + key integrations]

## Build & Test Commands

- Install: `[exact command]`
- Dev: `[exact command]`
- Test: `[exact command]`
- Lint: `[exact command]`
- Build: `[exact command]`

## Code Standards

- Language/Runtime: [e.g., TypeScript 5.x, Node 20]
- Module system: [e.g., ES modules]
- Export style: [e.g., Prefer named exports]
- Indentation: [e.g., 2 spaces]
- Max line length: [e.g., 100 characters]

## Architecture

- Directory structure: [key patterns]
- Design patterns: [e.g., Repository pattern for DB access]
- API conventions: [e.g., REST in /src/api/[resource]/route.ts]

## Testing Requirements

- Framework: [e.g., vitest for unit, playwright for e2e]
- Coverage: [e.g., >80% for critical paths]
- PR requirements: [e.g., All PRs must include tests]

## Security Invariants

- [Critical security rules]

## Additional Resources

- See @docs/architecture.md for system design
- See @docs/testing.md for test patterns
- See @docs/security.md for security policies
```

______________________________________________________________________

## 6. Discussion: Convergence and Future

### 6.1 The Convergence Trajectory

AGENTS.md is positioned to become the standard the way README.md did.[^1]

**Evidence**:

1. **Governance**: Linux Foundation AAIF provides neutral stewardship (announced Dec 2025, co-founded by OpenAI, Anthropic, Google, Microsoft, AWS)[^2][^3]

1. **Adoption**: 60,000+ projects; supported by Claude Code, Cursor, GitHub Copilot, Gemini CLI, Windsurf, and growing[^4]

1. **Design**: Plain Markdown, no schema—prioritizes interoperability over features (KISS principle)[^4]

1. **Necessity**: Fragmentation is unsustainable; teams need one standard

**Tool-Specific Files Persist As**:[^1]

- Feature extensions (Cursor's .mdc activation modes)
- Personal preferences (CLAUDE.local.md)
- Auto-memory (Claude's MEMORY.md)

**But Shared Context Consolidates To**: One AGENTS.md.

The convergence is already happening. Six months ago, five files for five tools. Today, most tools read AGENTS.md. The Linux Foundation backing ensures this trend will continue.[^1][^2]

### 6.2 The Mechanics of Standardization

README.md didn't achieve ubiquity through technical superiority. It succeeded through:

1. **Network effects**: Once enough projects adopted it, tools had to support it
1. **Neutral governance**: No vendor lock-in
1. **Simplicity**: Low barrier to adoption

AGENTS.md has all three:

1. **Network effects**: 60,000+ projects create momentum[^4]
1. **Neutral governance**: Linux Foundation AAIF[^2]
1. **Simplicity**: Plain Markdown, no schema[^4]

Additionally, AGENTS.md has something README.md didn't: **deliberate industry coordination**. The co-founding of AAIF by major AI vendors is an explicit commitment to convergence.[^2][^3]

This isn't organic emergence. This is orchestrated standardization.

### 6.3 Practical Implications for Teams

**Adopt AGENTS.md now**. Even if your team only uses one AI tool today, you will use multiple tools tomorrow. The AI coding assistant landscape is evolving rapidly. AGENTS.md future-proofs your project.

**Use shim files for tool compatibility**. Don't use symlinks. The portability and simplicity of shim files outweigh the tiny duplication.

**Keep AGENTS.md comprehensive but concise**. Target under 300 lines. Move detailed guidance to separate docs and reference them.

**Review and update regularly**. Instructions accumulate, some become redundant, others conflict. Ask your AI assistant to review and optimize your AGENTS.md every few weeks.[^1]

______________________________________________________________________

## 7. Conclusion

AGENTS.md is positioned to achieve README.md-level ubiquity by replicating the same success formula.

The evidence converges across multiple dimensions:

1. **Governance**: Linux Foundation AAIF provides neutral stewardship (announced Dec 2025, co-founded by OpenAI, Anthropic, Google, Microsoft, AWS)[^2][^3]

1. **Adoption**: 60,000+ projects; supported by Claude Code, Cursor, GitHub Copilot, Gemini CLI, Windsurf, and growing[^4]

1. **Design**: Plain Markdown, no schema—prioritizes interoperability over features (KISS principle)[^4]

1. **Necessity**: Fragmentation (CLAUDE.md, .cursorrules, copilot-instructions.md, etc.) is unsustainable; teams need one standard

**Recommended Implementation Strategy**:

- One comprehensive AGENTS.md at repo root
- Thin shims at tool-expected paths (.github/, .cursor/rules/)
- No symlinks (Windows fragility, CI issues)
- Hierarchical layout for large repos (closest wins)

The gap between "Claude, we use pnpm" every session and "Claude already knows" is the difference between a tool and a teammate. AGENTS.md bridges that gap—not just for Claude, but for every AI assistant your team uses.[^1]

Six months ago, five files for five tools. Today, most tools read AGENTS.md. The convergence is happening. The Linux Foundation backing ensures it will last.[^1][^2]

The fragmentation era is ending. The AGENTS.md era is beginning.

**Call to Action**: Adopt AGENTS.md now. Use shim files for tool compatibility. Skip the symlink complexity. Your future teammates—human and AI—will thank you.

______________________________________________________________________

## References

______________________________________________________________________

## Appendix A: File Format Comparison

| File                    | Tool                   | Governance            | Format         | Schema               | Adoption      |
| ----------------------- | ---------------------- | --------------------- | -------------- | -------------------- | ------------- |
| AGENTS.md               | Universal              | Linux Foundation AAIF | Plain Markdown | None                 | 60k+ projects |
| CLAUDE.md               | Claude Code            | Anthropic             | Markdown       | None                 | Claude-only   |
| .cursorrules            | Cursor                 | Cursor                | Markdown       | None                 | Legacy        |
| .cursor/rules/\*.mdc    | Cursor                 | Cursor                | Markdown+YAML  | Frontmatter required | Cursor-only   |
| copilot-instructions.md | GitHub Copilot         | GitHub                | Markdown       | None                 | GitHub-only   |
| .windsurfrules          | Windsurf               | Codeium               | Markdown       | None                 | Windsurf-only |
| JULES.md                | Google Jules           | Google                | Markdown       | None                 | Jules-only    |
| CLAUDE.local.md         | Claude Code (personal) | User                  | Markdown       | None                 | Personal use  |
| MEMORY.md               | Claude Code (auto)     | Anthropic             | Markdown       | None                 | AI-written    |

______________________________________________________________________

## Appendix B: Shim File Templates

### GitHub Copilot

`.github/copilot-instructions.md`:

```markdown
# GitHub Copilot Instructions

This project follows the guidance in `AGENTS.md` at the repository root.
Please refer to that file for build commands, code standards, and architecture patterns.
```

### Cursor

`.cursor/rules/base.mdc`:

```text
---
description: Base project rules
glob: **/*
---

# Cursor Rules

See `AGENTS.md` in the repository root for complete project guidance.
All coding standards, build commands, and architecture patterns are defined there.
```

______________________________________________________________________

## Appendix C: Complete AGENTS.md Template

```markdown
# [Project Name]

## Project Overview

[One-sentence description: tech stack + project type + key integrations]

## Build & Test Commands

- Install: `[exact command]`
- Dev: `[exact command]`
- Test: `[exact command]`
- Lint: `[exact command]`
- Build: `[exact command]`

## Code Standards

- Language/Runtime: [e.g., TypeScript 5.x, Node 20]
- Module system: [e.g., ES modules]
- Export style: [e.g., Prefer named exports]
- Indentation: [e.g., 2 spaces]
- Max line length: [e.g., 100 characters]

## Architecture

- Directory structure: [key patterns]
- Design patterns: [e.g., Repository pattern for DB access]
- API conventions: [e.g., REST in /src/api/[resource]/route.ts]

## Testing Requirements

- Framework: [e.g., vitest for unit, playwright for e2e]
- Coverage: [e.g., >80% for critical paths]
- PR requirements: [e.g., All PRs must include tests]

## Security Invariants

- [Critical security rules]

## Additional Resources

- See @docs/architecture.md for system design
- See @docs/testing.md for test patterns
- See @docs/security.md for security policies
```

[^1]: Perrone, P. (2026, February 26). The Complete Guide to AI Agent Memory Files (CLAUDE.md, AGENTS.md, and Beyond). *Medium Data Science Collective*. <https://medium.com/data-science-collective/the-complete-guide-to-ai-agent-memory-files-claude-md-agents-md-and-beyond-49ea0df5c5a9>

[^7]: HumanLayer. (2025, November 25). Writing a good CLAUDE.md. *HumanLayer Blog*. <https://www.humanlayer.dev/blog/writing-a-good-claude-md>

[^9]: Cursor. (n.d.). Rules. *Cursor Documentation*. <https://cursor.com/docs/context/rules>

[^8]: GitHub Docs. (n.d.). Adding custom instructions for GitHub Copilot. *GitHub Documentation*. <https://docs.github.com/en/copilot/how-tos/copilot-cli/add-repository-instructions>

[^11]: ChatGPT Analysis. (2026, March 5). Symlinking Best Practices and Alternatives for AI Agent Memory Files. OpenAI ChatGPT conversation c/69a9df0e-3d20-8333-bfe7-f342732c8253.

[^2]: Linux Foundation. (2025, December 9). Linux Foundation Announces the Formation of the Agentic AI Foundation (AAIF). *Linux Foundation Press Release*. <https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation>

[^3]: OpenAI. (2025, December 9). OpenAI co-founds the Agentic AI Foundation under the Linux Foundation. *OpenAI Blog*. <https://openai.com/index/agentic-ai-foundation/>

[^4]: AGENTS.md Specification. (n.d.). *AGENTS.md Official Site*. <https://agents.md/>

[^10]: SecurityWeek. (2025). GitHub Issues Abused in Copilot Attack Leading to Repository Takeover. *SecurityWeek*. <https://www.securityweek.com/github-issues-abused-in-copilot-attack-leading-to-repository-takeover/>
