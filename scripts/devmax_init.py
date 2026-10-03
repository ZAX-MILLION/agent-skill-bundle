#!/usr/bin/env python3
"""DEV MAX one-command project bootstrap for Google Antigravity.

Installs a small project-local core profile under .agents/skills while keeping
the complete agent-skill-bundle checkout outside the project for on-demand
retrieval. Existing project rules and unmarked skills are preserved by default.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any

REPO_URL = "https://github.com/ZAX-MILLION/agent-skill-bundle.git"
DEFAULT_REF = "main"
MANAGER = "devmax-project-bootstrap"
BEGIN = "<!-- DEVMAX:BEGIN -->"
END = "<!-- DEVMAX:END -->"


class BootstrapError(RuntimeError):
    pass


def run(cmd: list[str], *, cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if check and proc.returncode != 0:
        detail = (proc.stderr or proc.stdout).strip()
        raise BootstrapError(f"command failed: {' '.join(cmd)}\n{detail}")
    return proc


def find_project(explicit: str | None) -> Path:
    if explicit:
        project = Path(explicit).expanduser().resolve()
    else:
        probe = run(["git", "rev-parse", "--show-toplevel"], check=False)
        project = Path(probe.stdout.strip()).resolve() if probe.returncode == 0 and probe.stdout.strip() else Path.cwd().resolve()
    if not project.exists() or not project.is_dir():
        raise BootstrapError(f"project directory does not exist: {project}")
    return project


def default_checkout() -> Path:
    root = Path(os.environ.get("DEVMAX_HOME", str(Path.home() / ".devmax"))).expanduser()
    return root / "agent-skill-bundle"


def ensure_checkout(source_arg: str | None, no_update: bool, ref: str) -> Path:
    if source_arg:
        source = Path(source_arg).expanduser().resolve()
        if not (source / "profiles" / "devmax" / "profile.json").is_file():
            raise BootstrapError(f"not a DEV MAX bundle checkout: {source}")
        return source

    source = default_checkout()
    source.parent.mkdir(parents=True, exist_ok=True)

    if not source.exists():
        run(["git", "clone", "--depth", "1", "--branch", ref, REPO_URL, str(source)])
        return source

    if not (source / ".git").is_dir():
        raise BootstrapError(f"DEV MAX source path exists but is not a Git checkout: {source}")

    if no_update:
        return source

    dirty = run(["git", "-C", str(source), "status", "--porcelain"], check=False)
    if dirty.returncode != 0:
        raise BootstrapError(f"cannot inspect bundle checkout: {source}")

    if dirty.stdout.strip():
        print(f"NOTE: bundle checkout has local changes; using it without updating: {source}")
        return source

    pull = run(["git", "-C", str(source), "pull", "--ff-only", "origin", ref], check=False)
    if pull.returncode != 0:
        print("NOTE: bundle update was unavailable; using the existing reviewed checkout.")
    return source


def load_profile(source: Path) -> dict[str, Any]:
    path = source / "profiles" / "devmax" / "profile.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    skills = data.get("core_skills")
    if not isinstance(skills, list) or not skills:
        raise BootstrapError("DEV MAX profile has no core_skills")
    for entry in skills:
        if not isinstance(entry, dict) or not entry.get("name") or not entry.get("source"):
            raise BootstrapError("invalid core skill entry in DEV MAX profile")
    return data


def marker_path(destination: Path) -> Path:
    return destination / ".devmax-managed.json"


def is_managed(destination: Path, source_key: str) -> bool:
    marker = marker_path(destination)
    if not marker.is_file() or marker.is_symlink():
        return False
    try:
        data = json.loads(marker.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return False
    return data.get("manager") == MANAGER and data.get("source") == source_key


def git_head(source: Path) -> str | None:
    proc = run(["git", "-C", str(source), "rev-parse", "HEAD"], check=False)
    return proc.stdout.strip() if proc.returncode == 0 and proc.stdout.strip() else None


def install_skill(source: Path, destination: Path, source_key: str, force: bool, head: str | None) -> None:
    origin = source / source_key
    if not (origin / "SKILL.md").is_file():
        raise BootstrapError(f"missing core skill source: {source_key}")

    if destination.exists():
        if destination.is_symlink():
            raise BootstrapError(f"refusing to replace symlink skill: {destination}")
        if not is_managed(destination, source_key) and not force:
            raise BootstrapError(
                f"refusing to replace existing unmarked skill: {destination}\n"
                "Review it first, then rerun with --force only if replacement is intended."
            )
        if destination.is_dir():
            shutil.rmtree(destination)
        else:
            destination.unlink()

    shutil.copytree(origin, destination, symlinks=False)
    marker_path(destination).write_text(
        json.dumps(
            {"manager": MANAGER, "source": source_key, "bundle_commit": head},
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
    )


def managed_rules(source: Path, profile: dict[str, Any]) -> str:
    relative = profile.get("rules_template")
    if not isinstance(relative, str) or not relative:
        raise BootstrapError("DEV MAX profile rules_template is missing")
    body = (source / relative).read_text(encoding="utf-8").strip()
    return f"{BEGIN}\n{body}\n{END}"


def update_agents(project: Path, block: str) -> None:
    path = project / "AGENTS.md"
    current = path.read_text(encoding="utf-8") if path.exists() else ""
    has_begin, has_end = BEGIN in current, END in current
    if has_begin != has_end:
        raise BootstrapError("AGENTS.md has an incomplete DEV MAX managed block; refusing to edit it")

    if has_begin:
        start = current.index(BEGIN)
        stop = current.index(END, start) + len(END)
        updated = current[:start].rstrip() + "\n\n" + block + current[stop:]
    else:
        updated = current.rstrip()
        if updated:
            updated += "\n\n"
        updated += block + "\n"

    path.write_text(updated.rstrip() + "\n", encoding="utf-8")


def write_manifest(project: Path, source: Path, profile: dict[str, Any], head: str | None) -> None:
    agents = project / ".agents"
    agents.mkdir(parents=True, exist_ok=True)
    payload = {
        "manager": MANAGER,
        "profile": profile.get("name", "DEV MAX"),
        "profile_version": profile.get("profile_version"),
        "host": profile.get("host", "Google Antigravity"),
        "vault_mode": profile.get("vault_mode", "on-demand"),
        "vault_path": str(source),
        "bundle_commit": head,
        "core_skills": [entry["name"] for entry in profile["core_skills"]],
        "specialist_search": f'python "{source / "scripts" / "skill_doctor.py"}" search "<keywords>"',
    }
    (agents / "devmax.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def remove_managed_block(path: Path) -> None:
    if not path.exists():
        return
    current = path.read_text(encoding="utf-8")
    has_begin, has_end = BEGIN in current, END in current
    if not has_begin and not has_end:
        return
    if has_begin != has_end:
        raise BootstrapError("AGENTS.md has an incomplete DEV MAX managed block; refusing to remove it")
    start = current.index(BEGIN)
    stop = current.index(END, start) + len(END)
    updated = (current[:start].rstrip() + "\n\n" + current[stop:].lstrip()).strip()
    if updated:
        path.write_text(updated + "\n", encoding="utf-8")
    else:
        path.unlink()


def remove_profile(project: Path, profile: dict[str, Any]) -> None:
    skills_root = project / ".agents" / "skills"
    removed = 0
    for entry in profile["core_skills"]:
        destination = skills_root / entry["name"]
        if destination.exists() and is_managed(destination, entry["source"]):
            shutil.rmtree(destination)
            removed += 1
    manifest = project / ".agents" / "devmax.json"
    if manifest.is_file():
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            data = {}
        if data.get("manager") == MANAGER:
            manifest.unlink()
    remove_managed_block(project / "AGENTS.md")
    print(f"DEV MAX profile removed: {removed} managed skills. Unmarked skills/project rules were preserved.")


def status(project: Path, profile: dict[str, Any]) -> int:
    skills_root = project / ".agents" / "skills"
    missing = []
    unmanaged = []
    for entry in profile["core_skills"]:
        destination = skills_root / entry["name"]
        if not (destination / "SKILL.md").is_file():
            missing.append(entry["name"])
        elif not is_managed(destination, entry["source"]):
            unmanaged.append(entry["name"])

    manifest_ok = (project / ".agents" / "devmax.json").is_file()
    agents_text = (project / "AGENTS.md").read_text(encoding="utf-8") if (project / "AGENTS.md").exists() else ""
    rules_ok = BEGIN in agents_text and END in agents_text

    print(f"Project: {project}")
    print(f"Core skills: {len(profile['core_skills']) - len(missing)}/{len(profile['core_skills'])}")
    print(f"Manifest: {'OK' if manifest_ok else 'MISSING'}")
    print(f"AGENTS rules: {'OK' if rules_ok else 'MISSING'}")
    if missing:
        print("Missing: " + ", ".join(missing))
    if unmanaged:
        print("Unmanaged/conflicting: " + ", ".join(unmanaged))
    return 0 if not missing and not unmanaged and manifest_ok and rules_ok else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Install the DEV MAX Antigravity profile into the current project.")
    parser.add_argument("--project", help="Project directory; defaults to Git root or current directory.")
    parser.add_argument("--source", help="Use an existing agent-skill-bundle checkout (mainly for development/tests).")
    parser.add_argument("--bundle-ref", default=os.environ.get("DEVMAX_BUNDLE_REF", DEFAULT_REF), help="Bundle Git ref to clone/update.")
    parser.add_argument("--no-update", action="store_true", help="Do not update an existing bundle checkout.")
    parser.add_argument("--force", action="store_true", help="Replace conflicting same-name unmarked core skills after review.")
    parser.add_argument("--status", action="store_true", help="Check the current project's DEV MAX profile.")
    parser.add_argument("--remove", action="store_true", help="Remove only DEV MAX-managed project files/skill copies.")
    args = parser.parse_args()

    project = find_project(args.project)
    source = ensure_checkout(args.source, args.no_update, args.bundle_ref)
    profile = load_profile(source)

    if args.status:
        return status(project, profile)
    if args.remove:
        remove_profile(project, profile)
        return 0

    skills_root = project / ".agents" / "skills"
    skills_root.mkdir(parents=True, exist_ok=True)
    head = git_head(source)

    for entry in profile["core_skills"]:
        install_skill(
            source,
            skills_root / entry["name"],
            entry["source"],
            args.force,
            head,
        )

    update_agents(project, managed_rules(source, profile))
    write_manifest(project, source, profile, head)

    print("DEV MAX project profile installed.")
    print(f"Project: {project}")
    print(f"Core skills: {len(profile['core_skills'])}")
    print(f"On-demand vault: {source}")
    print("Next: open this project in Antigravity and start working.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BootstrapError as exc:
        print(f"DEV MAX setup failed: {exc}", file=sys.stderr)
        raise SystemExit(2)
