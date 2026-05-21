#!/usr/bin/env bash
# install.sh — Install LinkRight skills to Claude Code or Agent Skills directory

set -euo pipefail

SKILLS_DIR="${1:-$HOME/.claude/skills}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing LinkRight skills → $SKILLS_DIR"

for skill in linkright-mem linkright-hunt linkright-sync linkright-interview linkright-push; do
    src="$SCRIPT_DIR/$skill"
    dst="$SKILLS_DIR/$skill"
    if [ -d "$src" ]; then
        cp -r "$src" "$dst"
        echo "  ✓ $skill"
    else
        echo "  ✗ $skill (not found in bundle)"
    fi
done

echo ""
echo "Done. Start with: /linkright-push → F) First-time setup"
echo "Then: /linkright-mem → onboard your resume"
