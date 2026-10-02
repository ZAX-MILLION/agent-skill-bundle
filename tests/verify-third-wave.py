#!/usr/bin/env python3
"""Check recorded upstream Git blobs and their copied install equivalents (stdlib only)."""
import json
import pathlib
import sys

from git_pin_utils import assert_tracked_pin

repo = pathlib.Path(sys.argv[1]).resolve()
target = pathlib.Path(sys.argv[2]).resolve()
pins = json.loads((repo / "registry/vendor-third-wave.json").read_text())
expected = pins["pinned_git_blob_sha"]
assert len(expected) == 100, f"expected 100 reviewed source/license blobs, got {len(expected)}"
for rel, sha in expected.items():
    source = repo / rel
    installed = target / pathlib.Path(rel).parts[1] / pathlib.Path(*pathlib.Path(rel).parts[2:])
    assert_tracked_pin(repo, source, sha, installed)
print(f"PASS: {len(expected)} pinned Git blobs and installed copies match across checkout line endings")
