# Codex adapter

Codex supports the Agent Skills format. Agent Skill Bundle therefore keeps upstream `SKILL.md` files portable instead of maintaining a Codex-specific fork.

Official OpenAI Skills overview: https://openai.com/academy/skills/

Use the skills import/install mechanism exposed by your Codex environment and provide the complete selected skill directory, including any scripts, references, examples and assets it uses.

For any task that creates or modifies application code, configuration, infrastructure, authentication, APIs, data access, dependencies, or deployment, include `security/secure-by-default-development` as the baseline skill and then add the narrow task-specific skill.

`secure-by-default-development` remains active while implementation/refactoring skills run. A task-specific skill is not permission to weaken authorization, RLS, validation, CSP, CORS, TLS, secret handling, rate limiting, or another security boundary merely to make the implementation pass. Security-relevant completion requires relevant negative/security verification, not only a working happy path.

Some upstream skills contain host-specific instructions for subagents, terminals or browser tools. Treat those as capability requirements. Follow the tools actually available in the current Codex environment; never invent a missing tool or weaken a security boundary to satisfy a skill.

## Strict on-demand installation (preferred for this bundle)

Keep a **single local source checkout** and install only the two native bootstrap skills into your active Codex skill root:

```bash
./install.sh "$HOME/.codex/skills" --flat --on-demand
```

Check your installed Codex version's skill locations before using the target; project skills can live in `.agents/skills/`. If a full bundle already occupies that target, review it and explicitly use `--prune-managed` to remove only correctly marked bundle copies. Do not remove Codex's own built-in or personal skills. The other 193 non-bootstrap skill bodies stay in the local source checkout, indexed by optional Skill Retrieval MCP, not loaded into native discovery. Configure the local MCP in Codex's `~/.codex/config.toml` or MCP manager by **merging**, not replacing, existing servers; see [multi-host guide](../multi-host/README.md). The installer does not install the MCP runtime or edit your config.

## Optional Codex credit-efficient profile

If you explicitly want a small native set for active Codex development instead of strict two-bootstrap mode:

```bash
./install.sh "$HOME/.codex/skills" --flat --codex-efficient
```

It exposes 12 reviewed skills: the two bootstraps, `credit-usage-helper`, Ponytail, Graft, Graphify, secure-by-default development, completion verification, and the Blueprint task/test/review/coordinator chain.

This profile is intentionally small. `factory`, `architecture-review`, specialist QA/design skills and the rest of the vault remain on demand.

See [Codex credit-efficient profile](../../docs/CODEX_EFFICIENT_PROFILE.md).

For cross-session action-first communication, merge the reviewed Antigravity `i-have-adhd` *style principles* into your user-global Codex `AGENTS.md`, preserving existing project rules; do not copy Antigravity-specific paths, and verify in a new session. Installing the manually invoked original skill alone does not make it always-on.

The nine selected ECC skills are retrieved from the same local source checkout. Upstream ECC also has a separate native Codex plugin path; do not layer its marketplace install and sync install (or copies of our same skills) without reviewing collisions. No Codex plugin/hook was registered by this bundle. See [ECC provenance](../../registry/vendor-ecc.json).
