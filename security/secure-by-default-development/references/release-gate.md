# Mandatory Security Release Gate

Use this before claiming a security-relevant change, feature, deployment, library, application, firmware, service, or project is production-ready, secure, hardened, or ready to ship.

The purpose is not to prove perfect security. It is to block preventable high-impact mistakes and make unverified risk explicit.

## Verdicts

Use exactly one:

- **SECURITY PASS** — no known release blocker in the reviewed surface; required relevant adversarial checks passed; current advisory/version research was performed when material and available; residual risks are documented.
- **SECURITY WARNING** — no known critical blocker, but meaningful controls/tests/configurations/current advisory research remain incomplete or unverified. Do not describe the result as fully production-hardened.
- **SECURITY BLOCKER** — a release-blocking condition exists. Do not claim production-ready until fixed or an authorized owner explicitly accepts the risk.

## Automatic SECURITY BLOCKER conditions

Mark `SECURITY BLOCKER` when any relevant condition is known to exist.

### Access control

- private/sensitive API, IPC, local control interface, device service, admin path, tool, or privileged action works without required authentication;
- authorization exists only in UI/client/middleware/model reasoning and is absent at the trusted action/data boundary;
- user A can read/write/delete user B's private resource by changing an ID/key/path;
- tenant A can access or infer tenant B's private data;
- normal user can invoke privileged/admin mutation;
- client-controlled `role`, `isAdmin`, `ownerId`, `tenantId`, permission, price, credit, entitlement or security state is trusted as authoritative;
- forgotten legacy/debug/old-version endpoint or local service exposes protected data or privileged behavior.

### Secrets / sessions / cryptography

- private credential/service-role key/database password/signing/encryption key is exposed in client code, mobile/desktop binary, firmware, public env, repository, public logs, model context, image, package or artifact without a justified safe design;
- passwords are stored plain-text or with an unsuitable fast/general-purpose hash;
- reusable sensitive session/reset credentials are exposed without an explicit unavoidable design;
- predictable security/session/reset/device tokens are used;
- signature/authentication token is accepted without required cryptographic verification/issuer/audience/purpose validation;
- production TLS/certificate verification is disabled as a workaround;
- sensitive production cryptography relies on an unreviewed home-grown scheme;
- privileged software/firmware/update artifacts are accepted without required integrity/authenticity verification.

### Database / injection / unsafe execution

- RLS/access policy is disabled/widened only to make functionality work;
- privileged database/service credential bypasses tenant/ownership checks without equivalent server authorization;
- attacker-controlled data is concatenated/interpreted as SQL/NoSQL/shell/template/code/query language in an unsafe way;
- unsafe deserialization or dynamic code/module loading accepts untrusted input;
- destructive operation can be broadened to unrelated records/files/resources by missing or attacker-controlled scope.

### Native / memory / process safety

- known attacker-controlled memory corruption path (out-of-bounds, use-after-free, double-free or equivalent);
- attacker-controlled size/offset/index reaches memory operations without required bounds/checked arithmetic;
- unsafe FFI ownership/lifetime bug is known exploitable or can corrupt privileged state;
- privileged process trusts user-writable DLL/library/plugin/search paths;
- exploitable TOCTOU/symlink/temp-file race crosses a privilege boundary.

### Web / browser

- untrusted raw HTML/script/content executes without deliberate sanitization/isolation;
- private/authenticated data can leak through shared caching to another user;
- CSP/CORS/TLS/auth validation is broadly disabled merely to silence an error;
- credentialed/sensitive API is exposed with an unjustified permissive browser policy.

### Mobile / desktop / local client

- reusable backend/admin/service secret is embedded in mobile/desktop client;
- privileged server action is authorized only by client/device/UI state;
- privileged deep link/intent/URI handler/exported component/IPC is callable without intended authorization;
- untrusted WebView/Electron/browser content can invoke over-privileged native bridge capability;
- desktop privileged localhost/IPC service has no meaningful authorization;
- mobile/desktop production TLS verification is disabled;
- desktop auto-update accepts unsigned/unverified/downgraded privileged code contrary to the security model.

### Files / network / integrations

- unrestricted upload can execute server/trusted-origin code;
- private files are downloadable without authorization;
- path traversal/archive escape can leave an allowed storage root;
- privileged process/server performs arbitrary user/model-controlled URL fetches that can reach internal/private/link-local/cloud-metadata networks;
- trusted webhook/message can mutate sensitive state without authenticity verification;
- replayable sensitive webhook/event has no provider-appropriate idempotency/replay defense.

### AI / LLM / agent systems

- model output or retrieved content is treated as authorization;
- untrusted prompt/document/web/tool output can directly trigger privileged/destructive tools without deterministic policy/authorization;
- cross-user/cross-tenant private RAG/retrieval data can leak;
- model-generated shell/SQL/code/path/URL is executed without risk-appropriate validation, constraints or sandboxing;
- prompt injection can exfiltrate secrets/private data through available tools;
- over-privileged agent loops can cause material uncontrolled cost/resource/destructive effects without bounds.

