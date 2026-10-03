# DEV MAX project bootstrap

The DEV MAX profile is ADMIN's reusable Antigravity starter.

## Goal

Run one command at the start of any project:

```text
devmax-init
```

That command:

- keeps the full reviewed agent-skill-bundle outside the project;
- installs only the 10 DEV MAX core skills into `.agents/skills/`;
- adds/updates a marked DEV MAX block in `AGENTS.md` without deleting existing project rules;
- writes `.agents/devmax.json` with the vault path and profile state;
- leaves all specialist skills on demand;
- refuses to overwrite same-name unmarked project skills unless `--force` is explicitly used.

## Core profile

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

The three DEV MAX-specific skills (`credit-usage-helper`, `task-to-pr`, `test`) live under `profiles/devmax/skills/`; they are not added to the reviewed 188-skill vault count.

## One-time command installation

### Windows PowerShell

```powershell
irm https://raw.githubusercontent.com/ZAX-MILLION/agent-skill-bundle/main/install-devmax.ps1 | iex
```

### macOS / Linux / Git Bash

```bash
curl -fsSL https://raw.githubusercontent.com/ZAX-MILLION/agent-skill-bundle/main/install-devmax.sh | bash
```

Then, for every new project:

```text
devmax-init
```

## Useful commands

```text
devmax-init --status
devmax-init --remove
```

`--remove` deletes only DEV MAX-managed project skill copies, manifest, and the marked AGENTS block. It preserves unmarked skills and other project rules.

Specialist retrieval remains on demand through `skill-retrieval-routing`; the local offline fallback can search the checkout with `scripts/skill_doctor.py`. Skill Retrieval MCP remains optional and can be connected separately.
