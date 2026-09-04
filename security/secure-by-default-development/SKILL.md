---
name: secure-by-default-development
description: Universal security orchestrator for any software project. Before security-relevant code, configuration, database, dependency, infrastructure, mobile, desktop, native, CLI, embedded, AI/LLM, API, web, or deployment work, fingerprint the project and versions, discover attack surfaces, select applicable current standards and security references, research version-specific vulnerabilities when tools permit, enforce secure-by-default implementation, run adversarial verification, and block unsafe production-ready claims.
---

# Universal Secure-by-Default Development

Security is a development constraint, not a final checklist.

Use this skill for **every software project and every security-relevant code/configuration/data/dependency/infrastructure change**. The project may be web, backend, mobile, desktop, CLI, library, native/system, embedded/IoT, WordPress, infrastructure, or AI/LLM. Never assume the project type before inspecting it.

## Core rule

**Never make functionality work by weakening a security boundary.**

Do not solve problems by broadly disabling authentication, authorization, RLS, validation, CSP, CORS, TLS, signature checks, sandboxing, file restrictions, rate limits, least privilege, dependency integrity, update verification, or equivalent controls.

## Mandatory workflow

### 1. SCAN — fingerprint the project first

Read `references/project-discovery.md`.

Before security-relevant implementation or a full security review, build a compact `PROJECT_SECURITY_PROFILE` from repository/runtime evidence:

- project types and languages;
- frameworks/runtimes and **resolved versions**;
- package managers/lockfiles;
- deployment/container/cloud/OS targets;
- database/storage/auth/session systems;
- public network/API/IPC/admin surfaces;
- files/uploads/parsers/outbound requests/webhooks;
- mobile/desktop/native/embedded/AI-specific surfaces;
- CI/CD, signing/update paths and security tooling already present.

A repository can have several project types. Do not force it into one category.

For a trivial text-only change, do not perform an unnecessary full scan. For a new project, unfamiliar repository, production-readiness review, security audit, or changed trust boundary, scanning is mandatory.

### 2. RESEARCH — use the actual stack and versions

Read `references/standards-research.md`.

Route to security standards based on what was discovered, not what is familiar to the agent. Examples:

- all software -> current CWE high-risk weakness coverage + secure-development guidance;
- web -> OWASP ASVS;
- API -> OWASP API Security;
- mobile -> OWASP MASVS/MASTG;
- desktop/thick client -> OWASP TCASVS;
- supply chain -> ecosystem advisories and trusted supply-chain evidence;
- native/embedded -> applicable memory-safety, parser, privilege, update-integrity and platform guidance.

When web/security-advisory access is available, research vulnerabilities against the **installed/resolved versions**. Prefer vendor advisories, ecosystem/GitHub advisories, OSV/NVD/CVE and CISA KEV as appropriate. Do not declare a version vulnerable or safe from package name alone.

If current vulnerability research cannot be performed, state that limitation; do not invent an all-clear.

### 3. ROUTE — load only relevant security profiles

Read `references/README.md` and load the profiles matching the discovered project and changed attack surface.

Examples include:

- `api-security.md`
- `auth-session.md`
- `authorization-tenancy.md`
- `database-rls.md`
- `input-injection.md`
- `uploads-storage.md`
- `webhooks-ssrf.md`
- `browser-security.md`
- `mobile-security.md`
- `desktop-client.md`
- `native-systems.md`
- `cli-service-library.md`
- `embedded-iot.md`
- `ai-llm-security.md`
- `supply-chain.md`
- `business-logic.md`
- `secrets-logging-privacy.md`
- `cryptography-integrity.md`
- `monitoring-incident.md`
- `infra-deployment.md`
- `stack-checklists.md`

Do not load every reference by default. Progressive disclosure keeps the security reasoning focused.

### 4. PROTECT — preserve universal security invariants

These invariants apply whenever relevant regardless of language/framework:

1. **Untrusted inputs stay untrusted.** Browser/mobile/desktop clients, CLI args, files, messages, network packets, environment/config from weaker trust zones, model output and retrieved content cannot grant themselves authority.
2. **Authentication is not authorization.** Every protected action/data boundary verifies the caller and permission for the exact resource/action.
3. **Deny by default.** Missing identity/scope, malformed input, failed crypto/policy checks, unavailable security dependencies and exceptional conditions fail closed.
4. **Validate at trust boundaries.** Validate structure, size, type, ranges, semantics and business invariants where data enters a trusted component.
5. **Secrets are scoped and non-public.** Never expose reusable private/service/admin credentials through client binaries, public env, repository, logs, URLs, model context, artifacts or firmware unless the architecture explicitly and safely requires disclosure.
6. **Least privilege is default.** Avoid root/admin/service-role/wildcards/`777`/privileged containers/broad IAM as convenience fixes.
7. **Memory/process/file/network boundaries matter.** Prevent injection, path traversal, unsafe parsing, SSRF, unsafe deserialization, memory corruption and uncontrolled execution according to the technology.
8. **Updates and artifacts require integrity.** Privileged software/firmware/update pipelines must not trust unsigned/unverified artifacts where signing/integrity is part of the security model.
9. **Dependencies are executable trust.** Identity, maintenance, vulnerabilities, install scripts, permissions, telemetry and transitive risk matter.
10. **Business logic is security.** Money, credits, quotas, ownership, workflow state, one-time operations and concurrency must remain authoritative and abuse-resistant.
11. **Sensitive data has a lifecycle.** Protect it in storage, transit, logs, backups, exports, analytics and deletion/retention flows according to risk.
12. **Security claims require evidence.** A happy path, compilation success or zero findings from one scanner is not proof of security.

