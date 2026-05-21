#!/usr/bin/env bash
# push_memory.sh — Diff + confirm + commit local memory to linkright-memory repo

set -euo pipefail

MEM_LOCAL="$HOME/.linkright/memory"
MEM_REPO="$HOME/linkright-repos/linkright-memory"
SETUP_LOCAL="$HOME/.linkright/user_setup.md"

die() { echo "ERROR: $*" >&2; exit 1; }

[ -d "$MEM_REPO/.git" ] || die "linkright-memory not cloned at $MEM_REPO. Run scaffold_repos.sh first."

# ── Pull latest ────────────────────────────────────────────────────────────
git -C "$MEM_REPO" pull --ff-only 2>/dev/null || true

# ── Sync local → repo (never overwrite newer repo files) ──────────────────
sync_file() {
    local src="$1" dst="$2"
    [ -f "$src" ] && cp "$src" "$dst"
}

sync_file "$MEM_LOCAL/facts.md"    "$MEM_REPO/memory/facts.md"
sync_file "$MEM_LOCAL/signals.md"  "$MEM_REPO/memory/signals.md"
sync_file "$MEM_LOCAL/outcomes.json" "$MEM_REPO/memory/outcomes.json"
sync_file "$SETUP_LOCAL"           "$MEM_REPO/user_setup.md"

# Sync expressions/stories if exist
if [ -d "$MEM_LOCAL/expressions/stories" ]; then
    mkdir -p "$MEM_REPO/memory/expressions/stories"
    rsync -a --exclude='.DS_Store' \
        "$MEM_LOCAL/expressions/stories/" \
        "$MEM_REPO/memory/expressions/stories/" 2>/dev/null || \
        cp -r "$MEM_LOCAL/expressions/stories/." "$MEM_REPO/memory/expressions/stories/"
fi

# Sync evidence/ if exist
if [ -d "$MEM_LOCAL/evidence" ]; then
    mkdir -p "$MEM_REPO/memory/evidence"
    rsync -a --exclude='.DS_Store' "$MEM_LOCAL/evidence/" "$MEM_REPO/memory/evidence/" 2>/dev/null || \
        cp -r "$MEM_LOCAL/evidence/." "$MEM_REPO/memory/evidence/"
fi

# ── Show diff ─────────────────────────────────────────────────────────────
echo ""
echo "MEMORY DIFF:"
git -C "$MEM_REPO" add -A
git -C "$MEM_REPO" diff --cached --stat

if git -C "$MEM_REPO" diff --cached --quiet; then
    echo "Nothing changed. Memory vault is up to date."
    exit 0
fi

# ── Confirm ────────────────────────────────────────────────────────────────
echo ""
read -p "Commit and push? (y/n) " -n 1 -r
echo
[[ $REPLY =~ ^[Yy]$ ]] || { echo "Aborted."; exit 0; }

# ── Commit ─────────────────────────────────────────────────────────────────
COMMIT_MSG="memory: sync $(date +%Y-%m-%d)"

# Build summary for commit message
FACTS_COUNT=$(grep -c "^id:" "$MEM_REPO/memory/facts.md" 2>/dev/null || echo 0)
SIGS_COUNT=$(grep -c "^name:" "$MEM_REPO/memory/signals.md" 2>/dev/null || echo 0)
COMMIT_MSG="memory: sync $(date +%Y-%m-%d) — ${FACTS_COUNT} facts, ${SIGS_COUNT} signals"

git -C "$MEM_REPO" commit -m "$COMMIT_MSG"
git -C "$MEM_REPO" push origin main

HASH=$(git -C "$MEM_REPO" rev-parse --short HEAD)
echo ""
echo "✓ Memory pushed: $HASH"
echo "  Facts: $FACTS_COUNT  Signals: $SIGS_COUNT"
