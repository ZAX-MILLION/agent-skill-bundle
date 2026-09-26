---
name: server-triage
description: Investigate a failing site, VPS service, network problem or resource alarm without harming unrelated apps.
---
# server triage

1. Confirm target project and environment using project-inventory.
2. Read health responses, scoped service logs, listeners, dependencies, storage/inodes, memory, CPU, TLS and Nginx routing. Redact secrets.
3. Separate symptom from cause. Do not restart Nginx, PostgreSQL, Docker or the entire server simply because one site fails.
4. Before any production change, capture baseline, exact target, impact and rollback; obtain exact-action approval. Prefer the smallest reversible fix.
5. Verify target function, error logs and at least one neighboring app afterward. Distinguish confirmed root cause from hypothesis.

For code/config/security work also use `security/secure-by-default-development` and `process/verification-before-completion`.
