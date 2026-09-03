# Sync Status

Last registry review: **2026-09-03**

This file reports what the bundle can prove today. It deliberately avoids claiming automatic synchronization before provenance is complete.

| Capability | Status | Notes |
|---|---|---|
| Upstream source registry | ✅ Ready | Sources are recorded in `registry/sources.json`. |
| Upstream repository verification | ✅ Ready | Registered public repositories and default branches were verified. |
| Original credits preserved | ✅ Ready | See `CREDITS.md`; existing per-skill license files remain untouched. |
| Existing skill directories modified | ✅ No | This trust-layer update does not rewrite bundled skills. |
| Upstream revision checker | ✅ Ready | `scripts/check_upstreams.py` checks current upstream branch revisions. |
| Per-skill provenance registry | 🟡 Partial | `process/` is mapped; remaining third-party categories still need exact paths. |
| Automatic upstream copy/update | ⏸ Disabled | Intentionally disabled until provenance and license checks are complete for each skill. |
| Automatic merge to `main` | 🚫 Disabled by policy | Upstream changes must be reviewed. |
| Generic AI compatibility guidance | ✅ Ready | See `adapters/generic/README.md`. |
| Host-specific adapters | 🟡 Incremental | Add only where a host actually needs one; avoid duplicating skill content. |

## Verified category: `process/`

Compared against `obra/superpowers` at upstream commit:

`b36e0829c6d0140e93cfef2ca599b1b07d4a7797`

Directory-tree comparison currently shows:

- **7 EXACT** — local skill directory matches the current tracked upstream tree.
- **7 UPDATE_AVAILABLE** — upstream skill directory has changed.

Exact per-skill results are stored in `registry/skills.json`.

No upstream skill was replaced during this audit. Updates remain review-first.

## Provenance coverage

| Category | Status |
|---|---|
| `process/` | ✅ Exact source paths mapped |
| `qa/` | ✅ Local/custom |
| `design/` | 🟡 Mapping pending (multiple upstream sources) |
| `security/` | 🟡 Mapping pending (local + upstream mix) |
| `multiplayer/` | 🟡 Mapping pending / source relationship requires verification |
| `wordpress/` | 🟡 Mapping pending |
| `marketing/` | 🟡 Mapping pending |

## Update states

- `EXACT` — local copy matches the tracked upstream directory tree at the checked revision.
- `UPDATE_AVAILABLE` — upstream directory tree differs from the local copy.
- `MODIFIED` — local third-party skill is known to contain bundle-side changes.
- `LICENSE_CHANGED` — upstream licensing changed and requires review.
- `UPSTREAM_REMOVED` — the tracked source path no longer exists upstream.
- `QUARANTINED` — update requires security/manual inspection before use.

No state should be marked `EXACT` unless the source repository, source path, checked upstream revision and tree comparison are known.
