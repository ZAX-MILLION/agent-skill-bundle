#!/bin/bash
# Install all skills from this bundle into a target skills directory.
# Usage: ./install.sh [target]   (default: ~/.claude/skills)
set -euo pipefail

TARGET="${1:-$HOME/.claude/skills}"
BUNDLE_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Installing skill bundle → $TARGET"
mkdir -p "$TARGET"

count=0
for category in design security process multiplayer wordpress marketing qa; do
  for skill_dir in "$BUNDLE_DIR/$category"/*/; do
    [ -d "$skill_dir" ] || continue
    skill_name="$(basename "$skill_dir")"
    dest="$TARGET/$category/$skill_name"
    mkdir -p "$dest"
    cp -r "$skill_dir"/. "$dest"/
    count=$((count + 1))
  done
done

echo "✅ Installed $count skills into $TARGET"
echo "Categories: design/ security/ process/ multiplayer/ wordpress/ marketing/ qa/"
