#!/usr/bin/env bash
# install.sh — Install LinkRight skills to Claude Code or Agent Skills directory

set -euo pipefail

SKILLS_DIR="${1:-$HOME/.claude/skills}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing LinkRight skills, $SKILLS_DIR"
mkdir -p "$SKILLS_DIR"

# Every skill in the bundle. Discovered dynamically so a new skill dir is picked
# up automatically, with an explicit fallback list for older bundles.
SKILLS="$(cd "$SCRIPT_DIR" && ls -d linkright-* 2>/dev/null | tr '\n' ' ')"
if [ -z "$SKILLS" ]; then
    SKILLS="linkright-setup linkright-mem linkright-hunt linkright-sync linkright-push linkright-interview linkright-interview-coach linkright-companion linkright-network linkright-portfolio"
fi

for skill in $SKILLS; do
    src="$SCRIPT_DIR/$skill"
    dst="$SKILLS_DIR/$skill"
    if [ -d "$src" ]; then
        rm -rf "$dst"
        cp -r "$src" "$dst"
        echo "  installed $skill"
    else
        echo "  missing $skill (not in bundle)"
    fi
done

echo ""
echo "Done. First run, /linkright-setup, then /linkright-mem to onboard your resume."
