from __future__ import annotations

import json
from pathlib import Path

import typer

from . import __version__
from .core import (
    CliError,
    get_skill,
    filter_skills,
    load_registry,
    resolve_paths,
    ensure_submodule,
    materialize_skill,
    ensure_git_installed,
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
    remote: bool = typer.Option(True, "--remote/--local", help="Use remote registry or local"),
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
    registry: str | None = typer.Option(None, "--registry", help="Path to registry.json"),
    tag: list[str] | None = typer.Option(None, "--tag", help="Filter by tag (repeatable)"),
    as_json: bool = typer.Option(False, "--json", help="Output JSON"),
    remote: bool = typer.Option(True, "--remote/--local"),
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

        for skill in skills:
            tags = ", ".join(skill.get("tags", []))
            typer.echo(
                f"{skill['id']} [{skill['primary_language']}] - {skill['description']}"
            )
            typer.echo(f"  category={skill['category']} tags={tags}")
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
) -> None:
    ensure_git_installed()
    ctx = resolve_paths(registry=registry, use_remote=use_remote)
    data = load_registry(ctx)

    source = data["source"]
    submodule_path = _target_submodule(target_root, source["submodule_path"])
    actions = ensure_submodule(
        repo_url=source["repo"],
        submodule_path=submodule_path,
        ref=source["default_ref"],
        project_root=ctx.project_root,
        dry_run=dry_run,
    )

    if skill_id == "all":
        skills = data["skills"]
    else:
        skills = [get_skill(data, skill_id)]

    installed: list[str] = []
    for skill in skills:
        source_file = submodule_path / skill["source_path"] / skill["entrypoint"]
        target_file = _target_skill_file(
            target_root, skill["install"]["target_path"], skill["entrypoint"]
        )
        installed.append(
            materialize_skill(
                source_file=source_file,
                target_file=target_file,
                link_mode=skill["install"]["link_mode"],
                project_root=ctx.project_root,
                dry_run=dry_run,
            )
        )

    if as_json:
        _print_json(
            {
                "actions": [a for a in actions if a],
                "results": installed,
                "dry_run": dry_run,
            }
        )
        return

    for action in actions:
        if action:
            typer.echo(action)
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
) -> None:
    """Alias for add."""
    add_skill(
        skill_id=skill_id,
        registry=registry,
        target_root=target_root,
        dry_run=dry_run,
        as_json=as_json,
        remote=remote,
    )


@app.command("sync", hidden=True)
def sync_alias(
    registry: str | None = typer.Option(None, "--registry"),
    target_root: str | None = typer.Option(None, "--target-root"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    as_json: bool = typer.Option(False, "--json"),
    remote: bool = typer.Option(True, "--remote/--local"),
) -> None:
    """Alias for add all."""
    add_skill(
        skill_id="all",
        registry=registry,
        target_root=target_root,
        dry_run=dry_run,
        as_json=as_json,
        remote=remote,
    )


@app.command("update", hidden=True)
def update_alias(
    registry: str | None = typer.Option(None, "--registry"),
    target_root: str | None = typer.Option(None, "--target-root"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    as_json: bool = typer.Option(False, "--json"),
    remote: bool = typer.Option(True, "--remote/--local"),
) -> None:
    """Alias for sync."""
    sync_alias(
        registry=registry, target_root=target_root, dry_run=dry_run, as_json=as_json, remote=remote
    )


def main() -> None:
    app()


if __name__ == "__main__":
    main()
