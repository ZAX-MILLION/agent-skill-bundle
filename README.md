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
- a review-first update policy;
- host-neutral compatibility guidance without silently rewriting third-party skills.

## Trust model

| Rule | Policy |
|---|---|
| Third-party source of truth | Original upstream repository |
| Silent edits to upstream skills | **Not allowed** |
| Original license / notices / credits | **Preserved** |
| Upstream updates | **Review before merge** |
| Automatic upstream → `main` merge | **Disabled** |
| Host-specific compatibility changes | Kept in `adapters/` |

See [`registry/`](registry/README.md), [`CREDITS.md`](CREDITS.md), and [`SYNC_STATUS.md`](SYNC_STATUS.md) for the current provenance and sync state.

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

The existing installer copies each skill's **complete directory**, including `SKILL.md`, scripts, references, examples and assets.

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

## Upstream checking

Registered upstream collections live in [`registry/sources.json`](registry/sources.json).

Check their current branch revisions with no third-party Python dependencies:

```bash
python3 scripts/check_upstreams.py
```

Write a revision snapshot only after every source check succeeds:

```bash
python3 scripts/check_upstreams.py --write
```

This **does not automatically replace skills**. Exact per-skill source paths and commit provenance are being recorded before automatic copying is enabled. Upstream changes will remain review-first rather than auto-merged into `main`.

## Repository layout

```text
agent-skill-bundle/
├── design/ security/ process/ multiplayer/ wordpress/ marketing/ qa/
│   └── original skill directories
├── registry/          # upstream sources + provenance policy
├── adapters/          # host compatibility without rewriting skills
├── scripts/           # source checking / future safe sync tooling
├── CREDITS.md
├── SYNC_STATUS.md
└── install.sh
```

## Credits & licensing

This repository is an aggregation/distribution project. It does **not** claim authorship of third-party skills.

Original upstream projects include Anthropic, daymade, Google Labs, VoltAgent, obra, Rivet, WordPress, and Corey Haines' Marketing Skills. See [`CREDITS.md`](CREDITS.md) for direct source links and the attribution policy.

Each bundled skill must retain the license/notice requirements of its upstream source. A change in upstream licensing is a review event, not an automatic update.

## Current status

The trust layer and upstream collection registry are in place. Exact per-skill provenance mapping and safe reviewed sync are the next steps. See [`SYNC_STATUS.md`](SYNC_STATUS.md) for what is complete versus intentionally not yet enabled.
