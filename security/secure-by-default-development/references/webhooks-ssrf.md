# Webhooks, Outbound Requests & SSRF Security Gate

Use this reference whenever the application receives trusted webhooks or fetches/connects to a URL/host influenced by a user, integration, import, callback, avatar, feed, document, or webhook configuration.

## Inbound webhooks

- Verify the provider's signature/authentication before trusting payload data or mutating state.
- Use the raw request body when the provider's signature scheme requires it.
- Use constant-time comparison where appropriate for secret-derived signatures.
- Validate timestamp/freshness and reject replayed event IDs when supported.
- Keep webhook secrets server-side and separate by environment/provider where possible.
- Validate event type and payload schema after authenticity is established.
- Make handlers idempotent where duplicate delivery is expected.
- Do not treat a secret-looking URL path as sufficient webhook authentication.

## Outbound URL fetching / SSRF

Do not call `fetch(userUrl)` or an equivalent privileged network client without an outbound policy.

At minimum consider:

- allowlisted protocols (normally HTTPS/HTTP only when justified);
- explicit destination/hostname allowlists when the feature permits them;
- rejection of loopback, link-local, private/internal network ranges, unix/file schemes, and cloud metadata destinations;
- DNS resolution/rebinding behavior;
- redirects: re-validate every redirect destination or disable redirects;
- port restrictions;
- response size/time/content limits;
- no automatic forwarding of internal credentials/cookies/authorization headers to user-selected hosts.

When arbitrary public URLs are a legitimate feature, isolate the fetcher from internal networks/secrets where architecture permits instead of relying only on string validation.

## Callback / webhook registration

- Do not permit callbacks to internal/private endpoints without explicit trusted use.
- Verify ownership/challenge flows where a platform supports callback verification.
- Limit how often callbacks can be triggered and how much data is sent.
- Avoid placing secrets or sensitive records into query parameters.

## Adversarial checks

- webhook with missing/wrong signature -> rejected before mutation;
- valid webhook replay -> no duplicate sensitive action when replay defense/idempotency is expected;
- stale timestamp -> rejected when protocol supports freshness;
- URL points to localhost/127.0.0.1/::1/private network/link-local/metadata service -> rejected or unreachable by isolation;
- allowed URL redirects to an internal destination -> rejected;
- user-selected destination does not receive server cookies/cloud credentials/internal auth headers;
- outbound response/body/time limits are enforced.

## Release blockers

- unauthenticated webhook can mutate trusted state;
- webhook signature verification is performed after irreversible side effects;
- arbitrary server-side URL fetch can reach internal/private/metadata networks;
- redirects bypass destination validation;
- outbound requests leak internal credentials or unrestricted sensitive data;
- replayable payment/account/security events have no provider-appropriate replay/idempotency defense.
