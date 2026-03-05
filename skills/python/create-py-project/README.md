# create-py-project

A skill for creating modern Python projects with best-in-class tooling.

## What It Does

This skill bootstraps complete, production-ready Python projects using agent-driven dynamic content generation. Instead of rigid templates, it intelligently generates appropriate, working code based on your specific requirements.

### Supported Project Types

- **FastAPI Applications** - APIs, microservices, web services with proper routing
- **CLI Tools** - Command-line utilities with argument parsing
- **Python Packages** - Libraries and modules with proper packaging

### Tool Stack

- **Package Manager**: `poetry` (default) or `uv`
- **Linter/Formatter**: `ruff` (replaces black, flake8, isort, pydocstyle)
- **Type Checker**: `mypy` (default) or `ty`
- **Testing**: `pytest`
- **Git Hooks**: `pre-commit`

### Generated Structure

All projects follow company conventions:

```text
my-project/
├── main.py                 # Entry point (FastAPI or CLI)
├── pyproject.toml          # Project configuration
├── shared/                 # Infrastructure layer
│   ├── __init__.py
│   ├── config.py          # Settings (pydantic-settings)
│   └── router.py          # FastAPI routes (if applicable)
├── modules/               # Domain layer
│   ├── __init__.py
│   └── models.py          # Domain models
├── my_project/            # Package (minimal)
│   └── __init__.py
├── .pre-commit-config.yaml
├── .gitignore
├── .env.example
├── README.md
└── Justfile
```

## Usage

### Quick Start

Ask your AI assistant to create a project:

```text
Use skill to create a project for a FastAPI microservice that handles user authentication
```

Or be more specific:

```text
Set up a Python CLI tool for processing CSV files with pandas
```

The skill auto-executes when requirements are clear, or asks clarifying questions when needed.

### For Developers

To view available skills and their capabilities:

```text
List available skills
```

To introspect this skill specifically:

```text
Show me the create-py-project skill
```

**Best practice for invoking:**

1. **Be specific about project type**

   - "Use skill to create project for a FastAPI API with Redis caching"
   - "Use skill to create project for a CLI tool that converts JSON to CSV"

1. **Include domain details**

   - Mention technologies: "with PostgreSQL", "using JWT auth", "with httpx"
   - State purpose: "for user management", "for data processing", "for webhook handling"

1. **Let the skill handle defaults**

   - Package manager, Python version, and tooling are auto-selected
   - Override only if you have preferences: "use uv instead of poetry"

**Example prompts:**

| Intent          | Prompt                                                                                        |
| --------------- | --------------------------------------------------------------------------------------------- |
| FastAPI service | `Use skill to create project for a FastAPI microservice for order processing with PostgreSQL` |
| CLI tool        | `Use skill to create project for a CLI tool that syncs files to S3`                           |
| Library         | `Use skill to create project for a Python package for parsing log files`                      |

## How It Works

1. **Smart Preflight** - Analyzes request to determine if auto-execution is appropriate
1. **Requirement Gathering** - Collects project type, dependencies, tooling preferences
1. **Dynamic Generation** - File Generator agent creates customized, working files
1. **Validation** - Project Validator ensures correctness and completeness
1. **Environment Setup** - Installs dependencies with chosen package manager
1. **Live Testing** - Optionally runs the application to verify it works

## Files Included

| File                          | Purpose                                 |
| ----------------------------- | --------------------------------------- |
| `SKILL.md`                    | Main skill definition and workflow      |
| `LICENSE.txt`                 | Apache 2.0 license                      |
| `agents/setup-coordinator.md` | Orchestrates the bootstrap process      |
| `agents/file-generator.md`    | Dynamically generates project files     |
| `agents/project-validator.md` | Validates generated project correctness |

## License

Apache License 2.0 - See [LICENSE.txt](LICENSE.txt)
