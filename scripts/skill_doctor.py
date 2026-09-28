#!/usr/bin/env python3
"""Read-only discovery/diagnostics and explicit, pinned external-package staging.

No network, package installation, host configuration, MCP registration, provider
access, or execution of third-party skill scripts. Python standard library only.
"""
import argparse
import hashlib
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CATEGORIES = (
    "design", "security", "process", "multiplayer", "wordpress",
    "marketing", "qa", "operations", "coding", "research",
    "productivity", "automation", "creative",
)
BOOTSTRAPS = {
    "i-have-adhd": "productivity/i-have-adhd",
    "skill-retrieval-routing": "research/skill-retrieval-routing",
}
MARKER = ".agent-skill-bundle-external.json"


class ValidationError(Exception):
    pass


def manifest():
    return json.loads((ROOT / "registry/shuohao-packages.json").read_text(encoding="utf-8"))


def git_blob(path):
    h = hashlib.sha1()
    size = path.stat().st_size
    h.update(f"blob {size}\0".encode("ascii"))
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def check_file(path, record):
    if path.is_symlink() or not path.is_file():
        raise ValidationError(f"missing or unsafe file: {path}")
    if path.stat().st_size != record["size"] or git_blob(path) != record["sha"]:
        raise ValidationError(f"file hash/size differs from reviewed source: {path}")


def check_package(directory, package, require_marker=False):
    """Reject missing, modified, unexpected and symlinked contents."""
    if directory.is_symlink() or not directory.is_dir():
        raise ValidationError(f"missing or unsafe package directory: {directory}")
    expected = {f["path"] for f in package["files"]}
    expected.add(MARKER) if require_marker else None
    seen = set()
    for path in directory.rglob("*"):
        relative = path.relative_to(directory).as_posix()
        if path.is_symlink():
            raise ValidationError(f"symlink not allowed in reviewed package: {relative}")
        if path.is_file():
            seen.add(relative)
        elif not path.is_dir():
            raise ValidationError(f"unsupported filesystem entry: {relative}")
    if expected != seen:
        raise ValidationError(f"incomplete/unreviewed package {package['name']}; missing={sorted(expected-seen)}, unexpected={sorted(seen-expected)}")
    for item in package["files"]:
        check_file(directory / item["path"], item)
    if require_marker:
        metadata = json.loads((directory / MARKER).read_text(encoding="utf-8"))
        if metadata != {"repository": manifest()["source_repository"], "revision": manifest()["source_revision"], "skill": package["name"]}:
            raise ValidationError(f"unrecognized managed package marker: {directory}")
    return len(package["files"])


def packages():
    return {x["name"]: x for x in manifest()["packages"]}


def skill_catalog(vault):
    result = []
    for cat in CATEGORIES:
        category = vault / cat
        for path in sorted(category.glob("*/SKILL.md")):
            if not path.is_file() or path.is_symlink() or path.parent.is_symlink():
                continue
            body = path.read_text(encoding="utf-8")
            prefix = body[: min(3500, len(body))]
            match = re.search(r"^description:\s*(.+)$", prefix, re.MULTILINE)
            desc = match.group(1).strip().strip("'\"") if match else ""
            result.append({"name": path.parent.name, "source": f"{cat}/{path.parent.name}",
                           "description": desc, "path": str(path.resolve())})
    return result


def search(args):
    rows = skill_catalog(args.vault.resolve())
    if args.command == "list":
        for entry in rows:
            print(f"{entry['source']}\t{entry['description'][:140]}")
        print(f"Total: {len(rows)}", file=sys.stderr)
        return
    words = re.findall(r"[a-z0-9][a-z0-9-]*", " ".join(args.query).lower())
    if not words:
        raise ValidationError("provide a non-empty search query")
    ranked = []
    for row in rows:
        name = row["name"].lower()
        desc = row["description"].lower()
        score = sum(5 * (w in name) + 2 * (w in desc) for w in words)
        if score:
            ranked.append((score, row["source"], row))
    for _, _, item in sorted(ranked, key=lambda v: (-v[0], v[1]))[:args.limit]:
        print(f"{item['source']}\t{item['description'][:180]}\n  {item['path']}")
    if not ranked:
        print("No matching local skill description; no external search was performed.")


def run_git_head(source):
    if source.is_symlink() or not source.is_dir():
        raise ValidationError("upstream source must be an existing real directory")
    proc = subprocess.run(["git", "-C", str(source), "rev-parse", "HEAD"],
                          capture_output=True, text=True, check=False)
    if proc.returncode:
        raise ValidationError("upstream source must be a Git checkout at the reviewed commit")
    return proc.stdout.strip()


def verify_checkout(source, package):
    m = manifest()
    head = run_git_head(source)
    if head != m["source_revision"]:
        raise ValidationError(f"unreviewed checkout revision {head}; expected {m['source_revision']}")
    src = source / package["source_path"]
    count = check_package(src, package)
    for file in m["root_notice_files"]:
        check_file(source / file["path"], file)
    return src, count


