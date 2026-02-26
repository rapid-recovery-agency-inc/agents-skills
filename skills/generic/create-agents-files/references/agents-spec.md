# AGENTS.md Specification Brief

## Initial Instruction

Use this document as first reference for AGENTS.md format and usage.

If deeper detail is needed, consult the official specification at <https://agents.md/>.

## What AGENTS.md Is

AGENTS.md is an open, tool-agnostic instruction file for coding agents.

It complements README.md:

- README.md stays focused on human contributors.
- AGENTS.md carries agent-specific execution context and conventions.

## Why Keep AGENTS.md Separate from README.md

- Gives agents one predictable instruction location.
- Keeps README concise for humans.
- Allows detailed build/test/style guidance without cluttering contributor docs.

## Cross-Agent Compatibility

The format is intended to work across multiple coding-agent products and IDEs.

Practical implication:

- Prefer stable markdown conventions over tool-specific syntax.
- Keep instructions portable and explicit.

## Recommended Content Areas

The spec highlights practical sections that help agents execute reliably:

- Project overview
- Build and test commands
- Code style guidelines
- Testing instructions
- Security considerations

## Authoring Pattern

Use short, operational sections with explicit commands and expectations.

Common high-value content:

- Environment setup shortcuts
- Canonical test command paths
- Lint/typecheck requirements
- PR and commit requirements

## Migration Notes

From FAQ guidance:

- Existing `AGENT.md` can be renamed to `AGENTS.md`.
- A symlink can be used for backward compatibility when needed.

## Tool Integration Notes

FAQ examples mention:

- Aider can be configured to read `AGENTS.md`.
- Gemini CLI can be configured with `contextFileName: AGENTS.md`.

Use these as integration hints when tool-specific setup is required.

## Practical Guidance for This Skill

When generating AGENTS.md files:

- Write one clear Purpose statement grounded in package runtime role.
- Keep sections concise and actionable.
- Prefer concrete commands and constraints over narrative.
- Keep hierarchy semantics explicit (`Inherits`, precedence, child links where relevant).
- Avoid policy duplication across parent/child AGENTS files.

## Quick Compliance Checklist

- File is named `AGENTS.md`.
- Content is markdown and tool-agnostic.
- Includes execution-relevant sections (build/test/style/security as applicable).
- Uses clear, imperative instructions.
- Aligns with parent AGENTS authority and scope.
