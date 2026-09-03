# Agent Skill Bundle

**A source-preserving distribution layer for AI agent skills.**

Use curated skills from established upstream projects in Cursor, Claude Code, and other file-based agents without losing the original authors, licenses, or source history.

> **Upstream authors keep the credit. Upstream repositories remain the source of truth. Host compatibility belongs outside the original skill.**

## Why this exists

AI skill ecosystems are fragmented: useful skills live across many repositories, different agents install them differently, and copied skills quickly become stale or lose provenance.

Agent Skill Bundle aims to make distribution safer and easier by providing:

- one installable collection;
- explicit upstream source tracking;
- preserved licenses and attribution;
- Git-tree provenance for mapped skills;
- review-first exact upstream syncing;
- host-neutral compatibility guidance without silently rewriting third-party skills.

## Trust model

| Rule | Policy |
|---|---|
| Third-party source of truth | Original upstream repository |
| Silent edits to upstream skills | **Not allowed** |
| Original license / notices / credits | **Preserved** |
| Upstream updates | **Review before integration** |
| Automatic upstream → `main` merge | **Disabled** |
| Host-specific compatibility changes | Kept in `adapters/` |

See [`registry/`](registry/README.md), [`CREDITS.md`](CREDITS.md), [`SECURITY.md`](SECURITY.md), and [`SYNC_STATUS.md`](SYNC_STATUS.md) for the current trust and provenance state.

## What's inside

| Category | Skills | Primary sources |
|---|---|---|
| `design/` | UI/UX, frontend, documents, design systems and visual tooling | [Anthropic Skills](https://github.com/anthropics/skills), [daymade](https://github.com/daymade/claude-code-skills), [Google Labs design.md](https://github.com/google-labs-code/design.md), [VoltAgent](https://github.com/VoltAgent/awesome-design-md) |
| `security/` | Web/API/WordPress security auditing | Local + [WordPress Agent Skills](https://github.com/WordPress/agent-skills) |
| `process/` | Planning, TDD, debugging, code review and verification | [obra/superpowers](https://github.com/obra/superpowers) |
| `multiplayer/` | Multiplayer state, chat-room and live-cursor patterns | [Rivet Skills](https://github.com/rivet-dev/skills) |
| `wordpress/` | Plugin, theme, block, REST API, performance and CLI workflows | [WordPress Agent Skills](https://github.com/WordPress/agent-skills) |
| `marketing/` | SEO, copywriting, CRO, pricing, social and outreach | [Marketing Skills](https://github.com/coreyhaines31/marketingskills) |
| `qa/` | Browser QA, visual polish and silent-failure detection | Local |

The bundle currently contains roughly **116 skills**. The number is not the trust signal; provenance and correct usage are.

## Install

The installer copies each skill's **complete directory**, including `SKILL.md`, scripts, references, examples and assets.

### Claude Code

```bash
./install.sh ~/.claude/skills
```

### Cursor

```bash
./install.sh ~/.cursor/skills
```

### Any file-based agent

```bash
./install.sh /path/to/agent/skills
```

For agents without a native skills directory, start with [`adapters/generic/README.md`](adapters/generic/README.md).

## Compatibility

| Host | Current support |
|---|---|
| Claude Code | ✅ Install to its skills directory |
| Cursor | ✅ Install to its skills directory |
| File-based / custom agents | ✅ Custom install path + generic adapter |
| Other hosted AI systems | 🟡 Use a host-specific integration when available; do not assume local filesystem access |

The project intentionally avoids claiming universal *native* support. Different AI hosts expose different tools, permissions and instruction mechanisms.

## Provenance & upstream checking

The canonical upstream collection registry is [`registry/sources.json`](registry/sources.json), while [`registry/upstream-state.json`](registry/upstream-state.json) records verified source revisions.

Check current upstream branch revisions:

```bash
python3 scripts/check_upstreams.py
```

Audit mapped skill directories using Git tree SHAs:

```bash
python3 scripts/audit_skills.py
```

Discover provenance candidates for mixed-source categories without accepting name-only matches:

```bash
python3 scripts/discover_provenance.py
```

`process/`, `wordpress/`, and `marketing/` use reviewed same-directory-name mapping conventions. Mixed-source categories remain explicit/manual until provenance is proven.

## Review-first upstream sync

Preview the source that would be used for a skill:

```bash
python3 scripts/sync_reviewed.py process/writing-skills
```

After provenance and the upstream diff have been reviewed, create a local review branch and copy the **entire upstream skill directory** exactly:

```bash
python3 scripts/sync_reviewed.py process/writing-skills --apply --reviewed
```

Optionally create a local commit on that review branch:

```bash
python3 scripts/sync_reviewed.py process/writing-skills --apply --reviewed --commit
```

The sync tool:

1. refuses a dirty working tree;
2. creates an `upstream-sync/...` review branch;
3. shallow-clones the registered upstream repository;
4. replaces the selected skill with the complete upstream directory;
5. re-runs provenance auditing;
6. runs `git diff --check`;
7. **never pushes and never merges**.

This deliberately separates *discovering an upstream update* from *trusting and integrating it*.

## Verified `process/` status

Against `obra/superpowers` at the recorded 2026-09-03 revision:

- **12 of 14 skill directories are `EXACT`**;
- **2 have `UPDATE_AVAILABLE`**: `subagent-driven-development` and `writing-skills`.

Five previously stale process skills were refreshed as exact upstream copies and verified by directory-tree SHA. Exact state is recorded in [`registry/skills.json`](registry/skills.json).

## Repository layout

```text
agent-skill-bundle/
├── design/ security/ process/ multiplayer/ wordpress/ marketing/ qa/
│   └── skill directories
├── registry/          # sources, revisions, mapping rules, provenance
├── adapters/          # host compatibility without rewriting skills
├── scripts/           # discovery, audits, reviewed sync tooling
├── CREDITS.md
├── SECURITY.md
├── SYNC_STATUS.md
├── CONTRIBUTING.md
└── install.sh
```

## Credits & licensing

This repository is an aggregation/distribution project. It does **not** claim authorship of third-party skills.

Original upstream projects include Anthropic, daymade, Google Labs, VoltAgent, obra, Rivet, WordPress, and Corey Haines' Marketing Skills. See [`CREDITS.md`](CREDITS.md) for direct source links and the attribution policy.

Each bundled skill must retain the license/notice requirements of its upstream source. A change in upstream licensing is a review event, not an automatic update.

## Current status

The trust layer, upstream revision tracking, Git-tree auditing, provenance discovery, convention mappings, and review-first full-directory sync tooling are in place. Mixed-source categories (`design`, `security`, `multiplayer`) still require exact source-path discovery before they can use reviewed sync safely.

See [`SYNC_STATUS.md`](SYNC_STATUS.md) for what is verified versus intentionally not yet enabled.
