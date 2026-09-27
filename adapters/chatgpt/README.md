# ChatGPT adapter

Eligible ChatGPT workspaces support reusable Agent Skills built around `SKILL.md`. Agent Skill Bundle keeps those files portable and source-preserving rather than rewriting them for ChatGPT. For personal ChatGPT accounts, the ADHD-style adapter below uses Custom Instructions rather than claiming native Skills installation.

Official OpenAI overview: https://openai.com/academy/skills/

## ADHD-friendly default for personal ChatGPT

1. Open **Settings → Personalization → Custom Instructions** and enable customization (mobile: Settings → Customize ChatGPT).
2. Merge the [compact action-first instruction](custom-instructions.md) with your existing instructions. It is 1,465 characters, including the final newline. Do not replace other important preferences or paste credentials.
3. For a long-running ChatGPT Project, merge the [project-specific extension](project-instructions.md) in **Project settings**. Project instructions take precedence within that project.
4. For a single chat only, paste the [one-chat activation prompt](one-chat-prompt.md). Saying "normal mode" relaxes the style in that conversation; globally disable it by changing Custom Instructions.

These files shape output; they do not install software, provide permanent memory, make external accounts accessible, or guarantee that the assistant has worked in the background. The account limit for Custom Instructions is currently 1,500 characters on Free/Go and 5,000 on Plus/Pro/Business/Enterprise/Edu. Count your existing instructions when merging. This is the practical path for a personal Plus account.

Official references: [Custom Instructions](https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions) · [Projects](https://help.openai.com/en/articles/10169521-projects-in-chatgpt) · [Skills eligibility](https://help.openai.com/en/articles/20001066-skills-in-chatgpt).

## Native Skills in eligible workspaces

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

## Adaptation and attribution

The new communication prompts are an adaptation of [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd), MIT licensed, with ChatGPT-specific limitations and plain-language execution guidance. The original `productivity/i-have-adhd/SKILL.md` is not modified. The ChatGPT Skills interface is currently available to eligible Business, Enterprise, Healthcare, and Edu users, subject to workspace settings; it is not a general automatic synchronization of this GitHub bundle.
