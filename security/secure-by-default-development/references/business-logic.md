# Business-Logic Abuse Security Gate

Use this reference for payments, credits, rewards, coupons, invitations, voting, submissions, exams, inventory, booking, account verification, workflow transitions, quotas, referrals, or any action where repeating/reordering requests can create value or bypass policy.

## Core questions

For every sensitive workflow ask:

- Can the operation be repeated when it should be one-time?
- Can steps be skipped or performed out of order?
- Can the client choose authoritative values such as price, discount, credits, score, role, status, or ownership?
- Can two concurrent requests both pass the same precondition?
- Can a stale/replayed request repeat a side effect?
- Can limits be bypassed with multiple accounts, tenants, IPs, IDs, or alternate endpoints?

## Server-authoritative values

- Recalculate prices, discounts, entitlements, scores, quotas, ownership, and permission-sensitive state on the trusted server from authoritative data.
- Do not accept final amounts/statuses from the client when the server can derive them.
- Validate allowed state transitions explicitly rather than accepting arbitrary status strings.

## Idempotency and replay

- Payment/order/account-security/event handlers should use provider-appropriate idempotency or unique event constraints where duplicate delivery/request is possible.
- One-time tokens/codes/actions must become unusable after success.
- Do not rely on the UI disabling a button to prevent duplicate operations.

## Concurrency

- Protect read-check-write sequences that can race with transactions, conditional updates, uniqueness constraints, row locks, atomic operations, or equivalent mechanisms.
- Test double-submit/concurrent requests for inventory, credits, quotas, invites, redemptions, and state transitions.

## Workflow authorization

- Authorization is checked at each privileged transition, not only at workflow entry.
- A user cannot call a later/internal endpoint directly to bypass required earlier steps.
- Background/admin endpoints require their own authorization and business invariant validation.

## Abuse economics

Bound operations that have real-world or infrastructure cost:

- emails/SMS/push notifications;
- exports/report generation;
- AI/LLM calls;
- media processing;
- invitations/referrals;
- password reset/verification messages;
- coupons/rewards/credits;
- search/scraping-sensitive endpoints.

## Adversarial checks

- submit same request twice quickly -> no duplicate unintended value;
- run two concurrent redemptions/updates -> invariant holds;
- skip workflow step and call final endpoint directly -> rejected;
- alter price/score/role/status in client payload -> server ignores/rejects and derives authoritative value;
- reuse one-time token/event -> rejected/idempotent;
- exceed per-user/tenant/business limit through alternate route -> blocked consistently.

## Release blockers

- client is authoritative for money, credits, permissions, ownership, verification, or security-sensitive status;
- one-time sensitive action can be replayed for repeated effect;
- obvious concurrent double-spend/double-submit race on valuable state;
- workflow can be bypassed by calling internal/final endpoint directly;
- expensive/abusable business action has no reasonable server-side limit.
