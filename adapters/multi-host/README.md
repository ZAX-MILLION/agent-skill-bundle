# One reviewed vault — Antigravity, Codex, Claude Code and other agents

**Design:** one authoritative source checkout, two native bootstrap skills per host, one reviewed local Skill Retrieval MCP index, and explicit optional executables. Do not put all 188 instructions in a global prompt. Native skill registries typically expose names/descriptions before loading bodies; this strict mode exposes only two of this bundle's native descriptions.

| Host | Native global skill target | On-demand install |
|---|---|---|
| Antigravity 2.0 / IDE | `~/.gemini/config/skills/` | `./install.sh "$HOME/.gemini/config/skills" --flat --on-demand` |
| Codex | `~/.codex/skills/` (verify installed version) | `./install.sh "$HOME/.codex/skills" --flat --on-demand` |
| Claude Code | `~/.claude/skills/` | `./install.sh "$HOME/.claude/skills" --flat --on-demand` |
| Generic agent | Host's documented skills directory | `./install.sh /absolute/path/to/skills --flat --on-demand` |

The Antigravity CLI has a **different** global path, `~/.gemini/antigravity-cli/skills/`. Workspace-specific installs can use `<repo>/.agents/skills/` if supported. On Windows, use the machine's actual profile and the host's documented location; Bash commands require an appropriate shell. The Vercel Skills CLI may use a different version-specific global location from the native IDE—**do not install the same copy into several discovery roots**.

## Two-stage setup on the actual workstation

1. Clone/update this bundle in a *private local folder*. Review `SECURITY.md`, inspect your existing skill targets, then run `bash tests/on-demand-install.sh`.
2. Install the two bootstrap skills for each host you actually use. If full bundle copies exist, the installer refuses to call the install minimal; review, back up, and add `--prune-managed` deliberately. Never use `--force` on personal or external skills.
3. Review/install the external Skill Retrieval MCP in its own isolated environment, import the **one source checkout**, build its index and run status/search. Follow [the existing setup](../antigravity/skill-retrieval-mcp.md), which uses `init --no-register` and a local data directory; do not pull the unrelated third-party corpus. The source checkout preserves scripts/references/assets the index does not import.
4. Connect a local `stdio` `skill-mcp` executable to **each supported host**, using its existing MCP manager: Antigravity merges into `~/.gemini/config/mcp_config.json`, Codex merges into `~/.codex/config.toml`, Claude Code uses its user-scoped MCP manager. In every host use the same actual executable and data-dir absolute paths, with command arguments `--data-dir /ABSOLUTE/DATA/DIR serve`. Do not overwrite existing MCP config; consider a separate index/data directory if concurrent writes are observed. Check local permission boundaries and the active app version.
5. Verify skill discovery and four MCP tool calls (`list_categories`, `keyword_search`, `search_skills`, `get_skill`) in **each** host, then read the selected skill's referenced files from the local checkout and perform one harmless task. A successful install script is not a working MCP test.

## Requested expansion: what is actually packaged

| Requested | Local skill | Boundary |
|---|---|---|
| Graphify | `graphify` | Original local adapter; actual `graphifyy` CLI is separate. If using upstream `graphify install`, avoid a duplicate skill or unreviewed rules/hooks. |
| Graft | `graft` | Original distribution-guide skill; optional Python manager not bundled. Our tested installer already covers copying this bundle. |
| Awesome Design | `awesome-design` | Selective catalog/router, **not** all 67 third-party style bodies. Add one approved upstream style when needed. |
| Taste Skill | `design-taste-frontend` | Original author frontmatter name retained, complete upstream SKILL.md and MIT license copied unchanged. Large skill—load only when relevant. |
| Image to Code | `image-to-code` | Original Taste Skill source, not a general-purpose image generator; requires host visual input and image-generation availability where called for. |
| Web Design Guidelines | `web-design-guidelines` | Original adapter + frozen locally vendored Vercel rules, no mutable instruction fetch at run time. |
| Agent Skills | `agent-skills` | Original discovery/review workflow; optional `npx skills` tool separate. |

