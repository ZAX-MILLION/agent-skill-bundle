# Codex adapter

Codex supports the Agent Skills format. Agent Skill Bundle therefore keeps upstream `SKILL.md` files portable instead of maintaining a Codex-specific fork.

Official OpenAI Skills overview: https://openai.com/academy/skills/

Use the skills import/install mechanism exposed by your Codex environment and provide the complete selected skill directory, including any scripts, references, examples and assets it uses.

For any task that creates or modifies application code, configuration, infrastructure, authentication, APIs, data access, dependencies, or deployment, include `security/secure-by-default-development` as the baseline skill and then add the narrow task-specific skill.

`secure-by-default-development` remains active while implementation/refactoring skills run. A task-specific skill is not permission to weaken authorization, RLS, validation, CSP, CORS, TLS, secret handling, rate limiting, or another security boundary merely to make the implementation pass. Security-relevant completion requires relevant negative/security verification, not only a working happy path.

Some upstream skills contain host-specific instructions for subagents, terminals or browser tools. Treat those as capability requirements. Follow the tools actually available in the current Codex environment; never invent a missing tool or weaken a security boundary to satisfy a skill.
