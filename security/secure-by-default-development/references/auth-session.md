# Authentication & Session Security Gate

Use this reference for login, signup, password reset, email verification, MFA/2FA, session handling, tokens, logout, account recovery, and privilege changes.

## Passwords and credentials

- Hash passwords with a modern password hashing function supported by the platform (for example Argon2id or appropriately configured bcrypt). Never encrypt or hash passwords with general-purpose fast hashes.
- Never log passwords, one-time codes, reset tokens, session cookies, bearer tokens, private keys, or secret answers.
- Rate-limit credential and recovery flows without relying on rate limits as the only defense.
- Avoid account-enumeration responses where practical.

## Session rules

- Prefer server-managed sessions or cookies with `HttpOnly`, `Secure`, and an appropriate `SameSite` setting.
- Do not move sensitive auth/session tokens to `localStorage` merely for convenience.
- Use reasonable expiry and idle/absolute lifetime according to the application's risk.
- Rotate or re-establish sessions after login and privilege-sensitive changes when supported.
- Logout must terminate the usable server session or revoke/expire the relevant credential where the architecture supports revocation.
- Do not accept expired, malformed, unsigned, incorrectly signed, or wrong-audience/issuer tokens.

## Recovery and verification

- Reset/verification tokens should be random, short-lived, single-use, and bound to the intended account/action.
- Consuming a reset token must invalidate it and any superseded token.
- Do not put reusable credentials in URLs. If a one-time token must appear in a URL, minimize lifetime and prevent it from being logged or reused.
- High-risk account changes should require appropriate re-authentication/step-up verification.

## MFA / 2FA

- Prefer MFA for administrator and other privileged accounts when the product supports it.
- Recovery codes are credentials: store/protect them accordingly and make them one-time where applicable.
- Never let a "remember this device" convenience silently bypass the intended privilege boundary forever.

## Adversarial checks

When relevant, verify:

- invalid password cannot create a session;
- expired/revoked session is rejected server-side;
- logout prevents reuse of the old session where revocation is supported;
- reset token cannot be reused;
- reset token for account A cannot reset account B;
- privilege changes cannot be performed solely by editing client state/claims;
- repeated login/reset attempts hit an abuse control;
- session/token values do not appear in browser-readable storage unless explicitly required and risk-accepted.

## Release blockers

- plain-text/recoverable password storage;
- reusable reset tokens without deliberate design;
- privileged authentication based only on client state;
- sensitive session credentials exposed to browser JavaScript unnecessarily;
- logout UI that leaves the server credential fully usable without an explicit architectural reason;
- authentication endpoints with no brute-force/abuse protection at all.
