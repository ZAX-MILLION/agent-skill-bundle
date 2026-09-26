---
name: backup-recovery
description: Verify backup coverage and test recoverability of files, databases, releases and configuration.
---
# backup recovery

1. Inventory project assets, PostgreSQL clusters, offsite copies, retention, encryption and last successful backup without dumping sensitive data.
2. Do not equate backup file existence with successful restore. Rehearse recovery in an isolated environment with separate credentials.
3. Verify restored schema, relevant data counts, uploaded files and application health. Capture restore date and any gap.
4. Never restore, prune, delete or overwrite production data without precise target, current-state snapshot when feasible and approval.
5. Report coverage, demonstrated restore status and uncertainty.

For code/config/security work also use `security/secure-by-default-development` and `process/verification-before-completion`.
