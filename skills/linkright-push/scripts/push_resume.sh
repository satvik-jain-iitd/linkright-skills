#!/usr/bin/env bash
# push_resume.sh — Validate → PDF → commit → tag → push resume to linkright-resume repo
# Usage: push_resume.sh <html_path> <pdf_path> <company-slug> <role-slug> <date>

set -euo pipefail

HTML_PATH="$1"
PDF_PATH="$2"
COMPANY_SLUG="$3"
ROLE_SLUG="$4"
DATE="${5:-$(date +%Y-%m-%d)}"

RESUME_REPO="$HOME/linkright-repos/linkright-resume"
TAG="resume-${COMPANY_SLUG}-${ROLE_SLUG}-${DATE}"
ROLE_DIR="$RESUME_REPO/roles/${COMPANY_SLUG}-${ROLE_SLUG}"

die() { echo "ERROR: $*" >&2; exit 1; }

# ── Verify inputs ──────────────────────────────────────────────────────────
[ -f "$HTML_PATH" ] || die "HTML not found: $HTML_PATH"
[ -f "$PDF_PATH"  ] || die "PDF not found: $PDF_PATH"
[ -d "$RESUME_REPO/.git" ] || die "linkright-resume not cloned at $RESUME_REPO. Run scaffold_repos.sh first."

# ── Pull latest ────────────────────────────────────────────────────────────
git -C "$RESUME_REPO" pull --ff-only 2>/dev/null || true

# ── Copy files ────────────────────────────────────────────────────────────
mkdir -p "$ROLE_DIR"
cp "$HTML_PATH" "$ROLE_DIR/index.html"
cp "$PDF_PATH"  "$ROLE_DIR/resume.pdf"

# Update root index.html if this is flagged as latest
if [ "${6:-}" = "--latest" ]; then
    cp "$HTML_PATH" "$RESUME_REPO/index.html"
    echo "Updated root index.html (latest)"
fi

# ── Commit ─────────────────────────────────────────────────────────────────
git -C "$RESUME_REPO" add "roles/${COMPANY_SLUG}-${ROLE_SLUG}/"
git -C "$RESUME_REPO" diff --cached --stat

git -C "$RESUME_REPO" commit -m "resume: ${COMPANY_SLUG} ${ROLE_SLUG} [${DATE}]"

# ── Tag ────────────────────────────────────────────────────────────────────
git -C "$RESUME_REPO" tag "$TAG" 2>/dev/null || \
  git -C "$RESUME_REPO" tag -f "$TAG"

# ── Push ───────────────────────────────────────────────────────────────────
git -C "$RESUME_REPO" push origin main
git -C "$RESUME_REPO" push origin "$TAG" 2>/dev/null || \
  git -C "$RESUME_REPO" push origin --tags

GH_USER=$(git -C "$RESUME_REPO" remote get-url origin | sed 's|.*github.com[:/]\([^/]*\)/.*|\1|')

echo ""
echo "✓ Pushed: roles/${COMPANY_SLUG}-${ROLE_SLUG}/"
echo "✓ Tag: $TAG"
echo ""
echo "Public URL: https://${GH_USER}.github.io/linkright-resume/roles/${COMPANY_SLUG}-${ROLE_SLUG}/"
echo "Latest:     https://${GH_USER}.github.io/linkright-resume/"
