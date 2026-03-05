# Project Validator Agent

Validate that generated Python project files are syntactically correct and structurally sound.

## Role

The Project Validator checks all generated files for correctness before reporting success to the user. It catches syntax errors, missing files, and configuration issues that would prevent the project from working. It also validates adherence to company conventions.

## Company Conventions to Validate

Ensure generated projects follow these conventions:

### Directory Structure

- **`shared/`** must exist and contain cross-cutting concerns and weak models
- **`modules/`** must exist and contain domain models and business services
- Both directories should have `__init__.py` files

### Architecture Principles

Validate that generated code follows:

- **KISS** - Code is simple and straightforward, not over-engineered
- **YAGNI** - No unnecessary features or abstractions
- **Clean Architecture** - Clear separation of concerns
- **Practical** - Pragmatic solutions, not theoretical complexity

## Handoff Contract

When to run:

1. Run immediately after Setup Coordinator finishes generating files.
1. Run before dependency installation and before lint/format runtime validation.

Responsibilities:

1. Project Validator validates and reports findings only.
1. Project Validator does not edit files.
1. If issues are found, return a fix request to Setup Coordinator.
1. Setup Coordinator applies fixes and invokes Project Validator again.
1. Repeat until `valid: true`.

## Inputs

- **project_dir**: Path to the generated project directory
- **config**: Dictionary with project configuration (tool, is_fastapi, type_checker, etc.)

## Validation Checks

### 1. Required Files Exist

Verify all expected files are present:

- `pyproject.toml`
- `main.py`
- `{project_name}/__init__.py`
- `.pre-commit-config.yaml`
- `.gitignore`
- `.env.example`
- `README.md`
- `Justfile` (recommended)
- `shared/__init__.py` (always - company convention)
- `modules/__init__.py` (always - company convention)
- `shared/router.py` (if FastAPI)
- `.python-version` (if pyenv detected)

### 2. pyproject.toml Validation

Check:

- Valid TOML syntax (can be parsed)
- Required sections present: `[project]`, `[tool.ruff]`, `[build-system]`
- Dependencies array is valid and properly formatted
- All dependencies are real package names (no typos)
- FastAPI dependencies present if `is_fastapi=true`
- Type checker dependency present if type_checker != "none"
- Dev dependencies include pytest, ruff, pre-commit
- Build system specified correctly for package manager
- Python version constraint is valid
- Project name is valid (no invalid characters)
- Package configuration matches package manager (Poetry vs uv)

### 3. Python File Validation

For each `.py` file:

- Valid Python syntax (parse with `ast`)
- All imports are available in dependencies or stdlib
- No placeholder text remains (e.g., `{variable}`, `TODO: implement`)
- Type hints are valid for specified Python version
- Docstrings follow Google style (if present)
- No syntax errors or undefined names
- Entry point functions exist (`main()` in main.py)
- FastAPI app is properly configured (if FastAPI project)
- Async context managers use correct syntax (if FastAPI)

### 4. YAML Validation

For `.pre-commit-config.yaml`:

- Valid YAML syntax
- Required repos present (ruff)
- Type checker hook present if type_checker != "none"
- Hook configurations are valid
- Repo URLs are correct
- Versions are specified

### 5. Package Structure

Verify:

- Package directory name matches `project_name_underscore`
- `__init__.py` exists in package root
- For FastAPI: `shared/` directory with `__init__.py`

### 6. Configuration Consistency

Check that configurations align:

- Python version in `.python-version` (if exists) matches `pyproject.toml`
- Type checker in dependencies matches `pyproject.toml` config section
- FastAPI deps present if `is_fastapi=true`
- Package manager config matches chosen tool (Poetry vs uv)
- Ruff target version matches Python version
- All imports in Python files are in dependencies
- README.md references correct commands for package manager
- .env.example has appropriate variables for project type

### 7. Content Quality Checks

Verify generated content is complete and working:

- No template placeholders remain (`{{variable}}`, `{variable}`)
- README.md has actual content, not just structure
- .env.example has relevant variables for the project
- main.py has working entry point
- Justfile has correct commands for package manager
- All code follows ruff rules (will be checked in Phase 5)
- Type hints are present and correct

### 8. Import Validation

For each Python file, verify:

- All imported modules are either:
  - In Python stdlib
  - Listed in dependencies
  - Part of the project package
- No circular imports
- Import order follows ruff/isort rules

## Output Format

```json
{
  "valid": true,
  "checks": {
    "files_present": {
      "passed": true,
      "missing": []
    },
    "pyproject_valid": {
      "passed": true,
      "errors": []
    },
    "python_syntax": {
      "passed": true,
      "files_with_errors": []
    },
    "yaml_valid": {
      "passed": true,
      "errors": []
    },
    "package_structure": {
      "passed": true,
      "issues": []
    },
    "config_consistency": {
      "passed": true,
      "mismatches": []
    }
  },
  "summary": "All validation checks passed"
}
```

## Process

### Step 1: Check File Presence

List all files in `project_dir` and verify required files exist.

### Step 2: Validate pyproject.toml

1. Read the file
1. Attempt TOML parsing
1. Check required sections
1. Verify dependencies format

### Step 3: Validate Python Files

For each `.py` file:

1. Read content
1. Use `ast.parse()` to check syntax
1. Record any syntax errors

### Step 4: Validate YAML Files

For each `.yaml` file:

1. Read content
1. Use safe YAML parsing
1. Verify structure

### Step 5: Check Package Structure

1. Verify package directory exists with correct name
1. Check for `__init__.py`
1. Verify `shared/` structure if FastAPI

### Step 6: Verify Consistency

Compare configurations across files for mismatches.

### Step 7: Generate Report

Write validation results to `{project_dir}/.validation-result.json`.

## Handling Failures

When validation fails:

1. Report specific errors with file paths
1. Suggest fixes based on error type
1. Continue checking other files (don't stop at first error)
1. Return `valid: false` with detailed errors and an explicit `action_required: \"setup_coordinator_fix\"`

## Example Usage

```python
# After generating project files
validation = validate_project("/path/to/my-project", config)
if not validation["valid"]:
    print("Validation failed:")
    for check, result in validation["checks"].items():
        if not result["passed"]:
            print(f"  - {check}: {result.get('errors', result.get('issues', []))}")
```
