# Contributing

Agent Skill Bundle is a distribution project first. Changes must preserve provenance and upstream authorship.

## Do not edit upstream-backed skills directly

If a skill is copied from a third-party upstream repository, do not patch its instructions locally to make it work better for one agent.

Instead:

1. contribute the improvement upstream when appropriate; or
2. add host-specific compatibility behavior under `adapters/`.

Direct local edits make future synchronization ambiguous and can erase the distinction between upstream work and bundle-owned work.

## Adding an upstream skill

Before a third-party skill is treated as syncable, record:

- upstream repository;
- default branch;
- exact source path;
- checked upstream commit;
- local path;
- upstream directory tree SHA;
- local directory tree SHA;
- license / notice requirements.

Add the source to `registry/sources.json` when it is new and add per-skill provenance to `registry/skills.json`.

Preserve the complete skill directory when relative scripts, references, examples or assets are required.

## Updating an upstream skill

Upstream updates are review-first.

Before merging an update:

1. inspect the upstream diff;
2. review license or notice changes;
3. review new executable scripts, network calls, package installs, credential handling and destructive commands;
4. confirm the update still belongs to the same source path/project;
5. copy the upstream files without rewriting attribution;
6. run the relevant provenance audit;
7. update the recorded commit/tree metadata.

Do not auto-merge an upstream change directly into `main`.

## Custom skills

Bundle-owned custom skills must be clearly distinguishable from third-party upstream skills. Current local/custom categories include parts of `security/` and `qa/`.

## Adapters

Adapters should stay thin. They may describe installation paths, capability mappings or host-specific invocation, but should not duplicate the full skill body.

If a host lacks a required capability, report the limitation instead of inventing a fake equivalent.

## Useful checks

```bash
python3 scripts/check_upstreams.py
python3 scripts/audit_skills.py
```

The first checks registered source revisions. The second audits per-skill Git tree mappings that have already been registered.
