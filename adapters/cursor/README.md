# Cursor adapter

Cursor can use file-based skill directories. Keep the upstream skill directory intact and install the bundle with the existing installer:

```bash
./install.sh ~/.cursor/skills
```

For a smaller context footprint, copy/install only the skill directories needed by the project instead of treating all bundled skills as always-on instructions.

For any task that creates or modifies application code, configuration, infrastructure, authentication, APIs, data access, dependencies, or deployment, include `security/secure-by-default-development` as the baseline skill and then add the narrow task-specific skill.

The security baseline is the exception to the usual narrow-selection rule: it is intentionally cross-cutting for code/config changes. It must not be interpreted as permission to load every security-audit skill. Keep the baseline plus the few specialist skills relevant to the task.

Host-specific Cursor rules belong outside upstream skill directories. Never patch a third-party `SKILL.md` merely to make it Cursor-specific; put those notes in this adapter or project-level Cursor configuration. Project rules should reinforce that task-specific instructions may not weaken authorization, RLS, validation, CSP, CORS, TLS, secret handling, rate limiting, or another security boundary just to make an implementation pass.
