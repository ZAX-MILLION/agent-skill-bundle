# AI / LLM / Agent Security Profile

Use for applications that call language models, use RAG, ingest external content, expose model tools/functions, run agents, generate executable code, or allow model output to influence privileged actions.

## Core rule

**Model output and retrieved content are untrusted input.** A model is not an authorization engine and a prompt is not a security boundary.

## Discover

- system/developer/user prompt boundaries;
- external documents, web pages, emails, files or database content injected into context;
- RAG/vector-store ingestion and retrieval permissions;
- tool/function definitions and permissions;
- browser/shell/filesystem/database/cloud actions available to the model;
- secrets placed in model context;
- cross-user/tenant conversation or retrieval storage;
- model-generated code/SQL/commands/templates;
- webhook/agent-to-agent messages;
- human confirmation gates for consequential actions;
- model/provider data retention/privacy settings.

## Required controls

- Treat indirect prompt injection from documents/web/email/tool output as attacker-controlled instructions, not authority.
- Keep authentication/authorization outside model reasoning; server-side code verifies every privileged tool/action.
- Scope tools to least privilege and the authenticated user/tenant; do not give a broad service credential to the model when a narrow server tool can enforce policy.
- Separate data from instructions where the platform supports it, but do not assume formatting alone prevents prompt injection.
- Validate/parameterize model-generated SQL, shell commands, URLs, paths and code before execution; prefer constrained structured tools over arbitrary execution.
- Do not place reusable secrets in prompts/context unless strictly necessary and controlled; redact provider logs/traces where required.
- RAG retrieval must enforce source authorization before content reaches the model.
- Treat model-generated URLs/outbound requests under the same SSRF rules as user-controlled URLs.
- Require confirmation or deterministic policy for irreversible/high-impact actions when appropriate.
- Bound loops/tool calls/tokens/costs and prevent uncontrolled recursive agents/resource abuse.

## Adversarial checks

- malicious document/web page cannot instruct the system to expose secrets or bypass permissions;
- user A cannot retrieve user B/tenant B private embeddings/documents;
- model cannot call admin/financial/destructive tool outside caller authorization;
- tool arguments are validated independently of model output;
- generated shell/SQL/path/URL cannot bypass injection/SSRF/path controls;
- repeated/recursive agent behavior is bounded;
- sensitive prompt/tool data is not unnecessarily retained/logged by provider or app.

## Release blockers

- model decides authorization without deterministic server enforcement;
- untrusted retrieved content can directly trigger privileged tools with no independent policy;
- broad service/admin credentials exposed to model/tool context unnecessarily;
- cross-tenant RAG retrieval leakage;
- arbitrary generated shell/code/SQL executed without validation/sandbox/authorization appropriate to risk;
- prompt injection can cause secret/data exfiltration through available tools;
- consequential agent loops are unbounded enough to cause material resource/cost abuse.
