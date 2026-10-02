---
name: graft
description: Maintain a single skills vault across coding agents using reviewed declarative distribution; inspect status and dry-run before applying changes.
---
# Graft — optional distribution manager

Reviewed source: https://github.com/Mikko-ww/agent-skills-graft at `a5e1564560b06c8bbb682f221b74cb915fa0c559`. Upstream package name is `graft` `0.1.0`, Python 3.11+, MIT, with `typer` and `ruamel.yaml`.

This bundle ships only this adapter. The existing bundle `install.sh` already provides a tested copy workflow, including strict on-demand and Codex-efficient profiles.

## When Graft is worth using

Use Graft when the user wants one declarative skill vault distributed across several agents/hosts.

Do **not** run Graft during normal coding turns. It is setup/maintenance tooling, not a per-task requirement.

## Setup

1. Check `graft --help`.
2. If missing and the user explicitly wants the runtime, use a pinned isolated install after reviewing the source:

```bash
uv tool install 'git+https://github.com/Mikko-ww/agent-skills-graft.git@a5e1564560b06c8bbb682f221b74cb915fa0c559'
```

3. Verify with `graft --help` and `graft platforms`.
4. Do not import private skills into this public repository.

## Safe workflow

1. `graft status`
2. `graft apply --dry-run`
3. Review targets, duplicate names, symlinks, copies, overwrites and prune actions.
4. Only then use `graft apply` when the user has approved the change.
5. `graft apply --prune` is destructive cleanup and requires explicit approval.

Keep the bundle's strict/on-demand design intact. A Graft profile that exposes every skill natively defeats the context/credit-saving goal.

On Windows or hosts where symlinks are unsuitable, prefer the bundle's reviewed copy installer rather than forcing Graft's symlink model.

A successful filesystem operation is not proof that Codex/Claude/Antigravity discovered or can execute the skill.
