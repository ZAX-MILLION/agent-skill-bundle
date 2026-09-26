#!/usr/bin/env bash
# Isolated installer regression: full install, strict bootstrap, safe migration.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf -- "$tmp"' EXIT

"$root/install.sh" "$tmp/full" --flat >/dev/null
full="$(find "$tmp/full" -mindepth 2 -maxdepth 2 -name SKILL.md | wc -l)"
[ "$full" -eq 143 ] || { echo "FAIL: expected 143 full skills, got $full" >&2; exit 1; }
for skill in graphify graft awesome-design design-taste-frontend image-to-code web-design-guidelines agent-skills; do
  [ -f "$tmp/full/$skill/SKILL.md" ] || { echo "FAIL: missing $skill" >&2; exit 1; }
done
[ -f "$tmp/full/web-design-guidelines/references/pinned-command.md" ]
[ -f "$tmp/full/awesome-design/references/catalog.md" ]
[ -f "$tmp/full/image-to-code/LICENSE.txt" ]

"$root/install.sh" "$tmp/minimal" --flat --on-demand >/dev/null
minimal="$(find "$tmp/minimal" -mindepth 2 -maxdepth 2 -name SKILL.md | wc -l)"
[ "$minimal" -eq 2 ] || { echo "FAIL: expected 2 bootstrap skills, got $minimal" >&2; exit 1; }
[ -f "$tmp/minimal/i-have-adhd/SKILL.md" ]
[ -f "$tmp/minimal/skill-retrieval-routing/SKILL.md" ]
[ ! -e "$tmp/minimal/ponytail" ]

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
echo "PASS: 143 full packages (seven new), two-skill bootstrap, deliberate migration, unmarked user skill preserved."
