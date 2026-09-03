# Database & RLS Security Gate

Use this reference for database schema, queries, ORM changes, Supabase/Postgres policies, service credentials, storage metadata, migrations, bulk operations, or multi-tenant data access.

## Database authorization

- Application authorization and database authorization should reinforce each other where the platform supports it.
- Enable and maintain RLS/policy controls for client-accessible or multi-tenant tables when appropriate.
- Never disable RLS, widen a policy to everyone, or switch to a service/admin credential merely to make a failing query work.
- If a privileged server credential legitimately bypasses RLS, recreate the full authorization/tenant checks before each operation.

## Query safety

- Parameterize SQL and query-language values. Never concatenate attacker-controlled input into executable query text.
- Do not allow user-controlled column names, table names, sort expressions, operators, or raw filters without strict allowlists.
- Bound pagination, result counts, joins, filters, full-text search, and expensive queries to reduce data leakage and resource abuse.
- Destructive updates/deletes must include explicit scope. Treat missing/empty filters as dangerous.

## Data integrity

- Use database constraints for invariants that must remain true regardless of application path: foreign keys, unique constraints, NOT NULL, check constraints, and transaction boundaries where appropriate.
- Protect money/credits/counters/state transitions from client-provided authoritative values.
- Use transactions or concurrency controls when partial completion would create exploitable state.
- Avoid TOCTOU authorization patterns where permission is checked separately and can change before mutation without a suitable transaction/constraint.

## Sensitive data

- Store only data the product needs.
- Encrypt highly sensitive data where the threat model/platform requires it; keep encryption keys separate from encrypted data when possible.
- Protect backups, replicas, exports, staging copies, and debug snapshots with the same sensitivity as production data.
- Do not expose raw database errors or schema details to clients.

## Supabase-specific guardrails

When Supabase is used:

- `anon`/public client access must be constrained by RLS policies.
- Service-role keys are server-only and must never enter browser bundles, `NEXT_PUBLIC_*`, mobile client source, logs, or public examples.
- Review `USING` and `WITH CHECK` semantics for read/write policies.
- Test policies as different authenticated users/tenants, not only through the service role.
- Storage buckets/objects require ownership/tenant rules just like tables.

## Adversarial checks

- user A queries user B's row directly -> rejected;
- tenant A filters/searches/exports for tenant B -> no leakage;
- client changes owner/tenant foreign key during create/update -> rejected;
- service-role code path still enforces equivalent authorization;
- update/delete without intended filter cannot affect unrelated rows;
- unsafe raw SQL/filter input cannot alter query structure;
- RLS policies are tested for SELECT/INSERT/UPDATE/DELETE paths that exist.

## Release blockers

- RLS disabled or widened only to fix functionality;
- service/admin credential exposed to a client;
- service credential bypasses authorization without replacement checks;
- unparameterized attacker-controlled query construction;
- cross-tenant data access through database/storage policies;
- destructive mutation can run with missing or attacker-broadened scope.
