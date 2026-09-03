#!/usr/bin/env python3
"""Review-first whole-directory upstream skill synchronization.

Default mode is dry-run. Applying a sync requires both --apply and --reviewed.
The tool creates a local review branch, replaces each selected skill directory
with an exact copy from its registered upstream source, audits provenance, and
runs git diff --check. It never pushes or merges.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry"
SOURCES_FILE = REGISTRY / "sources.json"
SKILLS_FILE = REGISTRY / "skills.json"
MAPPINGS_FILE = REGISTRY / "category-mappings.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run(*args: str, cwd: Path = ROOT, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        cwd=cwd,
        check=True,
        text=True,
        capture_output=capture,
    )


def ensure_clean_tree() -> None:
    status = run("git", "status", "--porcelain", capture=True).stdout.strip()
    if status:
        raise RuntimeError("Working tree is not clean; commit or stash changes before applying sync.")


def source_lookup() -> dict[str, dict]:
    return {
        item["id"]: item
        for item in load_json(SOURCES_FILE)["sources"]
        if item.get("type") == "upstream"
    }


def explicit_lookup() -> dict[str, dict]:
    return {
        item["local_path"]: item
        for item in load_json(SKILLS_FILE).get("skills", [])
    }


def convention_lookup() -> dict[str, dict]:
    result = {}
    for item in load_json(MAPPINGS_FILE).get("mappings", []):
        if item.get("enabled", True):
            result[item["local_category"]] = item
    return result


def resolve(local_path: str, explicit: dict[str, dict], conventions: dict[str, dict]) -> tuple[str, str]:
    if local_path in explicit:
        entry = explicit[local_path]
        return entry["source_id"], entry["source_path"]

    parts = Path(local_path).parts
    if len(parts) != 2:
        raise RuntimeError(f"Unsupported local skill path: {local_path}")
    category, name = parts
    mapping = conventions.get(category)
    if not mapping:
        raise RuntimeError(
            f"No reviewed provenance mapping for {local_path}. Run scripts/discover_provenance.py first."
        )
    source_path = "/".join(
        part for part in (mapping.get("source_prefix", ""), name) if part
    )
    return mapping["source_id"], source_path


def clone_source(source: dict, destination: Path) -> None:
    run(
        "git",
        "clone",
        "--depth",
        "1",
        "--single-branch",
        "--branch",
        source["default_branch"],
        source["url"],
        str(destination),
        cwd=destination.parent,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Safely mirror selected skills from reviewed upstream sources."
    )
    parser.add_argument("skills", nargs="+", help="Local paths, e.g. process/writing-skills")
    parser.add_argument("--apply", action="store_true", help="Apply exact upstream copies locally.")
    parser.add_argument(
        "--reviewed",
        action="store_true",
        help="Confirm provenance/source selection has been reviewed.",
    )
    parser.add_argument("--commit", action="store_true", help="Commit the reviewed sync locally.")
    parser.add_argument("--branch", help="Review branch name. Defaults to upstream-sync/<timestamp>.")
    args = parser.parse_args()

    if args.apply and not args.reviewed:
        parser.error("--apply requires --reviewed")
    if args.commit and not args.apply:
        parser.error("--commit requires --apply")

    sources = source_lookup()
    explicit = explicit_lookup()
    conventions = convention_lookup()
    planned = []

    for local_path in args.skills:
        destination = ROOT / local_path
        if not destination.is_dir() or not (destination / "SKILL.md").is_file():
            raise RuntimeError(f"Not a bundled skill directory: {local_path}")
        source_id, source_path = resolve(local_path, explicit, conventions)
        source = sources.get(source_id)
        if not source:
            raise RuntimeError(f"Unknown or non-upstream source: {source_id}")
        planned.append((local_path, source_id, source_path, source))
        print(f"PLAN  {local_path} <- {source['repository']}:{source_path}@{source['default_branch']}")

    if not args.apply:
        print("\nDry run only. Re-run with --apply --reviewed after reviewing the provenance above.")
        return 0

    ensure_clean_tree()
    branch = args.branch or f"upstream-sync/{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
    run("git", "switch", "-c", branch)

    clones: dict[str, Path] = {}
    try:
        with tempfile.TemporaryDirectory(prefix="agent-skill-bundle-sync-") as tmp:
            tmpdir = Path(tmp)
            for local_path, source_id, source_path, source in planned:
                if source_id not in clones:
                    clone_dir = tmpdir / source_id
                    clone_source(source, clone_dir)
                    clones[source_id] = clone_dir

                upstream_dir = clones[source_id] / source_path
                if not upstream_dir.is_dir() or not (upstream_dir / "SKILL.md").is_file():
                    raise RuntimeError(
                        f"Registered upstream path is not a skill directory: {source['repository']}:{source_path}"
                    )

                destination = ROOT / local_path
                shutil.rmtree(destination)
                shutil.copytree(upstream_dir, destination, symlinks=True)
                print(f"SYNC  {local_path}")

        run(sys.executable, "scripts/audit_skills.py", "--write")
        run("git", "diff", "--check")

        if args.commit:
            for local_path, *_ in planned:
                run("git", "add", "--", local_path)
            run("git", "add", "--", "registry/skills.json")
            names = ", ".join(path for path, *_ in planned)
            run("git", "commit", "-m", f"sync: refresh reviewed upstream skills ({names})")
            print("Committed locally on review branch.")

        print(f"\nReview branch ready: {branch}")
        print("Nothing was pushed or merged. Review the diff before integrating it.")
        return 0
    except Exception:
        print(
            f"\nSync stopped on review branch {branch}. Nothing was pushed or merged.",
            file=sys.stderr,
        )
        raise


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"Sync failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
