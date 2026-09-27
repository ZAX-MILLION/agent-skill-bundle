---
name: cross-agent-skill-verification
description: Use when confirming that Antigravity, Codex, and Claude Code actually discover and follow relevant on-demand skills, load complete references, and preserve a minimal two-skill native bootstrap.
---
# Cross-agent skill verification

**Original Agent Skill Bundle skill.** Offline-first test plan. No installer, hook, plugin, MCP, PC configuration or cloud service is activated by reading this file.

## Scope
- Verify the *same reviewed source checkout* and only two bundle-native bootstrap skills (`i-have-adhd` and `skill-retrieval-routing`) in each chosen host's documented discovery root.
- Distinguish **native listing**, **local retrieval index**, **supporting-file access**, **actually followed instructions**, and **external tool availability**. One successful installer command proves none of the later stages by itself.
- Never assert that every host has identical subagents, hooks, shell, image generation, search or file access. Keep the host's own built-ins and pre-existing personal skills out of bundle counts.

## Safe acceptance scenarios
1. Record host name/version, approved test workspace and discovery root. Read-only inspect the installed bundle directory and source checksum/revision; do not traverse unrelated private project material.
2. Inspect only metadata for native discovery; assert exactly two **bundle** bootstrap names and no bundled third-party full-copy leftovers. If unexpected copies exist, **stop** and ask before any managed prune.
3. If Skill Retrieval MCP is already approved and configured, inspect its status and source roots; assert it indexes only the intended vault, not the user's unrelated files or public third-party corpus. If absent, mark retrieval **not configured** rather than installing it.
4. Query a narrowly scoped example such as `systematic-debugging`, `frontend-design`, or `secure-by-default-development`. Confirm `get_skill` returns the appropriate original skill and load one actual referenced file from the source checkout. A metadata-only result does not pass.
5. Run a harmless task through the host with no mention of skill names and inspect the observable retrieval/tool events or structured transcript; explicitly distinguish actual evidence from the agent's self-report. Compare that the relevant skill was invoked, unrelated skills stayed unloaded, and safety constraints remained active.
6. Test a negative case: no code/design skill should be loaded for a trivial unrelated text request. Test a missing-runtime case: an n8n/MCP-specific skill must report lack of authorization rather than pretend the tool exists.
7. Re-run or review test evidence for Antigravity, Codex and Claude Code separately; report **not tested** for any host without access. Do not infer installation on one machine from repository CI.

## Release criteria
- Source directory unique names, per-directory license/supporting files, and upstream pins pass the repository tests.
- Full install in an isolated temporary target contains all registered skills; strict `--on-demand` target contains exactly two bundle skills. Never run a full install into the owner's actual global roots during verification.
- Any change affecting code, access, or infrastructure must keep `secure-by-default-development` and `verification-before-completion` when applicable.
- Record a matrix per host: native discovery, retrieval indexing, exact skill chosen, supporting files read, behavior observed, external runtime, and limitations. Do not mark tests green without logs/artifacts.
