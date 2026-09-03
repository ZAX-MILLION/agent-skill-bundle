#!/usr/bin/env python3
"""Prepare canonical upstream updates without merging them.

Runs the read-only canonical audit, selects only entries classified as
UPDATE_AVAILABLE, and delegates exact copying to sync_reviewed.py on a review
branch. Default mode is dry-run. The default branch name is deterministic for
the selected upstream tree revisions, so a scheduled run does not create a new
branch every day for the same unreviewed update.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINE = re.compile(r"^UPDATE_AVAILABLE\s+(\S+).*?upstream=([0-9a-f]+)")


def run(*args: str, capture: bool = False, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(list(args), cwd=ROOT, check=check, text=True, capture_output=capture)


def branch_exists(branch: str) -> bool:
    result = run("git", "show-ref", "--verify", "--quiet", f"refs/heads/{branch}", check=False)
    return result.returncode == 0


def default_branch(updates: list[tuple[str, str]]) -> str:
    material = "\n".join(f"{path}:{sha}" for path, sha in sorted(updates))
    fingerprint = hashlib.sha256(material.encode("utf-8")).hexdigest()[:12]
    return f"upstream-sync/{fingerprint}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare a review branch for canonical upstream skill updates.")
    parser.add_argument("--apply", action="store_true", help="Create and commit a local review branch.")
    parser.add_argument("--push", action="store_true", help="Push the prepared review branch to origin. Requires --apply.")
    parser.add_argument("--branch", help="Explicit review branch name. Default is deterministic from upstream tree SHAs.")
    args = parser.parse_args()
    if args.push and not args.apply:
        parser.error("--push requires --apply")

    audit = run(sys.executable, "scripts/audit_skills.py", capture=True)
    print(audit.stdout, end="")
    updates: list[tuple[str, str]] = []
    for line in audit.stdout.splitlines():
        match = LINE.match(line)
        if match:
            updates.append((match.group(1), match.group(2)))

    if not updates:
        print("\nNo canonical UPDATE_AVAILABLE entries found. Baseline/review-required differences are never auto-selected.")
        return 0

    print("\nCanonical updates:")
    for path, sha in updates:
        print(f"  - {path} (upstream tree {sha})")

    branch = args.branch or default_branch(updates)
    print(f"Review branch: {branch}")

    if not args.apply:
        print("\nDry run only. Use --apply to prepare an exact-copy review branch; main will remain untouched.")
        return 0

    if branch_exists(branch):
        print(f"\nReview branch already exists for this exact update set: {branch}")
        if args.push:
            run("git", "push", "-u", "origin", branch)
            print("Published/reconciled the existing review branch. No merge was performed.")
        return 0

    run(
        sys.executable,
        "scripts/sync_reviewed.py",
        *(path for path, _ in updates),
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
