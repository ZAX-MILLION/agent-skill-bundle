#!/usr/bin/env python3
"""Audit canonical bundle mappings against current upstream Git trees.

The auditor is read-only unless --write is passed. Even with --write, only
registry/skills.json metadata is changed; bundled skill content is never
replaced. Canonical mappings live in registry/mappings.json.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES_FILE = ROOT / "registry" / "sources.json"
SKILLS_FILE = ROOT / "registry" / "skills.json"
MAPPINGS_FILE = ROOT / "registry" / "mappings.json"
API = "https://api.github.com"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def github_json(path: str) -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "agent-skill-bundle-auditor",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(f"{API}{path}", headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def local_tree_sha(path: str) -> str:
    return subprocess.run(
        ["git", "rev-parse", f"HEAD:{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def get_upstream_snapshot(source: dict) -> tuple[str, dict[str, str]]:
    repo = source["repository"]
    branch = source["default_branch"]
    commit = github_json(
        f"/repos/{repo}/commits/{urllib.parse.quote(branch, safe='')}"
    )["sha"]
    tree = github_json(f"/repos/{repo}/git/trees/{commit}?recursive=1")
    if tree.get("truncated"):
        raise RuntimeError(f"Truncated Git tree for {repo}; refusing incomplete audit")
    trees = {
        item["path"]: item["sha"]
        for item in tree.get("tree", [])
        if item.get("type") == "tree"
    }
    return commit, trees


def canonical_entries(mappings: dict, previous: dict) -> list[dict]:
    entries: dict[str, dict] = {}

    for convention in mappings.get("conventions", []):
        category = convention["local_category"]
        root = ROOT / category
        if not root.is_dir():
            continue
        for item in sorted(root.iterdir()):
            if not item.is_dir() or not (item / "SKILL.md").is_file():
                continue
            entries[f"{category}/{item.name}"] = {
                "local_path": f"{category}/{item.name}",
                "source_id": convention["source_id"],
                "source_path": convention["source_path_template"].format(name=item.name),
                "kind": convention.get("kind", "skill"),
                "mapping": "convention",
            }

    for name in mappings.get("anthropic_design_skills", []):
        local_path = f"design/{name}"
        if (ROOT / local_path / "SKILL.md").is_file():
            entries[local_path] = {
                "local_path": local_path,
                "source_id": "anthropic-skills",
                "source_path": f"skills/{name}",
                "kind": "skill",
                "mapping": "canonical-list",
            }

    for override in mappings.get("overrides", []):
        if override.get("sync") == "manual-review" or not override.get("source_path"):
            continue
        entry = dict(override)
        entry["mapping"] = "explicit"
        entries[entry["local_path"]] = entry

    previous_by_path = {
        item["local_path"]: item for item in previous.get("skills", [])
    }
    for path, entry in list(entries.items()):
        old = previous_by_path.get(path, {})
        merged = dict(old)
        merged.update(entry)
        entries[path] = merged

    return [entries[path] for path in sorted(entries)]


def determine_state(entry: dict, local_sha: str, upstream_sha: str | None) -> str:
    if upstream_sha is None:
        return "UPSTREAM_REMOVED"
    if local_sha == upstream_sha:
        return "EXACT"
    previous_local = entry.get("local_tree_sha")
    previous_upstream = entry.get("upstream_tree_sha")
    if previous_local and local_sha != previous_local:
        return "MODIFIED"
    if previous_upstream and upstream_sha != previous_upstream:
        return "UPDATE_AVAILABLE"
    return "DIFFERS_FROM_UPSTREAM"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    sources_registry = load_json(SOURCES_FILE)
    previous = load_json(SKILLS_FILE)
    mappings = load_json(MAPPINGS_FILE)
    entries = canonical_entries(mappings, previous)

    sources = {
        source["id"]: source
        for source in sources_registry["sources"]
        if source.get("type") == "upstream" and source.get("syncable", True)
    }
    needed = {entry["source_id"] for entry in entries}
    snapshots: dict[str, tuple[str, dict[str, str]]] = {}

    try:
        for source_id in sorted(needed):
            source = sources.get(source_id)
            if not source:
                raise RuntimeError(f"Unknown or non-syncable source_id: {source_id}")
            snapshots[source_id] = get_upstream_snapshot(source)
    except (urllib.error.URLError, urllib.error.HTTPError, KeyError, RuntimeError) as exc:
        print(f"Upstream snapshot failed: {exc}", file=sys.stderr)
        return 1

    counts: dict[str, int] = {}
    updated: list[dict] = []
    for original in entries:
        entry = dict(original)
        commit, trees = snapshots[entry["source_id"]]
        try:
            local_sha = local_tree_sha(entry["local_path"])
        except subprocess.CalledProcessError as exc:
            print(f"Local tree lookup failed for {entry['local_path']}: {exc}", file=sys.stderr)
            return 1
        upstream_sha = trees.get(entry["source_path"])
        state = determine_state(entry, local_sha, upstream_sha)
        entry["checked_upstream_commit"] = commit
        entry["local_tree_sha"] = local_sha
        entry["upstream_tree_sha"] = upstream_sha
        entry["state"] = state
        updated.append(entry)
        counts[state] = counts.get(state, 0) + 1
        print(
            f"{state:<24} {entry['local_path']:<50} "
            f"local={local_sha[:12]} upstream={(upstream_sha or '-')[:12]}"
        )

    print("\nSummary:")
    for state in sorted(counts):
        print(f"  {state:<24} {counts[state]}")

    if args.write:
        output = {
            "schema_version": 2,
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "coverage": {
                "process": "canonical-mapped",
                "wordpress": "canonical-mapped",
                "marketing": "canonical-mapped",
                "design": "canonical-mapped",
                "security": "local",
                "qa": "local",
                "multiplayer": "legacy-derived-manual-review"
            },
            "skills": updated,
        }
        SKILLS_FILE.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
        print(f"\nUpdated {SKILLS_FILE.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
