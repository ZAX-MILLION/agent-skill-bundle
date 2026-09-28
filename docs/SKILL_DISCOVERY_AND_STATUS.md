# Skill discovery, package status and selective external staging

**Scope:** one reviewed source vault, strictly two native bootstrap skills, and optional local Skill Retrieval MCP. A skill file is an instruction, not a program, a connected tool, or proof that its workflow has run.

## Distinguish the four checks

| Layer | Evidence | What it does not prove |
|---|---|---|
| Native bootstrap | The `i-have-adhd` and `skill-retrieval-routing` directories exist in a verified host skill root | That the host discovered them or applied the global style rule |
| Source discovery | `python3 scripts/skill_doctor.py search "video storyboard"` returns a named skill path and description | That the external package is copied, or that any MCP service is connected |
| Complete package | Files match the pinned reviewed Git blob hashes, with required notice/license | That Node, a provider, model, credential, or host tool is available |
| Live execution | An explicitly authorized local test **and** the relevant host workflow actually succeed | That the same outcome will occur on all hosts or providers |

**Status meanings:** `Setup Required` = router/description is present but the complete package, connection or bootstrap is absent; `Missing Dependencies` = the package is altered/incomplete or a required runtime is missing/incompatible; `Unverified` = package appears complete but actual host execution is not proven; `Ready` requires documented successful end-to-end execution in the target host. The offline checker intentionally never prints `Ready` based on file presence alone.

## No MCP? Find a local bundle skill without installation

From the **existing** local Agent Skill Bundle checkout, using an available Python 3 interpreter:

```bash
python3 scripts/skill_doctor.py search "Godot performance"
python3 scripts/skill_doctor.py search "shuohao character"
python3 scripts/skill_doctor.py list
python3 scripts/skill_doctor.py doctor
```

This uses only local `SKILL.md` names/descriptions; no web, API key, model, index, or third-party code is run. Open the selected original directory and its references/assets. It is a **terminal fallback**, not proof of automatic discovery or an alternative to connecting the optional Skill Retrieval MCP. The agent still needs access to a terminal and the source checkout. If neither is available, it must say so.

For strict automatic **host-mediated** discovery, configure the separate local [Skill Retrieval MCP](../adapters/antigravity/skill-retrieval-mcp.md), import the source checkout and explicitly connect it to each used host. To encourage agents to search when tasks warrant it, review and manually merge the [cross-host on-demand rule example](../adapters/multi-host/on-demand-discovery-rule.example.md) into your existing personal host rules; the repository never edits them. Verify `list_categories`, `keyword_search`, `search_skills`, `get_skill`, supporting-file access and a harmless task **in each** host. The installer and offline finder do not edit MCP or global host configuration. Native startup remains only the two bundle bootstraps; do not install the other bundle skills globally.

## Six Shuohao originals — full packages, not the router

The existing `creative/shuohao-skills` directory is an **original local guide**. The six complete upstream packages are separate; they include **97 pinned original files** (scripts, bilingual READMEs, references, examples, image assets) and upstream Apache-2.0 `LICENSE` and `NOTICE`. [Reviewed full manifest](../registry/shuohao-packages.json) pins `eternityspring/shuohao-skills` commit `ef4ac0c313c7eeb1f918db5f0f0eb319745900bc`.

A complete existing upstream checkout is required, **obtained and reviewed separately with your approval**. No auto-clone or arbitrary branch is accepted. Example for one selected workflow:

```bash
# Read-only plan (no copy or execution):
python3 scripts/skill_doctor.py stage character-refs \
  --source "/absolute/path/to/reviewed/shuohao-skills" \
  --target "/absolute/path/to/private/external-skills" --dry-run

# Explicit local staging after reviewing source/target:
python3 scripts/skill_doctor.py stage character-refs \
  --source "/absolute/path/to/reviewed/shuohao-skills" \
  --target "/absolute/path/to/private/external-skills"

# Check staged package and optional native bootstrap directory:
python3 scripts/skill_doctor.py doctor \
  --external-root "/absolute/path/to/private/external-skills" \
  --host-root "/absolute/path/to/host/skills" --check-runtime --json
```

**Windows:** run the equivalent `py -3 scripts/skill_doctor.py ...` if Python is installed; use quoted actual Windows paths. These examples are **not executed by the bundle**, and no Python/Node/Git installation is performed for you. The default stage command will not overwrite an existing directory. `--replace-managed` is opt-in and only accepts a previously verified package with the expected marker, all original file hashes and license/notice. Copy/replace uses a temporary directory and preserves the last valid copy if moving the new copy fails. Do not place user projects or personal media in the public Git repository.

Staging is into a separate **private external source directory**, not the host's native global skill root. Read the staged `SKILL.md` or explicitly add the reviewed external directory to your local retrieval setup after checking for name collisions. The bundle does not automatically register or index this package; the central reviewed bundle count stays **188**. No third-party scripts are invoked by the status or stage commands.

### Runtime and workflow prerequisites

- Shuohao's scripts need **Node 18+**, using its documented standard-library tooling; no npm install is needed for those skill scripts at the reviewed revision. `doctor --check-runtime` runs only `node --version`, not the skill scripts.
- Story planning, writing, and art-direction packages need an active model/host. The `character-refs` image-generation workflow also requires a supported image provider or model and any applicable authorization. The storyboard's actual image/video delivery similarly depends on available providers.
- A local package with valid bytes is **Unverified** until the chosen task runs successfully in the active host; neither `doctor` nor a GitHub CI pass proves provider access, correct images, or native host integration.
- Never install upstream shuohao's blanket symlink installer automatically: it targets host directories and can expose more skill names globally. Keep selective staging separate from the two native bootstraps.
- Some combined-report workflows use upstream root-level scripts (`scripts/report.mjs`): use the separately reviewed full upstream checkout for those, not a single staged directory. A staged original skill is not the complete upstream multi-skill application.

## Other external runtimes

PAUL's native slash-command framework, OpenMontage video app, Pixel Agents extension, ECC's native plugin/agents/hooks, Claude-Mem worker, n8n instance MCP and the local retrieval MCP each have independent installation/authorization requirements. Their router in this bundle is **Setup Required**, not a working external runtime. Review upstream licenses, dependencies and security before enabling any of them. Do not treat `SKILL.md` as installation of an executable or grant of credentials.

## Maintenance and test boundaries

```bash
python3 scripts/public_repo_gate.py .
python3 tests/verify-skill-doctor.py
bash tests/on-demand-install.sh
```

CI verifies the offline lookup, six pinned Shuohao package manifests, staged completeness, binary hashes, license/NOTICE, failure on tampering, opt-in replacement and native two-bootstrap invariant. It does **not** download or execute Shuohao or configure your PC. Manual host acceptance is a separate step.
