#!/usr/bin/env python3
"""Verify pinned selected ECC source files and metadata-only catalog; no network."""
import json
import pathlib
import subprocess
import sys

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
    for file in (repo / local_path, installed / name / "SKILL.md"):
        assert file.is_file(), file
        assert f"name: {name}" in file.read_text().split("---", 2)[1], file
        digest = subprocess.check_output(["git", "hash-object", str(file)], text=True).strip()
        assert digest == spec["blob_sha"], file
        checks += 1
    for file in (repo / pathlib.Path(local_path).parent / "LICENSE.txt", installed / name / "LICENSE.txt"):
        assert file.is_file(), file
        digest = subprocess.check_output(["git", "hash-object", str(file)], text=True).strip()
        assert digest == spec["license_blob_sha"] == pins["root_license_blob_sha"], file
        checks += 1
print(f"PASS: ECC {len(entries)} unique canonical index entries; {len(pins['skill_pins'])} selected complete skill+license packages; {checks} original and installed blob checks")
