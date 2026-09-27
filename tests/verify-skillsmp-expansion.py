#!/usr/bin/env python3
"""Verify 11 exact reviewed source packages, complete supporting files and two local skills.

Offline: no network, third-party script execution, runtime install, or user config edits.
"""
import hashlib
import json
import pathlib
import subprocess
import sys

repo, installed = map(lambda s: pathlib.Path(s).resolve(), sys.argv[1:3])
data = json.loads((repo / "registry/vendor-skillsmp-2026-09-27.json").read_text())
assert data["schema_version"] == 1
packages = data["packages"]
assert len(packages) == 11
assert len({p["local_directory"].split("/")[-1] for p in packages}) == 11

def digest(file):
    assert file.is_file(), f"missing required package file: {file}"
    return subprocess.check_output(["git", "hash-object", str(file)], text=True).strip()

checks = 0
original_count = 0
for package in packages:
    assert package["upstream_license"] == "MIT", package["repository"]
    local = repo / package["local_directory"]
    copied = installed / local.name
    assert "SKILL.md" in package["files"]
    recorded = set(package["files"]) | {"LICENSE.txt"}
    actual = {str(p.relative_to(local)).replace("\\", "/") for p in local.rglob("*") if p.is_file()}
    assert actual == recorded, f"partial/extra package files: {local}, {sorted(actual ^ recorded)}"
    for relative, source in package["files"].items():
        assert source["size"] >= 0
        for path in (local / relative, copied / relative):
            assert digest(path) == source["sha"], path
            checks += 1
        original_count += 1
    for path in (local / "LICENSE.txt", copied / "LICENSE.txt"):
        assert digest(path) == package["root_license_blob_sha"], path
        checks += 1

assert original_count == 97, original_count
assert checks == 216, checks  # (97 original source files + 11 licenses) x two copies

for local_name in ("game-ready-2d-asset-pipeline", "cross-agent-skill-verification"):
    match = list(repo.glob(f"*/{local_name}/SKILL.md"))
    assert len(match) == 1 and (installed / local_name / "SKILL.md").is_file()
    assert match[0].read_bytes() == (installed / local_name / "SKILL.md").read_bytes()
    assert "Original Agent Skill Bundle skill" in match[0].read_text()

# These original sibling names must stay unchanged for relative references.
assert (repo / "qa/core-web-vitals/SKILL.md").is_file()
assert (repo / "qa/performance/references/MEASUREMENT.md").is_file()
assert "../performance/references/MEASUREMENT.md" in (repo / "qa/core-web-vitals/SKILL.md").read_text()
assert "../performance/references/MEASUREMENT.md" in (repo / "qa/web-quality-audit/SKILL.md").read_text()
for relative in (
    "data/styles.csv", "data/ux-guidelines.csv", "data/stacks/html-tailwind.csv",
    "references/quick-reference.md", "scripts/search.py", "scripts/core.py",
    "scripts/design_system.py", "scripts/tests/test_core.py",
):
    assert (repo / "design/ui-ux-pro-max" / relative).is_file(), relative

# No external host/plugins/MCP settings added by these package imports.
assert all(
    not p["local_directory"].startswith(("adapters/", ".claude/", ".codex/", ".gemini/"))
    for p in packages
)
print(
    f"PASS: {len(packages)} full MIT packages, {original_count} exact original files, "
    f"{checks} source/install hashes, 2 original local skills, unchanged cross-skill references"
)
