---
name: agent-skills
description: Discover, review and distribute portable Agent Skills across Antigravity, Codex, Claude Code and other compatible coding agents without bloating startup context.
---
# Agent Skills discovery and portability

Open format: https://agentskills.io/ ; canonical installer/discovery tool: https://github.com/vercel-labs/skills (MIT, reviewed at `7407f3893ad4dceab546ac002c3ef806e4000c73`). This is a bundle-authored workflow, not a clone of the package manager or the `find-skills` skill.

1. Search the **existing bundle and local retrieval index first** for the task. Prefer the reviewed local copy over an unknown skill or accidental second copy.
2. If absent, use `npx skills find <topic>` only after confirming Node/npm is available and the user approves running a third-party CLI; alternatively inspect `https://skills.sh` without executing code.
3. Inspect the canonical author, specific repository/path/commit, `SKILL.md`, any scripts, references, license, external requests, prompts and credentials before installation. Popularity is not a security audit.
4. For approved additions, preserve a full skill directory and license. Record source revision and SHA; avoid an upstream skill whose instructions fetch mutable code or instructions unless reviewed/pinned.
5. Install only the chosen native skill or leave it searchable through the local Skill Retrieval MCP; never bulk-install a discovered repository by default. Use `adapters/multi-host/README.md` for Antigravity, Codex, Claude Code and generic paths.
6. Skills are instructions, not automatically installed executables, authenticated tools, MCP connections, model upgrades or production permissions. Test host discovery and the required runtime separately.
