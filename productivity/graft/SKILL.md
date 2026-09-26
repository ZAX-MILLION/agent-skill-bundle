---
name: graft
description: Maintain a single skills vault across coding agents using reviewed, declarative distribution; inspect status and dry-run before applying changes.
---
# Graft — optional distribution manager

Source: https://github.com/Mikko-ww/agent-skills-graft at `a5e1564560b06c8bbb682f221b74cb915fa0c559`. Original adapter; no Graft program or external dependency is bundled. Its Python package metadata declares MIT, Python 3.11+, `typer` and `ruamel.yaml`; review upstream licensing/distribution before installing.

The present bundle's `install.sh --flat [--on-demand]` already provides a tested safe copy workflow. Graft is **optional**, for a user who wants a declarative profile and links from one local vault to multiple agent directories. Do not replace working installs merely because Graft exists.

1. Check whether `graft` is available. If not, explain that this skill is a guide, not a runtime; review the pinned source before installing.
2. Use `graft status` and `graft apply --dry-run` first; review every target, duplicate name, symlink, overwrite and prune action.
3. Preserve the bundle's source checkout and the strict two-bootstrap on-demand mode. A Graft profile that installs every skill natively defeats minimal discovery; distribute only the selected bootstrap unless the user opts in to full native installation.
4. Do not run `graft apply --prune` or import private skills into the public repository without explicit approval. Back up target configurations and preserve unrelated skills.
5. On Windows or hosts without symlink support, use a reviewed copy-based installation instead; do not assume every editor permits external symlinks.
6. Verify the actual host's skill list after any change; a successful filesystem copy is not proof of native discovery or runtime execution.
