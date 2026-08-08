---
name: ui-screenshot-specs
description: "Use when the user marks a screenshot (red box) as UI spec."
---

# UI Specs From Marked Screenshots

Use when the user sends a screenshot with a drawn annotation — a red box, arrow, circle, or scribble — marking a region and asks you to place, resize, or restyle a UI element to fill it ("make the draw area in this whole red box"). The annotation IS the spec: size and position the element to the marked bounds, not to your guess.

Applies to non-developer users who communicate visual changes by drawing on screenshots (DEVMAX's established workflow: reference images + marked screenshots instead of text specs).

## Workflow

1. **Vision-analyze the screenshot first** (`analyze_image.py` or your vision tool) to understand WHAT the mark covers and the surrounding context — the description tells you which element the user means (e.g. "a red box highlights a blank area on the left" = the region where the new panel goes). Crop + zoom the marked area if the description is ambiguous.

2. **Pixel-extract the mark's exact bounds.** Most annotations are a bright red/pink fill or stroke:
   ```python
   from PIL import Image
   import numpy as np
   a = np.array(Image.open(path).convert('RGB'))
   red = (a[:,:,0] > 150) & (a[:,:,1] < 100) & (a[:,:,2] < 100)
   ys, xs = np.where(red)
   print(xs.min(), xs.max(), ys.min(), ys.max())   # x0, x1, y0, y1 in SCREENSHOT pixels
   ```
   If the mask looks like a hollow outline, also band-scan rows/columns to find the box's edges (a thick marker stroke reads as a solid block).

3. **Scale screenshot → device coordinates.** Screenshots are often downscaled from the real viewport. `scale = deviceWidth / screenshotWidth` (e.g. 390/370), apply to every bound. Verify the scale assumption: known UI landmarks (top-bar height, status pill) should land on expected device px.

4. **Position the element with the ancestor offset in mind.** `position: absolute; top/left` is relative to the NEAREST POSITIONED ANCESTOR, not the viewport. If the board section starts at screen y=90, `top: 55px` renders at screen y=145. Compute `top = markedY0 - ancestorScreenY`, `left = markedX0 - ancestorScreenX`. This bit twice in one session (panel landed 90px low).

5. **Verify live with `getBoundingClientRect()`** — the placed element's rect must match the marked region (x/y/w/h), and it must not overlap other interactive elements (chain tiles, drop zones). Screenshot mobile + desktop and vision-verify before delivering.

## Pitfalls

- **The mark is a FILL, not an outline** — a thick marker paints the whole strip solid; the bbox of red pixels is the correct region even when it hugs the screen edge (x=0).
- **The red box may cover a drop zone / text** — the vision description will say "obscured by red box"; that's the region the user wants repurposed.
- **Don't trust your guess at the region** — measure. The user's box was 56×362px in a 370×800 screenshot; the panel sized to the scaled bounds (64×382 on a 390px device) was accepted; a guessed size would have missed.
- **Keep the element's content proportionate to the region** — a tall narrow panel needs vertically stacked content (icon, label, count), not a scaled-up button layout.
- The user iterates fast: deliver the positioned element + screenshot in one pass, then let them judge.

## Related

- CardNite-specific case (draw-panel from red box): see the cardnite skills' references.
- `image-recognition` skill for Gemini description of what the annotation covers.
