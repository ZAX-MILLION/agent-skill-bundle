#!/usr/bin/env python3
"""Check recorded upstream Git blobs and their copied install equivalents (stdlib only)."""
import hashlib
import json
import pathlib
import sys

repo = pathlib.Path(sys.argv[1]).resolve()
target = pathlib.Path(sys.argv[2]).resolve()
pins = json.loads((repo / "registry/vendor-third-wave.json").read_text())
expected = pins["pinned_git_blob_sha"]
assert len(expected) == 100, f"expected 100 reviewed source/license blobs, got {len(expected)}"
for rel, sha in expected.items():
    source = repo / rel
    installed = target / pathlib.Path(rel).parts[1] / pathlib.Path(*pathlib.Path(rel).parts[2:])
    for path in (source, installed):
        assert path.is_file(), f"missing pinned file: {path}"
        content = path.read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()
        assert actual == sha, f"source/content mismatch: {path}"
print(f"PASS: {len(expected)} pinned original/license files and {len(expected)} installed copies match")
