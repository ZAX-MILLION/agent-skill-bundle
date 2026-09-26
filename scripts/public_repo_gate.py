#!/usr/bin/env python3
"""Fail closed on common secret material in the current public repository snapshot.

Never print matched secret values. This check does not erase Git history or
replace manual source review and credential rotation.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys

FILE_RISK = re.compile(r"(^|/)(?:\.env(?:\..+)?|id_(?:rsa|ed25519)|credentials\.(?:json|ya?ml)|secrets?\.(?:json|ya?ml)|[^/]+\.(?:pem|p12|pfx|key))$", re.I)
PRIVATE_KEY = re.compile(rb"-----BEGIN (?:RSA |OPENSSH |EC |DSA |PGP )?PRIVATE KEY-----")
TOKEN = re.compile(rb"(?<![A-Za-z0-9_-])(?:github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9]{30,}|glpat-[A-Za-z0-9_-]{15,}|xox[baprs]-[A-Za-z0-9-]{15,}|sk-(?:proj-)?[A-Za-z0-9_-]{25,}|AKIA[0-9A-Z]{16})")
CRED_URL = re.compile(rb"(?:https?|postgres(?:ql)?|mysql|redis)://[^\s\x00/@]+:[^\s\x00/@]{5,}@", re.I)
PASSWORD_LINE = re.compile(rb"(?im)^\s*[-*]\s+\*{0,2}\s*(?:password|passphrase|api[_ -]?key|access[_ -]?token|auth[_ -]?token|session[_ -]?cookie)\s*:\s*\*{0,2}\s*(\S[^\r\n]*)")
ASSIGNMENT = re.compile(rb"(?im)^\s*(?:export\s+)?(?:\w*(?:API_KEY|SECRET_KEY|ACCESS_TOKEN|AUTH_TOKEN|PASSWORD|PASSWD|PRIVATE_KEY)\w*)\s*=\s*(\S[^\r\n]*)")
SAFE = re.compile(rb"(?i)^(?:['\"\` ]*)(?:YOUR[_ -]|REPLACE|CHANGEME|CHANGE_ME|EXAMPLE|PLACEHOLDER|DUMMY|FAKE|REDACTED|xxx|<|\$|os\.environ|process\.env|undefined|null|none|\\{\\{|\\.{3}|[*]{4,})")
MAX_BYTES = 5_000_000

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--private-denylist", help="Locally stored one literal marker per line; never commit this file.")
    args = ap.parse_args()
    root = pathlib.Path(args.root).resolve()
    try:
        paths = [x.decode("utf-8", "surrogateescape") for x in subprocess.run(
            ["git", "ls-files", "-z"], cwd=root, capture_output=True, check=True
        ).stdout.split(b"\0") if x]
    except subprocess.CalledProcessError:
        print("FAIL: cannot enumerate tracked files", file=sys.stderr)
        return 2
    markers = []
    if args.private_denylist:
        loc = pathlib.Path(args.private_denylist).resolve()
        if root == loc or root in loc.parents:
            print("FAIL: private denylist must be outside repository", file=sys.stderr)
            return 2
        markers = [x.strip().encode() for x in loc.read_text().splitlines() if len(x.strip()) >= 5 and not x.lstrip().startswith("#")]
    approval_path = root / "registry" / "approved-public-examples.json"
    approvals = json.loads(approval_path.read_text())["approved_blobs"] if approval_path.is_file() else {}
    results = []
    approved_count = 0
    for rel in paths:
        p = root / rel
        if FILE_RISK.search(rel) and not re.search(r"\.env\.(?:example|sample|template)$", rel, re.I):
            results.append((rel,"sensitive filename"))
        if p.is_symlink():
            results.append((rel,"symlink requires review"))
            continue
        if not p.is_file():
            continue
        if p.stat().st_size > MAX_BYTES:
            continue
        data = p.read_bytes()
        if b"\0" in data[:4096]:
            continue
        for private_marker in markers:
            if private_marker.lower() in data.lower():
                results.append((rel, "private marker"))
                break
        blob_sha = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        if approvals.get(rel, {}).get("sha") == blob_sha:
            approved_count += 1
            continue
        for label, pattern in (("private key",PRIVATE_KEY),("service token",TOKEN),("credential URL",CRED_URL)):
            for m in pattern.finditer(data):
                if label == "credential URL" and re.search(rb"(?i)(?:<|>|\b(?:user|username|password|pass|token|example|sample)\b|\$\{)", m.group(0)):
                    continue
                results.append((rel,label)); break
        for label, pattern in (("password field",PASSWORD_LINE),("credential assignment",ASSIGNMENT)):
            for found in pattern.finditer(data):
                if not SAFE.search(found.group(1).strip()) and not re.match(rb"(?i)^re\\.compile\\(", found.group(1).strip()):
                    results.append((rel,label))
                    break
    if results:
        print(f"FAIL: {len(results)} public-content findings across {len(set(p for p,_ in results))} paths; values withheld.")
        for rel,label in sorted(set(results)):
            print(f"  file-id={hashlib.sha256(rel.encode()).hexdigest()[:12]}: {label}")
        return 1
    print(f"PASS: {len(paths)} tracked paths; {approved_count} unchanged reviewed examples; no matching secret patterns.")
    print("Limitation: heuristics and HEAD only. Review historical commits, forks/caches, metadata and all third-party code separately.")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