def stage(args):
    selected = packages().get(args.skill)
    if not selected:
        raise ValidationError(f"unknown external skill: {args.skill}")
    source = args.source.resolve()
    src, count = verify_checkout(source, selected)
    target = args.target.resolve()
    if target == source or source in target.parents or target == ROOT or ROOT in target.parents:
        raise ValidationError("target must not be within the upstream checkout or this public repository")
    destination = target / selected["name"]
    if destination.is_symlink() or target.is_symlink():
        raise ValidationError("symlink target not allowed")
    if destination.exists():
        if not args.replace_managed:
            raise ValidationError("target exists; review it and explicitly pass --replace-managed")
        verify_staged(destination, selected)
    if args.dry_run:
        print(f"DRY RUN: reviewed {count} files for {args.skill}; would stage at {destination}")
        return
    target.mkdir(parents=True, exist_ok=True)
    temporary = pathlib.Path(tempfile.mkdtemp(prefix=".skill-stage-", dir=target))
    try:
        shutil.copytree(src, temporary / selected["name"], symlinks=True)
        out = temporary / selected["name"]
        check_package(out, selected)
        for file in manifest()["root_notice_files"]:
            shutil.copy2(source / file["path"], temporary / file["path"])
            check_file(temporary / file["path"], file)
        (out / "LICENSE.txt").write_bytes((temporary / "LICENSE").read_bytes())
        (out / "NOTICE.txt").write_bytes((temporary / "NOTICE").read_bytes())
        # In-package license and notice are tracked as additional, required files.
        (out / MARKER).write_text(json.dumps({
            "repository": manifest()["source_repository"],
            "revision": manifest()["source_revision"],
            "skill": selected["name"],
        }, sort_keys=True) + "\n", encoding="utf-8")
        final = target / selected["name"]
        backup = temporary / "previous-managed"
        if final.exists():
            # Replacement is opt-in and only after verifying the existing marker,
            # complete file hashes and license/notice. Roll back on rename failure.
            final.rename(backup)
        try:
            out.rename(final)
        except OSError:
            if backup.exists():
                backup.rename(final)
            raise
        if backup.exists():
            shutil.rmtree(backup)
        print(f"STAGED: {selected['name']} ({count} reviewed source files + license/notice) at {final}")
        print("Execution unverified. No host/MCP configuration or external script was run.")
    finally:
        shutil.rmtree(temporary, ignore_errors=True)


def node_prerequisite(check_version=False):
    executable = shutil.which("node")
    if not executable:
        return "Missing Dependencies", "Node 18+ not found in PATH"
    if not check_version:
        return "Unverified", "complete package found; Node version and execution have not been checked"
    proc = subprocess.run([executable, "--version"], capture_output=True,
                          text=True, timeout=5, check=False)
    match = re.match(r"^v?(\d+)\.", proc.stdout.strip()) if proc.returncode == 0 else None
    if not match or int(match.group(1)) < 18:
        return "Missing Dependencies", "Node 18+ required; current version was not compatible or could not be read"
    return "Unverified", f"Node {proc.stdout.strip()} present; host/provider and full execution still unverified"


def doctor(args):
    vault = args.vault.resolve()
    entries = skill_catalog(vault)
    names = [x["name"] for x in entries]
    issues = []
    if len(entries) != 188:
        issues.append(f"source vault has {len(entries)} skill directories, expected 188")
    if len(names) != len(set(names)):
        issues.append("duplicate local native skill names")
    host = None
    if args.host_root:
        host = {}
        for name, expected_source in BOOTSTRAPS.items():
            target = args.host_root / name
            marker = target / ".agent-skill-bundle-source"
            status = "Unverified"
            if not (target / "SKILL.md").is_file() or not marker.is_file():
                status = "Setup Required"
            elif marker.read_text(encoding="utf-8").strip() != expected_source:
                status = "Setup Required"
            host[name] = status
        other_managed = []
        if args.host_root.is_dir():
            for target in args.host_root.iterdir():
                if not target.is_dir() or target.is_symlink() or target.name in BOOTSTRAPS:
                    continue
                marker = target / ".agent-skill-bundle-source"
                if marker.is_file() and not marker.is_symlink():
                    other_managed.append(target.name)
        if other_managed:
            issues.append("additional bundle-managed native skill copies: " + ", ".join(sorted(other_managed)))
    external = {}
    for name, package in packages().items():
        if not args.external_root:
            external[name] = {"status": "Setup Required", "reason": "router only; external source not supplied"}
            continue
        target = args.external_root / name
        if not target.exists():
            external[name] = {"status": "Setup Required", "reason": "full external package not staged"}
            continue
        try:
            # Installed license/notice are copied in addition to original source manifest.
            verify_staged(target, package)
            status, reason = node_prerequisite(getattr(args, "check_runtime", False))
            external[name] = {"status": status, "reason": reason}
        except (ValidationError, OSError, ValueError) as exc:
            external[name] = {"status": "Missing Dependencies", "reason": str(exc)}
    # Source integrity/discovery is distinct from runtime use. A fully present
    # SKILL.md is not automatically 'Ready' in every host. Routers are marked
    # Setup Required because their separate product/runtime is not in the vault.
    runtime_guides = {
        "creative/shuohao-skills", "creative/openmontage",
        "process/paul", "automation/n8n-instance",
        "productivity/claude-mem", "research/skill-retrieval-routing",
    }
    per_skill = {
        item["source"]: {
            "status": "Setup Required" if item["source"] in runtime_guides else "Unverified",
            "reason": ("external source/runtime or MCP setup must be checked separately"
                       if item["source"] in runtime_guides else
                       "source SKILL.md present; actual host use not tested"),
        }
        for item in entries
    }
    status_counts = {
        status: sum(1 for item in per_skill.values() if item["status"] == status)
        for status in ("Ready", "Setup Required", "Missing Dependencies", "Unverified")
    }
    output = {
        "source_vault_count": len(entries),
        "status_counts": status_counts,
        "per_skill": per_skill,
        "native_mode": "two-bootstrap only; runtime host discovery not verified",
        "native_bootstraps": host if host is not None else "Unverified (provide --host-root)",
        "retrieval_mcp": "Unverified; test the live MCP in each host with list_categories/keyword_search/search_skills/get_skill",
        "external": external,
        "issues": issues,
        "execution": "Unverified; this offline doctor never executes third-party skill code",
    }
    print(json.dumps(output, indent=2, ensure_ascii=False) if args.json else pretty_doctor(output))


