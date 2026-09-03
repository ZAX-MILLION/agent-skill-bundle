# Credits & Upstream Sources

Agent Skill Bundle is a distribution project. It does **not** claim authorship of third-party skills.

Third-party work remains credited to its canonical author/project. Original license and notice files inside mirrored directories must be preserved. Mirrors and downstream copies do not replace the canonical author as the attribution source.

## Canonical skill sources

| Project | Repository | Used for |
|---|---|---|
| Anthropic Skills | https://github.com/anthropics/skills | Document, design, frontend and agent skills |
| daymade Claude Code Skills | https://github.com/daymade/claude-code-skills | `design-style-picker`, `ui-designer`, and related UI skills |
| Hermes Agent / NousResearch | https://github.com/NousResearch/hermes-agent | `design-md` skill |
| obra Superpowers | https://github.com/obra/superpowers | Process, debugging, planning, TDD, reviews and verification |
| WordPress Agent Skills | https://github.com/WordPress/agent-skills | WordPress development skills |
| Marketing Skills by Corey Haines | https://github.com/coreyhaines31/marketingskills | Marketing skills |

## Collections and reference sources

These projects are important sources, but they are not falsely presented as authors of unrelated skills:

| Project | Repository | Relationship |
|---|---|---|
| Google Labs design.md | https://github.com/google-labs-code/design.md | Reference specification/tool used by the Hermes `design-md` skill |
| VoltAgent awesome-design-md | https://github.com/VoltAgent/awesome-design-md | Upstream for the bundled `design/design-systems` collection |
| Rivet Skills | https://github.com/rivet-dev/skills | Current Rivet skill ecosystem; legacy multiplayer paths are no longer present there |
| Rivet Actors | https://github.com/rivet-dev/actors | Current canonical docs/examples underlying the legacy Rivet-derived multiplayer material |

## Local skills

The `security/` and `qa/` categories are maintained locally in this repository unless an individual entry is explicitly remapped later. They are not attributed to WordPress, Anthropic, or another upstream merely because they cover the same topic.

## Attribution policy

When syncing upstream content:

- preserve original author attribution, license files and notices;
- prefer the canonical author repository over mirrors or aggregators;
- record repository, source path and checked revision;
- never silently rewrite upstream instructions;
- place host-specific compatibility in `adapters/`, outside the upstream copy;
- review license and security-sensitive changes before merging;
- never mark a legacy/derived item as an exact mirror when the original source path can no longer be proven.

Canonical source roles are in `registry/sources.json`; path mappings are in `registry/mappings.json`.
