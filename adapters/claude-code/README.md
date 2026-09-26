# Claude Code adapter

Install the complete skill directories into Claude Code's skills location:

```bash
./install.sh ~/.claude/skills
```

The installer copies each whole directory, not only `SKILL.md`, so referenced scripts, examples, templates and assets remain available.

For any task that creates or modifies application code, configuration, infrastructure, authentication, APIs, data access, dependencies, or deployment, include `security/secure-by-default-development` as the baseline skill and then add the narrow task-specific skill.

The security baseline remains active while implementation/refactoring skills run. A task-specific skill must not be used to justify weakening authorization, RLS, validation, CSP, CORS, TLS, secret handling, rate limiting, or another security boundary. Security-relevant completion requires relevant negative/security verification, not only a working happy path.

Do not modify third-party skills for Claude-specific behavior. Keep host configuration and compatibility notes outside upstream skill directories.

## Strict on-demand installation (preferred)

```bash
./install.sh "$HOME/.claude/skills" --flat --on-demand
```

This installs only `i-have-adhd` and `skill-retrieval-routing` natively. Keep the other 141 skills in the same local source checkout and index them through the separately configured Skill Retrieval MCP; see [multi-host guide](../multi-host/README.md). If a previous bundle full install occupies this root, review first and use `--prune-managed` explicitly; leave unmarked personal and plugin skills untouched. The installer does not register MCP or change Claude settings. To make the response style cross-session, merge only the applicable i-have-adhd style principles into `~/.claude/CLAUDE.md`, preserving existing rules and checking for plugin duplicates. Never assume that a skill automatically grants an executable, an image generator or project access.
