# Optional global rule: select skills on demand

**Merge these principles into existing Antigravity / Codex / Claude Code user rules only after reviewing them. Do not overwrite current rules.** This file is an example, not an automatically installed global rule.

- For a substantial task, discover **only** the relevant reviewed skill(s) before following their instructions. Prefer connected local Skill Retrieval MCP (`keyword_search` or `search_skills`, then `get_skill`), never bulk-load the vault. Use the original checkout to read supporting files.
- If the retrieval MCP is absent and a local terminal + source checkout are available, run `python3 <absolute-path-to-bundle>/scripts/skill_doctor.py search "<task keywords>"` as an **offline fallback**, then open the returned `SKILL.md`. A local finder is not an MCP server and is not proof the app discovers skills automatically.
- Load `security/secure-by-default-development` alongside relevant implementation skills, and `process/verification-before-completion` before claiming completion. Choose a small number of specific skills, not every matching description.
- For external sources (Shuohao, OpenMontage, PAUL native, ECC runtime, n8n MCP, Claude-Mem), a local router is not the full package or runtime. Run `doctor` or inspect actual prerequisites; request approval before installs, cloud connections, credentials, hooks, or executing third-party scripts. Never claim `Ready` without a successful test in the current host.
- Keep strict native discovery limited to this bundle's two bootstraps, `i-have-adhd` and `skill-retrieval-routing`. Other unrelated user skills are not to be removed.
- If a tool, local checkout, MCP connection, or runtime is unavailable, report that limitation rather than simulating tool execution. Preserve existing user/project instructions and security boundaries.

Manual acceptance: reload each chosen host, verify only the two bundle native entries appear, test MCP `list_categories`, `keyword_search`, `search_skills`, `get_skill`, open referenced support files, and complete one harmless task. The existence of this rule file alone proves none of those actions happened.
