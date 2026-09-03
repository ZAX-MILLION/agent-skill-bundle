# Credits & Upstream Sources

Agent Skill Bundle is a distribution project. It does **not** claim authorship of third-party skills.

Third-party skills remain credited to their original authors and projects. Original license and notice files inside skill directories must be preserved.

## Upstream projects

| Project | Repository | Used for |
|---|---|---|
| Anthropic Skills | https://github.com/anthropics/skills | Design / document / agent skills |
| daymade Claude Code Skills | https://github.com/daymade/claude-code-skills | Design and UI/UX skills |
| Google Labs design.md | https://github.com/google-labs-code/design.md | Design guidance |
| VoltAgent awesome-design-md | https://github.com/VoltAgent/awesome-design-md | Design systems |
| obra Superpowers | https://github.com/obra/superpowers | Process, debugging, planning, TDD and verification |
| Rivet Skills | https://github.com/rivet-dev/skills | Multiplayer patterns |
| WordPress Agent Skills | https://github.com/WordPress/agent-skills | WordPress and WordPress security skills |
| Marketing Skills by Corey Haines | https://github.com/coreyhaines31/marketingskills | Marketing skills |

## Local skills

Some security and QA skills are maintained directly in this repository. They are not presented as upstream work.

## Attribution policy

When syncing an upstream skill:

- preserve the original author attribution;
- preserve its license and notice files;
- record the upstream repository and source path before automated syncing is enabled;
- do not silently rewrite upstream skill instructions;
- put host-specific compatibility logic in `adapters/`, not inside the original skill;
- review license changes before merging an upstream update.

The canonical source list is `registry/sources.json`.
