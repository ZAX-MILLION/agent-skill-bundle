# Everything Claude Code (ECC) — selectively indexed source

- Original author: [Affaan Mustafa, ECC](https://github.com/affaan-m/ECC).
- Reviewed revision: [`e482e579415fde18357cafce70f177ae19fd7f03`](https://github.com/affaan-m/ECC/tree/e482e579415fde18357cafce70f177ae19fd7f03).
- Original license: MIT root license; check each selected source directory and dependencies before acquisition.
- Exactly **292** canonical source skill paths appear under `skills/<name>/SKILL.md` at this revision. The repo also includes language translations and host-packaging copies, agents, commands, hooks, runtime scripts, rules, and plugin manifests. Those additional files are not interchangeable with portable skill bodies.
- Full searchable *name/sha* registry: [`registry/ecc-source-index.json`](../../../registry/ecc-source-index.json). It includes exact pinned upstream paths; it is **metadata only**, not a clone of the 292 bodies.

## Eight selected portable workflows

| Workflow | Local selected path | Use case |
|---|---|---|
| Iterative retrieval | `process/iterative-retrieval` | Find relevant source and progressively refine context for subagents |
| Architecture decision records | `process/architecture-decision-records` | Record why project architecture choices were made |
| Agent harness construction | `coding/agent-harness-construction` | Improve agent tool/action/observation design |
| Agent architecture audit | `coding/agent-architecture-audit` | Diagnose problems across agent prompt, memory, tools and output layers |
| AI regression testing | `qa/ai-regression-testing` | Catch repeat bugs and sandbox/production discrepancies |
| Production audit | `qa/production-audit` | Assess real release/readiness evidence without uploading private code |
| Context budget | `productivity/context-budget` | Diagnose duplicated instructions, tool schemas and startup context bloat |
| Codebase onboarding | `operations/codebase-onboarding` | Build a repo architecture map and project instructions |

These eight retain their exact original `SKILL.md` Git blobs, with an original MIT license copy inside each installable directory. See [pinned hashes](../../../registry/vendor-ecc.json). Do not infer full native ECC functionality from their presence: they are instructions, not executables, CLI plugins or hooks.

## Safe future additions

1. Look up the user's specific task in the **local bundle first**, including Superpowers, secure-by-default-development, verified skills and existing marketing/QA modules.
2. If missing, find a suitable name in the metadata-only [ECC index](../../../registry/ecc-source-index.json); open its exact `skills/<name>` source path at the reviewed revision. Avoid `.agents/skills`, `.cursor/skills` and translations if a canonical original exists.
3. Read the **complete** skill directory for references, scripts, assets, nested licenses, external downloads, model/tool assumptions and security-sensitive instructions. Reject ambiguous licensing or missing runtime files.
4. Add one approved original skill at a time, recording commit/tree and original blobs. Preserve source text and keep host-specific mappings in `adapters/`. Do not silently install all 292 bodies into Antigravity, Codex or Claude Code.
5. Retain the two native bootstraps and refresh the local Skill Retrieval MCP index separately; test discovery in the real host. If a runtime/plugin is needed, use a separate, reviewed opt-in installation and compare its configuration diff.

### Upstream native installer is separate

ECC provides [Antigravity installation guidance](https://github.com/affaan-m/ECC/blob/e482e579415fde18357cafce70f177ae19fd7f03/docs/ANTIGRAVITY-GUIDE.md) that writes workspace `.agents/` rules/workflows/skills/agents. ECC supports native Claude Code and Codex installation paths, but host parity varies. Do not run a full ECC installer or its GitHub App as part of this bundle; it may duplicate existing skill discovery and install/configure rules, hooks and provider integrations. The snapshot is a starting point for source review, not an automated update.
