---
name: graphify
description: Build or query a local codebase knowledge graph for architecture, dependencies, impact analysis, and change planning when the separately installed Graphify CLI is available.
---
# Graphify codebase navigation — external-runtime adapter

Reviewed source: https://github.com/Graphify-Labs/graphify at `e10df08877f8819a625a1afa38c3297a31fda296` (Graphify `0.9.74` / PyPI package `graphifyy`). This bundle ships only this local adapter; it does not install Graphify or copy Graphify's generated assistant skill.

## Credit-efficient rule

Use Graphify when it replaces repeated broad repository scans.

Do **not** build/rebuild a graph for a tiny isolated change.

For code-only graphs, Graphify's parser is local and does not need an LLM. Docs/media semantic passes may use a configured model/backend and can consume external model/API credits, so do not enable those backends without a reason.

## Setup

1. Check `graphify --version`.
2. If missing and the user explicitly wants the runtime, prefer an isolated reviewed install:

```bash
uv tool install 'graphifyy==0.9.74'
```

Alternative: `pipx install 'graphifyy==0.9.74'`.

3. **Do not run `graphify install` automatically when this bundle skill is already installed.** Upstream's install command writes another Graphify skill/rules into host discovery and can create duplicates.
4. If the user wants Graphify's upstream assistant integration instead of this bundle adapter, preview that change and choose one installation method. For project-scoped Codex, upstream supports `graphify install --project --platform codex`.
5. Codex parallel extraction may require `multi_agent = true` in Codex config according to the reviewed Graphify release. Do not enable it merely for normal single-thread queries.

## Use

- Confirm the target is the intended local repository.
- Prefer an existing graph:
  - `graphify query "<question>"`
  - `graphify path "<A>" "<B>"`
  - `graphify explain "<concept>"`
- Treat `INFERRED` edges as hypotheses and verify material conclusions in source.
- If a new graph is justified, verify exclusions first. Never index secrets, keys, customer data, or inaccessible/private material by accident.
- Generated `graphify-out/` is local analysis data unless the project explicitly decides to track it.

Graphify is a navigation aid, not proof of correctness, security, build success, or deployment readiness.
