---
name: secure-server-access
description: Configure bounded SSH or MCP access for an AI server assistant without exposing credentials.
---
# secure server access

1. Distinguish assistant workstation, remote relay and production server; a skill does not itself connect anything.
2. Prefer dedicated non-root identity, scoped SSH key or MCP, host-key checking, exact allowed paths/services and revocation procedure.
3. Keep private keys, tokens, passwords and full environment files out of chat, Git and logs. Verify only harmless identity/hostname first.
4. Keep read-only diagnosis separate from deploy rights. Require review for privilege escalation, credentials, production writes and destruction.
5. Never disable host key verification or open public management ports merely to make an integration work.

For code/config/security work also use `security/secure-by-default-development` and `process/verification-before-completion`.
