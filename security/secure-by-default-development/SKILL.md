---
name: secure-by-default-development
description: Mandatory security baseline for any task that creates, modifies, refactors, reviews, fixes, configures, or deploys application code or infrastructure. Use alongside stack-specific skills, especially for authentication, authorization, APIs, databases, secrets, uploads, dependencies, React, Next.js, WordPress, deployment, and production changes. Prevent vulnerabilities during implementation instead of relying only on a final audit.
---

# Secure-by-Default Development

Security is a cross-cutting implementation constraint, not a final checklist.

Use this skill for **every code- or configuration-changing task**. It does not replace specialist security skills; it is the baseline that should remain active while other skills are used.

## Core rule

Do not make a feature work by weakening a security boundary.

If the quickest functional fix requires disabling or broadening authentication, authorization, RLS, CSP, CORS, TLS, input validation, rate limiting, sandboxing, file restrictions, permission checks, secret handling, or another security control, stop and choose a safer implementation.

## Non-negotiable security invariants

1. **The client is never the authority.** UI hiding, disabled buttons, route guards, JavaScript checks, client claims, tenant IDs, user IDs, roles, prices, permissions, or ownership values supplied by the browser are untrusted until verified server-side.
2. **Authentication is not authorization.** Every protected server boundary must verify both who the caller is and whether that caller may perform the requested action on the requested resource.
3. **Deny by default.** Missing identity, missing ownership, ambiguous tenant scope, malformed input, unknown permissions, failed verification, or unavailable security dependencies must fail closed.
4. **Validate at trust boundaries.** Validate and normalize untrusted input in the server/API/action that consumes it. Client-side validation is UX, not a security boundary.
5. **Secrets stay server-side.** Never place private keys, service-role keys, database passwords, signing secrets, privileged API keys, session secrets, or equivalent credentials in browser code, public environment variables, logs, URLs, examples, source control, or error messages.
6. **Use least privilege.** Grant only the minimum database, filesystem, API, cloud, runtime, and user permissions required for the operation.
7. **Sensitive data has a lifecycle.** Minimize collection, avoid unnecessary copies, encrypt where appropriate, keep backups protected, set retention deliberately, and provide deletion/export behavior when the product requires it.
8. **Sessions must resist theft and replay.** Prefer secure server-managed sessions or `HttpOnly`, `Secure`, appropriately `SameSite` cookies. Do not move sensitive session tokens to `localStorage` merely because it is convenient.
9. **Logs are data exfiltration surfaces.** Do not log passwords, cookies, bearer tokens, reset links, secret headers, private keys, full payment data, sensitive personal data, or unrestricted request bodies.
10. **Uploads are hostile input.** Enforce size and type allowlists, validate server-side, generate safe filenames/paths, keep uploaded content outside executable locations where possible, and prevent path traversal or script execution.
11. **Dependencies are supply-chain decisions.** Before adding a package/plugin/SDK, confirm it is necessary, reasonably maintained, appropriately licensed, and not asking for excessive permissions. Preserve lockfiles and run the ecosystem's vulnerability tooling where available.
12. **Security claims require evidence.** Never say a change is secure because the happy path works or because a checklist was read. Verify negative cases and report what was not tested.

## Before changing code: security pre-flight

For the requested change, identify only the relevant items:

- trust boundaries: browser, server, database, third-party service, admin surface, file system, queue, webhook, CLI, deployment host;
- sensitive assets: credentials, sessions, personal data, money/credits, privileged actions, private files, tenant data;
- identities and roles involved;
- resources whose ownership or tenant scope matters;
- attacker-controlled inputs;
- outbound destinations and third parties;
- new dependencies, permissions, public endpoints, uploads, webhooks, background jobs, or configuration changes.

Then state the security invariants that must remain true. Examples:

- a student can only read their own progress;
- changing a URL ID cannot reveal another tenant's record;
- a normal user cannot call an admin action directly;
- a webhook without a valid signature cannot mutate state;
- browser JavaScript never receives the service-role key;
- an uploaded file can never execute as server code.

Do not over-engineer a threat model for trivial text-only changes. Scale the depth to the risk.

## During implementation

### Authentication and authorization

- Verify identity at the server boundary that performs the action.
- Verify role/capability and resource ownership/tenant membership there as well.
- Query with the authorized scope whenever possible instead of loading broadly and filtering later.
- Treat middleware and UI guards as defense-in-depth, not the only authorization check.
- For multi-tenant systems, bind every sensitive query/mutation to the authenticated tenant context.
- Never trust `userId`, `role`, `tenantId`, `isAdmin`, ownership, or price from the client without server verification.

### APIs, actions, webhooks, and forms

- Validate method, content type, schema, ranges, lengths, enum values, IDs, and business invariants.
- Apply rate limits to authentication, password/reset flows, invitations, expensive actions, uploads, public forms, and abuse-prone endpoints.
- Protect state-changing browser requests against CSRF when the session model requires it.
- Verify webhook signatures using the raw payload when required by the provider; reject stale/replayed events when the protocol supports timestamps or event IDs.
- Return minimal errors to clients; keep sensitive diagnostic details in protected server logs.
- Do not send sensitive data in query strings when headers/body are appropriate.

