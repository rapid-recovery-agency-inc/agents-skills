# skill-creator (vendored)

This directory is a vendored copy of Anthropic's `skill-creator` skill.

## Provenance

- **Upstream repository:** [anthropics/skills](https://github.com/anthropics/skills)
- **Upstream path:** `skills/skill-creator/`
- **Local path:** `skills/generic/skill-creator/`
- **Sync method:** shallow clone + `rsync --delete`

## What is included

This local copy includes the full upstream directory tree:

- `SKILL.md`
- `LICENSE.txt`
- `agents/`
- `assets/`
- `eval-viewer/`
- `references/`
- `scripts/`

## Initial clone/sync workflow

Run from repository root (`/Users/anon/Developer/agents-skills`):

```bash
tmp_dir="$(mktemp -d)"
git clone --depth 1 https://github.com/anthropics/skills.git "$tmp_dir/anthropic-skills"
mkdir -p skills/generic/skill-creator
rsync -av --delete \
  "$tmp_dir/anthropic-skills/skills/skill-creator/" \
  "skills/generic/skill-creator/"
rm -rf "$tmp_dir"
```

## Update workflow

To refresh this vendored copy from upstream:

```bash
tmp_dir="$(mktemp -d)"
git clone --depth 1 https://github.com/anthropics/skills.git "$tmp_dir/anthropic-skills"
rsync -av --delete \
  "$tmp_dir/anthropic-skills/skills/skill-creator/" \
  "skills/generic/skill-creator/"
rm -rf "$tmp_dir"
```

Then review changes before commit:

```bash
git diff -- skills/generic/skill-creator
```

## Local staging flow for testing

Use the local `.agents` sandbox to test installs without modifying tracked skill directories.

Stage this skill into the sandbox:

```bash
just stage-skill skill=skill-creator
```

This copies:

- from: `skills/generic/skill-creator/`
- to: `.agents/staging/skill-creator/`

Notes:

- `.agents/**` is gitignored (except `.agents/.gitkeep`).
- Re-running the command uses `rsync --delete`, so the staged copy always mirrors source.
- Use staged contents for local experiments, then re-stage from source when you want a clean reset.

## Practical maintenance guidance

1. **Treat this directory as vendored upstream content.**
   - Prefer upstream syncs over ad-hoc edits.
1. **If local customization is required, document it in commit messages.**
   - Keep custom patches minimal and intentional.
1. **After every update, sanity-check key files:**
   - `SKILL.md` metadata and routing description
   - `scripts/` entrypoints used by your workflow
   - `references/` schema compatibility
1. **Run repository checks before commit:**

```bash
just lint
```

## Notes

- `rsync --delete` intentionally removes files no longer present upstream.
- If you need to preserve local-only files, keep them outside this vendored directory.
