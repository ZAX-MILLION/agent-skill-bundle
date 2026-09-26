---
name: project-inventory
description: Catalog projects and live services before changing a shared VPS.
---
# project inventory

1. Inspect authorized repos, service names, reverse-proxy mappings, databases, deployment methods and backups read-only. Never search for or disclose credential values.
2. Record project, environment, repository/ref, path, service, domain (private locations redacted), database instance/cluster, health URL, dependencies, backup and last verified date.
3. Distinguish planned, present on disk, running, deployed and verified healthy. Do not infer production status from a repository or directory.
4. Map shared infrastructure and blast radius. Store personal inventory only in private project/workspace files, never in this public bundle.
5. Return a concise verified inventory and unresolved gaps before work proceeds.

For code/config/security work also use `security/secure-by-default-development` and `process/verification-before-completion`.
