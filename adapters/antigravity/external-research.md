# Optional research integrations for Antigravity

The 500+ AI Agent Projects catalog is reference-only: https://github.com/ashishpatel26/500-AI-Agents-Projects . Use agent-project-catalog to select a useful example, then check the linked project's own license and dependencies. No bulk download or execution is included.

Agent Reach is an optional external Python CLI: https://github.com/Panniantong/Agent-Reach . Use agent-reach-routing only after the runtime is installed on the authorized workstation where Antigravity executes, not automatically on a shared production server.

Pin reviewed source to commit a19a171fa980a0785849596492e0af4db800c82f. After explicit approval for local package installation, upstream recommends pipx. Example:
    pipx install 'git+https://github.com/Panniantong/Agent-Reach.git@a19a171fa980a0785849596492e0af4db800c82f'

Read-only checks after installation:
    agent-reach install --env=auto --dry-run
    agent-reach doctor --json

The package installation itself changes the local Python environment. Do not run --system, add browser cookies, access a Chrome profile, configure MCP, install optional channels or touch production without separate permission. Third-party URL readers may receive the URL/query, so use authorized native tools for private sources. Credentials remain local and out of Git and chat.

Install these two bundle skills through the normal Antigravity global flat installer and verify they appear. Actual Agent Reach commands require the separate runtime; adding SKILL.md alone does not activate them.