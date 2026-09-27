---
name: game-ready-2d-asset-pipeline
description: Use when preparing, splitting, importing, or validating production-ready 2D game assets such as characters, monsters, sprite parts, animation frames, and UI sprites; reject concept sheets and unusable backgrounds.
---
# Game-ready 2D asset pipeline

**Original Agent Skill Bundle skill.** Task-scoped instructions only. Does not install art tools, generate images without a host capability, call paid services, or upload files without permission.

## Intake and acceptance
1. Inspect the target engine, rendering/camera angle, reference, art direction, required states, pivot convention, and expected output filename scheme. For Godot, confirm engine version and importer settings from the real project rather than assuming them.
2. Record exactly which file corresponds to each logical asset. One deliverable image must hold **one** requested slot or frame. Do not substitute a character sheet, collage, infographic, mockup, or labeled presentation board for an importable asset. A sprite sheet is permitted **only** when the game's importer explicitly needs one and the owner approves.
3. If the owner supplies a visual master, preserve its characteristic silhouette, costume, proportions, palette, lighting, and camera angle across extracted parts. Distinguish the visual master from importable cutouts.
4. Confirm original creation or documented licenses for every source/texture. Do not imitate a recognizable third-party character or claim an image is cleared for commercial use without evidence.

## Production contract
- Export real transparent PNGs with alpha (not a checkerboard, painted white/black backdrop, or fake transparency). Preserve a lossless master.
- Keep each cutout fully visible, uncropped, with sensible transparent padding, consistent pixels-per-unit, matching perspective and scale, and stable attachment points. Avoid baking shadows into unrelated slots.
- Use descriptive, collision-free names with stable IDs (e.g. `character_01__head__idle_00.png`) and a manifest mapping asset ID to role, state, dimensions, pivot, frame order, source, and license.
- For modular actors, list mandatory body/helmet/cloak/weapon slots and the layers that overlap. Export each as its **own file**. Give moving capes/hair their own rigging/animation plan if needed.
- Keep render layer rules explicit (e.g. canopy occludes the player; weapon layer follows project specification). Collision masks and sprite transparency are separate concerns.
- Keep animation frame counts, frame timing, origins and attachment points coherent across states. Export normal/emission maps only when actually supported by the project.

## Verify rather than assume
- Open every output file and check RGBA alpha at corners, empty transparent outside the subject, expected dimensions, no unexpected letters or extra objects, and no missing/duplicate asset IDs.
- Validate sprite bounds and pivot alignment by compositing representative states; inspect seams while moving, not only in one pose. Check the smallest target mobile display size.
- Import a small sample into the target Godot project if access is authorized. Inspect filtering/mipmaps, pixel scale, canvas layer/Y-sort and mobile draw cost; never claim a real APK test without building and testing it.
- Compare asset manifest to actual files and the intended upload API/dashboard contract. Do not bypass an upload limit or publish media automatically.
- If generation cannot provide reliable individual alpha cutouts, mark the result **concept/reference only** and request an approved extraction/rework step. Never call an unusable collage production-ready.

## Handoff
Report files with paths, slot/state, resolution, provenance, animation/pivot contract, import test performed (or not), and remaining blockers. Keep any private source media out of this public skill vault.
