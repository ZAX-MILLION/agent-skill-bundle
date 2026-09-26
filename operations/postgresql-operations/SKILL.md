---
name: postgresql-operations
description: Diagnose and maintain isolated PostgreSQL databases and clusters safely.
---
# postgresql operations

1. Verify project, cluster, port, database, role and environment; never assume default port or cluster.
2. Use read-only health, connections, locks, storage and scoped logs first; do not print sensitive records.
3. Require reviewed migration, backup/restore test, compatibility plan and approval for production writes. Use scoped roles and parameterized queries.
4. Verify app behavior and other clusters after changes; never restart all clusters to resolve a single database issue.

For code/config/security work also use `security/secure-by-default-development` and `process/verification-before-completion`.
