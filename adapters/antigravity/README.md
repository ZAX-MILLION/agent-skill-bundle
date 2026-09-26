# Antigravity adapter

## Install on the machine running Antigravity

For Antigravity IDE / Antigravity 2.0 use the official global skills root `~/.gemini/config/skills/`; workspace skills live at `<workspace>/.agents/skills/`. Antigravity CLI may use `~/.gemini/antigravity-cli/skills/` instead. Use the installed product's current documentation.

1. Review `SECURITY.md` and `install.sh` before running bundled code.
2. Clone the repository locally. In Bash (macOS/Linux, or Git Bash on Windows) run `./install.sh "$HOME/.gemini/config/skills" --flat`. On Windows, ensure the shell's HOME points to the Antigravity user profile; an agent can copy directories equivalently.
3. Do not use `--force` on unmarked preexisting destinations; back up and review conflicts.
4. Open Antigravity Customizations → Skills and confirm `project-inventory`, `server-triage`, `safe-deployment` and `secure-server-access` are discovered.
5. Merge `global-rule.example.md` into your existing personal `~/.gemini/AGENTS.md` or `GEMINI.md`, rather than overwriting any current rules. Keep each project's detailed instructions and private infrastructure inventory in its private workspace.
6. Connect server SSH/MCP separately via the native MCP manager. This repository contains **no** credentials or grant of permissions. Start with Default/Ask permissions, not unrestricted Turbo/Always Proceed.
7. Validate read-only project inventory and diagnosis before authorizing production operations.

Operating sequence: project-inventory → narrow operations skill → secure-by-default-development for changes → verification-before-completion → project-handoff. Skills load on demand; do not inject all skill bodies into global rules.

References: https://www.antigravity.google/docs/skills ; https://www.antigravity.google/docs/rules ; https://www.antigravity.google/docs/mcp ; https://www.antigravity.google/docs/permissions

## Ponytail on Antigravity

The bundle installs the six original [Ponytail](https://github.com/DietrichGebert/ponytail) skills using the normal flat installer. Original skill text is unchanged; each directory has the MIT `LICENSE.txt` for standalone distribution.

- **IDE / Antigravity 2.0:** global skills at `~/.gemini/config/skills/`; optional [ponytail-global-rule.example.md](ponytail-global-rule.example.md) can be merged into `~/.gemini/GEMINI.md` or `~/.gemini/AGENTS.md`, preserving existing rules. The default coding mode is then `full`. Check Customizations → Skills and Rules. Skill names: `/ponytail`, `/ponytail-review`, `/ponytail-audit`, `/ponytail-debt`, `/ponytail-gain`, `/ponytail-help`.
- **Antigravity CLI:** consult its current native global skills path (`~/.gemini/antigravity-cli/skills/`), or use upstream's native Gemini/Antigravity extension separately. Avoid installing both in the same skill discovery scope without checking duplicate names.
- We deliberately **do not install Claude/Codex lifecycle hooks, statusline or mode tracker**. `lite/full/ultra/off` in this portable IDE adapter are conversational mode requests; hook-backed persistent switching and subagent injection are not claimed.
- Simplicity never removes required tests, input validation, security, accessibility, data-loss protection, backups, rollback, or user-requested functionality. Use `secure-by-default-development` and `verification-before-completion` for applicable tasks. Project test requirements override Ponytail's minimalist test suggestions.
- `ponytail-gain` contains historical **upstream benchmark** figures, not independently validated gains on Antigravity or ADMIN's projects.

Verification: after installation/reload, invoke `/ponytail-help`, and run `/ponytail-review` against a harmless test diff.
