from __future__ import annotations

import json
from pathlib import Path

import typer

from . import __version__
from .core import (
    CliError,
    get_skill,
    get_ide_dir,
    filter_skills,
    load_registry,
    resolve_paths,
    ensure_git_installed,
    fetch_skill_directory,
)


app = typer.Typer(
    add_completion=True,
    no_args_is_help=True,
    rich_markup_mode="rich",
    help="Install and update agent skills from registry.json",
)


@app.callback()
def main_callback(
    version: bool = typer.Option(False, "--version", "-v", help="Show version"),
    remote: bool = typer.Option(
        True, "--remote/--local", help="Use remote registry or local"
    ),
) -> None:
    if version:
        typer.echo(f"agents-skills {__version__}")
        raise typer.Exit()


def _print_json(payload: object) -> None:
    typer.echo(json.dumps(payload, indent=2, sort_keys=True))


def _target_submodule(target_root: str | None, configured_submodule_path: str) -> Path:
    if target_root:
        return Path(target_root) / "skills"
    return Path(configured_submodule_path)


def _target_skill_file(
    target_root: str | None, target_path: str, entrypoint: str
) -> Path:
    root = Path(target_root) if target_root else Path(".agents")
    return root / "skills" / target_path / entrypoint


@app.command("list")
def list_skills(
    query: list[str] | None = typer.Argument(None, help="Search terms (repeatable)"),
    registry: str | None = typer.Option(
        None, "--registry", help="Path to registry.json"
    ),
    tag: list[str] | None = typer.Option(
        None, "--tag", help="Filter by tag (repeatable)"
    ),
    as_json: bool = typer.Option(False, "--json", help="Output JSON"),
    remote: bool = typer.Option(True, "--remote/--local"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show full details"),
) -> None:
    """List skills from the registry."""
    try:
        ctx = resolve_paths(registry=registry, use_remote=remote)
        data = load_registry(ctx)
        skills = filter_skills(data, queries=query or [], tags=tag or [])

        if as_json:
            _print_json({"count": len(skills), "skills": skills})
            return

        if not skills:
            typer.echo("No matching skills found.")
            return

        if verbose:
            for skill in sorted(skills, key=lambda s: s["id"]):
                skill_name = skill["id"].split("/")[-1]
                tags = skill.get("tags", [])
                tag_str = " " + " ".join(f"[{tag}]" for tag in tags) if tags else ""
                typer.echo(typer.style(skill_name, fg=typer.colors.BLUE) + tag_str)
                typer.echo(f"  {skill['description']}")
                typer.echo()
        else:
            for skill in sorted(skills, key=lambda s: s["id"]):
                skill_name = skill["id"].split("/")[-1]
                typer.echo(skill_name)
    except CliError as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from None


def _add_impl(
    *,
    skill_id: str,
    registry: str | None,
    target_root: str | None,
    dry_run: bool,
    as_json: bool,
    use_remote: bool = True,
    skip_confirm: bool = False,
    ide_choice: str | None = None,
) -> None:
    ensure_git_installed()
    ctx = resolve_paths(registry=registry, use_remote=use_remote)
    data = load_registry(ctx)

    source = data["source"]

    if skill_id == "all":
        skills = data["skills"]
    else:
        skills = [get_skill(data, skill_id)]

    ide_dir = get_ide_dir(ide_choice)

    # Build list of target paths for confirmation
    target_paths: list[str] = []
    for skill in skills:
        target_path = Path(ide_dir) / skill["install"]["target_path"]
        target_paths.append(str(ctx.project_root / target_path))

    # Show confirmation prompt if not skipped
    if not skip_confirm and not dry_run:
        typer.echo(
            "Are you installing skills for use with Claude, Antigravity/Gemini, or Cursor?"
        )
        typer.echo("1. Copilot/Windsurf/Codex -> .agents/skills/<skill> /")
        typer.echo("2. Claude                 -> .claude/skills/<skill> /")
        typer.echo("3. Antigravity/Gemini     -> .gemini/skills/<skill> /")
        typer.echo("4. Cursor                 -> .cursor/skills/<skill> /")
        typer.echo()
        selected = typer.prompt("Choice", type=str, default=ide_choice or "1")
        ide_dir = get_ide_dir(selected)

        # Rebuild target paths with new ide_dir
        target_paths = []
        for skill in skills:
            target_path = Path(ide_dir) / skill["install"]["target_path"]
            target_paths.append(str(ctx.project_root / target_path))

        typer.echo()
        typer.echo("Skill(s) will be installed to:")
        for path in target_paths:
            typer.echo(f"  {path}")
        typer.echo()
        confirm = typer.prompt("Continue? (y/n)", type=str, default="y")
        if confirm.lower() not in ("y", "yes"):
            typer.echo("Aborted.")
            raise typer.Exit(code=0)

    # Fetch each skill directory from GitHub
    installed: list[str] = []
    for skill in skills:
        target_path = Path(ide_dir) / skill["install"]["target_path"]
        installed.extend(
            fetch_skill_directory(
                repo_url=source["repo"],
                source_path=skill["source_path"],
                target_path=target_path,
                ref=source["default_ref"],
                project_root=ctx.project_root,
                dry_run=dry_run,
            )
        )

    if as_json:
        _print_json(
            {
                "actions": [],
                "results": installed,
                "dry_run": dry_run,
            }
        )
        return

    for line in installed:
        typer.echo(line)


@app.command("add")
def add_skill(
    skill_id: str = typer.Argument(help="Skill id from registry, or 'all'"),
    registry: str | None = typer.Option(
        None, "--registry", help="Path to registry.json"
    ),
    target_root: str | None = typer.Option(
        None, "--target-root", help="Override destination root"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Print actions without writing"
    ),
    as_json: bool = typer.Option(False, "--json", help="Output JSON"),
    remote: bool = typer.Option(True, "--remote/--local"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation"),
    ide: str | None = typer.Option(
        None,
        "--ide",
        help="IDE choice: 1 (default), 2 (claude), 3 (gemini), 4 (cursor)",
    ),
) -> None:
    """Add or update one skill (or all)."""
    try:
        _add_impl(
            skill_id=skill_id,
            registry=registry,
            target_root=target_root,
            dry_run=dry_run,
            as_json=as_json,
            use_remote=remote,
            skip_confirm=yes,
            ide_choice=ide,
        )
    except CliError as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from None


@app.command("install", hidden=True)
def install_alias(
    skill_id: str = typer.Argument(help="Skill id from registry, or 'all'"),
    registry: str | None = typer.Option(None, "--registry"),
    target_root: str | None = typer.Option(None, "--target-root"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    as_json: bool = typer.Option(False, "--json"),
    remote: bool = typer.Option(True, "--remote/--local"),
    yes: bool = typer.Option(False, "--yes", "-y"),
    ide: str | None = typer.Option(None, "--ide"),
) -> None:
    """Alias for add."""
    add_skill(
        skill_id=skill_id,
        registry=registry,
        target_root=target_root,
        dry_run=dry_run,
        as_json=as_json,
        remote=remote,
        yes=yes,
        ide=ide,
    )


@app.command("sync", hidden=True)
def sync_alias(
    registry: str | None = typer.Option(None, "--registry"),
    target_root: str | None = typer.Option(None, "--target-root"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    as_json: bool = typer.Option(False, "--json"),
    remote: bool = typer.Option(True, "--remote/--local"),
    yes: bool = typer.Option(False, "--yes", "-y"),
    ide: str | None = typer.Option(None, "--ide"),
) -> None:
    """Alias for add all."""
    add_skill(
        skill_id="all",
        registry=registry,
        target_root=target_root,
        dry_run=dry_run,
        as_json=as_json,
        remote=remote,
        yes=yes,
        ide=ide,
    )


@app.command("update", hidden=True)
def update_alias(
    registry: str | None = typer.Option(None, "--registry"),
    target_root: str | None = typer.Option(None, "--target-root"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    as_json: bool = typer.Option(False, "--json"),
    remote: bool = typer.Option(True, "--remote/--local"),
    yes: bool = typer.Option(False, "--yes", "-y"),
    ide: str | None = typer.Option(None, "--ide"),
) -> None:
    """Alias for sync."""
    sync_alias(
        registry=registry,
        target_root=target_root,
        dry_run=dry_run,
        as_json=as_json,
        remote=remote,
        yes=yes,
        ide=ide,
    )


def main() -> None:
    app()


if __name__ == "__main__":
    main()
