# Agent Skill Bundle

A curated collection of **agent skills** — UI/UX design quality, security auditing, process discipline, multiplayer game patterns, WordPress, and marketing — collected into one place, ready to install into any Claude Code / Cursor / agent setup.

The goal: **avoid vibe-coding mistakes** (design slop, security holes, untested code) by giving agents battle-tested, structured skills instead of vibes.

## 📦 What's inside

| Category | Skills | Source |
|---|---|---|
| `design/` | 21 skills — frontend-design, webapp-testing, ui-designer, design-style-picker, design-md, brand-guidelines, canvas-design, web-artifacts-builder, theme-factory + 74 real brand design systems | [anthropics/skills](https://github.com/anthropics/skills), [daymade/claude-code-skills](https://github.com/daymade/claude-code-skills), [google-labs-code/design.md](https://github.com/google-labs-code/design.md), [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) |
| `security/` | 5 skills — web-security-audit, ultimate-security-audit, api-security-probing, wordpress-security-audit, wordpress-security | Custom + [WordPress/agent-skills](https://github.com/WordPress/agent-skills) |
| `process/` | 14 skills — plan, writing-plans, executing-plans, TDD, systematic-debugging, code review, verification-before-completion | [obra/superpowers](https://github.com/obra/superpowers) |
| `multiplayer/` | 3 skills — multiplayer-game, chat-room, live-cursors (netcode + state sync) | [rivet-dev/skills](https://github.com/rivet-dev/skills) |
| `wordpress/` | 18 skills — plugin/theme/block dev, REST API, performance, Playground, CLI | [WordPress/agent-skills](https://github.com/WordPress/agent-skills) |
| `marketing/` | 49 skills — SEO, copywriting, CRO, pricing, social, cold-email | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) |
| `qa/` | 6 skills — dogfood, spa-browser-qa, ui-screenshot-specs, visual polish, silent-failure debugging | Custom |

**Total: ~116 skills.**

## 🚀 Install

### Claude Code (all skills)

```bash
./install.sh ~/.claude/skills
```

### Cursor

```bash
./install.sh ~/.cursor/skills
```

### Any agent (custom path)

```bash
./install.sh /path/to/skills
```

The installer copies every skill's **full directory** (SKILL.md + scripts/ + examples/ + references/ + assets/) into `<target>/<category>/<skill>/`, so nothing breaks.

## 📝 License & credits

Each skill keeps its own license from its source repo. See the individual `LICENSE.txt` / `LICENSE` files inside each skill directory. This repo is an aggregation; all upstream credits go to the original authors (Anthropic, daymade, Google Labs, VoltAgent, obra, Rivet, WordPress, coreyhaines31).

Custom skills (security audit, QA) were built from production project experience — see their SKILL.md bodies for methodology.
