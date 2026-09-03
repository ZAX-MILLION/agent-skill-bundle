# Registry

This directory is the trust layer for Agent Skill Bundle.

## Rules

1. Canonical author repositories are the source of truth for mirrored third-party skills.
2. A downstream mirror with identical content does not replace the original author as the attribution source.
3. Upstream skill contents must not be silently modified in this bundle.
4. Original authorship, repository links, licenses and notices must be preserved.
5. Upstream changes may be prepared on review branches, but automatic upstream-to-`main` merge is forbidden.
6. Host-specific compatibility belongs in `adapters/`, not inside upstream copies.
7. Local/custom material is explicitly marked `local`.
8. Legacy/derived material is not called `EXACT` unless an exact original directory can be proven.

## Files

- `sources.json` — source registry, source roles, sync eligibility and attribution priority.
- `mappings.json` — canonical local-path → upstream-path conventions and explicit overrides.
- `upstream-state.json` — snapshot of checked upstream repository revisions.
- `skills.json` — last written per-directory Git-tree audit snapshot.

## Source roles

- `skill_upstream` — canonical source for exact skill syncing.
- `collection_upstream` — canonical source for a non-skill collection.
- `reference_spec` / `reference_docs` — authoritative reference material, but not an exact skill mirror.
- `related_upstream` — related current project where legacy exact provenance no longer exists.
- `local` — maintained by this bundle.

## Auditing

```bash
python3 scripts/check_upstreams.py
python3 scripts/audit_skills.py
python3 scripts/discover_provenance.py
```

`audit_skills.py --write` refreshes metadata only. It never changes a bundled skill.

## Syncing

Preview an exact canonical source:

```bash
python3 scripts/sync_reviewed.py process/writing-skills
```

Prepare a review branch only after provenance/source selection is reviewed:

```bash
python3 scripts/sync_reviewed.py process/writing-skills --apply --reviewed --commit
```

For recurring server-side checks, `scripts/prepare_updates.py` selects only known `UPDATE_AVAILABLE` entries and prepares a separate review branch. It never merges to `main`.

Git tree SHAs cover the complete tracked directory, not only `SKILL.md`.
