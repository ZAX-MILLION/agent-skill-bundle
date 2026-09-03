# Mandatory Security Release Gate

Use this reference before claiming a security-relevant change, feature, deployment, or application is production-ready.

The purpose is not to prove perfect security. It is to block preventable, high-impact mistakes and make unverified risk explicit.

## Verdicts

Use exactly one:

- **SECURITY PASS** — no known release blocker in the changed surface; required relevant negative tests passed; residual risks are documented.
- **SECURITY WARNING** — no known critical blocker, but one or more meaningful controls/tests/configurations remain incomplete or unverified. Do not describe the result as fully production-hardened.
- **SECURITY BLOCKER** — a release-blocking condition exists. Do not claim production-ready until fixed or an authorized owner explicitly accepts the risk.

## Automatic SECURITY BLOCKER conditions

Mark `SECURITY BLOCKER` when any relevant condition is known to exist:

### Access control

- private/sensitive API works without valid authentication;
- authorization is implemented only in frontend/UI/middleware and absent at the server action/data boundary;
- user A can read/write/delete user B's private resource by changing an ID;
- tenant A can access/infer tenant B's private data;
- normal user can invoke privileged/admin mutation;
- client-controlled `role`, `isAdmin`, `ownerId`, `tenantId`, permission, price, credit, or security state is trusted as authoritative.

### Secrets / sessions

- private credential/service-role key/database password/signing key is exposed in client code, public env, repository, public logs, or artifacts;
- passwords are stored plain-text or with an unsuitable fast/general-purpose hash;
- reusable sensitive session/reset credentials are exposed without an explicit unavoidable design.

### Database / injection

- RLS/access policy is disabled/widened only to make functionality work;
- privileged database/service credential bypasses tenant/ownership checks without equivalent server authorization;
- attacker-controlled data is concatenated into SQL/NoSQL/shell/template/dynamic code execution;
- destructive database operation can be broadened to unrelated records by missing/attacker-controlled scope.

### Web / browser

- untrusted raw HTML executes without deliberate sanitization/isolation;
- private/authenticated data can leak through shared caching to another user;
- CSP/CORS/TLS/auth validation is broadly disabled merely to silence an error;
- credentialed/sensitive API is exposed with an unjustified permissive browser policy.

### Files / network / integrations

- unrestricted upload can execute server/trusted-origin code;
- private files are downloadable without authorization;
- path traversal can escape an allowed storage root;
- server performs arbitrary user-controlled URL fetches that can reach internal/private/metadata networks;
- trusted webhook can mutate sensitive state without authenticity verification;
- replayable sensitive webhook/event has no provider-appropriate idempotency/replay defense.

### Supply chain / infrastructure

- cracked/nulled dependency/plugin/theme;
- suspicious dependency/install script gets privileged secrets/host access without review;
- public unauthenticated database/cache/admin/debug service;
- production secret baked into image/public build artifact;
- application/deployment is made to work by granting unexplained root/privileged/777-style access.

## Minimum negative verification matrix

Run only relevant tests, but do not skip an applicable category because the happy path passed.

| Surface changed | Minimum negative checks |
|---|---|
| Protected API/action | no-auth; wrong-role; cross-user/cross-tenant; malformed input |
| Auth/session | bad credential; expired/revoked session; replay/reuse where applicable; rate limit |
| Database/RLS | different users/tenants; unauthorized SELECT/INSERT/UPDATE/DELETE paths used by app |
| Upload/storage | oversize; disallowed/mismatched type; traversal; unauthorized download |
| Webhook | invalid signature; stale/replay where supported; duplicate idempotency |
| Outbound fetch | localhost/private/link-local/metadata destination; redirect to blocked destination |
| Business workflow | duplicate/concurrent request; skipped step; client-tampered authoritative values |
| Browser/private data | secret absent from bundle; XSS/raw HTML path; cache isolation; CSP/CORS as relevant |
| Deployment | public ports/services; runtime privilege; TLS; secret exposure; admin/debug exposure |
| Dependency | provenance; lockfile; vulnerability tooling; install-script/permissions review |

## Evidence standard

A completion claim should identify:

1. the changed trust boundary;
2. the authorization/security invariant protecting it;
3. negative tests actually executed and results;
4. tooling used (tests, HTTP requests, browser verification, DB policy tests, dependency audit, config inspection, etc.);
5. important unverified assumptions;
6. final verdict: PASS / WARNING / BLOCKER.

Do not invent evidence. If the agent lacks access needed to run a critical verification, use `SECURITY WARNING` or `SECURITY BLOCKER` according to the risk instead of pretending it passed.

## Risk acceptance

An explicit owner decision can accept a known risk, but the agent must:

- state the exact risk and affected boundary;
- state the safer alternative considered;
- distinguish temporary mitigation from a fix;
- never silently rewrite a blocker as a pass.
