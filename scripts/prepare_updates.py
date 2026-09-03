#!/usr/bin/env python3
"""Prepare canonical upstream updates without merging them.

Runs the read-only canonical audit, selects only entries classified as
UPDATE_AVAILABLE, and delegates exact copying to sync_reviewed.py on a new
local review branch. By default this is a dry run. --apply prepares and commits
the review branch. --push optionally publishes that review branch; main is
never merged or force-updated by this tool.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINE = re.compile(r"^(UPDATE_AVAILABLE)\s+(\S+)")


def run(*args: str, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(list(args), cwd=ROOT, check=True, text=True, capture_output=capture)


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare a review branch for canonical upstream skill updates.")
    parser.add_argument("--apply", action="store_true", help="Create and commit a local review branch.")
    parser.add_argument("--push", action="store_true", help="Push the prepared review branch to origin. Requires --apply.")
    parser.add_argument("--branch", help="Review branch name; defaults to upstream-sync/YYYYMMDD-HHMMSS.")
    args = parser.parse_args()
    if args.push and not args.apply:
        parser.error("--push requires --apply")

    audit = run(sys.executable, "scripts/audit_skills.py", capture=True)
    print(audit.stdout, end="")
    updates = []
    for line in audit.stdout.splitlines():
        match = LINE.match(line)
        if match:
            updates.append(match.group(2))

    if not updates:
        print("\nNo canonical UPDATE_AVAILABLE entries found. Baseline/review-required differences are never auto-selected.")
        return 0

    print("\nCanonical updates:")
    for path in updates:
        print(f"  - {path}")

    if not args.apply:
        print("\nDry run only. Use --apply to prepare an exact-copy review branch; main will remain untouched.")
        return 0

    branch = args.branch or f"upstream-sync/{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
    run(
        sys.executable,
        "scripts/sync_reviewed.py",
        *updates,
        "--apply",
        "--reviewed",
        "--commit",
        "--branch",
        branch,
    )

    if args.push:
        run("git", "push", "-u", "origin", branch)
        print(f"\nPublished review branch: {branch}")
        print("No merge was performed. Review the branch/PR before integrating it into main.")
    else:
        print(f"\nPrepared local review branch: {branch}")
        print("Nothing was pushed or merged.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        print(f"Update preparation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
