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
| Per-skill source path mapping | 🟡 In progress | Required before exact automatic skill syncing is enabled. |
| Exact per-skill commit provenance | 🟡 In progress | Will be stored separately from upstream skill contents. |
| Automatic upstream copy/update | ⏸ Disabled | Intentionally disabled until per-skill provenance and license checks are complete. |
| Automatic merge to `main` | 🚫 Disabled by policy | Upstream changes must be reviewed. |
| Generic AI compatibility guidance | ✅ Ready | See `adapters/generic/README.md`. |
| Host-specific adapters | 🟡 Incremental | Add only where a host actually needs one; avoid duplicating skill content. |

## Update states

Future per-skill tracking should use explicit states rather than a vague "synced" label:

- `EXACT` — local copy matches the reviewed upstream revision.
- `UPDATE_AVAILABLE` — upstream changed after the reviewed revision.
- `MODIFIED` — local third-party skill differs from the tracked upstream copy.
- `LICENSE_CHANGED` — upstream licensing changed and requires review.
- `UPSTREAM_REMOVED` — the tracked source path no longer exists upstream.
- `QUARANTINED` — update requires security/manual inspection before use.

No state should be marked `EXACT` unless the source repository, source path and upstream commit are known.
