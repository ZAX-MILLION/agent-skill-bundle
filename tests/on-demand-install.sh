#!/usr/bin/env bash
# Isolated installer regression: full install, strict bootstrap, safe migration.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf -- "$tmp"' EXIT

"$root/install.sh" "$tmp/full" --flat >/dev/null
full="$(find "$tmp/full" -mindepth 2 -maxdepth 2 -name SKILL.md | wc -l)"
[ "$full" -eq 187 ] || { echo "FAIL: expected 187 full skills, got $full" >&2; exit 1; }
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
for skill in paul diagnosing-superpowers openmontage shuohao-skills n8n-instance; do
  [ -f "$tmp/full/$skill/SKILL.md" ] || { echo "FAIL: missing $skill" >&2; exit 1; }
done
[ -f "$tmp/full/diagnosing-superpowers/references/redaction-policy.md" ]
[ -f "$tmp/full/n8n-agents-official/references/CHAT_AGENT_PATTERNS.md" ]
[ -f "$tmp/full/n8n-error-handling-official/references/examples/validation-subworkflow.ts" ]
[ -f "$tmp/full/using-n8n-skills-official/LICENSE.txt" ]
python3 "$root/tests/verify-third-wave.py" "$root" "$tmp/full"
python3 "$root/tests/verify-ecc.py" "$root" "$tmp/full"
python3 "$root/tests/verify-skillsmp-expansion.py" "$root" "$tmp/full"

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

# Exercise each supported host's *documented* strict-native target in isolation.
# These are temporary simulated roots, not the owner's actual PC configuration.
for host in antigravity codex claude-code; do
  "$root/install.sh" "$tmp/hosts/$host/skills" --flat --on-demand >/dev/null
  host_count="$(find "$tmp/hosts/$host/skills" -mindepth 2 -maxdepth 2 -name SKILL.md | wc -l)"
  [ "$host_count" -eq 2 ] || { echo "FAIL: $host exposes $host_count bundle skills" >&2; exit 1; }
  [ -f "$tmp/hosts/$host/skills/i-have-adhd/SKILL.md" ]
  [ -f "$tmp/hosts/$host/skills/skill-retrieval-routing/SKILL.md" ]
  [ ! -e "$tmp/hosts/$host/skills/paul" ]
  [ ! -e "$tmp/hosts/$host/skills/n8n-instance" ]
  [ ! -e "$tmp/hosts/$host/skills/context-budget" ]
done
[ ! -e "$tmp/minimal/ponytail" ]
[ ! -e "$tmp/minimal/caveman" ]
[ ! -e "$tmp/minimal/claude-mem" ]
[ ! -e "$tmp/minimal/humanizer" ]
[ ! -e "$tmp/minimal/events" ]
[ ! -e "$tmp/minimal/paul" ]
[ ! -e "$tmp/minimal/openmontage" ]
[ ! -e "$tmp/minimal/shuohao-skills" ]
[ ! -e "$tmp/minimal/n8n-instance" ]
[ ! -e "$tmp/minimal/n8n-agents-official" ]
[ ! -e "$tmp/minimal/diagnosing-superpowers" ]
[ ! -e "$tmp/minimal/context-budget" ]
[ ! -e "$tmp/minimal/ui-ux-pro-max" ]
[ ! -e "$tmp/minimal/godot-gdscript-patterns" ]
[ ! -e "$tmp/minimal/agent-introspection-debugging" ]
[ ! -e "$tmp/minimal/cross-agent-skill-verification" ]
[ ! -e "$tmp/minimal/agent-architecture-audit" ]
[ ! -e "$tmp/minimal/production-audit" ]


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
echo "PASS: 187 full packages (51 beyond original 136), two-skill bootstrap, deliberate migration, unmarked user skill preserved."
