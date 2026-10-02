#!/bin/bash
# Install complete skill directories into an Agent Skills root.
# Usage: ./install.sh [target] [--flat] [--force] [--on-demand|--codex-efficient] [--prune-managed]
#   nested (default): <target>/<category>/<skill>/SKILL.md
#   --flat:           <target>/<skill>/SKILL.md
set -euo pipefail

TARGET=""
FLAT=0
FORCE=0
ON_DEMAND=0
CODEX_EFFICIENT=0
PRUNE_MANAGED=0

for arg in "$@"; do
  case "$arg" in
    --flat) FLAT=1 ;;
    --force) FORCE=1 ;;
    --on-demand) ON_DEMAND=1 ;;
    --codex-efficient) CODEX_EFFICIENT=1 ;;
    --prune-managed) PRUNE_MANAGED=1 ;;
    --help|-h)
      echo "Usage: ./install.sh [target] [--flat] [--force] [--on-demand|--codex-efficient] [--prune-managed]"
      echo "Default target: ~/.claude/skills"
      echo "--flat  install skills directly under the target root"
      echo "--force replace an existing unmarked destination skill"
      echo "--on-demand --flat  install only i-have-adhd + skill-retrieval-routing"
      echo "--codex-efficient --flat  install the small Codex credit-efficient profile"
      echo "--prune-managed  with a selective flat mode, remove only OTHER bundle-owned flat skills"
      exit 0
      ;;
    --*) echo "Unknown option: $arg" >&2; exit 2 ;;
    *)
      if [ -n "$TARGET" ]; then
        echo "Only one target directory may be supplied." >&2
        exit 2
      fi
      TARGET="$arg"
      ;;
  esac
done

if [ "$ON_DEMAND" -eq 1 ] && [ "$CODEX_EFFICIENT" -eq 1 ]; then
  echo "--on-demand and --codex-efficient are mutually exclusive." >&2
  exit 2
fi

MODE="full"
if [ "$ON_DEMAND" -eq 1 ]; then
  MODE="on-demand"
elif [ "$CODEX_EFFICIENT" -eq 1 ]; then
  MODE="codex-efficient"
fi

TARGET="${TARGET:-$HOME/.claude/skills}"
if [ "$MODE" != "full" ] && [ "$FLAT" -ne 1 ]; then
  echo "--$MODE requires --flat." >&2
  exit 2
fi
if [ "$PRUNE_MANAGED" -eq 1 ] && { [ "$MODE" = "full" ] || [ "$FLAT" -ne 1 ]; }; then
  echo "--prune-managed is only valid with --on-demand --flat or --codex-efficient --flat." >&2
  exit 2
fi

BUNDLE_DIR="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$TARGET"

selected_source_key() {
  local source_key="$1"
  case "$MODE:$source_key" in
    on-demand:productivity/i-have-adhd|on-demand:research/skill-retrieval-routing)
      return 0
      ;;
    codex-efficient:productivity/i-have-adhd|    codex-efficient:research/skill-retrieval-routing|    codex-efficient:productivity/credit-usage-helper|    codex-efficient:coding/ponytail|    codex-efficient:productivity/graft|    codex-efficient:coding/graphify|    codex-efficient:security/secure-by-default-development|    codex-efficient:process/verification-before-completion|    codex-efficient:process/task-to-pr|    codex-efficient:process/test|    codex-efficient:process/review|    codex-efficient:process/codex-issue-coordinator)
      return 0
      ;;
    full:*)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

