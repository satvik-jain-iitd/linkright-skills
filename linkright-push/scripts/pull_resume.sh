#!/usr/bin/env bash
# pull_resume.sh — Retrieve a specific resume version from linkright-resume repo
# Usage: pull_resume.sh <company-slug> <role-slug> [date-or-latest]

set -euo pipefail

COMPANY_SLUG="${1:-}"
ROLE_SLUG="${2:-}"
DATE="${3:-latest}"

RESUME_REPO="$HOME/linkright-repos/linkright-resume"

die() { echo "ERROR: $*" >&2; exit 1; }

[ -d "$RESUME_REPO/.git" ] || die "linkright-resume not cloned at $RESUME_REPO"

# ── Pull latest ────────────────────────────────────────────────────────────
git -C "$RESUME_REPO" pull --ff-only 2>/dev/null || true

# ── List mode: no args ─────────────────────────────────────────────────────
if [ -z "$COMPANY_SLUG" ]; then
    echo ""
    echo "AVAILABLE RESUME TAGS:"
    git -C "$RESUME_REPO" tag | grep "^resume-" | sort -r | while read -r tag; do
        echo "  $tag"
    done
    echo ""
    echo "Usage: pull_resume.sh <company-slug> <role-slug> [date]"
    exit 0
fi

# ── Find tag ───────────────────────────────────────────────────────────────
if [ "$DATE" = "latest" ]; then
    TAG=$(git -C "$RESUME_REPO" tag | grep "^resume-${COMPANY_SLUG}-${ROLE_SLUG}-" | sort -r | head -1)
    [ -n "$TAG" ] || die "No tag found for: resume-${COMPANY_SLUG}-${ROLE_SLUG}-*"
else
    TAG="resume-${COMPANY_SLUG}-${ROLE_SLUG}-${DATE}"
    git -C "$RESUME_REPO" tag | grep -q "^$TAG$" || die "Tag not found: $TAG"
fi

echo "Pulling: $TAG"

# ── Checkout to temp dir ───────────────────────────────────────────────────
OUT_DIR="$HOME/Desktop/${COMPANY_SLUG}-${ROLE_SLUG}-$(date +%Y%m%d%H%M%S)"
mkdir -p "$OUT_DIR"

git -C "$RESUME_REPO" show "${TAG}:roles/${COMPANY_SLUG}-${ROLE_SLUG}/index.html" > "$OUT_DIR/index.html" 2>/dev/null || \
  die "index.html not found in tag $TAG"

git -C "$RESUME_REPO" show "${TAG}:roles/${COMPANY_SLUG}-${ROLE_SLUG}/resume.pdf" > "$OUT_DIR/resume.pdf" 2>/dev/null || \
  echo "(PDF not found in this version)"

echo ""
echo "✓ Pulled: $TAG"
echo "  Local path: $OUT_DIR"
echo "  HTML: $OUT_DIR/index.html"
echo ""
echo "To edit: open in linkright-sync, then /linkright-push → A) Push when done."
