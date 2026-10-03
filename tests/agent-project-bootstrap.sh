#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf -- "$tmp"' EXIT

project="$tmp/project"
mkdir -p "$project/.agents/skills/personal"
printf '%s\n' '# Existing Project Rule' > "$project/AGENTS.md"
printf '%s\n' '---' 'name: personal' 'description: personal' '---' > "$project/.agents/skills/personal/SKILL.md"

python3 "$root/scripts/agent_init.py" --source "$root" --project "$project" --no-update >/dev/null

managed="$(find "$project/.agents/skills" -mindepth 2 -maxdepth 2 -name .agent-init-managed.json | wc -l | tr -d ' ')"
[ "$managed" -eq 10 ] || { echo "FAIL: expected 10 managed core skills, got $managed" >&2; exit 1; }
[ -f "$project/.agents/agent-init.json" ]
[ -f "$project/.agents/skills/personal/SKILL.md" ]
grep -q '# Existing Project Rule' "$project/AGENTS.md"
[ "$(grep -c '<!-- AGENT_INIT:BEGIN -->' "$project/AGENTS.md")" -eq 1 ]
[ "$(grep -c '<!-- AGENT_INIT:END -->' "$project/AGENTS.md")" -eq 1 ]

for skill in i-have-adhd skill-retrieval-routing credit-usage-helper ponytail graft graphify secure-by-default-development verification-before-completion task-to-pr test; do
  [ -f "$project/.agents/skills/$skill/SKILL.md" ] || { echo "FAIL: missing $skill" >&2; exit 1; }
done

# Re-running is idempotent for Project Core-owned files.
python3 "$root/scripts/agent_init.py" --source "$root" --project "$project" --no-update >/dev/null
[ "$(grep -c '<!-- AGENT_INIT:BEGIN -->' "$project/AGENTS.md")" -eq 1 ]
[ -f "$project/.agents/skills/personal/SKILL.md" ]

# Refuse to overwrite an unmarked same-name project skill.
conflict="$tmp/conflict"
mkdir -p "$conflict/.agents/skills/test"
printf '%s\n' 'personal test skill' > "$conflict/.agents/skills/test/SKILL.md"
if python3 "$root/scripts/agent_init.py" --source "$root" --project "$conflict" --no-update >/dev/null 2>"$tmp/conflict.err"; then
  echo "FAIL: bootstrap replaced an unmarked same-name skill" >&2
  exit 1
fi
grep -q 'refusing to replace existing unmarked skill' "$tmp/conflict.err"
grep -q 'personal test skill' "$conflict/.agents/skills/test/SKILL.md"

# Removal only removes managed content.
python3 "$root/scripts/agent_init.py" --source "$root" --project "$project" --no-update --remove >/dev/null
[ -f "$project/.agents/skills/personal/SKILL.md" ]
[ ! -e "$project/.agents/agent-init.json" ]
grep -q '# Existing Project Rule' "$project/AGENTS.md"
! grep -q '<!-- AGENT_INIT:BEGIN -->' "$project/AGENTS.md"
remaining_managed="$(find "$project/.agents/skills" -name .agent-init-managed.json | wc -l | tr -d ' ')"
[ "$remaining_managed" -eq 0 ]

echo "PASS: Project Core project bootstrap installs 10 core skills, preserves project content, reruns safely, refuses conflicts, and removes only managed files."
