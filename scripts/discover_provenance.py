#!/usr/bin/env python3
"""Discover provenance candidates without altering bundled skills.

Unique exact Git-tree matches can be emitted as registry candidates. Name-only
matches are reported for manual review and are never auto-accepted.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES_FILE = ROOT / "registry" / "sources.json"
CATEGORIES = ("design", "security", "multiplayer", "wordpress", "marketing", "process")
API = "https://api.github.com"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def github_json(path: str) -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "agent-skill-bundle-provenance-discovery",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(f"{API}{path}", headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def local_skills() -> list[tuple[str, str, str]]:
    result = []
    for category in CATEGORIES:
        root = ROOT / category
        if not root.is_dir():
            continue
        for skill in sorted(root.iterdir()):
            if not skill.is_dir() or not (skill / "SKILL.md").is_file():
                continue
            local_path = f"{category}/{skill.name}"
            sha = subprocess.run(
                ["git", "rev-parse", f"HEAD:{local_path}"],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            result.append((local_path, skill.name, sha))
    return result


def upstream_trees(source: dict) -> tuple[str, list[dict]]:
    repo = source["repository"]
    branch = source["default_branch"]
    commit = github_json(f"/repos/{repo}/commits/{urllib.parse.quote(branch, safe='')}")["sha"]
    tree = github_json(f"/repos/{repo}/git/trees/{commit}?recursive=1")
    if tree.get("truncated"):
        raise RuntimeError(f"Truncated Git tree for {repo}")
    dirs = [item for item in tree.get("tree", []) if item.get("type") == "tree"]
    return commit, dirs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    args = parser.parse_args()

    sources = [s for s in load_json(SOURCES_FILE)["sources"] if s.get("type") == "upstream"]
    by_sha: dict[str, list[dict]] = defaultdict(list)
    by_name: dict[str, list[dict]] = defaultdict(list)

    for source in sources:
        commit, dirs = upstream_trees(source)
        for item in dirs:
            record = {
                "source_id": source["id"],
                "repository": source["repository"],
                "source_path": item["path"],
                "tree_sha": item["sha"],
                "commit": commit,
            }
            by_sha[item["sha"]].append(record)
            by_name[Path(item["path"]).name].append(record)

    results = []
    for local_path, name, sha in local_skills():
        exact = by_sha.get(sha, [])
        if len(exact) == 1:
            state, candidates = "UNIQUE_EXACT_MATCH", exact
        elif len(exact) > 1:
            state, candidates = "AMBIGUOUS_EXACT_MATCH", exact
        else:
            same_name = by_name.get(name, [])
            state = "NAME_MATCH_REVIEW" if same_name else "UNMAPPED"
            candidates = same_name
        results.append({
            "local_path": local_path,
            "local_tree_sha": sha,
            "state": state,
            "candidates": candidates,
        })

    if args.json:
        print(json.dumps({"skills": results}, indent=2))
    else:
        counts: dict[str, int] = defaultdict(int)
        for item in results:
            counts[item["state"]] += 1
            candidate = item["candidates"][0] if len(item["candidates"]) == 1 else None
            suffix = f" -> {candidate['repository']}:{candidate['source_path']}" if candidate else ""
            print(f"{item['state']:<24} {item['local_path']}{suffix}")
        print("\nSummary:")
        for state in sorted(counts):
            print(f"  {state:<24} {counts[state]}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Provenance discovery failed: {exc}", file=sys.stderr)
        raise
