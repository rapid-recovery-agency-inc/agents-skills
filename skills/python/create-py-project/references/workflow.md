# Quality Gating Workflow

**CRITICAL**: After generating all files, run automated quality checks to ensure code meets standards.

## When to Run Quality Gates

1. **Periodically**: After generating major components (all routers, all clients, etc.)
1. **Finally**: After all files are generated, before reporting completion

## Quality Gate Command

```bash
just check
```

This runs:

- `just lint-fix` - Lint and auto-fix issues with ruff
- `just format` - Format code with ruff
- `just typecheck` - Type check with mypy/ty

## Iterative Fix Workflow

**If `just check` fails:**

1. **Read the error output** carefully to identify issues
1. **Categorize the errors**:
   - Linting errors (ruff)
   - Formatting issues (ruff format)
   - Type errors (mypy/ty)
1. **Fix errors systematically**:
   - Run `just lint-fix` to auto-fix linting issues
   - Run `just format` to auto-format code
   - Manually fix type errors by editing files
1. **Re-run `just check`** to verify fixes
1. **Repeat** until `just check` passes with no errors

## Common Issues and Fixes

### Linting errors

- Unused imports → Remove them
- Line too long → Break into multiple lines
- Missing docstrings → Add Google-style docstrings

### Type errors

- Missing type hints → Add proper type annotations
- Incorrect return types → Fix function signatures
- Import errors → Add missing imports or dependencies

### Formatting issues

- Usually auto-fixed by `just format`
- If not, check for syntax errors first

## Success Criteria

**Generation is complete when:**

- All files created successfully
- `just check` runs with **zero errors**
- No manual intervention needed from user

**If unable to fix after 3 iterations:**

- Report specific errors to user
- Provide guidance on manual fixes needed
- Do NOT report success if quality gate fails
