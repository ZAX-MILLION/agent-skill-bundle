---
name: secure-by-default-development
description: Mandatory security baseline for any task that creates, modifies, refactors, reviews, fixes, configures, or deploys application code or infrastructure. Use alongside stack-specific skills, especially for authentication, authorization, APIs, databases, secrets, uploads, dependencies, React, Next.js, WordPress, deployment, and production changes. Prevent vulnerabilities during implementation instead of relying only on a final audit.
---

# Secure-by-Default Development

Security is a cross-cutting implementation constraint, not a final checklist.

Use this skill for **every code-, configuration-, database-, dependency-, or infrastructure-changing task**. Keep it active while using narrower specialist skills.

## Core rule

**Never make a feature work by weakening a security boundary.**

If the quickest fix requires disabling or broadly weakening authentication, authorization, RLS, CSP, CORS, TLS, validation, rate limiting, sandboxing, file restrictions, secret handling, least privilege, or another security control, stop and choose a safer design.

## Non-negotiable invariants

1. **The client is never the authority.** Browser/mobile/client values such as IDs, roles, tenant IDs, ownership, prices, balances, permissions, verification status, and workflow state are untrusted until server-verified.
2. **Authentication is not authorization.** Every protected server/data boundary verifies both identity and permission for the exact resource/action.
3. **Deny by default.** Missing identity, ambiguous tenant scope, malformed input, failed verification, unknown permission, or unavailable security dependency fails closed.
4. **Validate at trust boundaries.** Client validation is UX; server/API/action/database boundaries enforce security validation.
5. **Secrets stay server-side.** Private/service/admin credentials never enter public env variables, browser bundles, logs, URLs, examples, source control, or public artifacts.
6. **Least privilege is the default.** Do not solve permission problems with root, admin, service-role, wildcard policies, `777`, privileged containers, or broad IAM unless the design genuinely requires it.
7. **Uploads and URLs are hostile input.** Files, paths, archives, callbacks, redirects, and outbound URLs require explicit constraints.
8. **Dependencies are executable trust decisions.** Package/plugin/SDK provenance, permissions, install scripts, vulnerabilities, and data collection matter.
9. **Business rules are security rules.** Money, credits, rewards, quotas, state transitions, one-time actions, and concurrency must be server-authoritative and abuse-resistant.
10. **Logs/backups/exports are data surfaces.** Protect them like production data and redact reusable credentials.
11. **Fail securely on exceptional conditions.** Timeouts, parse errors, unavailable auth providers, failed policy checks, or missing configuration must not silently become allow paths.
12. **Security claims require evidence.** Happy-path success is never sufficient evidence of security.

## Security pre-flight before changes

Scale depth to risk; do not create a giant threat model for trivial text changes.

For the changed surface identify:

- trust boundaries: client, server, database, file/object storage, third party, webhook, queue, admin surface, deployment host;
- sensitive assets: credentials, sessions, personal data, private files, money/credits, privileged actions, tenant data;
- caller identities/roles;
- resource ownership/tenant rules;
- attacker-controlled inputs;
- public endpoints or network destinations;
- new dependencies, permissions, secrets, uploads, callbacks, caches, jobs, or deployment exposure.

Write the security invariants that must remain true. Examples:

- user A cannot read user B's record by changing an ID;
- tenant A cannot enumerate tenant B's data;
- a normal user cannot invoke an admin mutation directly;
- an invalid webhook cannot mutate trusted state;
- a service-role key never reaches browser code;
- an upload cannot execute as server/trusted-origin code;
- a user-controlled URL cannot reach localhost/private/cloud-metadata services;
- the same redemption/payment event cannot create value twice.

## Progressive security references

Read `references/README.md` and load **only the references relevant to the changed surface**.

### Mandatory routing

- API / Route Handler / RPC / Server Action -> `references/api-security.md`
- login / session / reset / MFA -> `references/auth-session.md`
- roles / admin / ownership / multi-tenant -> `references/authorization-tenancy.md`
- database / Supabase / Postgres / RLS -> `references/database-rls.md`
- untrusted data reaches SQL/shell/HTML/path/template/redirect -> `references/input-injection.md`
- uploads / files / object storage / archives -> `references/uploads-storage.md`
- webhooks / callbacks / URL fetch/import -> `references/webhooks-ssrf.md`
- React / Next.js / browser / CSP / CORS / cache -> `references/browser-security.md`
- packages / plugins / SDKs / containers / CI actions -> `references/supply-chain.md`
- payments / credits / quotas / workflow state -> `references/business-logic.md`
- secrets / logs / analytics / privacy / backups / exports -> `references/secrets-logging-privacy.md`
- Docker / nginx / server / cloud / CI/CD / deployment -> `references/infra-deployment.md`
- React / Next.js / WordPress / general checklist overlay -> `references/stack-checklists.md`

A task can require several references. Do not load every reference by default.

## During implementation

### Access control

