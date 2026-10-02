#!/usr/bin/env python3
"""Verify pinned selected ECC source files and metadata-only catalog; no network."""
import json
import pathlib
import sys

from git_pin_utils import assert_tracked_pin

repo = pathlib.Path(sys.argv[1]).resolve()
installed = pathlib.Path(sys.argv[2]).resolve()
pins = json.loads((repo / "registry/vendor-ecc.json").read_text())
index = json.loads((repo / pins["source_index"]).read_text())
assert index["reviewed_commit"] == pins["reviewed_commit"]
entries = index["skills"]
assert len(entries) == index["original_skill_count"] == 292
names = [x["name"] for x in entries]
assert len(set(names)) == 292 and all(x["source_path"] == f"skills/{x['name']}/SKILL.md" for x in entries)
by_path = {x["source_path"]: x["blob_sha"] for x in entries}
assert len(pins["skill_pins"]) == 9
checks = 0
for local_path, spec in pins["skill_pins"].items():
    assert by_path[spec["upstream_path"]] == spec["blob_sha"], spec["upstream_path"]
    name = pathlib.Path(local_path).parent.name
    source_skill = repo / local_path
    installed_skill = installed / name / "SKILL.md"
    assert f"name: {name}" in source_skill.read_text().split("---", 2)[1], source_skill
    assert_tracked_pin(repo, source_skill, spec["blob_sha"], installed_skill)
    checks += 2

    source_license = repo / pathlib.Path(local_path).parent / "LICENSE.txt"
    installed_license = installed / name / "LICENSE.txt"
    assert spec["license_blob_sha"] == pins["root_license_blob_sha"]
    assert_tracked_pin(repo, source_license, spec["license_blob_sha"], installed_license)
    checks += 2
print(f"PASS: ECC {len(entries)} unique canonical index entries; {len(pins['skill_pins'])} selected complete skill+license packages; {checks} original and installed blob checks")
