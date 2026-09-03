# Claude Code adapter

Install the complete skill directories into Claude Code's skills location:

```bash
./install.sh ~/.claude/skills
```

The installer copies each whole directory, not only `SKILL.md`, so referenced scripts, examples, templates and assets remain available.

Do not modify third-party skills for Claude-specific behavior. Keep host configuration and compatibility notes outside upstream skill directories.
