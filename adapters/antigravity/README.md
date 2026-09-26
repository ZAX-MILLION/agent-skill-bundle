# Antigravity adapter

## Install on the machine running Antigravity

For Antigravity IDE / Antigravity 2.0 use the official global skills root `~/.gemini/config/skills/`; workspace skills live at `<workspace>/.agents/skills/`. Antigravity CLI may use `~/.gemini/antigravity-cli/skills/` instead. Use the installed product's current documentation.

1. Review `SECURITY.md` and `install.sh` before running bundled code.
2. Clone the repository locally. For the **on-demand setup**, in Bash run `./install.sh "$HOME/.gemini/config/skills" --flat --on-demand`. This installs only the two native bootstrap skills. On Windows, ensure the shell's HOME points to the correct user profile. Install all 136 natively only if you explicitly prefer having all their descriptions visible.
3. Do not use `--force` on unmarked preexisting destinations. If previously installed bundle skills remain, the two-skill mode will refuse to claim success. After review, `--prune-managed` removes only the other marked bundle copies; unrelated skills remain untouched.
4. Open Antigravity Customizations → Skills and confirm `project-inventory`, `server-triage`, `safe-deployment` and `secure-server-access` are discovered.
5. Merge `global-rule.example.md` into your existing personal `~/.gemini/AGENTS.md` or `GEMINI.md`, rather than overwriting any current rules. Keep each project's detailed instructions and private infrastructure inventory in its private workspace.
6. Connect server SSH/MCP separately via the native MCP manager. This repository contains **no** credentials or grant of permissions. Start with Default/Ask permissions, not unrestricted Turbo/Always Proceed.
7. Validate read-only project inventory and diagnosis before authorizing production operations.

Operating sequence: project-inventory → narrow operations skill → secure-by-default-development for changes → verification-before-completion → project-handoff. Skills load on demand; do not inject all skill bodies into global rules.

References: https://www.antigravity.google/docs/skills ; https://www.antigravity.google/docs/rules ; https://www.antigravity.google/docs/mcp ; https://www.antigravity.google/docs/permissions

## Ponytail on Antigravity

In full-install mode, the bundle installs the six original [Ponytail](https://github.com/DietrichGebert/ponytail) skills using the normal flat installer. Original skill text is unchanged; each directory has the MIT `LICENSE.txt` for standalone distribution.

- **IDE / Antigravity 2.0:** global skills at `~/.gemini/config/skills/`; optional [ponytail-global-rule.example.md](ponytail-global-rule.example.md) can be merged into `~/.gemini/GEMINI.md` or `~/.gemini/AGENTS.md`, preserving existing rules. The default coding mode is then `full`. Check Customizations → Skills and Rules. Skill names: `/ponytail`, `/ponytail-review`, `/ponytail-audit`, `/ponytail-debt`, `/ponytail-gain`, `/ponytail-help`.
- **Antigravity CLI:** consult its current native global skills path (`~/.gemini/antigravity-cli/skills/`), or use upstream's native Gemini/Antigravity extension separately. Avoid installing both in the same skill discovery scope without checking duplicate names.
- We deliberately **do not install Claude/Codex lifecycle hooks, statusline or mode tracker**. `lite/full/ultra/off` in this portable IDE adapter are conversational mode requests; hook-backed persistent switching and subagent injection are not claimed.
- Simplicity never removes required tests, input validation, security, accessibility, data-loss protection, backups, rollback, or user-requested functionality. Use `secure-by-default-development` and `verification-before-completion` for applicable tasks. Project test requirements override Ponytail's minimalist test suggestions.
- `ponytail-gain` contains historical **upstream benchmark** figures, not independently validated gains on Antigravity or ADMIN's projects.

Verification: after installation/reload, invoke `/ponytail-help`, and run `/ponytail-review` against a harmless test diff.

## Optional research

See external-research.md for the linked AI agent catalog and optional Agent Reach runtime. Neither is executed by the bundle installer. Keep private credentials outside this public repository.

## Primary response style: i-have-adhd

The portable upstream skill is in `productivity/i-have-adhd/`, with its MIT license. Its source `SKILL.md` is unchanged. The bundle does not install the upstream Antigravity plugin, CLI hooks or persistent state tracker.

**Enable by default:** merge the contents of [adhd-primary-rule.md](adhd-primary-rule.md) into the personal global rule on the machine running Antigravity (the same existing `GEMINI.md` or `AGENTS.md` named above). Do not overwrite other rules or publish private personal config. The standalone skill can also be invoked as `/i-have-adhd` where supported. `disable-model-invocation: true` in upstream frontmatter means installing its file alone is not a guarantee of always-on behavior.

If you instead use upstream's native `agy plugin install https://github.com/ayghri/i-have-adhd` route, check for duplicate `i-have-adhd` skills before additionally installing this bundle's copy. An Antigravity CLI plugin and an IDE-global rule may be separate configurations. Verify the actual IDE session displays action-first output; do not claim persistent mode without the global rule.

## Optional local skill retrieval

See [skill-retrieval-mcp.md](skill-retrieval-mcp.md) to index the reviewed bundle using a separate local Python MCP service and connect it only to Antigravity. No extra runtime or third-party dataset is installed by the bundle installer. The i-have-adhd global rule remains the primary communication layer.

## Strict on-demand skill discovery

The default recommendation is `--on-demand --flat`, which installs only `i-have-adhd` and `skill-retrieval-routing` into native global discovery. Import the entire **source checkout** into the separately installed local Skill Retrieval MCP, keeping its scripts/references/assets available in that checkout. The native and MCP libraries serve different purposes: native bootstrap provides routing and the main communication preference; MCP searches the other skills only when needed.

Do not assume enabling the MCP makes the 134 other skill bodies native or automatically executable. When a retrieved skill cites support files, read them from the source checkout. A user-global rule for `i-have-adhd` is still required for always-on communication across sessions.
