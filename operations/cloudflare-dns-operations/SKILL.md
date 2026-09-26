---
name: cloudflare-dns-operations
description: Review and safely change Cloudflare DNS, proxy status and domain TLS settings.
---
# cloudflare dns operations

1. Verify zone, exact record, TTL, proxy mode, origin and affected application before proposing changes.
2. Check neighboring mail, certificate validation, API and admin records. Do not rewrite a whole zone.
3. Prepare before/after record diff and rollback. Request approval for production DNS, access, nameserver and TLS changes.
4. Use scoped credentials or authorized integration, never paste API keys. Check authoritative DNS plus HTTP/TLS afterward; describe propagation uncertainty.

For code/config/security work also use `security/secure-by-default-development` and `process/verification-before-completion`.
