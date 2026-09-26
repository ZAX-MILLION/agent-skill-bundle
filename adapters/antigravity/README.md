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