Both upstream Taste skills remain as originally authored, including any Codex-specific language. Other hosts should follow the *workflow intent* using available equivalent tools, never fabricate unavailable image generation, browser, or execution capability. The portable package format is not a promise of identical outcomes.

## Security and global output style

Never copy private project memory, API keys, SSH material or production configuration into this **public** repository or an external skill index. Review external skills before installation, keep source pins and licenses, and obtain authorization for runtime installs, destructive changes or deployment. The earlier historical Git credential exposure remains unresolved until credentials are rotated and history is remediated; the HEAD-only public-content gate does not erase it.

The original `i-have-adhd` skill is marked for explicit invocation. For persistent communication, **merge** its reviewed action-first principles into the respective user-global rule rather than overwriting it: Antigravity `GEMINI.md`/host rules, Codex `AGENTS.md`, Claude Code `CLAUDE.md`. A default style is not a medical claim or a substitute for safety, security, testing or approvals.

## Curated discovery source (not a package installer)

The existing `agent-skills` workflow includes a [pinned VoltAgent catalog reference](../../research/agent-skills/references/voltagent-catalog.md). It is usable from all supported hosts through on-demand retrieval of that one source skill. The advertised 1,497+ entries are external links, **not** native skills, and no linked content is automatically installed or granted executable permissions.

## Optional session memory, prose editing and marketing

Caveman and Humanizer remain on-demand, not native always-on skills. Existing `i-have-adhd` global communication rules have priority. Use Caveman only when explicitly requested; use Humanizer for scoped prose edits, preserving source facts, quotes, code and data.

Claude-Mem is a separate memory plugin/worker. Upstream documents Claude Code, Codex and Antigravity **CLI** workflows; the Antigravity desktop IDE is a distinct host and its automatic capture must be verified independently. Installation may alter global hooks, rules, and MCP registration. Inspect backups and privacy settings first, and distinguish local storage from third-party extraction or cloud sync. Do not store private project history or credentials in this public skill bundle or the public skills index.

Marketing's `events` skill is installed with full references and evals. Keep the per-project marketing context file private; don't publish it with the shared skill repository.

## n8n, PAUL and media sources

The 14 **official n8n skills** are included in the one source vault with their references. The local `n8n-instance` adapter describes *separate* official instance-level MCP authorization. Antigravity, Codex and Claude Code can load the same skill text after local Skill Retrieval MCP is configured, but the actual n8n connection is not installed by the bundle. Review the official host MCP setup and avoid duplicated plugin connections; never enable workflow triggers or expose credentials without permission.

`paul` is a portable loop adaptation, not PAUL's installed Claude Code slash commands; don't mix its project-state management with an already running Superpowers orchestrator by default. `diagnosing-superpowers` is now the 15th source-preserved Superpowers skill; the first 14 remain pinned at their earlier reviewed revision. `openmontage`, `zax-editor` and `shuohao-skills` are local, non-executing routers to separate creative software/full source packages; the video-editor adapter additionally verifies a separately obtained reviewed package by hash; [Pixel Agents](../../research/external-tooling.md) is optional visual tooling, not a skill or model upgrade.

All new package bodies remain outside native startup discovery in strict on-demand mode. Keep private n8n credentials, source media, story manuscripts, agent transcripts and provider keys out of the public Git repository and public retrieval index.

## ECC selectively across all hosts

The nine selected [ECC skill bodies](../../registry/vendor-ecc.json) are in the reviewed source checkout and can be retrieved on demand. Use the [ECC index reference](../../research/agent-skills/references/ecc-catalog.md) to discover the other canonical upstream names; names alone are **not** installed instructions or grants of capability. The native ECC installer can modify host rules, workflows, commands, plugins and hooks; do not stack it over this bundle without examining affected paths and avoiding duplicates.

Map Claude-specific path/tool examples in unchanged source skills to the actual host safely: Antigravity uses its IDE/project scope, Codex uses its documented skill and instruction scope, Claude Code can use its native paths. If the expected tool or lifecycle hook does not exist, report the unsupported portion instead of pretending it ran. `context-budget` estimates are heuristics, not measured token usage. No ECC worker, agent hook, marketplace plugin, account, or paid GitHub App is enabled here.
