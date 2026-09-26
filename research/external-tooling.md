# Optional tools that are not Agent Skills

Reference-only upstream checks, 2026-09-26. These applications are not included in the public bundle, installed, connected or authorized by installing a `SKILL.md`.

| Tool | Canonical source & pinned commit | Correct role |
|---|---|---|
| Pixel Agents | [pixel-agents-hq/pixel-agents](https://github.com/pixel-agents-hq/pixel-agents) `3537e140c2094761beae748592aeb92ece8edfdd` (MIT) | VS Code extension or standalone local web office for viewing agent activity; **not** an agent-model upgrade or a portable skill. Upstream supports its specific session providers; confirm actual Antigravity/Codex compatibility in the installed version before claiming visual monitoring. Avoid `--dangerously-skip-permissions` and broad session watching by default. |
| OpenMontage full runtime | [calesthio/OpenMontage](https://github.com/calesthio/OpenMontage) `08e2151fa02de28a5d6a312b3d575692bf147ad7` (AGPL-3.0) | Separate media production app. The local `creative/openmontage` adapter has no renderer, API keys or upstream assets. |
| PAUL full framework | [ChristopherKahler/paul](https://github.com/ChristopherKahler/paul) `f8552c72d0e69309a0cb61b5de5c85a06838ddcb` (MIT) | Optional Claude Code-specific commands/rules installer, distinct from the portable `process/paul` adapter. Do not run a second always-on orchestrator alongside Superpowers by accident. |
| shuohao original skills | [eternityspring/shuohao-skills](https://github.com/eternityspring/shuohao-skills) `ef4ac0c313c7eeb1f918db5f0f0eb319745900bc` (Apache-2.0) | Six complete external original skill packages include JS scripts, references, binary preview assets. The local router is guidance only. |
| Community n8n-mcp | [czlonkowski/n8n-mcp](https://github.com/czlonkowski/n8n-mcp) `4cc0efda76f272e3b0816f215399f21599c29d34` (MIT) | Alternative independent MCP service, not the official n8n instance-level server. Use only after review. |

Host skills directory discovery is not proof that any of these external applications is installed. Avoid duplicate skills/plugins and preserve user-specific config.
