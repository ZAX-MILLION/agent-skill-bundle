#!/usr/bin/env python3
"""Regression test: CRLF checkout conversion must not break Git blob pins."""
from __future__ import annotations

import pathlib
import subprocess
import tempfile

from git_pin_utils import assert_tracked_pin, tracked_blob_sha


def run(repo: pathlib.Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


with tempfile.TemporaryDirectory() as td:
    root = pathlib.Path(td)
    run(root, "init")
    run(root, "config", "user.email", "test@example.invalid")
    run(root, "config", "user.name", "Pin Test")
    run(root, "config", "core.autocrlf", "true")

    source = root / "sample.md"
    source.write_bytes(b"line one\nline two\n")
    run(root, "add", "sample.md")
    run(root, "commit", "-m", "fixture")
    expected = tracked_blob_sha(root, source)

    # Simulate a Windows working-tree checkout. The committed Git blob remains LF.
    source.write_bytes(b"line one\r\nline two\r\n")
    installed = root / "installed.md"
    installed.write_bytes(source.read_bytes())
    assert_tracked_pin(root, source, expected, installed)

    # A real content change must still fail.
    source.write_bytes(b"line one\r\nCHANGED\r\n")
    installed.write_bytes(source.read_bytes())
    try:
        assert_tracked_pin(root, source, expected, installed)
    except AssertionError:
        pass
    else:
        raise AssertionError("semantic working-tree modification was not detected")

print("PASS: CRLF-only checkout conversion is accepted; real content changes still fail")
