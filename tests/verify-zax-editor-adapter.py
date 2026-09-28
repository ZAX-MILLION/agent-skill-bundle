#!/usr/bin/env python3
"""Offline tests for the zax-editor portable adapter and verifier."""
from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import pathlib
import tempfile
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "creative/zax-editor"
REGISTRY = json.loads((ROOT / "registry/zax-editor.json").read_text(encoding="utf-8"))
MANIFEST = json.loads((ADAPTER / "references/package-manifest.json").read_text(encoding="utf-8"))

spec = importlib.util.spec_from_file_location("veb_verify", ADAPTER / "scripts/verify_package.py")
verify = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verify)

assert REGISTRY["adapter_path"] == "creative/zax-editor"
assert REGISTRY["reviewed_package"]["archive_sha256"] == MANIFEST["archive"]["sha256"]
assert REGISTRY["reviewed_package"]["unpacked_file_count"] == MANIFEST["directory"]["file_count"] == 90
assert REGISTRY["reviewed_package"]["tree_sha256"] == MANIFEST["directory"]["tree_sha256"]
assert REGISTRY["licensing_boundary"]["general_code_redistribution_license_found"] is False
assert REGISTRY["bundle_distribution"]["original_runtime_files_copied"] == 0


def digest(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


with tempfile.TemporaryDirectory() as td:
    tmp = pathlib.Path(td)
    runtime = tmp / "video-editor-bassam"
    runtime.mkdir()
    (runtime / "SKILL.md").write_text("fixture skill\n", encoding="utf-8")
    (runtime / "note.txt").write_text("fixture note\n", encoding="utf-8")

    entries = []
    total = 0
    for path in sorted(runtime.rglob("*")):
        if path.is_file():
            rel = path.relative_to(runtime).as_posix()
            size = path.stat().st_size
            total += size
            entries.append((rel, size, digest(path)))

    fixture_manifest = {
        "archive": {"root_directory": "video-editor-bassam"},
        "directory": {
            "file_count": len(entries),
            "unpacked_size": total,
            "tree_sha256": verify.tree_digest(entries),
        },
    }

    with contextlib.redirect_stdout(io.StringIO()) as stdout:
        verify.verify_directory(runtime, fixture_manifest)
    assert "VERIFIED" in stdout.getvalue()

    (runtime / "note.txt").write_text("tampered\n", encoding="utf-8")
    try:
        verify.verify_directory(runtime, fixture_manifest)
        raise AssertionError("tampered runtime unexpectedly verified")
    except verify.VerificationError:
        pass

    good_zip = tmp / "good.zip"
    with zipfile.ZipFile(good_zip, "w") as zf:
        zf.writestr("video-editor-bassam/SKILL.md", "fixture skill\n")
        zf.writestr("video-editor-bassam/note.txt", "fixture note\n")
    zip_manifest = {
        "archive": {
            "root_directory": "video-editor-bassam",
            "size": good_zip.stat().st_size,
            "sha256": digest(good_zip),
        },
        "directory": {"file_count": 2},
    }
    with contextlib.redirect_stdout(io.StringIO()) as stdout:
        verify.verify_zip(good_zip, zip_manifest)
    assert "VERIFIED" in stdout.getvalue()

    bad_zip = tmp / "bad.zip"
    with zipfile.ZipFile(bad_zip, "w") as zf:
        zf.writestr("outside.txt", "nope")
    bad_manifest = {
        "archive": {
            "root_directory": "video-editor-bassam",
            "size": bad_zip.stat().st_size,
            "sha256": digest(bad_zip),
        },
        "directory": {"file_count": 1},
    }
    try:
        verify.verify_zip(bad_zip, bad_manifest)
        raise AssertionError("unsafe archive root unexpectedly verified")
    except verify.VerificationError:
        pass

print("PASS: zax-editor adapter registry, integrity verifier, tamper rejection and archive-root safety")
