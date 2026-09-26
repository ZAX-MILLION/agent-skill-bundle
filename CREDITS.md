# Credits & Upstream Sources

Agent Skill Bundle is a distribution project. It does **not** claim authorship of third-party skills.

Third-party work remains credited to its canonical author/project. Original license and notice files inside mirrored directories must be preserved. Mirrors and downstream copies do not replace the canonical author as the attribution source.

## Canonical skill sources

| Project | Repository | Used for |
|---|---|---|
| Anthropic Skills | https://github.com/anthropics/skills | Document, design, frontend and agent skills |
| daymade Claude Code Skills | https://github.com/daymade/claude-code-skills | `design-style-picker`, `ui-designer`, and related UI skills |
| Hermes Agent / NousResearch | https://github.com/NousResearch/hermes-agent | `design-md` skill |
| obra Superpowers | https://github.com/obra/superpowers | Process, debugging, planning, TDD, reviews and verification |
| WordPress Agent Skills | https://github.com/WordPress/agent-skills | WordPress development skills |
| Marketing Skills by Corey Haines | https://github.com/coreyhaines31/marketingskills | Marketing skills |
| Ponytail by Dietrich Gebert | https://github.com/DietrichGebert/ponytail | Six portable coding skills, MIT; upstream skill text unchanged, license added inside each distributed skill |
| i-have-adhd by Ayoub Ghriss | https://github.com/ayghri/i-have-adhd | Original portable communication SKILL.md and MIT license. Antigravity always-on rule is a bundle-specific adapter, not the upstream plugin/hook. |

## Additional portable expansion (2026-09-26)

