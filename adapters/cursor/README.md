# Cursor adapter

Cursor can use file-based skill directories. Keep the upstream skill directory intact and install the bundle with the existing installer:

```bash
./install.sh ~/.cursor/skills
```

For a smaller context footprint, copy/install only the skill directories needed by the project instead of treating all bundled skills as always-on instructions.

Host-specific Cursor rules belong outside upstream skill directories. Never patch a third-party `SKILL.md` merely to make it Cursor-specific; put those notes in this adapter or project-level Cursor configuration.
