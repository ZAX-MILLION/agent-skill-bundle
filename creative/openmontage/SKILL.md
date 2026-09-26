---
name: openmontage
description: Plan and review AI-assisted video, audio, image and animation production using an independently installed OpenMontage workspace; route video tasks to a complete runtime.
---
# OpenMontage — external studio adapter

Original local adapter for [calesthio/OpenMontage](https://github.com/calesthio/OpenMontage), pinned to `08e2151fa02de28a5d6a312b3d575692bf147ad7`; upstream is **AGPL-3.0**. This adapter does not redistribute the full app, its tool registry, production scripts, bundled skills, assets or third-party models/providers. OpenMontage's project-specific `skills/` and `.agents/skills/` have different purposes; don't bulk copy them or describe them as standalone portable tools.

When asked for a video task, first inspect the input footage and requested deliverable (platform, aspect, duration, language, brand, deadlines and rights). If the user points to a reference video, analyze its actual content and rights, not a guessed transcript. Produce a modest treatment and explicit editing/asset/verification plan. OpenMontage's authoring loop uses `AGENT_GUIDE.md` and its own app checkout; only use exact current docs within an authorized local copy.

Only if OpenMontage is **separately installed** and the needed tools actually exist:
- Inspect its advertised tool capability registry, provider configuration and budget; require approval before any paid model request, external upload or asset download.
- Use the selected pipeline and generated local artifacts; check source licensing for music, stock footage, people/likeness and characters. Do not assume search results are free for commercial use.
- Verify playback, audio, captions, mobile framing, export resolution/codec and provenance.
- Keep secrets and footage private; never publish project paths, tokens or outputs into this public skill repository.

If runtime is absent, provide an actionable pipeline plan using tools available to the host. Never say a video was rendered or edited if it wasn't. Review AGPL obligations separately if distributing or offering a modified hosted OpenMontage service. Not a replacement for actual editing/rendering tools.
