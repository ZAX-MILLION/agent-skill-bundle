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
- `upstream-state.json` — verified snapshot of upstream branch revisions at the last recorded check.
- `skills.json` — per-skill provenance/status for categories that have been mapped. `process/` is the first fully mapped upstream category.

## Provenance fields

A mapped upstream skill records:

- local path;
- source ID/repository;
- exact upstream source path;
- checked upstream commit SHA;
- local directory Git tree SHA;
- upstream directory Git tree SHA;
- explicit state (`EXACT`, `UPDATE_AVAILABLE`, etc.).

Git tree SHAs are used so the comparison covers the complete tracked directory, not only `SKILL.md`.

## Auditing

Check source branch revisions:

```bash
python3 scripts/check_upstreams.py
```

Audit mapped skills against their current upstream Git trees:

```bash
python3 scripts/audit_skills.py
```

Use `--write` only when you intentionally want to refresh registry metadata. Neither checker modifies skill directories.

## Sync gate

Automatic copying must not be enabled for a skill until its exact source path and provenance are mapped. A changed upstream tree is a review signal, not permission to overwrite local files.

The registry is intentionally separate from skill content so compatibility/provenance metadata never changes upstream-authored files.
