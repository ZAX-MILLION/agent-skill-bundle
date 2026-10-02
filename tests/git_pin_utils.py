#!/usr/bin/env python3
"""Cross-platform Git blob pin checks that tolerate checkout line-ending conversion."""
from __future__ import annotations

import pathlib
import subprocess


def _rel(repo: pathlib.Path, path: pathlib.Path) -> str:
    return path.resolve().relative_to(repo.resolve()).as_posix()


def tracked_blob_sha(repo: pathlib.Path, path: pathlib.Path) -> str:
    relative = _rel(repo, path)
    return subprocess.check_output(
        ["git", "-C", str(repo), "rev-parse", f"HEAD:{relative}"],
        text=True,
    ).strip()


def assert_tracked_pin(
    repo: pathlib.Path,
    source: pathlib.Path,
    expected_sha: str,
    installed: pathlib.Path | None = None,
) -> None:
    assert source.is_file(), f"missing pinned source file: {source}"
    relative = _rel(repo, source)

    actual = tracked_blob_sha(repo, source)
    assert actual == expected_sha, (
        f"Git blob pin mismatch: {relative}; expected {expected_sha}, got {actual}"
    )

    # Git applies the repository's clean/text rules here, so a Windows CRLF
    # checkout does not become a false modification when the committed blob is LF.
    unchanged = subprocess.run(
        ["git", "-C", str(repo), "diff", "--quiet", "--", relative],
        check=False,
    )
    assert unchanged.returncode == 0, f"working-tree source differs from HEAD: {relative}"

    if installed is not None:
        assert installed.is_file(), f"missing installed copy: {installed}"
        assert source.read_bytes() == installed.read_bytes(), (
            f"installed copy differs from checked-out source: {installed}"
        )