| Canonical upstream | Relationship |
|---|---|
| [Taste Skill — Leonxlnx](https://github.com/Leonxlnx/taste-skill) | Original `design-taste-frontend` and `image-to-code` SKILL.md files unchanged; MIT license overlaid in each directory. |
| [Vercel Web Interface Guidelines](https://github.com/vercel-labs/web-interface-guidelines) | Exact pinned MIT-licensed `command.md` snapshot; local `web-design-guidelines` adapter deliberately does not execute mutable upstream instructions. |
| [Awesome Design Skills — Bergside](https://github.com/bergside/awesome-design-skills) | Original catalog names referenced in local `awesome-design` router; 67 style bodies are not redistributed. |
| [Graphify Labs](https://github.com/Graphify-Labs/graphify) | Optional external `graphifyy` runtime; local `graphify` adapter only. |
| [Graft — Mikko-ww](https://github.com/Mikko-ww/agent-skills-graft) | Optional external manager; local `graft` adapter only. |
| [Vercel Skills CLI](https://github.com/vercel-labs/skills) and [Agent Skills standard](https://agentskills.io/) | External discovery/installer and specification; local `agent-skills` workflow only. |

Reviewed source hashes and revisions: [registry/portable-expansion.json](registry/portable-expansion.json).

## Additional skill sources (2026-09-26)

| Original project | Used for |
|---|---|
| [Caveman by Julius Brussee](https://github.com/JuliusBrussee/caveman) | Original MIT `skills/caveman` SKILL.md and README unchanged, with root scoped MIT license copied to `productivity/caveman`. Separate Engine-linked runtime is BSL-1.1, not redistributed. |
| [Humanizer by Siqi Chen](https://github.com/blader/humanizer) | Original `SKILL.md` unchanged with MIT license in `productivity/humanizer`. |
| [Claude-Mem by Alex Newman](https://github.com/thedotmack/claude-mem) | Local review-first adapter only; separate Apache-2.0 plugin/worker and session data not copied or installed. |
| [Marketing Skills by Corey Haines](https://github.com/coreyhaines31/marketingskills) | Added missing `events` original skill and all its references/eval, plus MIT root license overlay. Existing changed marketing skills remain under review. |

See [registry/vendor-second-wave.json](registry/vendor-second-wave.json) for source pins and exact original file hashes.

## More reviewed sources (2026-09-26)

| Source | Actual relationship |
|---|---|
| [n8n Official Skills](https://github.com/n8n-io/skills) | All 14 official `SKILL.md` packages plus 51 supporting files copied byte-for-byte into `automation/`, with Apache-2.0 license overlay per package. No plugin, session hook or instance MCP server installed. |
| [obra Superpowers](https://github.com/obra/superpowers) | Added `diagnosing-superpowers` skill's 20 original files unchanged plus upstream MIT license overlay. Existing 14 Superpowers skill copies remain under separate upstream review. |
| [PAUL — Chris Kahler](https://github.com/ChristopherKahler/paul) | Original local portable workflow adapter only. No Claude commands/runtime copied. |
| [OpenMontage — calesthio](https://github.com/calesthio/OpenMontage) | Original local video-workflow guide only. AGPL-3.0 runtime and creative assets not copied. |
| [shuohao-skills — eternityspring](https://github.com/eternityspring/shuohao-skills) | Original local router to six separately installed original skill packages. No JS executables or binary assets copied. |
| [Pixel Agents](https://github.com/pixel-agents-hq/pixel-agents) | Reference-only external MIT extension/CLI; not an upstream skill. |
| [czlonkowski/n8n-mcp](https://github.com/czlonkowski/n8n-mcp) | Reference-only third-party MCP; distinct from official n8n instance-level MCP. |

[Source commits and 100 pinned original/license Git blob hashes](registry/vendor-third-wave.json).

## Everything Claude Code source selection (2026-09-27)

| Original project | Relationship |
|---|---|
| [ECC — Everything Claude Code, Affaan Mustafa](https://github.com/affaan-m/ECC) | Eight unchanged original `SKILL.md` files from `skills/`, each with a copy of upstream MIT root license; reviewed commit `e482e579415fde18357cafce70f177ae19fd7f03`. The other 284 canonical skill names are tracked in a metadata-only source index; plugin, rules, hooks, agents, commands, memory, executables and GitHub App are not redistributed or installed. |

See [ECC pinned original blob hashes](registry/vendor-ecc.json) and [ECC catalog guidance](research/agent-skills/references/ecc-catalog.md). Upstream remains the source of truth; per-host notes are outside the unchanged copied skills.

## External references (not redistributed)

| Project | Source | Relationship |
|---|---|---|
| 500+ AI Agent Projects by ashishpatel26 | https://github.com/ashishpatel26/500-AI-Agents-Projects | Reference catalog only; listed projects have independent licenses. |
| Agent Reach by Agent Eyes / Panniantong | https://github.com/Panniantong/Agent-Reach | Optional external CLI, MIT. Original local permission-scoped adapter; no runtime or credentials copied. |

| Skill Retrieval MCP by Zhan Cheng | https://github.com/JayCheng113/skill-retrieval-mcp | Optional MIT-licensed external local MCP service; original, reviewed usage adapter only. Runtime, index, embedding model and external corpus are not redistributed. |
| VoltAgent Awesome Agent Skills | https://github.com/VoltAgent/awesome-agent-skills | Reviewed reference-only discovery directory integrated into the existing `agent-skills` workflow. Catalog MIT does not license external authors' linked skills. No linked skill packages or executables copied. |

## Collections and reference sources

These projects are important sources, but they are not falsely presented as authors of unrelated skills:

| Project | Repository | Relationship |
|---|---|---|
| Google Labs design.md | https://github.com/google-labs-code/design.md | Reference specification/tool used by the Hermes `design-md` skill |
| VoltAgent awesome-design-md | https://github.com/VoltAgent/awesome-design-md | Upstream for the bundled `design/design-systems` collection |
| Rivet Skills | https://github.com/rivet-dev/skills | Current Rivet skill ecosystem; legacy multiplayer paths are no longer present there |
| Rivet Actors | https://github.com/rivet-dev/actors | Current canonical docs/examples underlying the legacy Rivet-derived multiplayer material |

## Local skills

The `security/` and `qa/` categories are maintained locally in this repository unless an individual entry is explicitly remapped later. They are not attributed to WordPress, Anthropic, or another upstream merely because they cover the same topic.

## Attribution policy

When syncing upstream content:

- preserve original author attribution, license files and notices;
- prefer the canonical author repository over mirrors or aggregators;
- record repository, source path and checked revision;
- never silently rewrite upstream instructions;
- place host-specific compatibility in `adapters/`, outside the upstream copy;
- review license and security-sensitive changes before merging;
- never mark a legacy/derived item as an exact mirror when the original source path can no longer be proven.

Canonical source roles are in `registry/sources.json`; path mappings are in `registry/mappings.json`.
