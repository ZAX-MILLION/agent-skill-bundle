#!/usr/bin/env python3
"""Audit bundled skills against current upstream Git trees.

Uses explicit per-skill registry entries plus safe category conventions.
It never modifies skill directories. With --write it updates registry/skills.json
metadata only.
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
MAPPINGS_FILE = ROOT / "registry" / "category-mappings.json"
API = "https://api.github.com"


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def github_json(path: str) -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "agent-skill-bundle-skill-auditor",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(f"{API}{path}", headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def local_tree_sha(path: str) -> str:
    result = subprocess.run(
        ["git", "rev-parse", f"HEAD:{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def get_upstream_snapshot(source: dict) -> tuple[str, dict[str, str]]:
    repo = source["repository"]
    branch = source["default_branch"]
    commit = github_json(
        f"/repos/{repo}/commits/{urllib.parse.quote(branch, safe='')}"
    )["sha"]
    tree = github_json(f"/repos/{repo}/git/trees/{commit}?recursive=1")
    if tree.get("truncated"):
        raise RuntimeError(
            f"GitHub returned a truncated tree for {repo}; refusing incomplete audit."
        )
    trees = {
        item["path"]: item["sha"]
        for item in tree.get("tree", [])
        if item.get("type") == "tree"
    }
    return commit, trees


def discover_convention_entries(mappings: dict) -> list[dict]:
    entries: list[dict] = []
    for mapping in mappings.get("mappings", []):
        if not mapping.get("enabled", True):
            continue
        category = mapping["local_category"]
        category_dir = ROOT / category
        if not category_dir.is_dir():
            continue
        for skill_dir in sorted(category_dir.iterdir()):
            if not skill_dir.is_dir() or not (skill_dir / "SKILL.md").is_file():
                continue
            source_path = "/".join(
                part for part in [mapping.get("source_prefix", ""), skill_dir.name] if part
            )
            entries.append(
                {
                    "local_path": f"{category}/{skill_dir.name}",
                    "source_id": mapping["source_id"],
                    "source_path": source_path,
                    "mapping": "category-convention",
                }
            )
    return entries


def merged_entries(skills_registry: dict, mappings: dict) -> list[dict]:
    discovered = {entry["local_path"]: entry for entry in discover_convention_entries(mappings)}
    explicit = {entry["local_path"]: entry for entry in skills_registry.get("skills", [])}
    discovered.update(explicit)
    return [discovered[path] for path in sorted(discovered)]


def determine_state(entry: dict, current_local: str, current_upstream: str | None) -> str:
    if current_upstream is None:
        return "UPSTREAM_REMOVED"
    if current_local == current_upstream:
        return "EXACT"

    previous_local = entry.get("local_tree_sha")
    previous_upstream = entry.get("upstream_tree_sha")
    previous_state = entry.get("state")

    if previous_local and current_local != previous_local:
        return "MODIFIED"
    if previous_upstream and current_upstream != previous_upstream:
        return "UPDATE_AVAILABLE"
    if previous_state in {"UPDATE_AVAILABLE", "MODIFIED"}:
        return previous_state
    return "DIFFERS_FROM_UPSTREAM"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit mapped skill directories against current upstream Git trees."
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Update registry/skills.json metadata after a successful audit.",
    )
    args = parser.parse_args()

    sources_registry = load_json(SOURCES_FILE)
    skills_registry = load_json(SKILLS_FILE)
    mappings = load_json(MAPPINGS_FILE)
    entries = merged_entries(skills_registry, mappings)

    sources = {
        source["id"]: source
        for source in sources_registry["sources"]
        if source.get("type") == "upstream"
    }
    needed_source_ids = {entry["source_id"] for entry in entries}
    snapshots: dict[str, tuple[str, dict[str, str]]] = {}

    try:
        for source_id in sorted(needed_source_ids):
            source = sources.get(source_id)
            if source is None:
                raise RuntimeError(f"Unknown upstream source_id: {source_id}")
            snapshots[source_id] = get_upstream_snapshot(source)
    except (urllib.error.URLError, urllib.error.HTTPError, KeyError, RuntimeError) as exc:
        print(f"Upstream snapshot failed: {exc}", file=sys.stderr)
        return 1

    counts: dict[str, int] = {}
    updated_entries = []

    for original in entries:
        entry = dict(original)
        source_id = entry["source_id"]
        commit, upstream_trees = snapshots[source_id]
        try:
            current_local = local_tree_sha(entry["local_path"])
        except subprocess.CalledProcessError as exc:
            print(f"Local Git tree lookup failed for {entry['local_path']}: {exc}", file=sys.stderr)
            return 1

        current_upstream = upstream_trees.get(entry["source_path"])
        state = determine_state(entry, current_local, current_upstream)
        entry["checked_upstream_commit"] = commit
        entry["local_tree_sha"] = current_local
        entry["upstream_tree_sha"] = current_upstream
        entry["state"] = state
        updated_entries.append(entry)
        counts[state] = counts.get(state, 0) + 1
        upstream_short = current_upstream[:12] if current_upstream else "-"
        print(
            f"{state:<24} {entry['local_path']:<48} "
            f"local={current_local[:12]} upstream={upstream_short}"
        )

    print("\nSummary:")
    for state in sorted(counts):
        print(f"  {state:<24} {counts[state]}")

    if args.write:
        output = dict(skills_registry)
        output["checked_at"] = datetime.now(timezone.utc).isoformat()
        coverage = dict(output.get("coverage", {}))
        for mapping in mappings.get("mappings", []):
            if mapping.get("enabled", True):
                coverage[mapping["local_category"]] = "complete-by-convention"
        output["coverage"] = coverage
        output["skills"] = updated_entries
        SKILLS_FILE.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
        print(f"\nUpdated {SKILLS_FILE.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