### Embedded / IoT / firmware

- privileged firmware/update path accepts unauthenticated/unsigned code where authenticity is required;
- fleet-wide hardcoded admin/cloud credential is present in firmware;
- unauthenticated privileged LAN/radio/device-control service exists;
- production debug/test interface exposes sensitive control/secrets without deliberate protection;
- known remotely reachable memory-corruption/parser issue exists;
- recovery/downgrade path bypasses core security without explicit design/risk acceptance.

### Business logic

- client is authoritative for money, credits, rewards, scores, ownership, entitlement, security state or privileged workflow state;
- one-time high-value action can be replayed for repeated effect;
- obvious double-submit/race condition allows duplicate value or bypasses quotas/state rules;
- final/internal workflow endpoint can be called directly to skip required security/business steps.

### Supply chain / infrastructure

- cracked/nulled dependency/plugin/theme;
- suspicious dependency/install script gets privileged secrets/host access without review;
- known exploitable critical dependency/framework/runtime vulnerability affects the shipped/resolved version with no mitigation/risk decision;
- public unauthenticated database/cache/admin/debug/control service;
- production secret baked into image/public build/package artifact;
- application/deployment is made to work by granting unexplained root/privileged/`777`/wildcard access;
- untrusted build/PR code can access production write credentials/secrets without an explicit isolated design.

### Monitoring / exceptional conditions

Use a blocker for high-risk systems when:

- a critical auth/policy/signature/security dependency failure silently fails open;
- logs contain reusable passwords/tokens/session secrets/private keys;
- newly introduced long-lived privileged credentials cannot be revoked/rotated safely;
- privileged/high-value mutations are intentionally untraceable and there is no compensating control.

## Minimum adversarial verification matrix

Run only relevant tests, but do not skip an applicable category because the happy path passed.

| Surface changed | Minimum negative/adversarial checks |
|---|---|
| Protected API/action | no-auth; wrong-role; cross-user/cross-tenant; malformed input; legacy/debug exposure |
| Auth/session/OAuth | bad credential; expired/revoked session; replay/reuse; rate limit; wrong state/issuer/audience/redirect as relevant |
| Database/RLS | different users/tenants; unauthorized SELECT/INSERT/UPDATE/DELETE paths used by app |
| Upload/storage | oversize; disallowed/mismatched type; traversal/archive escape; unauthorized download |
| Webhook/message | invalid signature; stale/replay where supported; duplicate idempotency |
| Outbound fetch | localhost/private/link-local/metadata destination; redirect/rebinding path as relevant |
| Business workflow | duplicate/concurrent request; skipped step; client-tampered authoritative values |
| Browser/private data | secret absent from bundle; XSS/raw content path; cache isolation; CSP/CORS as relevant |
| Cryptography/token/update | unpredictability; expiry/purpose; modified signature/artifact; wrong key/issuer/audience; TLS verification; downgrade if relevant |
| Native/parser | malformed/truncated/oversized input; bounds; sanitizer/fuzzer/static-analysis evidence when project supports it |
| Mobile | tampered client state; deep link/intent/exported component; local storage/log leakage; WebView bridge; TLS |
| Desktop | IPC/localhost auth; URI/file handler abuse; update signature/downgrade; WebView/native bridge; plugin path |
| AI/LLM | prompt injection; tool authorization; cross-tenant retrieval; generated command/URL validation; tool/cost bounds |
| Embedded/IoT | modified firmware; default credentials; unauthenticated device control; debug exposure; malformed protocol input |
| CLI/service/library | command/path injection; secret output; management listener auth; resource bounds; secure default behavior |
| Deployment | public ports/services; runtime privilege; TLS; secret exposure; admin/debug exposure |
| Dependency/runtime | resolved version; provenance; lockfile; current advisories; known exploitation when relevant; install-script/permissions review |
| Monitoring/incident | safe denied-event log; no secret leakage; revocation/rotation path; fail-closed exceptional path |

## Evidence standard

A completion claim should identify:

1. detected project types, stack and resolved versions relevant to the reviewed surface;
2. changed trust boundaries/attack surfaces;
3. standards/security profiles applied;
4. authorization/security invariants protecting them;
5. adversarial tests actually executed and results;
6. version-specific advisory research performed and sources/types used when material;
7. tooling used (tests, requests, browser, DB policy tests, sanitizer/fuzzer, dependency audit, config inspection, etc.);
8. important unverified assumptions;
9. final verdict: PASS / WARNING / BLOCKER.

Do not invent evidence. If the agent lacks access needed to run a critical verification or current advisory research that materially affects release confidence, use `SECURITY WARNING` or `SECURITY BLOCKER` according to risk instead of pretending it passed.

## Risk acceptance

An explicit owner decision can accept a known risk, but the agent must:

- state the exact risk and affected boundary;
- state the safer alternative considered;
- distinguish temporary mitigation from a fix;
- preserve the blocker/warning in the report even if the owner chooses to ship;
- never silently rewrite a blocker as a pass.
