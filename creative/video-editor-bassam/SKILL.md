---
name: video-editor-bassam
description: Portable cross-agent router for the separately obtained video-editor-bassam Arabic talking-head editing runtime. Use for 9:16 reels, silence cutting, word-timed Arabic captions, light edits, full motion graphics, SFX, and verified MP4/SRT/TXT delivery when the reviewed external package is available locally.
---

# video-editor-bassam — portable external-runtime adapter

This is a **bundle-authored cross-host adapter**, not a redistributed copy of the original 90-file runtime.

The reviewed source was the user-supplied `video-editor-bassam.zip` package dated 2026-09-28:
- archive SHA-256: `6298972ab0429d74c2cf5607a535278b3156a8252f1bf007f46e4b808b700234`
- 90 files when unpacked
- reviewed tree SHA-256: `d1d5141d9682c5570648ae8bcccdfa0644a7c6cfc764c39c87e46a3a006dcd59`

The supplied guide permits personal/commercial **use**, but no general code-redistribution license was found. Therefore the original scripts, assets, font files, Remotion project, and source `SKILL.md` are **not** mirrored into this public repository.

## When to use

Use this router when the user wants Arabic talking-head editing such as:
- remove silences / failed takes;
- generate word-timed Arabic captions;
- make a vertical reel/short;
- add light zoom/SFX treatment;
- build a fuller motion-graphics edit;
- export the edited MP4 plus subtitle/text deliverables.

The reviewed runtime supports three production modes: quick, light, and full. The full workflow uses its own references, style files, checks, FFmpeg/Python tooling, transcription stack, and Remotion project. Do not reconstruct those files from memory.

## Required external package

The original package must already exist on the user's machine or authorized workspace.

Prefer an explicit path supplied by the user. Do not scan unrelated home folders without permission. Before executing any third-party script, verify the package:

```bash
python3 scripts/verify_package.py "/absolute/path/to/video-editor-bassam"
# or
python3 scripts/verify_package.py "/absolute/path/to/video-editor-bassam.zip"
```

On Windows, `py -3` is acceptable if that is the installed Python launcher.

A successful integrity check means the bytes match the reviewed package. It does **not** mean dependencies are installed, the host can execute terminal commands, or the editing workflow has been tested on that machine.

## Runtime authority

After integrity verification:

1. Read the external runtime's own `SKILL.md`.
2. Read each referenced file at the point the original workflow requires it.
3. Treat the original runtime as the authority for editing steps, styles, safety checks, project layout, and script arguments.
4. Use this adapter only to map those instructions onto the capabilities of the current AI host.
5. Keep the external runtime read-only. Put user media and generated work in the runtime's documented data/project location, never in this public bundle checkout.

The reviewed runtime stores its user data under `~/Documents/video-editor-bassam` by default and supports `VEB_HOME` for an alternate data location. Preserve that separation.

## Cross-agent capability contract

The host needs, at minimum:
- read/write access to the authorized project/media directory;
- terminal/process execution;
- ability to run Python and shell/Node commands when the original runtime calls for them;
- enough local storage for media, transcription models, and rendering dependencies.

Some steps may require installing FFmpeg, Python packages, Node/Remotion dependencies, transcription models, or platform tools. **Do not install them silently.** Inspect the original setup script first, summarize what it will change/download, and obtain the user's approval before installation or large downloads.

If the host cannot execute local tools (for example a chat-only interface with no filesystem/terminal), use this skill only to plan the workflow. Do not claim the video was edited or rendered.

## Host mapping

Read [references/host-compatibility.md](references/host-compatibility.md).

Core rule: the original package is host-neutral **only to the extent that the host can read its files and execute the required local tools**. Claude-specific wording in the supplied guide is installation/UI guidance, not a dependency of the video-processing scripts themselves.

## Safety and delivery

- Never overwrite source media.
- Do not publish or schedule the result unless explicitly requested and supported.
- Keep private footage, generated frames, transcripts, and project state outside this public repository.
- Preserve the original runtime's checks before declaring the render complete.
- Treat a successful render as insufficient until its documented preflight/postflight checks pass.
- Do not fabricate availability of image generation, web assets, fonts, providers, credentials, or paid services.
- Respect the original package's licensing boundary and the licenses of any downloaded media/fonts.

## If the external runtime is missing

Report **Setup Required**. Point the user to their legitimately obtained `video-editor-bassam.zip` package, verify it after they place it locally, then continue. Do not fetch or mirror an unverified copy on the user's behalf.
