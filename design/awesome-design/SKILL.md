---
name: awesome-design
description: Discover a suitable visual design language from the Awesome Design Skills catalog, then apply only the selected design system to UI work.
---
# Awesome Design Skills — selective style router

This is an original routing skill, not a mirror of the 67 third-party styles. Canonical collection: https://github.com/bergside/awesome-design-skills , MIT, reviewed at `f631a09b4fcc0166f2e2c1a8c81906ef680c57e8`. Load the local [style catalog](references/catalog.md) only when choosing a style.

1. Inspect the project brand, target audience, existing components and requested visual direction. **Preserve existing styling** when the user asks for a constrained update.
2. Select one style from the catalog; describe the concrete reasons and incompatible alternatives briefly. For design systems already locally installed, check `design/design-style-picker` or `design/design-systems` first rather than duplicating assets.
3. If the task needs the source's exact design-system rules, open the *specific* reviewed upstream `skills/<style>/SKILL.md` and `DESIGN.md` or a separately reviewed local copy. Do not pretend this router contains all 67 styles.
4. Implement consistent typography, semantic colors, spacing, surfaces, component states and responsiveness. Do not invent licensed fonts, artwork or brand identity; test contrast and touch/keyboard access.
5. Pair with `design-taste-frontend` for landing-page art direction and `web-design-guidelines` for final audit. Avoid loading every overlapping design skill into the same task.
