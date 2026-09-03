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

Audit every **mapped** skill directory using Git tree SHAs:

```bash
python3 scripts/audit_skills.py
```

Both tools are dependency-free Python scripts. Their `--write` modes refresh registry metadata only; they do **not** overwrite skill content.

### First verified result

`process/` is now fully mapped to `obra/superpowers`. At the recorded 2026-09-03 audit:

- **7 skill directories were `EXACT`**;
- **7 had `UPDATE_AVAILABLE`**.

That result is recorded in [`registry/skills.json`](registry/skills.json). No skill was replaced automatically.

## Repository layout

```text
agent-skill-bundle/
├── design/ security/ process/ multiplayer/ wordpress/ marketing/ qa/
│   └── skill directories
├── registry/          # sources, revisions, per-skill provenance
├── adapters/          # host compatibility without rewriting skills
├── scripts/           # source and Git-tree audits
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

The trust layer is live: upstream repositories have a recorded revision snapshot, `process/` has exact per-skill provenance, and the auditing tools are in place. Remaining mixed categories still need exact source-path mapping before safe reviewed syncing can be enabled for them.

See [`SYNC_STATUS.md`](SYNC_STATUS.md) for what is verified versus intentionally not yet enabled.
