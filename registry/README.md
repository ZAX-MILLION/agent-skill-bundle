# Registry

This directory is the trust layer for Agent Skill Bundle.

## Rules

1. Upstream repositories are the source of truth for third-party skills.
2. Upstream skill contents must not be silently modified in this bundle.
3. Original authorship, repository links, license files, notices, and credits must be preserved.
4. Upstream updates are reviewed before merge. Automatic upstream-to-main merges are not allowed.
5. If an upstream skill needs host-specific compatibility, add an adapter outside the skill directory instead of patching the skill.
6. Custom skills owned by this repository are explicitly marked as `local`.

## Files

- `sources.json` — canonical list of upstream collections and bundle policy.
- `upstream-state.json` — generated snapshot of checked upstream revisions. It may be absent until the checker is run with `--write`.
- Future `skills.json` — per-skill provenance mapping. Automatic sync must not be enabled for a skill until its exact upstream repository and path are recorded.

## Provenance target

Every upstream-backed skill should ultimately have these fields recorded:

- local path
- source repository
- source path
- upstream commit SHA
- license / notice location
- last reviewed sync revision

The source registry is intentionally separate from skill content so compatibility metadata never changes upstream-authored files.
