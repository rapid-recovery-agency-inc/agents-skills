# Agents Skills

Centralized registry of AI agent skills. Install via CLI, consume in your agent runtime.

![AI Skills workflow via Git submodules](./assets/ai-skills-flow.png)

## Quick Start

```bash
# Install CLI
pip install "git+https://github.com/rapid-recovery-agency-inc/agents-skills.git@main#subdirectory=cli"

# List available skills
agents-skills list

# Add a skill to your project
agents-skills add create-agents-files
```

## Skills

- **create-agents-files** - Generates hierarchical AGENTS.md from repo structure and usage evidence
- **skill-creator** - Draft, evaluate, and improve skills with evals and variance analysis

## Common Tasks

```bash
# Search for skills
agents-skills list python

# Add one skill
agents-skills add skill-creator

# Sync all skills
agents-skills sync
```

## Installation

<details>
<summary>Using pip (recommended)</summary>

```bash
pip install "git+https://github.com/rapid-recovery-agency-inc/agents-skills.git@main#subdirectory=cli"
```

</details>

<details>
<summary>Using Poetry</summary>

```bash
poetry self add "git+https://github.com/rapid-recovery-agency-inc/agents-skills.git@main#subdirectory=cli"
```

</details>

<details>
<summary>Using uv</summary>

```bash
# Install as a tool
uv tool install "git+https://github.com/rapid-recovery-agency-inc/agents-skills.git@main#subdirectory=cli"

# Or run ephemerally
uvx --from "git+https://github.com/rapid-recovery-agency-inc/agents-skills.git@main#subdirectory=cli" agents-skills list
```

</details>

## Contributing

1. Edit skills in `skills/`
1. Run `just lint`
1. Open PR

**Setup:** `pip install pre-commit && pre-commit install`

**Repository structure:**

- `skills/` - Skill definitions and assets
- `registry.json` - Source of truth index
- `registry.schema.json` - JSON Schema validation
- `cli/` - CLI tool for consuming skills

## License

Apache-2.0
