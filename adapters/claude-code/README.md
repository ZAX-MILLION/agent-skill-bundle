# Claude Code adapter

Install the complete skill directories into Claude Code's skills location:

```bash
./install.sh ~/.claude/skills
```

The installer copies each whole directory, not only `SKILL.md`, so referenced scripts, examples, templates and assets remain available.

For any task that creates or modifies application code, configuration, infrastructure, authentication, APIs, data access, dependencies, or deployment, include `security/secure-by-default-development` as the baseline skill and then add the narrow task-specific skill.

The security baseline remains active while implementation/refactoring skills run. A task-specific skill must not be used to justify weakening authorization, RLS, validation, CSP, CORS, TLS, secret handling, rate limiting, or another security boundary. Security-relevant completion requires relevant negative/security verification, not only a working happy path.

Do not modify third-party skills for Claude-specific behavior. Keep host configuration and compatibility notes outside upstream skill directories.
