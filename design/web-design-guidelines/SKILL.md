---
name: web-design-guidelines
description: Review web UI, accessibility, interaction, form, responsive layout, animation, and content quality against pinned Vercel Web Interface Guidelines.
---
# Web design guidelines — pinned local adapter

Original locally authored adapter for the [Vercel Web Interface Guidelines](https://github.com/vercel-labs/web-interface-guidelines), reviewed at commit `e3d624baaf29dc1fc645aff3e38f03e564d2d6b1`. The exact upstream `command.md` snapshot is in [references/pinned-command.md](references/pinned-command.md), and its MIT license is copied alongside this file. This is **not** an unchanged mirror of Vercel's separately published `agent-skills/web-design-guidelines` skill. Its upstream version fetches a mutable remote URL for each run; this adapter deliberately uses reviewed local rules unless an update is explicitly approved.

## Workflow
1. Read `references/pinned-command.md` **as guidance**, not as an instruction to dynamically fetch `main`; ignore its `$ARGUMENTS` placeholder and apply the supplied file paths.
2. Read the UI files and relevant tests. Evaluate accessibility, keyboard navigation, focus, labels, validation, layout, responsive behavior, animation, loading/error/empty states and wording, using rules that apply to this stack.
3. Cite concrete `path:line` findings with severity, user impact and a specific correction. Separate verified defects from judgments needing a browser or device test.
4. If explicitly asked to fix issues, make scoped changes then test in a real browser/mobile viewport where available. Do not say visual QA passed if no browser/screenshot tool exists.
5. Keep project design constraints and accessibility requirements ahead of aesthetic preferences. Do not fetch or execute unreviewed remote instruction text automatically.
