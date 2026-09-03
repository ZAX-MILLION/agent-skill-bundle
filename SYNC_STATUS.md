# Sync Status

Last registry review: **2026-09-03**

This file reports what the bundle can prove and deliberately separates provenance, update detection, review-branch preparation, and integration.

| Capability | Status | Notes |
|---|---|---|
| Canonical source registry | ✅ Ready | Source roles/priorities are in `registry/sources.json`. |
| Canonical path mappings | ✅ Ready | Conventions and explicit overrides are in `registry/mappings.json`. |
| Credits / canonical attribution | ✅ Ready | Mirrors do not replace original authors. See `CREDITS.md`. |
| Upstream revision checker | ✅ Ready | `scripts/check_upstreams.py`. |
| Git-tree auditor | ✅ Ready | `scripts/audit_skills.py`; metadata-only `--write`. |
| Canonical provenance discovery | ✅ Ready | `scripts/discover_provenance.py`; reference/mirror repos cannot steal attribution. |
| Reviewed exact skill sync | ✅ Ready | `scripts/sync_reviewed.py`; whole directory, review branch, no merge. |
| Known-update branch preparer | ✅ Ready | `scripts/prepare_updates.py`; selects only `UPDATE_AVAILABLE`. |
| Server-local scheduled checks | ✅ Ready | systemd units under `ops/`; no GitHub Actions required. |
| Automatic upstream → `main` merge | 🚫 Forbidden | Review/integration stays explicit. |
| ChatGPT / Codex adapters | ✅ Ready | Portable Agent Skills guidance. |
| Cursor / Claude Code adapters | ✅ Ready | File-based installation guidance. |
| Generic AI adapter | ✅ Ready | Capability-aware fallback. |
| `main` branch protection | ⚠️ External setting | Must be enabled in GitHub repository settings/rulesets. |

## Verified `process/`

Canonical upstream: `obra/superpowers`

Checked revision:

`b36e0829c6d0140e93cfef2ca599b1b07d4a7797`

**14 / 14 process skill directory trees are EXACT.**

The complete snapshot is in `registry/skills.json`.

## Provenance coverage

| Category | Classification |
|---|---|
| `process/` | ✅ Canonical mapped + 14/14 verified exact |
| `wordpress/` | ✅ Canonical same-name mapping to `WordPress/agent-skills/skills/<name>` |
| `marketing/` | ✅ Canonical same-name mapping to `coreyhaines31/marketingskills/skills/<name>` |
| `design/` | ✅ Canonical mapping model established: Anthropic, daymade, Hermes/NousResearch + VoltAgent collection; Google design.md correctly tracked as a reference spec |
| `security/` | ✅ Local/custom — not falsely attributed to WordPress or another upstream |
| `qa/` | ✅ Local/custom |
| `multiplayer/` | ⚠️ Legacy Rivet-derived — tracked against current Rivet docs/examples, intentionally excluded from exact automatic syncing until an exact historical skill source can be proven |

## Baseline vs update

A newly mapped directory that differs from current upstream may initially be `DIFFERS_FROM_UPSTREAM`. That is **not** auto-selected for replacement. A maintainer reviews the baseline first.

After a known baseline exists, a later upstream tree change becomes `UPDATE_AVAILABLE`, which may be prepared automatically on a review branch.

## Safe update workflow

```bash
python3 scripts/check_upstreams.py
python3 scripts/audit_skills.py
python3 scripts/prepare_updates.py
```

Prepare known updates locally:

```bash
python3 scripts/prepare_updates.py --apply
```

Optionally publish the review branch:

```bash
python3 scripts/prepare_updates.py --apply --push
```

Neither command merges to `main`.

## States

- `EXACT` — local directory tree equals the canonical upstream tree at the checked revision.
- `UPDATE_AVAILABLE` — a previously baselined canonical upstream tree changed.
- `MODIFIED` — local mirrored third-party content changed after the recorded baseline.
- `DIFFERS_FROM_UPSTREAM` — a difference exists but history is insufficient to safely call it an upstream update.
- `UPSTREAM_REMOVED` — canonical mapped path disappeared.
- `LICENSE_CHANGED` — license review is required before integration.
- `QUARANTINED` — security/manual review required.

No item is marked `EXACT` without a known canonical source, path, revision, and directory-tree comparison.
