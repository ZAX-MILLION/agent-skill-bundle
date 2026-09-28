# Host compatibility — video-editor-bassam

The bundle skill is portable. The external video runtime still needs local filesystem and process execution.

| Host | Bundle skill discovery | External runtime use |
|---|---|---|
| Google Antigravity IDE | Use the bundle's normal on-demand retrieval, or a reviewed native install. Global skills: `~/.gemini/config/skills/`; workspace skills may use `<workspace>/.agents/skills/`. | Keep the original runtime in a separate authorized local folder. Verify it, then read its own `SKILL.md` and execute only approved local commands. |
| OpenAI Codex | Use the bundle's normal on-demand retrieval or documented Codex skill root. | Same external runtime directory; map shell/file operations to the current Codex environment. |
| Claude Code | Use the bundle's normal on-demand retrieval or `~/.claude/skills/`. | The original guide was written around Claude, but the reviewed runtime files/scripts remain separate from this adapter. Avoid installing a second duplicate copy into another discovery root. |
| Generic file-based agent | Install/retrieve this bundle skill from the host's documented skills directory. | Works only if the agent can read the runtime and run its local commands. |
| Chat-only / no terminal | Skill text can guide planning. | No executable editing claim is possible without a filesystem/process runtime. |

## Recommended layout

Keep three concerns separate:

```text
agent-skill-bundle/                  # public reviewed bundle checkout
private-external-skills/
  video-editor-bassam/               # legitimately obtained original runtime
video-projects/
  <project>/                          # user's source media and outputs
```

Do not commit the private external runtime or user media to the public bundle.

## Installation principle

The same adapter can be used by many AI hosts; do not fork the 90-file runtime per host. Instead:

1. keep one verified external runtime copy;
2. expose this small adapter through the host's normal skill discovery;
3. give the host access only to the authorized runtime/project directories;
4. let the host read the original runtime instructions on demand;
5. verify actual dependencies and rendering separately on each machine/host.

A skill file grants no extra permissions. If the host lacks terminal, filesystem, subprocess, or required dependency access, report that limitation instead of inventing an equivalent.