def verify_staged(directory, package):
    if directory.is_symlink() or not directory.is_dir():
        raise ValidationError("not a complete external skill directory")
    expected = {x["path"] for x in package["files"]} | {"LICENSE.txt", "NOTICE.txt", MARKER}
    actual = set()
    for item in directory.rglob("*"):
        if item.is_symlink():
            raise ValidationError("symlink in staged package")
        if item.is_file():
            actual.add(item.relative_to(directory).as_posix())
    if expected != actual:
        raise ValidationError(f"staged files differ: missing={sorted(expected-actual)}, extra={sorted(actual-expected)}")
    for item in package["files"]:
        check_file(directory / item["path"], item)
    data = json.loads((directory / MARKER).read_text(encoding="utf-8"))
    m = manifest()
    if data != {"repository": m["source_repository"], "revision": m["source_revision"], "skill": package["name"]}:
        raise ValidationError("invalid managed marker")
    for filename in m["root_notice_files"]:
        dest = "LICENSE.txt" if filename["path"] == "LICENSE" else "NOTICE.txt"
        check_file(directory / dest, filename)


def pretty_doctor(data):
    counts = data["status_counts"]
    lines = [f"Vault: {data['source_vault_count']} local skill directories",
             f"Source status: {counts['Unverified']} unverified, {counts['Setup Required']} setup required; none marked execution-ready",
             "Retrieval MCP: Unverified (test the actual host connection)"]
    native = data["native_bootstraps"]
    if isinstance(native, dict):
        lines.extend(f"Bootstrap {name}: {status}" for name, status in native.items())
    else:
        lines.append(f"Native bootstraps: {native}")
    lines.extend(f"External {name}: {item['status']} — {item['reason']}" for name, item in data["external"].items())
    lines.extend(f"ISSUE: {issue}" for issue in data["issues"])
    lines.append("Third-party script execution: Unverified (never run by doctor)")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    s = commands.add_parser("search", help="offline on-demand source-vault lookup")
    s.add_argument("query", nargs="+")
    s.add_argument("--vault", type=pathlib.Path, default=ROOT)
    s.add_argument("--limit", type=int, default=5)
    l = commands.add_parser("list", help="list local skill names/descriptions")
    l.add_argument("--vault", type=pathlib.Path, default=ROOT)
    d = commands.add_parser("doctor", help="read-only status; no claim of live execution")
    d.add_argument("--vault", type=pathlib.Path, default=ROOT)
    d.add_argument("--host-root", type=pathlib.Path, help="optional host native skills directory")
    d.add_argument("--external-root", type=pathlib.Path, help="optional separate external staged skill vault")
    d.add_argument("--check-runtime", action="store_true", help="optionally run only node --version; no skill code")
    d.add_argument("--json", action="store_true")
    st = commands.add_parser("stage", help="opt-in complete pinned external skill copy; NO download, install or execution")
    st.add_argument("skill", choices=sorted(packages()))
    st.add_argument("--source", type=pathlib.Path, required=True, help="pre-existing reviewed upstream Git checkout")
    st.add_argument("--target", type=pathlib.Path, required=True, help="separate, non-public external skill cache")
    st.add_argument("--dry-run", action="store_true")
    st.add_argument("--replace-managed", action="store_true")
    args = parser.parse_args()
    try:
        if args.command in ("search", "list"):
            search(args)
        elif args.command == "doctor":
            doctor(args)
        else:
            stage(args)
    except (ValidationError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
