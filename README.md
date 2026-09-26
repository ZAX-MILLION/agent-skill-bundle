# Agent Skill Bundle

**A source-preserving distribution layer for portable AI Agent Skills.**

One repository for reusable `SKILL.md` workflows across ChatGPT, Codex, Cursor, Claude Code, and other Agent Skills-compatible/file-based AI systems — while keeping original authorship, licenses, source paths, and upstream history traceable.

> **Upstream authors keep the credit. Canonical upstream repositories remain the source of truth. Host compatibility stays outside original skills.**

## Why this exists

Useful AI skills are spread across many repositories. Copies become stale, attribution gets lost, and different AI hosts expose different tools. This bundle focuses on distribution rather than claiming ownership:

- complete skill directories, not stripped `SKILL.md` copies;
- canonical upstream source tracking;
- preserved licenses, notices, and credits;
- Git-tree provenance/auditing;
- review-first exact upstream syncing;
- safe handling of local, legacy-derived, reference, and collection content;
- thin host adapters instead of rewritten forks;
- server-side update monitoring without GitHub Actions.

## Trust model

| Rule | Policy |
|---|---|
| Canonical third-party source | Original author/project repository |
| Silent edits to mirrored upstream skills | **Not allowed** |
| Original licenses / notices / credits | **Preserved** |
| Mirror beats original author for attribution | **Never** |
| Upstream change → review branch | Allowed |
| Upstream change → automatic `main` merge | **Forbidden** |
| Host-specific changes | `adapters/`, never upstream copies |
| Legacy-derived content | Clearly labeled; never falsely marked `EXACT` |

See [`registry/`](registry/README.md), [`CREDITS.md`](CREDITS.md), [`SECURITY.md`](SECURITY.md), and [`SYNC_STATUS.md`](SYNC_STATUS.md).

## Sources

