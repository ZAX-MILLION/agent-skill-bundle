# Infrastructure & Deployment Security Gate

Use this reference for Docker, nginx/reverse proxies, cloud roles, server users, CI/CD, deployment scripts, environment configuration, DNS/TLS, containers, filesystem permissions, databases, queues, and production runtime changes.

## Network exposure

- Expose only ports/services that must be reachable.
- Bind internal services/databases/admin interfaces to private/internal networks where possible.
- Require TLS/HTTPS for production user traffic and sensitive service-to-service traffic as appropriate.
- Do not expose debug/admin/metrics/database ports publicly as a convenience workaround.
- Restrict origin access when a CDN/WAF/reverse proxy is intended to be the public boundary.

## Runtime identity and privilege

- Run applications as non-root/unprivileged identities unless root is genuinely required.
- Use least-privilege filesystem permissions, cloud/IAM roles, database accounts, API tokens, and deployment credentials.
- Avoid broad `chmod 777`, wildcard sudo permissions, privileged containers, host networking/mounts, or unrestricted Docker socket access.
- Separate deployment privileges from application runtime privileges where practical.

## Containers

- Use trusted/pinned base images according to project policy and keep them updated.
- Do not bake secrets into image layers or Dockerfiles.
- Minimize packages/tools in production images.
- Use read-only filesystems/capability drops/seccomp/no-new-privileges where compatible and warranted.
- Do not run with `--privileged` or mount host-sensitive paths merely to fix permissions.

## Reverse proxy / HTTP boundary

- Redirect HTTP to HTTPS when applicable.
- Forward trusted proxy headers deliberately; do not trust arbitrary client-supplied forwarding headers when making security decisions.
- Set request/body/time limits appropriate to the app.
- Avoid exposing internal server/version/debug detail unnecessarily.
- Configure security headers at the application or proxy without conflicting/duplicate unsafe overrides.

## Secrets and environment

- Store deployment secrets outside the repository and avoid printing them in CI logs.
- Production and development credentials should be separated.
- Limit who/what can read environment files/secret stores.
- Ensure backups/config exports do not accidentally include unprotected secrets.

## CI/CD and deploy safety

- Treat PR/fork code as untrusted around production secrets.
- Avoid running untrusted code with write tokens or production credentials.
- Pin/review third-party CI actions/tools according to project policy.
- Deploy from a known revision and keep a rollback path for production-critical changes.
- Health checks should not leak secrets or private operational data.

## Database/cache/service exposure

- Do not expose Postgres/Redis/admin consoles directly to the public Internet without an explicit secured design.
- Require authentication and network restrictions appropriate to the service.
- Disable/default credentials and unused sample/admin endpoints.

## Verification

When relevant verify:

- public listening ports match intended exposure;
- HTTP->HTTPS/TLS behavior;
- application runtime user is non-root where expected;
- secrets are absent from image/repo/public config/log output;
- database/cache/admin services are not accidentally public;
- proxy/CORS/security headers behave on the real production boundary;
- rollback/health checks function without weakening security.

## Release blockers

- public unauthenticated database/cache/admin/debug interface;
- production secret committed or baked into a public/client/image artifact;
- application runs privileged/root solely to bypass permissions issues;
- wildcard filesystem permissions or privileged container used as an unexplained fix;
- untrusted PR/build code can access production secrets/write credentials;
- TLS/auth/access control disabled to make deployment pass.
