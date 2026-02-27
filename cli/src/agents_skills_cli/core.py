from __future__ import annotations

import json
import shutil
import subprocess
from enum import Enum
from typing import Any
from pathlib import Path
from dataclasses import dataclass

from jsonschema import Draft202012Validator


class RegistrySource(Enum):
    LOCAL = "local"
    REMOTE = "remote"


PRIMARY_LANGUAGES = {"python", "node", "bash", "multi", "other"}

IDE_DIR_MAP = {
    "default": ".agents/skills",
    "claude": ".claude/skills",
    "gemini": ".gemini/skills",
}


def get_ide_dir(ide_choice: str | None) -> str:
    """Get the skills directory path for the selected IDE.

    Args:
        ide_choice: IDE choice string (None, "w", "c", "a", "claude", "gemini")

    Returns:
        The directory path for the selected IDE

    """
    if not ide_choice or ide_choice.lower() == "w":
        return IDE_DIR_MAP["default"]
    if ide_choice.lower() == "c":
        return IDE_DIR_MAP["claude"]
    if ide_choice.lower() == "a":
        return IDE_DIR_MAP["gemini"]
    return IDE_DIR_MAP.get(ide_choice, IDE_DIR_MAP["default"])


class CliError(RuntimeError):
    """Raised for expected, user-facing CLI errors."""


@dataclass(frozen=True)
class RegistryContext:
    registry_path: Path | None
    schema_path: Path | None
    tag_vocab_path: Path | None
    project_root: Path
    source: RegistrySource


def resolve_paths(
    registry: str | None,
    project_root: Path | None = None,
    use_remote: bool = True,
) -> RegistryContext:
    root = (project_root or Path.cwd()).resolve()

    if registry:
        registry_path = Path(registry).resolve()
        schema_path = registry_path.parent / "registry.schema.json"
        tag_vocab_path = registry_path.parent / "tags.vocab.json"
        return RegistryContext(
            registry_path=registry_path,
            schema_path=schema_path,
            tag_vocab_path=tag_vocab_path,
            project_root=root,
            source=RegistrySource.LOCAL,
        )

    if use_remote:
        return RegistryContext(
            registry_path=None,
            schema_path=None,
            tag_vocab_path=None,
            project_root=root,
            source=RegistrySource.REMOTE,
        )

    registry_path = root / "registry.json"
    schema_path = registry_path.parent / "registry.schema.json"
    tag_vocab_path = registry_path.parent / "tags.vocab.json"
    return RegistryContext(
        registry_path=registry_path,
        schema_path=schema_path,
        tag_vocab_path=tag_vocab_path,
        project_root=root,
        source=RegistrySource.LOCAL,
    )


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CliError(f"Missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise CliError(f"Invalid JSON in {path}: {exc}") from exc


def load_registry(ctx: RegistryContext) -> dict[str, Any]:
    if ctx.source == RegistrySource.REMOTE:
        from . import http_client  # noqa: PLC0415

        registry = http_client.fetch_registry()
        schema = http_client.fetch_schema()
        tag_vocabulary = http_client.fetch_tags_vocab()
    else:
        registry = load_json(ctx.registry_path)
        schema = load_json(ctx.schema_path)
        tag_vocabulary = load_json(ctx.tag_vocab_path)

    if not isinstance(registry, dict):
        path_str = str(ctx.registry_path) if ctx.registry_path else "remote"
        raise CliError(f"registry.json must be a JSON object: {path_str}")
    if not isinstance(schema, dict):
        path_str = str(ctx.schema_path) if ctx.schema_path else "remote"
        raise CliError(f"registry.schema.json must be a JSON object: {path_str}")
    if not isinstance(tag_vocabulary, list) or not all(
        isinstance(tag, str) for tag in tag_vocabulary
    ):
        path_str = str(ctx.tag_vocab_path) if ctx.tag_vocab_path else "remote"
        raise CliError(f"tags.vocab.json must be a JSON array of strings: {path_str}")

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(registry), key=lambda e: list(e.path))
    if errors:
        formatted = "; ".join(
            f"{'/'.join(str(p) for p in err.path) or '<root>'}: {err.message}"
            for err in errors[:5]
        )
        raise CliError(f"registry.json failed schema validation: {formatted}")

    _validate_language_and_tags(registry, set(tag_vocabulary))
    return registry


def _validate_language_and_tags(
    registry: dict[str, Any], allowed_tags: set[str]
) -> None:
    if not allowed_tags:
        raise CliError("tags.vocab.json must define at least one tag")

    for skill in registry.get("skills", []):
        lang = skill.get("primary_language")
        if lang not in PRIMARY_LANGUAGES:
            raise CliError(
                f"Skill '{skill.get('id')}' has invalid primary_language '{lang}'. "
                f"Allowed: {', '.join(sorted(PRIMARY_LANGUAGES))}"
            )

        tags = skill.get("tags", [])
        unknown = [tag for tag in tags if tag not in allowed_tags]
        if unknown:
            raise CliError(
                f"Skill '{skill.get('id')}' has tags outside tag_vocabulary: {', '.join(unknown)}"
            )


def ensure_git_installed() -> None:
    if shutil.which("git") is None:
        raise CliError("git is required. Install git and retry.")


