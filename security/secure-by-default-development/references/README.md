# Secure-by-Default Reference Router

`SKILL.md` is the always-on orchestrator. Start with `project-discovery.md`, then load only the references that match the discovered project and changed attack surface.

## Always at project start / first security-relevant task

1. `project-discovery.md` — fingerprint languages, frameworks, exact versions, deployment and attack surface.
2. `standards-research.md` — select applicable standards and research current version-specific vulnerabilities when tools permit.

Do not assume the project is a web app.

## Project-type routing

| Detected project/surface | Read |
|---|---|
| Web/SSR/browser app | `browser-security.md` + applicable API/auth/data references |
| API/backend/RPC/Server Action | `api-security.md` |
| Mobile Android/iOS/cross-platform | `mobile-security.md` |
| Desktop/Electron/Tauri/native GUI | `desktop-client.md` |
| C/C++/Rust unsafe/FFI/native parser/system software | `native-systems.md` |
| CLI/daemon/worker/library/SDK | `cli-service-library.md` |
| Embedded/IoT/firmware | `embedded-iot.md` |
| AI/LLM/RAG/agent/tool-calling | `ai-llm-security.md` |
| WordPress/React/Next.js/general app overlay | `stack-checklists.md` |

A repository can match several project types; load all relevant profiles.

## Cross-cutting surface routing

| Change touches | Read |
|---|---|
| Login, signup, sessions, reset, OAuth/OIDC, MFA | `auth-session.md` |
| Users, roles, admin, tenant/team/ownership | `authorization-tenancy.md` |
| Database, Supabase, Postgres, RLS, ORM, storage policies | `database-rls.md` |
| Untrusted input reaching SQL/shell/HTML/path/template/redirect | `input-injection.md` |
| Uploads, files, object storage, archives, downloads | `uploads-storage.md` |
| Webhooks, callbacks, URL fetch/import, outbound requests | `webhooks-ssrf.md` |
| Packages, plugins, SDKs, containers, CI actions | `supply-chain.md` |
| Payments, credits, rewards, quotas, workflow/state transitions | `business-logic.md` |
| Secrets, logs, analytics, privacy, backups, exports | `secrets-logging-privacy.md` |
| Encryption, hashing, signatures, random tokens, TLS integrity | `cryptography-integrity.md` |
| Security logging, abuse visibility, alerts, revocation/incident readiness | `monitoring-incident.md` |
| Docker, nginx, server/cloud/CI/deployment config | `infra-deployment.md` |
| Production-ready/security completion claim | `release-gate.md` |

## Progressive disclosure rule

Do **not** load every reference on every task. The project scan determines which profiles matter; the changed trust boundaries determine which cross-cutting gates matter.

Examples:

- Next.js + Supabase authenticated upload -> `browser-security.md` + `api-security.md` + `authorization-tenancy.md` + `database-rls.md` + `uploads-storage.md` + `stack-checklists.md`.
- React Native app -> `mobile-security.md` + relevant `api-security.md`/`auth-session.md` + `standards-research.md`.
- C++ network daemon -> `native-systems.md` + `cli-service-library.md` + `input-injection.md` + `infra-deployment.md`.
- Electron app with auto-update -> `desktop-client.md` + `supply-chain.md` + `cryptography-integrity.md`.
- LLM agent with tools and RAG -> `ai-llm-security.md` + `authorization-tenancy.md` + `webhooks-ssrf.md` + `secrets-logging-privacy.md`.
- IoT firmware -> `embedded-iot.md` + `native-systems.md` + `cryptography-integrity.md` + `supply-chain.md`.

Before a production-ready, secure, hardened, or equivalent claim, always apply `release-gate.md` to every changed security surface.
