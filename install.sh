#!/bin/bash
# Install complete skill directories into an Agent Skills root.
# Usage: ./install.sh [target] [--flat] [--force]
#   nested (default): <target>/<category>/<skill>/SKILL.md
#   --flat:           <target>/<skill>/SKILL.md
set -euo pipefail

TARGET=""
FLAT=0
FORCE=0
for arg in "$@"; do
  case "$arg" in
    --flat) FLAT=1 ;;
    --force) FORCE=1 ;;
    --help|-h)
      echo "Usage: ./install.sh [target] [--flat] [--force]"
      echo "Default target: ~/.claude/skills"
      echo "--flat  install skills directly under the target root"
      echo "--force replace an existing unmarked destination skill"
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

TARGET="${TARGET:-$HOME/.claude/skills}"
BUNDLE_DIR="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$TARGET"

echo "Installing Agent Skills → $TARGET"
count=0
skipped=0

for category in design security process multiplayer wordpress marketing qa; do
  [ -d "$BUNDLE_DIR/$category" ] || continue
  for skill_dir in "$BUNDLE_DIR/$category"/*/; do
    [ -d "$skill_dir" ] || continue
    if [ ! -f "$skill_dir/SKILL.md" ]; then
      skipped=$((skipped + 1))
      continue
    fi

    skill_name="$(basename "$skill_dir")"
    source_key="$category/$skill_name"
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

echo "Installed $count skill directories."
if [ "$skipped" -gt 0 ]; then
  echo "Skipped $skipped non-skill collection/directories (no SKILL.md)."
fi
if [ "$FLAT" -eq 0 ]; then
  echo "Layout: nested by category. Use --flat for hosts that require direct child skills."
else
  echo "Layout: flat."
fi
