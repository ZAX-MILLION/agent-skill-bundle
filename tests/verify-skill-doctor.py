#!/usr/bin/env python3
"""Offline tests: discovery, status, pinned complete copy and failure isolation."""
import contextlib
import hashlib
import importlib.util
import io
import json
import pathlib
import tempfile
from types import SimpleNamespace
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("skill_doctor", ROOT / "scripts/skill_doctor.py")
doctor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(doctor)


def record(path):
    return {"path": path.name, "sha": doctor.git_blob(path), "size": path.stat().st_size, "mode": "100644"}


with tempfile.TemporaryDirectory() as td:
    tmp = pathlib.Path(td)
    source = tmp / "upstream"
    package = source / "skills/novel-art"
    (package / "scripts").mkdir(parents=True)
    (package / "references").mkdir()
    (package / "assets").mkdir()
    (package / "SKILL.md").write_text("---\nname: novel-art\n---\n", encoding="utf-8")
    (package / "scripts/selftest.mjs").write_text("console.log('test');\n", encoding="utf-8")
    (package / "references/spec.md").write_text("reference\n", encoding="utf-8")
    (package / "assets/test.bin").write_bytes(b"\x00\xfe\x80BINARY")
    (source / "LICENSE").write_text("license fixture\n", encoding="utf-8")
    (source / "NOTICE").write_text("notice fixture\n", encoding="utf-8")
    pins = []
    for file in sorted(package.rglob("*")):
        if file.is_file():
            item = record(file)
            item["path"] = file.relative_to(package).as_posix()
            pins.append(item)
    meta = {
        "source_repository": "fixture/shuohao",
        "source_revision": "fixture-pinned-revision",
        "root_notice_files": [record(source / "LICENSE"), record(source / "NOTICE")],
        "packages": [{"name": "novel-art", "source_path": "skills/novel-art", "files": pins}],
    }
    meta["packages"][0]["source_tree_sha"] = "fixture-tree"
    out = tmp / "external"
    args = SimpleNamespace(
        skill="novel-art", source=source, target=out,
        dry_run=True, replace_managed=False,
    )
    with patch.object(doctor, "manifest", return_value=meta), patch.object(
        doctor, "run_git_head", return_value=meta["source_revision"]
    ):
        with contextlib.redirect_stdout(io.StringIO()) as stdout:
            doctor.stage(args)
        assert "DRY RUN" in stdout.getvalue()
        assert not out.exists(), "dry-run unexpectedly made files"

        args.dry_run = False
        with contextlib.redirect_stdout(io.StringIO()) as stdout:
            doctor.stage(args)
        assert "Execution unverified" in stdout.getvalue()
        dest = out / "novel-art"
        doctor.verify_staged(dest, meta["packages"][0])
        assert (dest / "scripts/selftest.mjs").read_bytes() == (package / "scripts/selftest.mjs").read_bytes()
        assert (dest / "assets/test.bin").read_bytes() == b"\x00\xfe\x80BINARY"
        assert (dest / "LICENSE.txt").is_file() and (dest / "NOTICE.txt").is_file()

        # Must never overwrite even a valid bundle-managed directory by default.
        try:
            doctor.stage(args)
            raise AssertionError("silent replacement accepted")
        except doctor.ValidationError as exc:
            assert "--replace-managed" in str(exc)
        args.replace_managed = True
        with contextlib.redirect_stdout(io.StringIO()):
            doctor.stage(args)
        doctor.verify_staged(dest, meta["packages"][0])

        # Fail closed on modified files, extras and symlinks.
        (dest / "SKILL.md").write_text("tampered", encoding="utf-8")
        try:
            doctor.verify_staged(dest, meta["packages"][0])
            raise AssertionError("tampered package accepted")
        except doctor.ValidationError:
            pass
        (dest / "SKILL.md").write_bytes((package / "SKILL.md").read_bytes())
        (dest / "extra.txt").write_text("not approved")
        try:
            doctor.verify_staged(dest, meta["packages"][0])
            raise AssertionError("unexpected package file accepted")
        except doctor.ValidationError:
            pass
        (dest / "extra.txt").unlink()
        doctor.verify_staged(dest, meta["packages"][0])
        (package / "scripts/selftest.mjs").write_text("tampered", encoding="utf-8")
        try:
            doctor.stage(args)
            raise AssertionError("modified source package accepted")
        except doctor.ValidationError:
            pass
        assert (dest / "SKILL.md").read_text().startswith("---"), "failed stage damaged good package"

        # Doctor does not report 'Ready' just because a guide or code copy exists.
        dargs = SimpleNamespace(vault=ROOT, host_root=None, external_root=None, json=True)
        with contextlib.redirect_stdout(io.StringIO()) as stdout:
            doctor.doctor(dargs)
        result = json.loads(stdout.getvalue())
        assert result["external"]["novel-art"]["status"] == "Setup Required"
        assert result["retrieval_mcp"].startswith("Unverified")
        assert result["execution"].startswith("Unverified")
        assert result["source_vault_count"] == 188
        assert len(result["per_skill"]) == 188
        assert result["status_counts"]["Ready"] == 0
        assert result["per_skill"]["creative/shuohao-skills"]["status"] == "Setup Required"
        assert result["per_skill"]["process/systematic-debugging"]["status"] == "Unverified"

        qargs = SimpleNamespace(vault=ROOT, command="search", query=["shuohao"], limit=8)
        with contextlib.redirect_stdout(io.StringIO()) as stdout:
            doctor.search(qargs)
        assert "creative/shuohao-skills" in stdout.getvalue()

# The checked-in upstream manifest is a complete inventory of 97 source files.
m = doctor.manifest()
assert m["source_repository"] == "eternityspring/shuohao-skills"
assert m["source_revision"] == "ef4ac0c313c7eeb1f918db5f0f0eb319745900bc"
assert set(doctor.packages()) == {
    "character-refs", "novel-art", "novel-characters",
    "novel-outline", "novel-script", "novel-storyboard",
}
assert sum(len(p["files"]) for p in m["packages"]) == 97
assert {f["path"] for f in m["root_notice_files"]} == {"LICENSE", "NOTICE"}
for pkg in m["packages"]:
    assert "SKILL.md" in {item["path"] for item in pkg["files"]}
    assert len({item["path"] for item in pkg["files"]}) == len(pkg["files"])
    assert all(len(item["sha"]) == 40 and item["size"] >= 0 for item in pkg["files"])

print("PASS: offline discovery, honest status, full-package staging, hashes, license/notice, dry-run, no silent overwrite, tamper rejection")
