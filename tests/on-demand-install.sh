#!/usr/bin/env bash
# Isolated installer regression: full install, strict bootstrap, safe migration.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf -- "$tmp"' EXIT

"$root/install.sh" "$tmp/full" --flat >/dev/null
full="$(find "$tmp/full" -mindepth 2 -maxdepth 2 -name SKILL.md | wc -l)"
[ "$full" -eq 147 ] || { echo "FAIL: expected 147 full skills, got $full" >&2; exit 1; }
for skill in graphify graft awesome-design design-taste-frontend image-to-code web-design-guidelines agent-skills; do
  [ -f "$tmp/full/$skill/SKILL.md" ] || { echo "FAIL: missing $skill" >&2; exit 1; }
done
for skill in caveman claude-mem humanizer events; do
  [ -f "$tmp/full/$skill/SKILL.md" ] || { echo "FAIL: missing $skill" >&2; exit 1; }
done
[ -f "$tmp/full/events/references/webinar-funnel.md" ]
[ -f "$tmp/full/events/evals/evals.json" ]
[ -f "$tmp/full/events/LICENSE.txt" ]
[ -f "$tmp/full/caveman/LICENSE.txt" ]
[ -f "$tmp/full/humanizer/LICENSE.txt" ]
# Integrity: complete copied upstream files must remain byte-identical to reviewed blobs.
python3 - "$root" "$tmp/full" <<'PY'
import json, pathlib, subprocess, sys
repo, target = map(pathlib.Path, sys.argv[1:])
pinned = json.loads((repo / "registry/vendor-second-wave.json").read_text())
checks = 0
for source in pinned["sources"]:
    for relative, expected in source.get("files", {}).items():
        local = repo / source["local_path"] / relative
        copied = target / pathlib.Path(source["local_path"]).name / relative
        for path in (local, copied):
            assert path.is_file(), f"missing file: {path}"
            actual = subprocess.check_output(["git", "hash-object", str(path)], text=True).strip()
            assert actual == expected, f"source pin mismatch: {path}"
            checks += 1
print(f"PASS: {checks} reviewed source and installed blob hashes")
PY
[ -f "$tmp/full/web-design-guidelines/references/pinned-command.md" ]
[ -f "$tmp/full/awesome-design/references/catalog.md" ]
[ -f "$tmp/full/image-to-code/LICENSE.txt" ]
[ -f "$tmp/full/agent-skills/references/voltagent-catalog.md" ]

"$root/install.sh" "$tmp/minimal" --flat --on-demand >/dev/null
minimal="$(find "$tmp/minimal" -mindepth 2 -maxdepth 2 -name SKILL.md | wc -l)"
[ "$minimal" -eq 2 ] || { echo "FAIL: expected 2 bootstrap skills, got $minimal" >&2; exit 1; }
[ -f "$tmp/minimal/i-have-adhd/SKILL.md" ]
[ -f "$tmp/minimal/skill-retrieval-routing/SKILL.md" ]
[ ! -e "$tmp/minimal/ponytail" ]
[ ! -e "$tmp/minimal/caveman" ]
[ ! -e "$tmp/minimal/claude-mem" ]
[ ! -e "$tmp/minimal/humanizer" ]
[ ! -e "$tmp/minimal/events" ]

# A previous full install must not silently masquerade as on-demand.
if "$root/install.sh" "$tmp/full" --flat --on-demand >"$tmp/warning.log" 2>&1; then
  echo "FAIL: on-demand accepted leftover full installation" >&2; exit 1
fi
[ -e "$tmp/full/ponytail" ]

# A user-authored, unmarked skill survives an explicitly approved migration.
mkdir -p "$tmp/full/personal-skill"
printf '%s\n' 'personal data' > "$tmp/full/personal-skill/SKILL.md"
"$root/install.sh" "$tmp/full" --flat --on-demand --prune-managed >/dev/null
[ -f "$tmp/full/personal-skill/SKILL.md" ]
[ ! -e "$tmp/full/ponytail" ]
[ -f "$tmp/full/i-have-adhd/SKILL.md" ]
[ -f "$tmp/full/skill-retrieval-routing/SKILL.md" ]
"$root/install.sh" "$tmp/full" --flat --on-demand >/dev/null

count="$(find "$tmp/full" -mindepth 2 -maxdepth 2 -name SKILL.md | wc -l)"
[ "$count" -eq 3 ] || { echo "FAIL: expected 2 bootstraps and personal skill, got $count" >&2; exit 1; }
echo "PASS: 147 full packages (eleven beyond original 136), two-skill bootstrap, deliberate migration, unmarked user skill preserved."
