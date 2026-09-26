---
name: claude-mem
description: Review and use Claude-Mem persistent coding-session memory only when its separate runtime is approved and actually connected; retrieve past work with project-scoped search.
---
# Claude-Mem — external memory runtime adapter

Canonical source: https://github.com/thedotmack/claude-mem , reviewed commit `abeb0dbf0d7371752b305852835f2299794601e1`, Apache-2.0. This **locally authored adapter** is not Claude-Mem's plugin or its `mem-search` skill. Bundling it does not install hooks, a worker, database, MCP server, AI provider, account, or cross-session capture.

## Before use

1. Confirm the user's active host (Antigravity **IDE** vs separate Antigravity **CLI**, Codex, or Claude Code). Check whether Claude-Mem's actual executable/worker and memory search tools are installed and authorized. Do not assume that a `SKILL.md` file starts collection or that Antigravity CLI support proves desktop IDE capture.
2. If absent, provide a host-specific installation plan from the reviewed [upstream source](https://github.com/thedotmack/claude-mem/tree/abeb0dbf0d7371752b305852835f2299794601e1). **Never run its installer automatically.** Installation can modify global rules, hooks and multiple MCP configurations, start a background worker, capture prompts/tool outputs, and request provider credentials or sign-in. Back up and diff existing host configuration before the user explicitly approves.
3. Privacy first: determine whether observations and prompts remain local or reach a hosted extraction provider or CMEM/cloud sync. The project documents cloud sync of observation narratives and full prompt text. Treat cloud features, account sign-in, repository scanning and capture of terminal/API material as opt-in; do not assume `<private>` tags fully prevent all sensitive capture. Exclude credentials, personal data and sensitive projects before enabling it; review retention, deletion, permissions and local HTTP exposure.
4. Do not index or upload the user's private project history into this **public** bundle. Maintain separate project boundaries in the memory store. Do not weaken existing auth, secret handling or approvals for ease of setup.

## When installed and verified

Use the **real** memory-search tools exposed by the connected host: scoped search for relevant project/session names, inspect only relevant summaries, retrieve a few selected observations, and request full raw tool outputs only when needed to verify an exact claim. Treat stored summaries as historical leads, not ground truth; check current source, commits and live environment before coding or deployment. If the runtime is absent, explicitly say memory retrieval is unavailable and use existing project documents instead.

Preferred architecture: local source checkout + Skill Retrieval MCP for skill instructions; optional, separately permissioned Claude-Mem for *user project history*. These are different indexes. Do not automatically install both for every agent or substitute Claude-Mem for the existing `project-handoff` and durable repo documentation.
