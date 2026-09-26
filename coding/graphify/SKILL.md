---
name: graphify
description: Build or query a local codebase knowledge graph for architecture, dependencies, impact analysis, and change planning when Graphify CLI is separately installed.
---
# Graphify codebase navigation — external-runtime adapter

Source: https://github.com/Graphify-Labs/graphify at `4139885a1212956cf69a76946fbde0d181ab85e9`. This original adapter is **not** the generated upstream Graphify skill, and bundling this file does not install `graphify`. The upstream software has Apache-2.0 / MIT notices; see its repository for the applicable file and distribution terms.

1. First check `graphify --version`, confirm the target is the intended local repository, and inspect `graphify --help`. If the runtime is missing, use ordinary source search and report that the Graphify workflow is unavailable.
2. For a new graph, ask the user before indexing confidential files or installing an executable. The reviewed upstream package is **`graphifyy`** (for example an isolated `uv tool install graphifyy` or `pipx install graphifyy`). Never pipe a remote install script to a shell by default.
3. For an existing graph, prefer a narrow `graphify query "<question>"`, `graphify path` or `graphify explain` before wide source scans. Treat `INFERRED` graph edges as hypotheses and verify conclusions in the actual source.
4. Graph construction writes local generated data; verify exclusions before indexing secrets, keys, customer data, or inaccessible paths. Do not push generated graph data or private content to this public skill repository.
5. The upstream `graphify install` command registers its own skills/rules/hooks. **Do not run it blindly alongside this bundle's `graphify` skill:** preview changes and avoid a duplicate skill, unexpected hook or global rule override. Platform commands exist for Antigravity, Codex and Claude Code; choose one deployment method after review.
6. Graphify is a code-navigation aid, not a replacement for actual build, test, security review, or deployment validation.
