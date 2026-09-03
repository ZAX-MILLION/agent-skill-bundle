#!/usr/bin/env python3
"""Check registered upstream repositories and optionally write a revision snapshot.

No third-party Python packages are required.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "sources.json"
STATE = ROOT / "registry" / "upstream-state.json"
API = "https://api.github.com"


def load_sources() -> dict:
    with REGISTRY.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def github_json(path: str) -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "agent-skill-bundle-upstream-checker",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(f"{API}{path}", headers=headers)
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check current upstream branch revisions.")
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write registry/upstream-state.json after all upstream checks succeed.",
    )
    args = parser.parse_args()

    registry = load_sources()
    results = []
    failures = 0

    for source in registry["sources"]:
        if source.get("type") != "upstream":
            continue

        repo = source["repository"]
        branch = source["default_branch"]
        try:
            commit = github_json(f"/repos/{repo}/commits/{branch}")
            sha = commit["sha"]
            results.append(
                {
                    "id": source["id"],
                    "repository": repo,
                    "branch": branch,
                    "commit": sha,
                }
            )
            print(f"OK   {source['id']:<32} {sha[:12]}")
        except (urllib.error.URLError, urllib.error.HTTPError, KeyError, ValueError) as exc:
            failures += 1
            print(f"FAIL {source['id']:<32} {exc}", file=sys.stderr)

    if failures:
        print(f"\n{failures} upstream check(s) failed; state file was not changed.", file=sys.stderr)
        return 1

    if args.write:
        payload = {
            "schema_version": 1,
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "sources": results,
        }
        STATE.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"\nWrote {STATE.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
