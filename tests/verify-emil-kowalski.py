#!/usr/bin/env python3
"""Verify selected Emil Kowalski packages and installed copies offline."""
from __future__ import annotations

import json
import pathlib
import sys

from git_pin_utils import assert_tracked_pin

repo, installed = map(lambda p: pathlib.Path(p).resolve(), sys.argv[1:3])
data = json.loads((repo / "registry/vendor-emil-kowalski.json").read_text(encoding="utf-8"))

assert data["canonical_repository"] == "emilkowalski/skills"
assert data["reviewed_commit"] == "e8a175de22ae1e49370fc144c1f3bb9aeedf988d"
assert data["upstream_license"] == "MIT"
assert len(data["packages"]) == 5

checks = 0
for package in data["packages"]:
    local = repo / package["local_directory"]
    copied = installed / local.name

    expected_files = set(package["files"]) | {"LICENSE.txt"}
    local_files = {
        p.relative_to(local).as_posix()
        for p in local.rglob("*")
        if p.is_file()
    }
    assert local_files == expected_files, (
        f"partial/extra Emil package files: {local}; "
        f"delta={sorted(local_files ^ expected_files)}"
    )

    for relative, sha in package["files"].items():
        assert_tracked_pin(repo, local / relative, sha, copied / relative)
        checks += 2

    assert_tracked_pin(
        repo,
        local / "LICENSE.txt",
        data["root_license_blob_sha"],
        copied / "LICENSE.txt",
    )
    checks += 2

print(f"PASS: {len(data['packages'])} selected Emil Kowalski packages; {checks} pin/install checks")
