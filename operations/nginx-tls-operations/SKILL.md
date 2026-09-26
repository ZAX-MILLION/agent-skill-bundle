---
name: nginx-tls-operations
description: Manage Nginx routing, HTTPS certificates and redirects on a shared server.
---
# nginx tls operations

1. Identify exact domain, owning vhost, upstream and certificate; redact private administration endpoints.
2. Read active routing and distinguish CDN/DNS/TLS/app errors before edits. Preserve security headers and authentication.
3. Back up target config, make a minimal diff, run nginx -t and stop on failure.
4. After approval, reload only if necessary and check the target plus an unrelated site. Retain rollback and certificate-renewal details.

For code/config/security work also use `security/secure-by-default-development` and `process/verification-before-completion`.
