# Cryptography & Integrity Security Gate

Use this reference for encryption, hashing, signatures, tokens, random IDs/codes, password storage, signed URLs, artifact verification, sensitive data at rest, or key management.

## Do not invent cryptography

- Use established platform/framework cryptographic primitives and protocols.
- Do not design custom encryption, signature, password hashing, token, or key-derivation schemes unless the task is explicitly cryptographic and expert-reviewed.
- Do not use encoding (Base64/hex), compression, obfuscation, or encryption without authentication as a substitute for real security.

## Passwords

- Use a password hashing function designed for password storage (for example Argon2id or appropriately configured bcrypt when supported).
- Never store plaintext passwords or fast general-purpose password hashes such as raw MD5/SHA-*.
- Use the framework/provider's secure password APIs rather than hand-rolling salt/compare logic where possible.

## Randomness and tokens

- Security tokens, reset codes, API secrets, nonces, session identifiers, and unguessable object capabilities require a cryptographically secure random source.
- Do not use timestamps, sequential IDs, `Math.random()`, weak PRNGs, or predictable concatenations for security tokens.
- Give tokens explicit purpose, scope, expiry, and one-time/revocation behavior where appropriate.

## Encryption

- Prefer authenticated encryption modes/APIs that provide confidentiality and integrity.
- Never use hardcoded encryption keys or reuse a single secret broadly across unrelated environments/purposes without deliberate key separation.
- Store keys separately from ciphertext when platform architecture permits.
- Define rotation/recovery behavior for long-lived sensitive keys.
- Encryption at rest does not replace authorization: an application that decrypts data for any caller is still broken.

## Signatures / integrity

- Verify signatures before trusting signed data or performing side effects.
- Verify algorithm, key, issuer/audience/purpose/context as applicable; do not merely check that a signature field exists.
- Use constant-time comparison for secret-derived MAC/signature values where the API does not already handle it.
- Verify downloaded/build artifacts using trusted ecosystem integrity/signature mechanisms when applicable.

## TLS

- Use HTTPS/TLS for sensitive production traffic.
- Do not disable certificate validation to fix development/production connectivity.
- Avoid custom "trust all certificates" handlers outside explicitly isolated test fixtures.

## Adversarial checks

- generated security tokens are not predictable/reused;
- expired/wrong-purpose token is rejected;
- modified signed payload is rejected;
- wrong key/issuer/audience/context is rejected where relevant;
- encryption keys/secrets do not appear in client code/repository/logs;
- TLS certificate verification remains enabled in production paths.

## Release blockers

- plaintext/unsuitably hashed passwords;
- predictable security/reset/session tokens;
- hardcoded production encryption/signing keys in source/client artifacts;
- signature accepted without actual cryptographic verification;
- certificate/TLS validation disabled as a production workaround;
- home-grown cryptography used for sensitive production data without a strong explicit justification/review.