| Area | Canonical relationship |
|---|---|
| `process/` | `obra/superpowers` — **14/14 verified EXACT** at the recorded audit revision |
| `wordpress/` | `WordPress/agent-skills` via `skills/<name>` mappings |
| `marketing/` | `coreyhaines31/marketingskills` via `skills/<name>` mappings |
| `design/` | Anthropic + daymade + Hermes/NousResearch; VoltAgent for the design-system collection; Google design.md is a reference spec, not falsely credited as the Hermes skill author |
| `security/` | Local/custom bundle skills |
| `qa/` | Local/custom bundle skills |
| `research/` | Original reference-only agent catalog and optional Agent Reach routing; no external runtime bundled |
| `productivity/` | [i-have-adhd](https://github.com/ayghri/i-have-adhd) by Ayoub Ghriss: action-first communication skill, MIT, original source retained |
| `coding/` | [Ponytail](https://github.com/DietrichGebert/ponytail) by Dietrich Gebert: six MIT-licensed coding skills, review-first |
| `multiplayer/` | Legacy Rivet-derived skills tracked against current Rivet docs/examples; not claimed as current exact `rivet-dev/skills` mirrors |

Canonical roles live in [`registry/sources.json`](registry/sources.json), and local/upstream path relationships live in [`registry/mappings.json`](registry/mappings.json).

## Public content safety

Run `python3 scripts/public_repo_gate.py .` before publishing. This checks current tracked content, not past Git history. See [Public Repository Policy](docs/PUBLIC_REPOSITORY_POLICY.md). External research repositories remain references, not automatically installed code.

## Primary Antigravity communication layer

The bundle includes [i-have-adhd](https://github.com/ayghri/i-have-adhd), pinned to a reviewed upstream revision. For a non-developer owner, the [Antigravity default response rule](adapters/antigravity/adhd-primary-rule.md) should be merged into the user's existing global rules **after installing the bundle**. The original portable skill can also be explicitly invoked as `/i-have-adhd`. A skill file alone does not guarantee persistent activation across new sessions: the global rule supplies that behavior. Do not install the separate upstream `agy` plugin in the same discovery scope without checking duplicates. Safety, correctness and complete technical work remain mandatory despite compact presentation.

## Seven additional portable skills

The bundle contains seven new task skills: `graphify` (code knowledge graph, external CLI required), `graft` (optional skill-vault manager), `awesome-design` (selective style router), `design-taste-frontend` (upstream Taste Skill), `image-to-code` (upstream visual implementation), `web-design-guidelines` (reviewed, pinned local Vercel rule snapshot), and `agent-skills` (portable skill discovery and review). See [source and license pins](registry/portable-expansion.json) and [multi-host setup](adapters/multi-host/README.md).

The original Taste Skill is named **`design-taste-frontend`** in its own frontmatter; retain that original name for consistent discovery. The `awesome-design` skill includes a selective catalog, not 67 bulk-installed style bodies. Neither Graphify nor Graft's executable is bundled. Source content and supporting files remain available for on-demand retrieval.

## Install

The `operations/` category adds 10 original, review-first shared-VPS and release management skills. The `coding/` category includes six Ponytail skills with untouched upstream skill text and the MIT license in every installed directory. See [Antigravity adapter](adapters/antigravity/README.md#ponytail-on-antigravity). See the [Antigravity adapter](adapters/antigravity/README.md) for native installation and permissions.


The installer copies **only directories containing `SKILL.md`**, along with all scripts, references, examples, templates, and assets. Non-skill collections are skipped.

### Claude Code

```bash
./install.sh ~/.claude/skills
```

### Cursor

```bash
./install.sh ~/.cursor/skills
```

### Generic/file-based host

```bash
./install.sh /path/to/skills
```

### Antigravity: two-skill on-demand mode (preferred)

```bash
./install.sh "$HOME/.gemini/config/skills" --flat --on-demand
```

This installs only `i-have-adhd` and `skill-retrieval-routing` natively, so this bundle contributes only two skill descriptions to startup discovery. The remaining 141 stay in the source checkout and can be searched by the separate local Skill Retrieval MCP. See [the two-stage Antigravity setup](adapters/antigravity/skill-retrieval-mcp.md). Merely running the two-skill installer **does not** install or connect the external MCP runtime.

If the full bundle is already installed natively, the command stops rather than misleadingly claiming minimal mode. After reviewing the existing installation, run the same command with `--prune-managed` to remove **only other marker-identified bundle copies**. It does not delete unmarked personal or third-party skills.

### Host requires skills directly under its skills root

```bash
./install.sh /path/to/skills --flat
```

Repeated installs replace only destinations previously marked as installed by this bundle. Use `--force` only after reviewing an existing unmarked destination.

### Optional local skill search

[Skill Retrieval MCP](https://github.com/JayCheng113/skill-retrieval-mcp) is a **separate, optional MCP service**. The original `skill-retrieval-routing` adapter can help Antigravity search this reviewed bundle by need and read one skill at a time. Its executable runtime, model, prebuilt 374-skill corpus, local SQLite database and MCP configuration are **not** included here. See [Antigravity setup](adapters/antigravity/skill-retrieval-mcp.md).

The `i-have-adhd` communication preference remains the primary output rule; retrieval changes how skills are found, not how the agent talks to the owner or what permissions it has.

## AI compatibility

- [`adapters/chatgpt/`](adapters/chatgpt/README.md)
- [`adapters/codex/`](adapters/codex/README.md)
- [`adapters/cursor/`](adapters/cursor/README.md)
- [`adapters/antigravity/`](adapters/antigravity/README.md)
- [`adapters/claude-code/`](adapters/claude-code/README.md)
- [`adapters/generic/`](adapters/generic/README.md)

See [portable setup for Antigravity, Codex and Claude Code](adapters/multi-host/README.md). The bundle targets the portable Agent Skills pattern (`SKILL.md` + optional scripts/references/assets). It does **not** pretend every host exposes the same browser, shell, subagent, GitHub, database, or filesystem capabilities.

## Audit provenance

```bash
python3 scripts/check_upstreams.py
python3 scripts/audit_skills.py
python3 scripts/discover_provenance.py
```

Refresh registry metadata intentionally with:

```bash
python3 scripts/check_upstreams.py --write
python3 scripts/audit_skills.py --write
```

Metadata writes never replace skill content.

## Review-first exact sync

Preview a canonical source:

```bash
python3 scripts/sync_reviewed.py process/writing-skills
```

Prepare and commit an exact upstream copy on a new local review branch:

```bash
python3 scripts/sync_reviewed.py process/writing-skills --apply --reviewed --commit
```

Nothing is pushed or merged by that command.

To detect known upstream updates and prepare a review branch automatically:

```bash
python3 scripts/prepare_updates.py
python3 scripts/prepare_updates.py --apply
```

`--push` may publish the review branch, but still never merges it.

## No GitHub Actions required

[`ops/`](ops/README.md) includes a hardened systemd service/timer for server-local daily checks. The default prepares local review branches; publishing them is explicit opt-in after repository credentials are configured outside the repo.

## Repository layout

```text
agent-skill-bundle/
├── design/ security/ process/ multiplayer/ wordpress/ marketing/ qa/ operations/ coding/ research/ productivity/
├── registry/          # source roles, mappings, revision/audit state
├── adapters/          # host-specific compatibility only
├── scripts/           # audit, provenance, sync, update preparation
├── ops/               # server-side timer/service guidance
├── CREDITS.md
├── SECURITY.md
├── SYNC_STATUS.md
├── CONTRIBUTING.md
└── install.sh
```

## Licensing and attribution

This repository does **not** claim authorship of third-party skills. Each redistributed item remains subject to its upstream license/notice requirements. A license change is a review event, not an automatic update.

See [`CREDITS.md`](CREDITS.md) for canonical sources and attribution rules.

## Current state

The v2 distribution/trust layer is implemented. `process/` is verified 14/14 exact; canonical mappings cover WordPress, Marketing, and known Design sources; Security/QA are explicitly local; legacy Rivet-derived material is explicitly separated from exact syncing; reviewed sync/update tooling and server-local scheduling are included.

Repository-level branch protection is still a GitHub setting and must be enabled on `main`; see [`ops/README.md`](ops/README.md).
