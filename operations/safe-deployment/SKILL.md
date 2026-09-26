---
name: safe-deployment
description: Perform scoped, reversible web/service deployments on multi-project infrastructure.
---
# safe deployment

1. Read project instructions, repo/ref, active release, app service and database ownership. Keep other projects untouched.
2. Preflight clean source, tests, dependencies, build artifact, disk space, health checks, backups and potential database compatibility.
3. Stage and validate first. Record immutable release ID, prior version and rollback procedure. Request approval before production mutation.
4. Deploy only target resources. Test external and internal health, functionality, logs and security negative checks; sample a neighboring site.
5. On failure stop rollout, use proven rollback, and disclose non-reversible migrations. Log exact version and what was actually verified.

For code/config/security work also use `security/secure-by-default-development` and `process/verification-before-completion`.