- Verify identity at the server boundary performing the action.
- Verify role/capability plus resource ownership/tenant membership there as well.
- Prefer queries scoped by trusted identity/tenant instead of broad fetch-then-filter.
- Treat middleware, route guards, hidden buttons, UUID unpredictability, and obscure URLs as defense-in-depth only.
- Explicitly allowlist mutable fields; do not blindly spread request objects into privileged records.

### APIs and abuse resistance

- Validate method, content type, schema, ranges, lengths, IDs, enums, and business invariants.
- Bound request body, page/batch size, query complexity, upload cost, export size, and expensive operations.
- Rate-limit authentication/recovery, invitations, messaging, public forms, expensive APIs, and abuse-prone business actions.
- Return minimal data and minimal public error detail.

### Database and storage

- Parameterize queries and strictly allowlist dynamic identifiers/operators.
- Keep RLS/policy protections intact. Never disable/widen them solely to make a request succeed.
- If privileged/service credentials bypass database policy, recreate equivalent authorization before every operation.
- Protect destructive operations with explicit scope and protect concurrency-sensitive invariants with transactions/constraints/atomic operations when appropriate.

### Browser

- Use framework escaping by default; sanitize genuinely required user-controlled HTML.
- Keep secrets/server-only data out of client components and serialized client payloads.
- Do not weaken CSP/CORS as a convenience fix.
- Review authenticated/private caching so one user's response cannot be served to another.
- Prefer secure server-managed sessions or `HttpOnly` cookies for sensitive authentication state when architecture permits.

### Files and outbound network

- Bound upload types/sizes/counts/processing; keep uploads non-executable and authorization-protected.
- Contain filesystem paths inside an allowed root and block traversal/archive escape.
- Do not perform unrestricted `fetch(userUrl)` from a privileged server. Restrict/isolate outbound requests and block internal/private/metadata destinations.
- Verify webhook authenticity before side effects and apply replay/idempotency protection where the provider/workflow supports it.

### Dependencies and deployment

- Prefer existing project/framework capabilities before adding dependencies.
- Verify dependency identity, maintenance, license, install scripts, permissions, vulnerabilities, and telemetry/data access.
- Keep production secrets outside source/client/image artifacts.
- Do not expose databases, caches, admin/debug consoles, or unnecessary ports publicly.
- Do not use root/privileged containers/wildcard permissions as unexplained functional fixes.

## Mandatory adversarial verification

Security verification must include relevant **negative cases**, not only happy-path tests.

Common required checks:

- unauthenticated caller rejected;
- authenticated wrong-role caller rejected;
- user A cannot access user B's resource;
- tenant A cannot access tenant B;
- client-tampered role/owner/tenant/price/balance/status rejected or ignored by explicit policy;
- malformed/oversized/out-of-range input rejected;
- invalid/replayed webhook rejected or idempotent;
- disallowed upload/traversal rejected;
- unsafe internal SSRF destination blocked;
- service/admin secrets absent from client bundle/logs/repository;
- duplicate/concurrent business action preserves invariants;
- newly introduced dependency has reviewed provenance and no ignored known critical/high issue without explanation.

Use behavioral tests/requests/policy tests where tools permit. Text search alone is not evidence that the boundary works.

## Mandatory release gate

Before saying **production-ready**, **secure**, **done**, **hardened**, or equivalent for a security-relevant change, read and apply:

`references/release-gate.md`

The final security verdict must be one of:

- **SECURITY PASS**
- **SECURITY WARNING**
- **SECURITY BLOCKER**

Do not upgrade WARNING/BLOCKER to PASS because the feature works.

### Examples of automatic BLOCKERs

- private API works without authentication;
- cross-user/cross-tenant access;
- admin action callable by normal user;
- private/service secret exposed client-side or publicly;
- RLS/auth/CSP/CORS/TLS/validation broadly disabled to make functionality work;
- attacker-controlled SQL/shell/template/dynamic-code injection;
- unsigned trusted webhook mutates sensitive state;
- arbitrary server-side URL fetch reaches private/internal/metadata networks;
- unrestricted executable upload/path traversal/private-file bypass;
- public unauthenticated database/cache/admin/debug service;
- obvious replay/double-spend/business-logic flaw on valuable state;
- cracked/nulled/suspicious dependency used without trusted provenance;
- root/privileged/`777`-style access used as an unexplained fix.

## Stop conditions

Stop and surface the issue instead of weakening security when:

- required identity/ownership/tenant information is unavailable;
- implementation would expose a secret to an untrusted client;
- functionality appears to require disabling a security control without an explicit authorized risk decision;
- a dependency/plugin is suspicious, abandoned, opaque, or over-privileged and a safer alternative has not been evaluated;
- production credentials/private data appear in source control, logs, artifacts, or client code;
- verification demonstrates cross-user/cross-tenant/privilege escalation;
- the agent lacks access/tools required to verify a critical assumption.

## Reporting

For security-relevant changes report compactly:

- **Protected:** invariants/boundaries preserved or added.
- **Verified:** negative/security checks actually run.
- **Residual:** important unverified assumptions/operator configuration.
- **Verdict:** SECURITY PASS / WARNING / BLOCKER.

Do not claim perfect security. The purpose is to prevent avoidable security mistakes, fail closed, and make residual risk visible.
