# Browser & Frontend Security Gate

Use this reference for React/Next.js/client code, cookies, browser storage, CSP, CORS, redirects, embedded content, client caches, and user-rendered content.

## Client trust boundary

- Browser code is attacker-visible and attacker-modifiable.
- Do not place private secrets, service-role keys, signing keys, privileged API keys, database passwords, or server-only logic in client bundles.
- Public environment variables are public by definition. In Next.js, anything exposed via `NEXT_PUBLIC_*` must be safe for every site visitor to read.
- UI hiding, disabled controls, client route guards, and client role checks are UX/defense-in-depth, never authorization.

## XSS and rendering

- Use framework output escaping by default.
- Avoid raw HTML sinks such as `dangerouslySetInnerHTML` unless the feature truly requires HTML.
- Sanitize untrusted HTML with a maintained sanitizer and restrictive policy.
- Treat URLs, CSS, HTML attributes, scripts, SVG, markdown renderers, and rich text as distinct contexts with distinct risks.
- Do not introduce `eval`, `new Function`, unsafe dynamic script injection, or broad CSP exceptions as convenience fixes.

## Sessions and storage

- Prefer `HttpOnly`, `Secure`, appropriately `SameSite` cookies or server-managed sessions for sensitive authentication state.
- Treat `localStorage`, `sessionStorage`, IndexedDB, JavaScript-readable cookies, and client state as exposed to successful XSS.
- Do not store secrets/sensitive records client-side without a deliberate need, lifecycle, and threat model.

## CSP and security headers

- Configure CSP deliberately for the actual app.
- Avoid adding `unsafe-eval`, broad wildcards, or `unsafe-inline` just to silence errors unless the risk is explicitly accepted and no safer design is practical.
- Consider frame protections (`frame-ancestors`), `X-Content-Type-Options`, appropriate referrer policy, and HSTS in production where relevant.
- Headers are defense-in-depth; they do not replace secure server authorization or output handling.

## CORS and CSRF

- CORS is a browser sharing policy, not an authentication mechanism.
- Sensitive APIs should not use permissive origins/credentials as a convenience workaround.
- Cookie-authenticated state changes require CSRF consideration based on the framework/session model.

## Redirects, links, and embedded content

- Validate untrusted redirect destinations; prefer safe relative paths or allowlisted destinations.
- Use appropriate `rel` protections for untrusted/new-window external links where required.
- Sandbox untrusted embedded documents/pages if embedding is necessary.

## Caching and data leakage

- Do not cache personalized/authenticated responses in shared caches without identity/tenant-aware cache keys and correct cache-control.
- In Next.js/CDN/server rendering, verify private data cannot be reused across users because of static/shared caching.
- Do not pass unnecessary sensitive server data into Client Components/serialized hydration payloads.

## Production exposure

- Remove sensitive debug output and test endpoints.
- Source maps are not a secret-control boundary; if production maps expose proprietary/sensitive implementation detail unnecessarily, restrict their public availability, but never rely on disabling source maps to hide secrets.
- Verify browser bundles do not contain server-only secrets.

## Release blockers

- private secret/service credential in client bundle or public env;
- server authorization replaced by UI/client checks;
- untrusted raw HTML rendered without deliberate sanitization;
- broad CSP/CORS weakening solely to make functionality work;
- authenticated/private response can be served from shared cache to another user;
- sensitive session credential moved to JavaScript-readable storage without explicit risk decision when safer session storage is available.
