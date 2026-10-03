#!/usr/bin/env bash
set -euo pipefail

RAW_BASE="${AGENT_INIT_RAW_BASE:-https://raw.githubusercontent.com/ZAX-MILLION/agent-skill-bundle/main}"
BIN_DIR="${AGENT_INIT_BIN_DIR:-$HOME/.local/bin}"
TARGET="$BIN_DIR/agent-init"
mkdir -p "$BIN_DIR"

if command -v curl >/dev/null 2>&1; then
  curl -fsSL "$RAW_BASE/scripts/agent_init.py" -o "$TARGET"
elif command -v python3 >/dev/null 2>&1; then
  python3 - "$RAW_BASE/scripts/agent_init.py" "$TARGET" <<'PY'
import pathlib, sys, urllib.request
url, target = sys.argv[1:]
pathlib.Path(target).write_bytes(urllib.request.urlopen(url, timeout=30).read())
PY
else
  echo "Need curl or Python 3 to install agent-init." >&2
  exit 2
fi

chmod +x "$TARGET"

echo "Installed: $TARGET"
case ":$PATH:" in
  *":$BIN_DIR:"*) ;;
  *)
    echo "NOTE: $BIN_DIR is not currently in PATH."
    echo "Add it to your shell PATH once, then use: agent-init"
    ;;
esac
echo "For every new project: cd into the project and run: agent-init"
