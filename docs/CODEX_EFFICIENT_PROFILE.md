# Codex credit-efficient profile

Use this profile when Codex credits/allowance matter and you still want the high-value UTOON development tools available natively.

## Install

From the reviewed Agent Skill Bundle checkout:

```bash
bash tests/on-demand-install.sh
./install.sh "$HOME/.codex/skills" --flat --codex-efficient
```

If an older full bundle install is already present, review it first. Then explicitly migrate only bundle-managed copies:

```bash
./install.sh "$HOME/.codex/skills" --flat --codex-efficient --prune-managed
```

Never use `--force` on unrelated personal/third-party skills without reviewing them.

## The 12 native skills

1. `i-have-adhd`
2. `skill-retrieval-routing`
3. `credit-usage-helper`
4. `ponytail`
5. `graft`
6. `graphify`
7. `secure-by-default-development`
8. `verification-before-completion`
9. `task-to-pr`
10. `test`
11. `review`
12. `codex-issue-coordinator`

Everything else remains in the one reviewed source checkout and is retrieved on demand.

## Why these 12

- **credit-usage-helper** controls context, retries, model/effort escalation, agent fan-out and repeated test work.
- **Ponytail** keeps code changes minimal without removing required safety or proof.
- **Graphify** can replace repeated broad codebase reads on large repositories.
- **Graft** is available for cross-host skill distribution, but should not run during normal coding.
- **secure-by-default-development** stays available because security is not an acceptable place to save credits.
- **verification-before-completion** prevents expensive follow-up turns caused by false “done” claims.
- **Blueprint task-to-pr/test/review/coordinator** provides a complete delivery path when a PR or issue batch is actually requested.

The more expensive Blueprint `factory` and `architecture-review` remain on demand.

## Optional runtimes

The profile installs **skill instructions**, not external executables.

### Graphify runtime

Reviewed current release:

```bash
uv tool install 'graphifyy==0.9.74'
graphify --version
```

Do not also run `graphify install` unless you deliberately choose upstream Graphify's generated host skill instead of this bundle adapter. Duplicating both wastes context and can create conflicting instructions.

### Graft runtime

Reviewed pinned source:

```bash
uv tool install 'git+https://github.com/Mikko-ww/agent-skills-graft.git@a5e1564560b06c8bbb682f221b74cb915fa0c559'
graft --help
graft platforms
```

Before applying any distribution change:

```bash
graft status
graft apply --dry-run
```

Do not use `graft apply --prune` without explicit approval.

## Verify the profile

```bash
python3 scripts/skill_doctor.py doctor \
  --host-root "$HOME/.codex/skills" \
  --native-profile codex-efficient \
  --json
```

This verifies files/markers only. It does not prove that external runtimes, MCP, Codex threads, accounts, or provider tools are available.

## Credit-saving operating rules

- Use `/status` when starting a long Codex task or when usage is uncertain; do not poll it every turn.
- Default to the current thread.
- For a normal task, use no subagent unless an independent review materially improves safety.
- For issue batches, default to at most two active workers.
- Search first, then read narrow file ranges.
- Avoid re-reading the same PRD/repository sections in one task.
- Run focused tests during implementation; run the full required suite once near completion.
- After two identical failures, investigate before retrying.
- After three failed rounds, stop and reconsider the assumption.
- Use the least expensive model/reasoning setting that safely fits the task when the host/user permits model selection.
- Do not lower security, migration, rollback, or data-loss proof to save credits.

## Blueprint selection

The bundle includes these exact reviewed Blueprint skill bodies:

- `task-to-pr`
- `test`
- `review`
- `factory`
- `codex-issue-coordinator`
- `architecture-review`

The overlapping Blueprint `plan`, `design`, and other skills were intentionally not bulk-imported because the bundle already has established planning/design workflows. This avoids duplicate routing and startup context.
