---
name: screenshot-driven-visual-polish
description: "Use when the user sends UI screenshots with red marks."
---

# Screenshot-Driven Visual Polish

Use when the user sends screenshots of their sites (CardNite, ZaxDoctor, site 3, portals) asking for visual changes — commonly with hand-drawn RED CIRCLES around the elements to change. The user iterates fast: screenshot → fix → screenshot, often 3-5 rounds per campaign, and judges purely by looking at the result.

## The loop (never skip steps)

1. **Vision-analyze the screenshot first** (image-recognition skill / vision_analyze) for the scene + transcribed text.
2. **Pixel-cluster ALL red marks** — the user marks EVERY element they care about, not just the headline one. Run `scripts/red_marks.py <image>` (red threshold ≈ `r>140, g<90, b<90`, ±2-neighborhood BFS clustering) to enumerate every blob's bbox BEFORE touching code. Missing one = "you forgot the two I marked in red".
3. **Crop each marked element** (+ generous margins), zoom 3-5×, vision-analyze each individually. The red circle often overlaps the element — measure the underlying pixels too (white-face bbox, pip-cluster counts, divider orientation, dark-border runs).
4. **Fix ALL marked elements**, not just the primary one. When two marks share one source (e.g. one SVG used by both a grid icon and a featured card), they update together — say so explicitly so the user knows the second mark was handled.
5. **Deploy + live-verify each marked element** with fresh screenshots at BOTH the viewport the user reported (measure their screenshot: 370×800 vs 591×1280 are different layouts) AND mobile 390×844.
6. **Report with MEDIA: screenshots** — the user judges by looking; always attach the evidence.

## Recurring pitfalls (found the hard way)

- **Flex item width collapse:** a container with `margin: 0 auto` + `max-width` on a flex item collapses its width to CONTENT (auto margins absorb free space) → narrow column with useless side bands on desktop ("so much useless space on both sides of screen"). Fix: add `width: 100%` alongside and keep a generous cap (~780px).
- **SVG poster stretch:** absolutely-positioned `width:100%; height:100%` SVGs stretch NON-uniformly in wide containers regardless of the viewBox → standing shapes render squat/horizontal ("still not a card design"). Fix: explicit `preserveAspectRatio="xMidYMid meet"` on the svg AND design the composition TALL (e.g. 140×200 tile in a 200×260 viewBox) so it survives any container aspect.
- **Duplicate-tile ambiguity:** matching "the center/anchor tile" by VALUES is wrong when duplicates exist (two [3|3]s) — track by INDEX/position instead, or the layout balloon-bugs.
- **Small-icon legibility:** rich compositions (tile + pips) blur into blobs at 38-58px icon sizes — make the main shape dominate the viewBox and keep pip/dot counts low enough to read at the smallest render.
- **Vision misreads small crops** — always pair vision with pixel measurements (bbox, cluster counts, orientation) before concluding what the user sees.
- **Design swatches must show the artifact:** a "choose design" strip of plain color blocks reads as "not a card design" — render each swatch as a mini version of the actual artifact (e.g. mini 6/6 domino cards with per-palette pip/divider colors that mirror the in-game CSS).

## Verification

- Re-screenshot after EVERY deploy; crop the same coordinates as the user's mark and vision-analyze both before claiming "fixed".
- Zero JS errors (pageerror listener) on every verification run.
- Geometry claims need live DOM/pixel proof (rect measurements), never counts alone.