is_bundle_source_key() {
  case "$1" in
    design/*|security/*|process/*|multiplayer/*|wordpress/*|marketing/*|qa/*|operations/*|coding/*|research/*|productivity/*|automation/*|creative/*)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

# A selective mode must not silently coexist with old bundle-owned native skills
# that would defeat the intended discovery/context budget.
legacy_count=0
if [ "$MODE" != "full" ]; then
  for existing in "$TARGET"/*/; do
    [ -d "$existing" ] || continue
    [ -L "$existing" ] && continue
    marker="$existing/.agent-skill-bundle-source"
    [ -f "$marker" ] && [ ! -L "$marker" ] || continue
    source_key="$(cat "$marker")"
    skill_name="$(basename "$existing")"
    [ "${source_key##*/}" = "$skill_name" ] || continue
    if is_bundle_source_key "$source_key" && ! selected_source_key "$source_key"; then
      legacy_count=$((legacy_count + 1))
    fi
  done
  if [ "$legacy_count" -gt 0 ] && [ "$PRUNE_MANAGED" -ne 1 ]; then
    echo "Found $legacy_count other bundle-managed native skills in $TARGET." >&2
    echo "$MODE mode would still expose their descriptions at startup." >&2
    echo "Review them, then add --prune-managed to remove ONLY marked bundle copies." >&2
    exit 1
  fi
fi

echo "Installing Agent Skills → $TARGET"
count=0
skipped=0

for category in design security process multiplayer wordpress marketing qa operations coding research productivity automation creative; do
  [ -d "$BUNDLE_DIR/$category" ] || continue
  for skill_dir in "$BUNDLE_DIR/$category"/*/; do
    [ -d "$skill_dir" ] || continue
    if [ ! -f "$skill_dir/SKILL.md" ]; then
      skipped=$((skipped + 1))
      continue
    fi

    skill_name="$(basename "$skill_dir")"
    source_key="$category/$skill_name"
    if ! selected_source_key "$source_key"; then
      continue
    fi

    if [ "$FLAT" -eq 1 ]; then
      dest="$TARGET/$skill_name"
    else
      dest="$TARGET/$category/$skill_name"
    fi
    marker="$dest/.agent-skill-bundle-source"

    if [ -e "$dest" ]; then
      owned=0
      if [ -f "$marker" ] && [ "$(cat "$marker")" = "$source_key" ]; then
        owned=1
      fi
      if [ "$owned" -eq 0 ] && [ "$FORCE" -ne 1 ]; then
        echo "Refusing to replace existing unmarked skill: $dest" >&2
        echo "Use --force only after reviewing that destination." >&2
        exit 1
      fi
      rm -rf "$dest"
    fi

    mkdir -p "$dest"
    cp -r "$skill_dir"/. "$dest"/
    printf '%s\n' "$source_key" > "$marker"
    count=$((count + 1))
  done
done

if [ "$MODE" = "on-demand" ] && [ "$count" -ne 2 ]; then
  echo "Expected exactly two bootstrap skills; installed $count." >&2
  exit 1
fi
if [ "$MODE" = "codex-efficient" ] && [ "$count" -ne 12 ]; then
  echo "Expected exactly 12 Codex-efficient skills; installed $count." >&2
  exit 1
fi

# Only act on direct child directories bearing this bundle's matching marker.
# Never delete unmarked, symlinked, or another owner's skill directory.
pruned=0
if [ "$PRUNE_MANAGED" -eq 1 ]; then
  for existing in "$TARGET"/*/; do
    [ -d "$existing" ] || continue
    [ -L "$existing" ] && continue
    marker="$existing/.agent-skill-bundle-source"
    [ -f "$marker" ] && [ ! -L "$marker" ] || continue
    source_key="$(cat "$marker")"
    skill_name="$(basename "$existing")"
    [ "${source_key##*/}" = "$skill_name" ] || continue
    if is_bundle_source_key "$source_key" && ! selected_source_key "$source_key"; then
      rm -rf -- "$existing"
      pruned=$((pruned + 1))
    fi
  done
  echo "Pruned $pruned other bundle-managed skills; unmarked skills were untouched."
fi

echo "Installed $count skill directories."
if [ "$skipped" -gt 0 ]; then
  echo "Skipped $skipped non-skill collection/directories (no SKILL.md)."
fi
if [ "$FLAT" -eq 0 ]; then
  echo "Layout: nested by category. Use --flat for hosts that require direct child skills."
else
  echo "Layout: flat."
fi
if [ "$MODE" = "on-demand" ]; then
  echo "On-demand mode: only two bootstrap descriptions are exposed by this bundle."
  echo "The full source checkout and a separately configured Skill Retrieval MCP remain necessary."
elif [ "$MODE" = "codex-efficient" ]; then
  echo "Codex-efficient mode: 12 high-value skills are exposed; expensive/specialist workflows remain on-demand."
  echo "External Graphify/Graft runtimes are NOT installed by this script."
fi
