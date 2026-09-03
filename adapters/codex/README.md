# Codex adapter

Codex supports the Agent Skills format. Agent Skill Bundle therefore keeps upstream `SKILL.md` files portable instead of maintaining a Codex-specific fork.

Official OpenAI Skills overview: https://openai.com/academy/skills/

Use the skills import/install mechanism exposed by your Codex environment and provide the complete selected skill directory, including any scripts, references, examples and assets it uses.

Some upstream skills contain host-specific instructions for subagents, terminals or browser tools. Treat those as capability requirements. Follow the tools actually available in the current Codex environment; never invent a missing tool or weaken a security boundary to satisfy a skill.
