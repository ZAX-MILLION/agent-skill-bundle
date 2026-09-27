# Claude Code adapter

**Preferred: strict on-demand**. Install only the two native bootstrap
skills into the active Claude Code skills root:

```bash
./install.sh "$HOME/.claude/skills" --flat --on-demand
```

The other 172 skills stay in the one local source checkout, with complete
scripts, references, examples, templates and assets. Discovery requires the
separately installed and configured local Skill Retrieval MCP; the install
command alone does not connect it. Do not install a second full copy or native
ECC/n8n plugin in the same discovery scope without first checking duplicates.

An optional **full native** install is `./install.sh "$HOME/.claude/skills"`
and exposes all 174 descriptions at startup; it is not strict on-demand.

For any task that creates or modifies application code, configuration, infrastructure, authentication, APIs, data access, dependencies, or deployment, include `security/secure-by-default-development` as the baseline skill and then add the narrow task-specific skill.

The security baseline remains active while implementation/refactoring skills run. A task-specific skill must not be used to justify weakening authorization, RLS, validation, CSP, CORS, TLS, secret handling, rate limiting, or another security boundary. Security-relevant completion requires relevant negative/security verification, not only a working happy path.

Do not modify third-party skills for Claude-specific behavior. Keep host configuration and compatibility notes outside upstream skill directories.

## Strict on-demand installation (preferred)

```bash
./install.sh "$HOME/.claude/skills" --flat --on-demand
```

This installs only `i-have-adhd` and `skill-retrieval-routing` natively. Keep the other 172 skills in the same local source checkout and index them through the separately configured Skill Retrieval MCP; see [multi-host guide](../multi-host/README.md). If a previous bundle full install occupies this root, review first and use `--prune-managed` explicitly; leave unmarked personal and plugin skills untouched. The installer does not register MCP or change Claude settings. To make the response style cross-session, merge only the applicable i-have-adhd style principles into `~/.claude/CLAUDE.md`, preserving existing rules and checking for plugin duplicates. Never assume that a skill automatically grants an executable, an image generator or project access.

The eight selected ECC skills are retrievable without installing the `ecc@ecc` plugin. If electing to use upstream's full native Claude plugin instead, inspect duplicate skill names, hooks, global rules, memory, and config before choosing one approach; the portable subset does not provide ECC's full Claude runtime. See [ECC provenance](../../registry/vendor-ecc.json).
