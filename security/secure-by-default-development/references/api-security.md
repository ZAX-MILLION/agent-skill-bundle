# API Security Gate

Use this reference whenever a change adds or modifies an API route, RPC, Server Action, webhook receiver, public endpoint, or backend handler.

## Default posture

- Treat every new endpoint as private unless it is explicitly documented as public.
- Authentication and authorization are separate checks.
- Never trust IDs, tenant identifiers, roles, prices, ownership claims, or permission flags supplied by the client.
- Reject ambiguous identity or scope. Fail closed.

## Required controls

1. **Authentication**
   - Protected endpoints verify the active session/token server-side.
   - Expired, malformed, revoked, or missing credentials are rejected.

2. **Authorization**
   - Verify role/capability and object ownership or tenant membership for the exact requested resource.
   - Scope queries by the authenticated principal/tenant where possible.
   - Do not load all records and filter in application memory when the datastore can enforce scope.

3. **Input validation**
   - Validate body, query, path params, headers, method, content type, ranges, lengths, enums, IDs, and business invariants.
   - Reject unknown privileged fields instead of blindly spreading request objects into database writes.

4. **Output minimization**
   - Return only fields required by the caller.
   - Never expose password hashes, reset tokens, internal secrets, privileged metadata, private keys, service credentials, or unrestricted user objects.

5. **Abuse controls**
   - Rate-limit login, signup, password reset, invitations, exports, search, uploads, email/SMS sending, AI/LLM calls, and other expensive or abuse-prone actions.
   - Bound pagination, batch size, body size, recursion, filtering complexity, and processing time.

6. **Transport and browser boundaries**
   - Require HTTPS in production.
   - Configure CORS to only the origins/methods/headers needed. CORS is not authentication.
   - Consider CSRF for cookie-authenticated state changes.

7. **Error handling**
   - Do not expose stack traces, SQL errors, internal paths, secrets, token parsing details, or tenant existence.
   - Log enough to investigate while keeping sensitive values redacted.

## Adversarial checks

When relevant, verify:

- no-auth request -> rejected;
- user A requests user B's object ID -> rejected;
- tenant A requests tenant B's object -> rejected;
- normal user calls admin route directly -> rejected;
- request adds privileged fields such as `role`, `isAdmin`, `verified`, `balance`, `ownerId`, or `tenantId` -> rejected/ignored according to an explicit allowlist;
- oversized body/batch/page size -> rejected;
- malformed method/content-type/schema -> rejected;
- repeated sensitive action hits an abuse control.

## Release blockers

Do not mark production-ready if any of these are true:

- a private endpoint works without valid authentication;
- authorization relies only on hidden UI or route visibility;
- changing an object ID crosses users or tenants;
- privileged properties can be mass-assigned;
- secrets or private data are returned unnecessarily;
- a sensitive/expensive endpoint has no reasonable abuse bound;
- credentialed/sensitive APIs are opened with permissive CORS as a convenience fix.
