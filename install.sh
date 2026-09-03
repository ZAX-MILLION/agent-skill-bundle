#!/bin/bash
# Install complete skill directories into an Agent Skills root.
# Usage: ./install.sh [target] [--flat]
#   nested (default): <target>/<category>/<skill>/SKILL.md
#   --flat:           <target>/<skill>/SKILL.md
set -euo pipefail

TARGET=""
FLAT=0
for arg in "$@"; do
  case "$arg" in
    --flat) FLAT=1 ;;
    --help|-h)
      echo "Usage: ./install.sh [target] [--flat]"
      echo "Default target: ~/.claude/skills"
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
    if [ "$FLAT" -eq 1 ]; then
      dest="$TARGET/$skill_name"
      if [ -e "$dest" ] && [ ! -f "$dest/SKILL.md" ]; then
        echo "Refusing to overwrite non-skill path: $dest" >&2
        exit 1
      fi
    else
      dest="$TARGET/$category/$skill_name"
    fi

    mkdir -p "$dest"
    cp -r "$skill_dir"/. "$dest"/
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
