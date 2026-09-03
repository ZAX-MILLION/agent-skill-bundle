# Secrets, Logging & Privacy Security Gate

Use this reference for environment variables, credentials, logs, analytics, backups, exports, personal data, notifications, support tooling, and incident/debug output.

## Secret handling

Secrets include API keys, service-role keys, database passwords, signing/encryption keys, private keys, session secrets, bearer tokens, cookies, OAuth client secrets, webhook secrets, recovery credentials, and privileged connection strings.

- Keep secrets server-side and outside source control.
- Public env variables are public; never place secrets in them.
- Use environment/secret-management facilities appropriate to the deployment platform.
- Scope credentials to minimum permissions and separate environments where practical.
- Rotate credentials after confirmed exposure; deleting the leaked file from the latest commit does not un-leak Git history/logs/build artifacts.
- Do not paste production secrets into examples, tests, prompts, issues, PRs, logs, or screenshots.

## Logging

Default to structured, minimal logs.

Never log:

- passwords or password-equivalent values;
- full cookies/session IDs/bearer tokens;
- reset/verification/MFA tokens;
- private keys or secret headers;
- full payment card/auth data;
- unrestricted request/response bodies containing personal or sensitive data.

When identifiers are required for diagnosis, prefer internal request/event IDs and deliberate redaction/truncation.

## Error handling

- Client errors should not reveal stack traces, SQL/schema details, internal file paths, environment values, secret headers, or private infrastructure topology.
- Server logs may contain diagnostics but must still redact credentials and sensitive payloads.
- Production debug modes/endpoints must not expose configuration or secrets publicly.

## Privacy and data minimization

- Collect/store/share only data the feature needs.
- Identify personal/sensitive fields before adding analytics, telemetry, ads, support tools, or third-party SDKs.
- Do not send private application data to third parties merely because an SDK accepts arbitrary metadata.
- Match privacy disclosures/data-safety declarations to actual behavior.
- Support deletion/export/retention requirements where the product requires them.
- Push notification content can appear on lock screens; avoid sensitive visible content by default.

## Backups, exports, and non-production copies

- Treat backups/exports/staging/debug snapshots as sensitive production data when they contain production records.
- Encrypt/protect backups according to the data risk and platform capabilities.
- Apply authorization to exports and generated download links.
- Avoid copying production secrets/data into test fixtures or public bug reports.

## Secret exposure checks

When tools are available, inspect:

- tracked files and Git diffs;
- client bundles/public env configuration;
- CI/build/deployment config;
- logs/debug output;
- container images/build layers;
- source maps/artifacts when relevant.

Do not print the secret itself while verifying exposure.

## Release blockers

- private credential committed or embedded in client/public artifact;
- service/admin key shipped to browser/mobile client;
- logs expose reusable authentication credentials;
- public error/debug endpoint reveals secrets/configuration;
- sensitive export/backup is publicly accessible or missing authorization;
- third-party telemetry receives sensitive user data without a documented need.
