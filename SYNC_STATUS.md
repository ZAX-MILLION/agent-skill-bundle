# Sync Status

Last registry review: **2026-09-03**

This file reports what the bundle can prove today. It deliberately separates update detection from reviewed integration.

| Capability | Status | Notes |
|---|---|---|
| Upstream source registry | ✅ Ready | Sources are recorded in `registry/sources.json`. |
| Upstream repository verification | ✅ Ready | Registered public repositories and default branches were verified. |
| Original credits preserved | ✅ Ready | See `CREDITS.md`; upstream attribution remains required. |
| Upstream revision checker | ✅ Ready | `scripts/check_upstreams.py` checks current upstream branch revisions. |
| Git-tree skill auditor | ✅ Ready | `scripts/audit_skills.py` compares mapped local/upstream directories. |
| Provenance discovery | ✅ Ready | `scripts/discover_provenance.py` finds exact candidates; name-only matches require review. |
| Convention mapping | ✅ Ready | `process/`, `wordpress/`, and `marketing/` have reviewed path conventions. |
| Reviewed whole-skill sync | ✅ Ready | `scripts/sync_reviewed.py` copies complete upstream directories on a review branch. |
| Automatic merge to `main` | 🚫 Disabled by policy | No sync tool pushes or merges automatically. |
| Generic AI compatibility guidance | ✅ Ready | See `adapters/generic/README.md`. |
| Host-specific adapters | 🟡 Incremental | Add only where a host actually needs one; avoid duplicating skill content. |

## Verified category: `process/`

Compared against `obra/superpowers` at upstream commit:

`b36e0829c6d0140e93cfef2ca599b1b07d4a7797`

Current directory-tree status:

- **12 EXACT** — local directory matches the tracked upstream tree.
- **2 UPDATE_AVAILABLE** — `subagent-driven-development` and `writing-skills`.

Five previously stale skills were refreshed from upstream and then verified by complete directory-tree SHA:

- `brainstorming`
- `finishing-a-development-branch`
- `requesting-code-review`
- `using-superpowers`
- `writing-plans`

Exact per-skill results are stored in `registry/skills.json`.

## Provenance coverage

| Category | Status |
|---|---|
| `process/` | ✅ Exact source paths / convention mapped; audited |
| `wordpress/` | ✅ Source-path convention mapped; full audit/update review pending |
| `marketing/` | ✅ Source-path convention mapped; full audit/update review pending |
| `qa/` | ✅ Local/custom |
| `design/` | 🟡 Mixed upstream sources — exact discovery pending |
| `security/` | 🟡 Local + upstream mix — exact discovery pending |
| `multiplayer/` | 🟡 Source relationship requires explicit verification |

## Safe sync workflow

Dry-run provenance preview:

```bash
python3 scripts/sync_reviewed.py process/writing-skills
```

Reviewed local sync:

```bash
python3 scripts/sync_reviewed.py process/writing-skills --apply --reviewed --commit
```

The command creates an `upstream-sync/...` branch and never pushes or merges it. Review the resulting diff, licenses/notices, executable scripts, network behavior, and prompt instructions before integration.

## Update states

- `EXACT` — local copy matches the tracked upstream directory tree at the checked revision.
- `UPDATE_AVAILABLE` — upstream directory tree differs from the local copy.
- `MODIFIED` — local third-party skill is known to contain bundle-side changes.
- `DIFFERS_FROM_UPSTREAM` — a difference exists but provenance history is insufficient to classify it further.
- `LICENSE_CHANGED` — upstream licensing changed and requires review.
- `UPSTREAM_REMOVED` — the tracked source path no longer exists upstream.
- `QUARANTINED` — update requires security/manual inspection before use.

No state should be marked `EXACT` unless the source repository, source path, checked upstream revision and directory-tree comparison are known.
