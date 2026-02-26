# Skill Builder Skills Research

Developer-facing research notes on meta-skills (skills that create other skills).

## Sources Reviewed

- [Anthropic skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)
- [FrancyJGLisboa/agent-skill-creator](https://github.com/FrancyJGLisboa/agent-skill-creator)
- [alirezarezvani/claude-code-skill-factory](https://github.com/alirezarezvani/claude-code-skill-factory)
- [LeoFanKm/claude-skill-generator](https://github.com/LeoFanKm/claude-skill-generator)
- [metaskills/skill-builder](https://github.com/metaskills/skill-builder)
- [ArneJanning/local-skills-agent](https://github.com/ArneJanning/local-skills-agent)
- [skillcreatorai/Ai-Agent-Skills](https://github.com/skillcreatorai/Ai-Agent-Skills)
- [heilcheng/awesome-agent-skills](https://github.com/heilcheng/awesome-agent-skills)
- [skillmatic-ai/awesome-agent-skills](https://github.com/skillmatic-ai/awesome-agent-skills)

## Key Feature and Design Concepts

| Feature / Concept                | Description                                                         | Benefit                                                  |
| -------------------------------- | ------------------------------------------------------------------- | -------------------------------------------------------- |
| Iterative evaluation loop        | Draft skill, run tests, evaluate, refine, repeat.                   | Produces higher-quality skills than one-pass generation. |
| Baseline comparisons             | Compare with-skill vs without-skill (or old vs new skill).          | Prevents false confidence and quantifies improvement.    |
| Trigger optimization             | Tune SKILL.md `description` against trigger/non-trigger cases.      | Better invocation precision and fewer false triggers.    |
| Progressive disclosure           | Keep SKILL.md concise; move depth to `references/` and scripts.     | Lower context cost and easier maintenance.               |
| Structured phase pipeline        | Discovery -> design -> architecture -> detection -> implementation. | Improves consistency and reduces omissions.              |
| Automated quality gates          | Validate schema, naming, frontmatter, structure, links.             | Blocks invalid skills from distribution.                 |
| Security scanning                | Detect secrets and risky patterns before publish/install.           | Reduces risk in shared registries.                       |
| Registry-based sharing           | Publish/list/install skills via team registry workflows.            | Reuses knowledge across teams and projects.              |
| Cross-platform install           | Support multiple agent runtimes from one skill format.              | Improves adoption and lowers fragmentation.              |
| Orchestrator + specialist agents | Top-level guide delegates to specialized builders.                  | Better UX and better outcomes for complex builds.        |
| Convention-driven naming         | Strict naming for skill IDs and support files.                      | Better discoverability and repository hygiene.           |
| Tooling-first workflows          | Prefer deterministic CLI/scripts over vague prose.                  | Better reproducibility and operational reliability.      |
| Self-extending local systems     | Agent creates new skills and uses them immediately.                 | Rapid capability growth without external dependencies.   |
| Composable skills                | Skills invoke other skills for multi-step workflows.                | Modular growth over monolithic skill design.             |
| Spec alignment                   | Build to shared SKILL.md standards.                                 | Interoperability across ecosystems.                      |

## Recommended Priorities

1. Add iterative eval + baseline workflows for all new/updated skills.
1. Add trigger tuning tests (should-trigger + should-not-trigger).
1. Enforce validation and security checks before publishing.
1. Keep SKILL.md concise and shift details into references.
1. Track lightweight registry metadata for discovery and reuse.