### 5. ATTACK — verify negative/adversarial cases

For each changed trust boundary, run the smallest meaningful adversarial tests supported by the environment.

Examples when applicable:

- no-auth / wrong-role / cross-user / cross-tenant attempts;
- tampered IDs, role, owner, tenant, price, balance or security state;
- malformed, oversized, boundary and unexpected input;
- injection payloads at actual interpreter/query/render boundaries;
- traversal/archive escape and unauthorized file access;
- invalid/replayed webhook or message;
- SSRF to localhost/private/link-local/cloud-metadata targets;
- duplicate/concurrent valuable business actions;
- secret absence from client/binary/log/artifact/history;
- unsigned/tampered/downgraded update rejection;
- mobile deep-link/IPC/WebView abuse;
- desktop localhost/IPC/URI-handler/update abuse;
- native malformed-input/sanitizer/fuzz cases when available;
- AI prompt-injection/tool-authorization/cross-tenant retrieval attempts;
- exposed production ports/admin/debug/database/cache interfaces;
- dependency/advisory checks against resolved versions.

Prefer behavioral evidence over grep/text assertions. Do not run destructive security tests against production without explicit authorization and safe scoping.

### 6. GATE — block unsafe completion claims

Before saying **production-ready**, **secure**, **hardened**, **ready to deploy**, or equivalent for a security-relevant change, apply `references/release-gate.md`.

Use exactly one verdict:

- **SECURITY PASS** — no known blocker in the reviewed surface; relevant negative tests passed; residual risk documented.
- **SECURITY WARNING** — no known critical blocker, but meaningful verification/configuration/current advisory research remains incomplete.
- **SECURITY BLOCKER** — a release-blocking weakness exists.

Never upgrade WARNING/BLOCKER to PASS because the feature works.

## Universal automatic blockers

A known issue is a `SECURITY BLOCKER` when relevant if it includes, for example:

- private/privileged endpoint/service/action without required authentication/authorization;
- cross-user/cross-tenant/privilege escalation;
- client-controlled authoritative role/owner/tenant/price/credit/security state;
- exposed private/service/admin credential;
- disabled/bypassed RLS or equivalent data policy without replacement authorization;
- SQL/NoSQL/OS/template/code injection or unsafe deserialization;
- attacker-controlled memory-corruption path in native code;
- executable/unrestricted upload, traversal or private-file bypass;
- arbitrary privileged SSRF/internal metadata access;
- trusted sensitive webhook/update/message without required authenticity/integrity/replay protection;
- production TLS/signature/update verification disabled;
- public unauthenticated database/cache/admin/debug/control interface;
- insecure privileged desktop/mobile/IPC/deep-link/WebView boundary;
- fleet-wide hardcoded IoT/firmware admin/cloud secret;
- LLM/model output or retrieved prompt content able to bypass deterministic authorization or directly exercise over-privileged tools;
- obvious replay/double-spend/race flaw on valuable state;
- cracked/nulled/suspicious dependency or known exploitable critical dependency issue without mitigation;
- root/privileged/`777`/wildcard access used merely to make deployment function.

## Stop conditions

Stop and surface the issue rather than weakening security when:

- identity/ownership/tenant/security scope cannot be established;
- a requested implementation exposes a secret or privileged capability to an untrusted client/component;
- a security control appears to need disabling to make functionality pass;
- the dependency/update/artifact source is suspicious or unverifiable;
- production credentials/private data appear in source, logs, artifacts or client-delivered code;
- testing demonstrates access-control bypass, injection, memory corruption, unsafe update, data leakage or privilege escalation;
- the agent lacks the access/tooling required to verify a critical assumption.

## Reporting

Keep output concise unless a full audit was requested:

- **Profile:** detected project types/stack/versions and relevant attack surfaces.
- **Protected:** invariants/controls preserved or added.
- **Verified:** adversarial/security checks actually run and current advisory research performed.
- **Residual:** unverified assumptions/operator actions.
- **Verdict:** SECURITY PASS / SECURITY WARNING / SECURITY BLOCKER.

Do not claim perfect security. The target is stronger: **no preventable, obvious security failure should survive because the agent failed to inspect the kind of software it was changing.**
