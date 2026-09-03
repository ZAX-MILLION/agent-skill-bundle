# Authorization & Multi-Tenant Security Gate

Use this reference whenever users, roles, organizations, tenants, teams, ownership, admin actions, private records, shared resources, or row-level policies are involved.

## Core model

For every protected action answer all four:

1. Who is the caller?
2. What capability/role are they allowed to exercise?
3. What exact resource are they operating on?
4. Why does that caller have access to that resource in this tenant/context?

Authentication alone answers only question 1.

## Required patterns

- Derive caller identity from the trusted server session/token, not a request field.
- Derive tenant/organization scope from trusted membership data where possible.
- Authorize every server-side read and mutation, including background/admin-style endpoints that a normal browser does not expose.
- Use explicit allowlists for fields a caller may mutate.
- Keep role/capability assignment itself behind stricter authorization than ordinary profile editing.
- Prefer scoped queries such as `WHERE tenant_id = trustedTenant AND id = requestedId` over unscoped fetch-then-check patterns.
- Treat exports, search, counts, analytics, file downloads, and indirect references as data access too.

## BOLA / IDOR checks

Test direct object references by changing:

- numeric IDs;
- UUIDs;
- slugs;
- filenames/object keys;
- parent IDs;
- tenant/team IDs;
- nested resource IDs;
- pagination/filter parameters that can widen scope.

Unpredictable UUIDs are not authorization.

## Privilege escalation checks

Reject or safely ignore client attempts to set fields such as:

- `role` / `roles`;
- `isAdmin` / `admin`;
- `verified` / `approved`;
- `ownerId` / `userId` / `tenantId`;
- `permissions` / `capabilities`;
- `balance` / `credits` / `price` / `discount`;
- workflow/security status fields.

## Cross-tenant invariants

- Tenant A cannot read, update, delete, enumerate, export, search, or infer Tenant B's private data.
- Cache keys for authenticated/tenant data include the relevant identity/scope and cannot leak one tenant's response to another.
- Background jobs carry an explicit trusted tenant/user context rather than using a global privileged context without filtering.
- Service/admin credentials do not silently bypass tenant scoping in application logic.

## Adversarial test matrix

For every new sensitive resource/action, test at least the relevant cells:

| Caller | Own resource | Other user same tenant | Other tenant | Admin action |
|---|---|---|---|---|
| unauthenticated | reject | reject | reject | reject |
| normal user | allow if intended | reject unless explicitly shared | reject | reject |
| tenant admin | per policy | per policy | reject | only tenant-scoped admin |
| platform admin | explicit audited policy | explicit | explicit | explicit |

## Release blockers

- authorization exists only in UI/middleware;
- changing an ID allows cross-user or cross-tenant access;
- client-controlled role/tenant/owner fields determine authorization;
- privileged service credentials are used to bypass RLS/authorization without recreating equivalent checks;
- shared cache can mix authenticated users/tenants;
- normal users can invoke admin mutations directly.
