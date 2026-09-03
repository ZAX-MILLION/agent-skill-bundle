# Agent Adapters

Adapters make the bundle easier to consume on different AI hosts **without changing upstream skill content**.

A bundled third-party skill remains the canonical source material. An adapter only explains host-specific discovery, installation, import, or capability mapping. Never copy and rewrite a whole upstream skill just to rename tools.

## Adapters

- `chatgpt/` — Agent Skills usage guidance for ChatGPT.
- `codex/` — Agent Skills usage guidance for Codex.
- `cursor/` — file-based Cursor installation and host configuration boundary.
- `claude-code/` — file-based Claude Code installation.
- `generic/` — fallback contract for any AI/agent that can read `SKILL.md` and supporting files.

## Capability rule

A skill may request terminal, browser, subagent, GitHub, database, filesystem, or other tools. That request does **not** create the capability or grant permission. The host must use an actually available equivalent, follow its own safety/confirmation rules, or stop the unsupported part safely.

## Portability rule

`SKILL.md` is the portable core. Host adapters are intentionally thin so a new AI host can be added without forking the skills themselves.
