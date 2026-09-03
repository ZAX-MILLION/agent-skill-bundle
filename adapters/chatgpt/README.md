# ChatGPT adapter

ChatGPT supports reusable Agent Skills built around `SKILL.md`. Agent Skill Bundle keeps those files portable and source-preserving rather than rewriting them for ChatGPT.

Official OpenAI overview: https://openai.com/academy/skills/

## Use

1. Choose only the skills relevant to the work; do not load the entire bundle into one task context.
2. Import or expose the complete selected skill directory through the ChatGPT Skills surface available to your account/workspace.
3. Keep `SKILL.md` together with its referenced scripts, templates, examples and assets.
4. Treat host/tool assumptions inside third-party skills as capability requests, not permissions. If ChatGPT does not expose a requested tool, use an available equivalent or stop safely.
5. Do not edit the bundled upstream copy to make it ChatGPT-specific. Put compatibility notes in this adapter layer.

## Provenance

Before using a third-party skill for sensitive work, check `registry/skills.json`, `registry/mappings.json`, `CREDITS.md`, and `SECURITY.md`.

The bundle is compatible with the Agent Skills format; it does not claim every skill can execute every instruction on every ChatGPT plan or surface.
