---
name: paul
description: Use a scoped Plan-Apply-Unify loop for implementation tasks needing explicit acceptance criteria, verified execution, decision records and handoff; do not install the Claude Code PAUL framework automatically.
---
# PAUL — portable loop adapter

Original bundle-authored adapter for [ChristopherKahler/paul](https://github.com/ChristopherKahler/paul), reviewed at `f8552c72d0e69309a0cb61b5de5c85a06838ddcb`, MIT. The upstream PAUL framework is a **Claude Code-specific command/rule installer**, not an upstream `SKILL.md` package. This file borrows its documented workflow contract and does not claim to contain, execute or install the PAUL runtime or support upstream slash commands.

Use **only if user requests PAUL** or a Plan–Apply–Unify workflow. The bundle already supplies Superpowers planning, TDD and verification; don't run two competing always-on orchestrators or silently create a second project-state hierarchy.

1. PLAN: inspect existing project context and worktree; capture objective, hard scope boundaries, risks, affected files, specific acceptance criteria and verification commands. Keep user approval for substantive scope/security decisions.
2. APPLY: make the scoped changes using available host tools, check each result against acceptance criteria, and preserve security baseline. Distinguish completed, completed-with-concerns, needs-context and blocked tasks. Do not pretend work or tool execution happened.
3. UNIFY: reconcile actual vs planned changes, actual tests, outstanding decisions, follow-up work and current branch/release state into the **project's existing** handoff/plan files. Don't overwrite unrelated `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` or project instructions.
4. Resume from the recorded actual state, revalidate current code and tool access. Do not treat a summary as evidence of live deployment or branch status.
5. The separate `npx paul-framework` may modify Claude Code commands/rules and create `.paul/` state files; install only on a separately reviewed workstation/project with explicit approval and backups. Do not claim native Antigravity/Codex slash-command parity.
