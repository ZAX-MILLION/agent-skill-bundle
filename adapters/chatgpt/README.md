# ChatGPT adapter

ChatGPT supports reusable Agent Skills built around `SKILL.md`. Agent Skill Bundle keeps those files portable and source-preserving rather than rewriting them for ChatGPT.

Official OpenAI overview: https://openai.com/academy/skills/

## Use

1. Choose only the skills relevant to the work; do not load the entire bundle into one task context.
2. For any task that creates or modifies application code, configuration, infrastructure, authentication, APIs, data access, dependencies, or deployment, include `security/secure-by-default-development` as the baseline skill and then add the narrow task-specific skill.
3. Import or expose the complete selected skill directory through the ChatGPT Skills surface available to your account/workspace.
4. Keep `SKILL.md` together with its referenced scripts, templates, examples and assets.
5. Treat host/tool assumptions inside third-party skills as capability requests, not permissions. If ChatGPT does not expose a requested tool, use an available equivalent or stop safely.
6. Do not edit the bundled upstream copy to make it ChatGPT-specific. Put compatibility notes in this adapter layer.

## Security baseline

`secure-by-default-development` is intentionally cross-cutting. It should remain active while implementation/refactoring skills run. A task-specific skill must not be interpreted as permission to weaken authorization, RLS, validation, CSP, CORS, TLS, secret handling, rate limiting, or another security boundary merely to make the implementation pass.

For security-relevant changes, completion requires at least one relevant negative/security verification, not only a working happy path.

## Provenance

Before using a third-party skill for sensitive work, check `registry/skills.json`, `registry/mappings.json`, `CREDITS.md`, and `SECURITY.md`.

The bundle is compatible with the Agent Skills format; it does not claim every skill can execute every instruction on every ChatGPT plan or surface.
