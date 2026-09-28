#!/usr/bin/env python3
"""Verify a locally obtained video-editor-bassam package without executing it.

Python standard library only. Accepts the original ZIP or an unpacked runtime
directory and compares it with the package reviewed for this bundle adapter.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
MANIFEST = HERE.parent / "references" / "package-manifest.json"


class VerificationError(Exception):
    pass


def digest_stream(stream) -> str:
    h = hashlib.sha256()
    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
        h.update(chunk)
    return h.hexdigest()


def digest_file(path: pathlib.Path) -> str:
    with path.open("rb") as stream:
        return digest_stream(stream)


def tree_digest(entries: list[tuple[str, int, str]]) -> str:
    h = hashlib.sha256()
    for rel, size, file_hash in sorted(entries):
        h.update(rel.encode("utf-8"))
        h.update(b"\0")
        h.update(str(size).encode("ascii"))
        h.update(b"\0")
        h.update(file_hash.encode("ascii"))
        h.update(b"\n")
    return h.hexdigest()


def verify_zip(path: pathlib.Path, manifest: dict) -> None:
    expected = manifest["archive"]
    if path.stat().st_size != expected["size"]:
        raise VerificationError(
            f"archive size differs: got {path.stat().st_size}, expected {expected['size']}"
        )
    actual = digest_file(path)
    if actual != expected["sha256"]:
        raise VerificationError("archive SHA-256 differs from the reviewed package")

    with zipfile.ZipFile(path) as zf:
        files = [x for x in zf.infolist() if not x.is_dir()]
        root = expected["root_directory"].rstrip("/") + "/"
        if len(files) != manifest["directory"]["file_count"]:
            raise VerificationError(
                f"archive file count differs: got {len(files)}, expected "
                f"{manifest['directory']['file_count']}"
            )
        for info in files:
            normalized = info.filename.replace("\\", "/")
            if not normalized.startswith(root):
                raise VerificationError("archive contains a file outside the reviewed root")
            rel = normalized[len(root):]
            if not rel or rel.startswith("/") or ".." in pathlib.PurePosixPath(rel).parts:
                raise VerificationError(f"unsafe archive path: {info.filename}")

    print("VERIFIED: archive matches the reviewed video-editor-bassam package.")
    print("No third-party script was executed. Runtime/dependency readiness is still unverified.")


def verify_directory(path: pathlib.Path, manifest: dict) -> None:
    if path.is_symlink() or not path.is_dir():
        raise VerificationError("runtime path must be a real directory")

    # Accept either the runtime directory itself or a parent containing exactly
    # the reviewed top-level directory name.
    candidate = path
    nested = path / manifest["archive"]["root_directory"]
    if not (candidate / "SKILL.md").is_file() and (nested / "SKILL.md").is_file():
        candidate = nested

    entries: list[tuple[str, int, str]] = []
    total = 0
    for item in candidate.rglob("*"):
        if item.is_symlink():
            raise VerificationError(f"symlink not allowed in reviewed runtime: {item}")
        if not item.is_file():
            continue
        rel = item.relative_to(candidate).as_posix()
        size = item.stat().st_size
        total += size
        entries.append((rel, size, digest_file(item)))

    expected = manifest["directory"]
    if len(entries) != expected["file_count"]:
        raise VerificationError(
            f"directory file count differs: got {len(entries)}, expected {expected['file_count']}"
        )
    if total != expected["unpacked_size"]:
        raise VerificationError(
            f"directory size differs: got {total}, expected {expected['unpacked_size']}"
        )
    actual_tree = tree_digest(entries)
    if actual_tree != expected["tree_sha256"]:
        raise VerificationError("directory content differs from the reviewed package")

    print(f"VERIFIED: {candidate} matches the reviewed video-editor-bassam package.")
    print("No third-party script was executed. Runtime/dependency readiness is still unverified.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("package", help="Path to video-editor-bassam.zip or unpacked directory")
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    path = pathlib.Path(args.package).expanduser().resolve()
    if not path.exists():
        print("FAIL: package path does not exist", file=sys.stderr)
        return 2

    try:
        if path.is_file():
            if path.suffix.lower() != ".zip":
                raise VerificationError("expected the reviewed ZIP or an unpacked directory")
            verify_zip(path, manifest)
        else:
            verify_directory(path, manifest)
    except (VerificationError, OSError, zipfile.BadZipFile) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
