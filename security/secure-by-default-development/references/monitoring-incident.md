# Security Monitoring & Incident-Readiness Gate

Use this reference when changes affect authentication, authorization, admin actions, payments, sensitive data, security controls, deployment, logging, rate limits, or externally exposed services.

## Security-relevant events

Where appropriate, record enough information to investigate without logging secrets or excessive personal data.

Consider structured events for:

- authentication success/failure and lockout/rate-limit events;
- password/MFA/recovery changes;
- privilege/role/capability changes;
- sensitive admin actions;
- denied cross-tenant/access-control attempts;
- security configuration changes;
- secret/API-key creation/rotation/revocation (never the secret value);
- webhook signature/replay failures;
- suspicious upload/parser failures;
- high-value payment/credit/workflow transitions;
- deployment/configuration changes.

## Log quality

- Include timestamp, request/event correlation ID, action, result, and a safe actor/resource identifier where useful.
- Redact credentials and sensitive payloads.
- Use consistent event names/severity so alerts can be built reliably.
- Do not treat client-supplied IP/user/tenant fields as authoritative without trusted proxy/session context.

## Abuse visibility

- Repeated authentication failures, password-reset abuse, enumeration attempts, cross-tenant denials, webhook failures, and resource-limit violations should be observable when the risk warrants it.
- Rate limiting should expose operational signals so defenders can distinguish real users from abuse and tune safely.
- Critical failures in auth/policy/security dependencies should be visible rather than silently falling back to permissive behavior.

## Alerting

For high-risk systems, define actionable alerts for events such as:

- sudden admin/privilege changes;
- mass export/deletion;
- repeated cross-tenant authorization failures;
- secret/token misuse indicators;
- unexpected public-service exposure or deployment failures;
- spikes in reset/login/webhook abuse;
- security-control configuration drift.

Avoid alerting on every benign event; noisy alerts become ignored.

## Incident readiness

For production-critical systems, ensure operators can:

- revoke/rotate compromised credentials;
- invalidate sessions/tokens as architecture permits;
- disable/restrict a vulnerable feature without disabling core authentication/security globally;
- identify the deployed revision/configuration;
- restore from protected backups where relevant;
- preserve enough audit evidence to investigate.

## Verification

- trigger representative denied/security events and confirm a safe useful log is produced when expected;
- verify no credentials/secrets appear in logs;
- verify high-risk changes are attributable to a safe actor/resource identifier;
- verify security-control failure is observable and fails closed;
- verify credential/session revocation/rotation procedures exist where the feature creates long-lived credentials.

## Release blockers

Use a blocker when the system has a high-risk security function but:

- critical auth/authorization/security failures silently fail open;
- privileged/high-value mutations are intentionally untraceable with no compensating control;
- incident response requires exposing/reusing hardcoded credentials;
- logs contain reusable secrets/tokens/passwords;
- production operators have no safe way to revoke a newly introduced privileged long-lived credential.