def run_git(args: list[str], project_root: Path, dry_run: bool = False) -> str:
    cmd = ["git", *args]
    if dry_run:
        return "$ " + " ".join(cmd)

    proc = subprocess.run(
        cmd,
        cwd=str(project_root),
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        stderr = proc.stderr.strip() or proc.stdout.strip() or "unknown git error"
        raise CliError(f"git command failed ({' '.join(cmd)}): {stderr}")
    return proc.stdout.strip()


def ensure_submodule(
    repo_url: str, submodule_path: Path, ref: str, project_root: Path, dry_run: bool
) -> list[str]:
    actions: list[str] = []
    rel_path = str(submodule_path)

    full_path = project_root / submodule_path

    # Check if submodule is already tracked
    submodule_exists = full_path.exists() and (
        (full_path / ".git").exists() or any(full_path.iterdir())
    )

    if not submodule_exists:
        actions.append(
            run_git(
                ["submodule", "add", "-f", "-b", ref, repo_url, rel_path],
                project_root,
                dry_run=dry_run,
            )
        )

    # Only update if submodule was added or already exists
    if submodule_exists or actions:
        actions.append(
            run_git(
                ["submodule", "update", "--init", "--remote", rel_path],
                project_root,
                dry_run=dry_run,
            )
        )
    return [a for a in actions if a]


def fetch_skill_directory(
    repo_url: str,
    source_path: str,
    target_path: Path,
    ref: str,
    project_root: Path,
    dry_run: bool,
) -> list[str]:
    """Fetch a skill directory from GitHub using API.

    Args:
        repo_url: GitHub repository URL (e.g., https://github.com/owner/repo)
        source_path: Path in the repo (e.g., skills/generic/create-agents-files)
        target_path: Local target directory relative to project_root
        ref: Git ref (branch, tag, commit)
        project_root: Project root directory
        dry_run: If True, only print actions without executing

    Returns:
        List of installed file paths

    """
    from .http_client import fetch_file_content, fetch_directory_tree  # noqa: PLC0415

    # Parse owner/repo from URL
    # URL format: https://github.com/owner/repo or git@github.com:owner/repo
    if "github.com" in repo_url:
        if repo_url.startswith("git@"):
            # SSH format: git@github.com:owner/repo.git
            parts = repo_url.rsplit(":", maxsplit=1)[-1].replace(".git", "").split("/")
        else:
            # HTTPS format: https://github.com/owner/repo
            parts = repo_url.rstrip("/").split("/")[-2:]
        owner, repo = parts[0], parts[1]
    else:
        raise CliError(f"Unsupported repo URL: {repo_url}")

    # Get list of all files in the directory tree
    files = fetch_directory_tree(owner, repo, source_path, ref)

    if not files:
        raise CliError(f"No files found in {source_path}")

    # Calculate base path for stripping source_path prefix
    base_path = source_path.rstrip("/")

    # Create target directory
    full_target = project_root / target_path

    if dry_run:
        actions = [f"Would fetch {len(files)} files to {full_target}"]
        return actions

    # Create target directory
    full_target.mkdir(parents=True, exist_ok=True)

    installed: list[str] = []
    for file_info in files:
        # Calculate relative path within the skill directory
        rel_path = file_info["path"]
        if rel_path.startswith(base_path + "/"):
            rel_path = rel_path[len(base_path) + 1 :]

        # Local file path
        local_file = full_target / rel_path

        # Create parent directories
        local_file.parent.mkdir(parents=True, exist_ok=True)

        # Download and write file
        content = fetch_file_content(file_info["download_url"])
        local_file.write_bytes(content)
        installed.append(str(local_file))

    return installed


def materialize_skill(
    *,
    source_file: Path,
    target_file: Path,
    link_mode: str,
    project_root: Path,
    dry_run: bool,
) -> str:
    src = project_root / source_file
    dst = project_root / target_file

    if dry_run:
        if not src.exists():
            return f"Would create {dst.parent} (source missing: {src})"
        return f"Would materialize {src} -> {dst} ({link_mode})"

    if not src.exists():
        raise CliError(f"Skill source does not exist: {src}")

    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() or dst.is_symlink():
        if dst.is_dir() and not dst.is_symlink():
            shutil.rmtree(dst)
        else:
            dst.unlink()

    if link_mode == "symlink":
        dst.symlink_to(src)
    elif link_mode == "copy":
        shutil.copy2(src, dst)
    else:
        raise CliError(f"Unsupported link_mode: {link_mode}")

    return f"Installed {target_file}"


def get_skill(registry: dict[str, Any], skill_id: str) -> dict[str, Any]:
    # Try exact ID match first
    for skill in registry.get("skills", []):
        if skill.get("id") == skill_id:
            return skill

    # Try short name match (last part after slash)
    for skill in registry.get("skills", []):
        if skill.get("id").split("/")[-1] == skill_id:
            return skill

    raise CliError(f"Unknown skill id or short name: {skill_id}")


def filter_skills(
    registry: dict[str, Any], queries: list[str], tags: list[str]
) -> list[dict[str, Any]]:
    skills = registry.get("skills", [])
    if tags:
        skills = [s for s in skills if set(tags).issubset(set(s.get("tags", [])))]

    for query in queries:
        q = query.lower()
        skills = [
            s
            for s in skills
            if q in s.get("id", "").lower()
            or q in s.get("name", "").lower()
            or q in s.get("category", "").lower()
            or q in s.get("description", "").lower()
            or q in s.get("primary_language", "").lower()
            or any(q in t.lower() for t in s.get("tags", []))
        ]

    return skills
