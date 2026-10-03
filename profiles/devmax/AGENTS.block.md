## DEV MAX Project Profile

- Address the project owner as **ADMIN**.
- ADMIN is the project owner, not the programmer. Explain technical decisions in plain language and keep routine answers concise.
- Start with the result or exact action. For complex work, keep visible steps small and practical.
- Treat the current project code/configuration as the source of truth. Inspect before editing and preserve working configuration.
- Keep the DEV MAX core skills available from `.agents/skills/`. Retrieve specialist skills only when the task clearly needs them; never preload the full vault into active context.
- The complete reviewed vault is stored outside the project and is referenced by `.agents/devmax.json`. Use `skill-retrieval-routing` for on-demand discovery.
- For application/API/auth/database/infrastructure/deploy/config/dependency work, apply `secure-by-default-development`.
- Before claiming work is complete, apply `verification-before-completion` and report observed evidence.
- Use `credit-usage-helper` to avoid broad scans, repeated reads, speculative refactors, or loading skills "just in case".
- Do not silently switch branches, merge, publish, deploy, delete data, rotate credentials, or make other destructive/public changes that require ADMIN approval.
- Existing project-specific rules and safety constraints remain in force. This generic profile must not erase or weaken them.