### Database and storage

- Enforce authorization in the application and, where supported, add database-level policies such as RLS as defense-in-depth.
- Do not disable RLS or widen a database policy simply to make a query pass.
- Parameterize database queries; do not concatenate untrusted input into SQL or query languages.
- Keep privileged database/service credentials out of client code.
- Encrypt sensitive data and backups where the platform/threat model requires it.
- Make destructive operations explicit and scoped; protect bulk delete/update paths.

### Browser / frontend

- Escape output by default and avoid raw HTML injection. If user-controlled HTML is genuinely required, sanitize it with a maintained sanitizer and a restrictive policy.
- Encode untrusted values before placing them in URLs/attributes where the framework does not handle it safely.
- Do not put secrets in frontend bundles or public environment variables.
- Use CSP and other response headers as defense-in-depth where applicable.
- Do not rely on source-map hiding, minification, or obscurity to protect secrets.

### Filesystem and uploads

- Block traversal (`../`, encoded variants, absolute paths) by resolving against an allowed root and verifying the final path.
- Do not trust filename extensions or client MIME headers alone.
- Restrict file size, count, type, and processing cost.
- Keep uploads non-executable and serve them with safe content disposition/type policies as appropriate.

### Dependencies, SDKs, plugins, and third parties

- Prefer existing project/framework capabilities over adding a new dependency for a small task.
- Review package/plugin provenance and maintenance before installation.
- Check what telemetry/data a third-party SDK sends and whether it needs access to sensitive data.
- Do not install nulled/cracked packages, themes, or plugins.
- Run dependency vulnerability checks when supported; do not blindly auto-fix breaking upgrades without review.

### Configuration and deployment

- Enforce HTTPS in production and avoid mixed content.
- Configure CORS to the required origins/methods/headers; do not use a broad `*` as a convenience fix for credentialed or sensitive APIs.
- Configure CSP deliberately; do not add broad `unsafe-inline`, `unsafe-eval`, or wildcard sources just to silence errors unless the risk is understood and explicitly accepted.
- Keep production debug output and sensitive stack traces disabled from public responses.
- Use least-privilege runtime users, filesystem permissions, cloud roles, and deployment credentials.
- Never commit `.env` files or secrets.

## Stack overlays

Read `references/stack-checklists.md` only for the stack being changed.

- **General application:** data storage, authentication, API/server authorization, privacy, permissions, third parties, logs, dependencies, notifications.
- **React:** XSS, `dangerouslySetInnerHTML`, browser secrets, token storage, server-side protected-resource checks, CORS, CSP, production debug/source-map exposure.
- **Next.js:** Server/Client boundaries, Route Handlers, Server Actions, `NEXT_PUBLIC_`, middleware as defense-in-depth, uploads/images, CSP and deployment headers.
- **WordPress:** core/plugin/theme maintenance, capabilities/nonces, sanitization/escaping, prepared queries, uploads, filesystem/admin hardening, plugin trust, login protection, backups, WAF, XML-RPC when unused.

Some WordPress hardening measures based on obscurity (for example changing the login URL or database prefix) can be defense-in-depth but are **not substitutes** for strong authentication, authorization, updates, least privilege, rate limiting, and secure code.

## Verification gate before completion

Run the smallest meaningful security verification for the changed surface. Prefer behavioral tests over text searches.

### Required negative checks when relevant

- unauthenticated caller is rejected;
- authenticated but unauthorized caller is rejected;
- user A cannot access user B's resource by changing an ID;
- tenant A cannot access tenant B data;
- invalid/malformed/out-of-range input is rejected;
- missing/invalid webhook signature is rejected;
- oversized/disallowed upload is rejected;
- path traversal is rejected;
- secret values are absent from client bundles/logs/source control;
- security headers/CORS/CSP behave as intended;
- dependency audit does not reveal an introduced known critical/high issue that is being ignored without explanation.

### Completion questions

Before claiming completion, answer:

1. What trust boundary changed?
2. What authorization rule protects it?
3. What attacker-controlled input is validated and where?
4. Did any secret, permission, dependency, public endpoint, upload, or third party change?
5. What negative/security test was run?
6. What security-relevant item remains unverified?

If a relevant question cannot be answered, the task is not security-complete.

## Stop conditions

Stop and surface the issue instead of silently weakening security when:

- required identity/ownership/tenant information is unavailable;
- a requested implementation would expose a secret to the client;
- a fix requires disabling auth, authorization, RLS, TLS, CSP, validation, rate limiting, or another security control without an explicit risk decision;
- a dependency/plugin is suspicious, abandoned, opaque, or requests excessive privilege and no safe alternative has been evaluated;
- production credentials or private data appear in source control or logs;
- verification demonstrates cross-user/cross-tenant access;
- the agent lacks the tool/access needed to verify a critical security assumption.

## Reporting

For security-relevant code changes, keep the report compact:

- **Protected:** security invariants preserved/added.
- **Verified:** negative/security checks actually run.
- **Residual:** anything important not verified or requiring operator configuration.

Do not claim perfect security. The goal is to avoid preventable mistakes, preserve explicit trust boundaries, and make residual risk visible.
