# Secure-by-Default Reference Router

Load only the references relevant to the changed surface. `SKILL.md` remains the always-on baseline.

| Change touches | Read |
|---|---|
| API route, RPC, Server Action, backend endpoint | `api-security.md` |
| Login, signup, sessions, reset, MFA | `auth-session.md` |
| Users, roles, admin, tenant/team/ownership | `authorization-tenancy.md` |
| Database, Supabase, Postgres, RLS, ORM, storage policies | `database-rls.md` |
| Untrusted input reaching SQL/shell/HTML/path/template/redirect | `input-injection.md` |
| Uploads, files, object storage, archives, downloads | `uploads-storage.md` |
| Webhooks, callbacks, URL fetch/import, outbound requests | `webhooks-ssrf.md` |
| React/Next.js/browser code, CSP, CORS, caching | `browser-security.md` |
| Packages, plugins, SDKs, containers, CI actions | `supply-chain.md` |
| Payments, credits, rewards, quotas, workflow/state transitions | `business-logic.md` |
| Secrets, logs, analytics, privacy, backups, exports | `secrets-logging-privacy.md` |
| Docker, nginx, server/cloud/CI/deployment config | `infra-deployment.md` |
| React / Next.js / WordPress / general stack audit overlay | `stack-checklists.md` |
| Production-ready/completion claim | `release-gate.md` |

## Rule

Do not load every reference by default. Progressive disclosure keeps the AI focused and reduces contradictory or irrelevant instructions.

When a task crosses multiple trust boundaries, load multiple references. For example:

- Next.js authenticated upload -> `api-security.md` + `authorization-tenancy.md` + `uploads-storage.md` + `browser-security.md` + `stack-checklists.md`.
- Supabase multi-tenant feature -> `authorization-tenancy.md` + `database-rls.md` + `api-security.md`.
- Stripe-style webhook -> `webhooks-ssrf.md` + `business-logic.md` + `secrets-logging-privacy.md`.
- Production Docker/nginx deployment -> `infra-deployment.md` + `secrets-logging-privacy.md` + `supply-chain.md`.

Before a production-ready claim, always apply `release-gate.md` to the changed surfaces.
