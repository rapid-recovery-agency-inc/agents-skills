set shell := ["bash", "-eu", "-o", "pipefail", "-c"]

default:
    @just --list

# Ensure pre-commit is available via standard installation methods.
ensure-pre-commit:
    @if command -v pre-commit >/dev/null 2>&1; then \
      pre-commit --version; \
    elif [ -x .tools/pre-commit-venv/bin/pre-commit ]; then \
      .tools/pre-commit-venv/bin/pre-commit --version; \
    else \
      echo "pre-commit is not installed."; \
      echo "(No global pre-commit and no .tools/pre-commit-venv/bin/pre-commit found.)"; \
      echo "Install using one of:"; \
      echo "  - brew install pre-commit"; \
      echo "  - pipx install pre-commit"; \
      echo "  - uv tool install pre-commit"; \
      echo "  - python3 -m pip install --user pre-commit"; \
      exit 1; \
    fi

# Install git hooks for this repo.
install-hooks: ensure-pre-commit
    @if command -v pre-commit >/dev/null 2>&1; then \
      pre-commit install --hook-type pre-commit --hook-type pre-push; \
    else \
      .tools/pre-commit-venv/bin/pre-commit install --hook-type pre-commit --hook-type pre-push; \
    fi

# Run format pass first, then all configured checks.
lint: ensure-pre-commit fmt
    @if command -v pre-commit >/dev/null 2>&1; then \
      pcmd="pre-commit"; \
    else \
      pcmd=".tools/pre-commit-venv/bin/pre-commit"; \
    fi; \
    files="$(git ls-files --cached --others --exclude-standard)"; \
    if [ -n "$files" ]; then \
      SKIP=mdformat "$pcmd" run --files $files; \
    else \
      echo "No repository files found to lint."; \
    fi

# Format markdown via mdformat hook.
fmt: ensure-pre-commit
    @if command -v pre-commit >/dev/null 2>&1; then \
      pcmd="pre-commit"; \
    else \
      pcmd=".tools/pre-commit-venv/bin/pre-commit"; \
    fi; \
    files="$(git ls-files --cached --others --exclude-standard -- '*.md')"; \
    if [ -n "$files" ]; then \
      "$pcmd" run mdformat --files $files; \
    else \
      echo "No Markdown files found to format."; \
    fi

# Backward-compatible alias.
check: lint

# Stage a skill into local sandbox for testing.
# Usage: just stage-skill skill-creator
# Also supported: just stage-skill skill=skill-creator
stage-skill skill:
    @requested="{{skill}}"; \
    normalized="${requested#skill=}"; \
    src="skills/generic/${normalized}"; \
    dst=".agents/skills/${normalized}"; \
    if [ ! -d "$src" ]; then \
      echo "Skill not found: $src"; \
      exit 1; \
    fi; \
    mkdir -p "$dst"; \
    rsync -a --delete "$src/" "$dst/"; \
    echo "Staged $src -> $dst"
