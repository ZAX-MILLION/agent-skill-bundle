# Stack Security Checklists

Use only the sections relevant to the project being changed. These checklists are implementation prompts, not proof of security by themselves.

## General application

### Data storage
- Sensitive data encrypted at rest where required by the threat model/platform.
- No unnecessary sensitive data stored in browser/local plaintext storage.
- No API keys or secrets hardcoded in source; use protected environment/secret stores.
- Backups containing sensitive data are protected/encrypted appropriately.

### Authentication
- Passwords use a strong password-hashing algorithm such as Argon2 or bcrypt through a maintained framework/library.
- Login/reset/recovery endpoints have abuse/rate limiting.
- Tokens/sessions have deliberate expiry and rotation/revocation behavior.
- Logout invalidates/revokes the server session where the session model supports it.
- 2FA/MFA is available or required for privileged/high-risk accounts when appropriate.

### API and server
- Every protected endpoint performs server-side authentication and authorization.
- Users/tenants can access only data/actions they are authorized for.
- HTTPS is enforced in production.
- All untrusted input is validated at the server boundary.
- Abuse-prone APIs are rate limited.
- Public error responses do not leak stack traces, secrets, queries, tokens, or sensitive internals.

### Permissions
- Request only permissions the application actually needs.
- Explain sensitive permissions such as camera, location, contacts, microphone, or filesystem access to users when applicable.

### Third parties / SDKs / analytics
- Review what each SDK collects and transmits.
- Keep sensitive product/user data separated from third parties unless explicitly required and justified.
- Avoid unnecessary SDK permissions/access.
- Confirm third-party data behavior matches product privacy disclosures.

### Privacy and data lifecycle
- Privacy Policy reflects actual behavior when user data is collected.
- Account/data deletion exists where product/legal requirements call for it.
- Data export exists where product/legal requirements call for it.
- Platform privacy/data-safety declarations match actual collection and sharing.

### General code / operations
- No sensitive data in logs or console output.
- Dependencies are reviewed and vulnerability tooling is run where available.
- Notifications do not expose sensitive data on lock screens/visible previews unless explicitly intended.

## React

### XSS
- Avoid unnecessary `dangerouslySetInnerHTML`.
- Sanitize genuinely required user-controlled HTML with a maintained sanitizer and restrictive policy.
- Do not inject untrusted data into URLs/attributes without framework-safe handling/encoding.

### Keys and secrets
- No private API keys/secrets in frontend code or bundles.
- `.env` files containing secrets are not committed.
- Public and private environment variables are clearly distinguished.

### Authentication and state
- Prefer secure server-managed sessions / `HttpOnly` cookies for sensitive session tokens when architecture permits.
- If browser storage is used for sensitive tokens, document and mitigate the XSS/replay risk rather than treating it as equivalent.
- Protected data/actions are authorized server-side; hiding routes/components is not authorization.

### API calls
- Production calls use HTTPS.
- CORS is restricted to required origins/methods/headers; do not use permissive CORS as a convenience fix.
- Sensitive values are not placed in query parameters when avoidable.

### Dependencies
- Run appropriate dependency audit/update checks.
- Review new packages before adding them, especially low-reputation or minimally maintained packages.

### Build and deployment
- Decide production source-map exposure deliberately; never assume hiding source maps protects secrets.
- Remove sensitive debug output from production.
- Configure CSP and supporting browser security headers deliberately.

## Next.js

### Server vs Client Components
- Secret-bearing or privileged logic stays server-side.
- Sensitive data is not passed unnecessarily to Client Components.
- Treat anything serialized to a Client Component as browser-visible.

### Route Handlers / API routes
- Authentication check before protected data/action access.
- Authorization/ownership/tenant check for the concrete resource/action.
- Request schema and business-rule validation.
- Rate limiting on login/signup/reset/uploads/expensive or abuse-prone routes.

### Environment variables
- `NEXT_PUBLIC_*` is browser-visible; no secrets there.
- Private secrets remain non-public and server-only.
- `.env` files with real secrets stay out of Git.

### Authentication
- Prefer `HttpOnly` secure cookies / maintained auth framework patterns over storing sensitive sessions in `localStorage`.
- Middleware may reject obviously unauthorized navigation, but server handlers/actions must still enforce authorization.

### Server Actions
- Every sensitive Server Action verifies identity and authorization inside the action.
- Validate all action input inside the server action.
- Return only data the caller needs and is authorized to receive.

### Images and uploads
- Validate upload type, size, count, filename/path and processing cost server-side.
- Restrict remote image hosts/domains/patterns to trusted destinations.

### Headers and deployment
- Configure CSP intentionally for the app's real resource needs.
- Enforce HTTPS in production.
- Run dependency vulnerability checks and review upgrades.

## WordPress

### Updates and provenance
- WordPress core is supported/current for the deployment policy.
- Plugins/themes are updated and still maintained.
- Remove abandoned/unsupported components when a supported alternative is available.
- Do not use nulled/cracked plugins or themes.

### Login and privilege
- Avoid default/shared administrator credentials.
- Rate limit login/recovery abuse.
- Use 2FA/MFA for administrator/privileged accounts where feasible.
- Treat login-URL changes or IP restrictions as optional defense-in-depth, not a replacement for strong authentication/rate limiting.

### WordPress application security
- Sensitive actions verify capabilities (`current_user_can` or the appropriate capability model).
- State-changing browser actions use and verify WordPress nonces where appropriate; remember nonces are CSRF defenses, not authorization.
- Sanitize/validate input on ingestion and escape output for the output context.
- Use `$wpdb->prepare()` or safe WordPress APIs for dynamic database queries.
- REST/AJAX endpoints define explicit permission checks/callbacks.

### Files and uploads
- `wp-config.php` and secret files are not publicly readable.
- Filesystem permissions follow least privilege; do not recursively loosen permissions as a generic fix.
- Disable dashboard file editing in production when operationally appropriate (`DISALLOW_FILE_EDIT`).
- Prevent PHP/server-side script execution from upload directories.
- Validate uploads and keep them non-executable.

### Database and backups
- Strong unique database credentials with least privilege.
- Automated tested backups appropriate to the site.
- Backup access is protected.
- A non-default table prefix can reduce noise from simplistic attacks but is not a primary security boundary.

### Plugins and extensions
- Remove unnecessary plugins.
- Use trusted sources and review broad permissions/integrations.
- Review security advisories for high-exposure plugins.

### General hardening
- Site-wide HTTPS.
- WAF/security tooling when appropriate to the deployment and threat model.
- Disable/restrict XML-RPC if the site does not need it; do not break required integrations blindly.
- Protect forms against spam/automation where needed.
- Protect personal/sensitive user data and maintain appropriate privacy disclosures.

## Audit output

When these references are used for an audit, report:

1. Implemented / verified controls ✅
2. Issues or missing controls ⚠️ with a concrete fix
3. Additional findings not explicitly listed here
4. Anything that could not be verified with the available access/tools
