---
name: credit-usage-helper
description: Keep Codex and other credit-metered coding-agent work efficient without trading away correctness: minimize context, agent fan-out, retries, broad scans and unnecessary high-effort work; check usage/status when available; escalate only when evidence justifies it.
---

# Credit Usage Helper

Use this workflow when the user wants to conserve Codex/agent credits, usage allowance, tokens, or expensive agent time.

This is a **budget governor**, not a promise about billing. It cannot read the user's balance unless the active host exposes usage/status. It never weakens security, validation, testing needed for the changed behavior, or explicit user requirements.

## Core rule

Spend reasoning and tool calls where they change the result.

Do not spend credits proving the same thing twice.

## Start with a budget class

Classify the task once:

| Class | Typical work | Default execution |
|---|---|---|
| **S** | one question, tiny fix, one/few files | current thread, no subagent, narrow read/test |
| **M** | feature/bug across a few files | short plan, focused reads, one specialist skill, focused tests |
| **L** | architecture/migration/many independent tasks | plan first; use agents only for genuinely parallel work |

If uncertain, start one class lower and escalate when evidence shows it is insufficient.

## Credit-saving ladder

1. **Reuse current context.** Do not re-read or re-paste large documents already verified in the current task.
2. **Search before reading.** Find the exact symbol/file/route first. Read only the relevant ranges.
3. **Use one narrow skill.** Keep the security baseline when required, then load only the task-specific skill that changes execution.
4. **Prefer the existing implementation.** Reuse code, native platform features and installed dependencies before inventing abstractions. Pair with Ponytail for coding.
5. **Focused test first.** Run the smallest test/check that can fail for the change. Run the full suite once near completion when repository policy requires it.
6. **No blind retry loops.** After the same failure twice, investigate root cause before another attempt. After three failed attempts, stop and reconsider the assumption.
7. **Limit agent fan-out.** Default to zero subagents for S, zero/one for M. For L, default to at most two active workers unless the user explicitly chooses more.
8. **Keep outputs compact.** Report decisions, evidence, blockers and changed files. Do not narrate every read/tool call.
9. **Do not rebuild context in new threads without reason.** Keep related work in the same task/branch when safe.
10. **Escalate model/reasoning only when needed.** If the host lets the user choose model/effort, prefer the least expensive setting that can safely do the job; increase it for unresolved architecture, security, data-loss, concurrency or difficult debugging. Never silently override the user's chosen model.

## Codex-specific usage check

When Codex exposes it, use `/status` at the start of a long task or when the user asks about remaining usage.

Do not call status repeatedly during ordinary work.

Current Codex usage can vary with model, input/output size, reasoning effort, task duration, tools and agent fan-out. Treat host usage/billing UI as authoritative for the account.

## Expensive workflow guardrails

### Graphify

Use Graphify when:
- the repository is large or unfamiliar; and
- a graph already exists, or building it will replace repeated broad source scans.

Do not build/rebuild the graph for a tiny isolated change.

For code-only graphs, prefer local parsing. Do not enable optional semantic/API backends merely to answer a normal code-navigation question.

### Graft

Use Graft for installation/distribution state, not during normal coding turns.

Prefer `graft status` and `graft apply --dry-run` before any apply/prune action.

### Blueprint Task to PR

Use `task-to-pr` when the user wants a complete tested/reviewed PR workflow.

For a tiny local edit or question, do not invoke a full PR/review loop automatically.

### Blueprint Factory

Factory is intentionally expensive: it writes specs, implements, waits for CI and may iterate review fixes.

Use only when the user explicitly wants an unsupervised issue-to-PR run.

### Codex Issue Coordinator

This can multiply usage through workers and reviews.

Use only for a real issue batch. In credit-saver mode:
- default max active workers: **2**;
- never dispatch duplicate workers;
- do not spawn workers for blocked/dependent issues;
- stop a worker after three failed rounds as the upstream skill requires.

## Quality boundaries

Never save credits by skipping:

- authorization/authentication checks on affected security boundaries;
- data-loss safeguards;
- required migration/rollback proof;
- trust-boundary input validation;
- accessibility basics for changed UI;
- the focused test that proves the requested behavior;
- explicit acceptance criteria.

Instead, reduce duplicate work around those checks.

## Completion report

Keep it short:

```text
Budget: S / M / L
Used: <main reads/tools/tests>
Avoided: <broad scan / extra agent / duplicate full suite / unnecessary runtime>
Verified: <fresh evidence>
Remaining expensive step: <none or one concrete item>
```
