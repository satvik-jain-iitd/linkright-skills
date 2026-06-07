#!/usr/bin/env bash
# scaffold_repos.sh — First-time setup: create 3 LinkRight GitHub repos + Pages

set -euo pipefail

SETUP="$HOME/.linkright/user_setup.md"
LOG="$HOME/.linkright/push_setup.log"

log() { echo "[scaffold] $*" | tee -a "$LOG"; }
die() { echo "ERROR: $*" >&2; exit 1; }

# ── Prerequisites ──────────────────────────────────────────────────────────
command -v git >/dev/null 2>&1 || die "git not found. Install: brew install git"
command -v gh  >/dev/null 2>&1 || die "gh not found. Install: brew install gh"
gh auth status >/dev/null 2>&1 || die "gh not authenticated. Run: gh auth login"

GH_USER=$(gh api user --jq '.login')
log "Authenticated as: $GH_USER"

# ── Confirm before creating ────────────────────────────────────────────────
echo ""
echo "Will create 3 repositories under $GH_USER:"
echo "  PUBLIC  : $GH_USER/linkright-resume"
echo "  PUBLIC  : $GH_USER/linkright-portfolio"
echo "  PRIVATE : $GH_USER/linkright-memory"
echo ""
read -p "Proceed? (y/n) " -n 1 -r
echo
[[ $REPLY =~ ^[Yy]$ ]] || { echo "Aborted."; exit 0; }

# ── Helper: create repo if not exists ─────────────────────────────────────
create_repo() {
    local name="$1" visibility="$2" desc="$3"
    if gh repo view "$GH_USER/$name" >/dev/null 2>&1; then
        log "$name already exists — skipping create"
    else
        gh repo create "$name" "--${visibility}" --description "$desc" --confirm 2>/dev/null \
          || gh repo create "$GH_USER/$name" "--${visibility}" --description "$desc"
        log "Created: $GH_USER/$name ($visibility)"
    fi
}

create_repo "linkright-resume"    "public"  "Resume — versioned, GitHub Pages"
create_repo "linkright-portfolio" "public"  "Portfolio + career dashboard"
create_repo "linkright-memory"    "private" "LinkRight memory vault (private)"

# ── Clone all 3 ────────────────────────────────────────────────────────────
REPOS_DIR="$HOME/linkright"
mkdir -p "$REPOS_DIR"

clone_or_pull() {
    local name="$1"
    local dir="$REPOS_DIR/$name"
    if [ -d "$dir/.git" ]; then
        log "$name already cloned — pulling latest"
        git -C "$dir" pull --ff-only 2>/dev/null || true
    else
        gh repo clone "$GH_USER/$name" "$dir"
        log "Cloned $name → $dir"
    fi
}

clone_or_pull "linkright-resume"
clone_or_pull "linkright-portfolio"
clone_or_pull "linkright-memory"

# ── Initialize linkright-resume ────────────────────────────────────────────
RESUME_DIR="$REPOS_DIR/linkright-resume"
mkdir -p "$RESUME_DIR/roles"

if [ ! -f "$RESUME_DIR/index.html" ]; then
cat > "$RESUME_DIR/index.html" <<'HTML'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Resume</title>
  <style>body{font-family:sans-serif;max-width:800px;margin:40px auto;padding:0 20px;}</style>
</head>
<body>
  <h1>Resume</h1>
  <p>Published via <a href="https://github.com/linkright">LinkRight</a>.</p>
  <p>Role-specific versions available under <code>/roles/</code>.</p>
</body>
</html>
HTML
log "Created placeholder index.html for linkright-resume"
fi

cat > "$RESUME_DIR/README.md" <<MD
# Resume

Published via [LinkRight](https://github.com/linkright). Role-specific versions live under \`/roles/\`.
MD

git -C "$RESUME_DIR" add .
git -C "$RESUME_DIR" diff --cached --quiet || \
  git -C "$RESUME_DIR" commit -m "init: placeholder resume"
git -C "$RESUME_DIR" push origin main 2>/dev/null || \
  git -C "$RESUME_DIR" push --set-upstream origin main

# ── Initialize linkright-portfolio ────────────────────────────────────────
PORT_DIR="$REPOS_DIR/linkright-portfolio"
mkdir -p "$PORT_DIR/cases" "$PORT_DIR/dashboard"

if [ ! -f "$PORT_DIR/index.html" ]; then
cat > "$PORT_DIR/index.html" <<'HTML'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Portfolio</title>
  <style>body{font-family:sans-serif;max-width:900px;margin:40px auto;padding:0 20px;}</style>
</head>
<body>
  <h1>Portfolio</h1>
  <p>Published via LinkRight.</p>
  <ul>
    <li><a href="dashboard/">Career Dashboard →</a></li>
  </ul>
</body>
</html>
HTML
fi

if [ ! -f "$PORT_DIR/dashboard/index.html" ]; then
cat > "$PORT_DIR/dashboard/index.html" <<'HTML'
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Dashboard</title></head>
<body><p>Dashboard not yet generated. Run: python3 build_dashboard.py</p></body>
</html>
HTML
fi

cat > "$PORT_DIR/README.md" <<MD
# Portfolio

Published via [LinkRight](https://github.com/linkright). Dashboard at \`/dashboard/\`.
MD

git -C "$PORT_DIR" add .
git -C "$PORT_DIR" diff --cached --quiet || \
  git -C "$PORT_DIR" commit -m "init: placeholder portfolio"
git -C "$PORT_DIR" push origin main 2>/dev/null || \
  git -C "$PORT_DIR" push --set-upstream origin main

# ── Initialize linkright-memory ────────────────────────────────────────────
MEM_REPO="$REPOS_DIR/linkright-memory"
mkdir -p "$MEM_REPO/memory/evidence" "$MEM_REPO/memory/expressions/stories" \
         "$MEM_REPO/diary" "$MEM_REPO/decisions"

# Sync local memory files into repo (do not overwrite if newer in repo)
for f in facts.md signals.md outcomes.json; do
    src="$HOME/.linkright/memory/$f"
    dst="$MEM_REPO/memory/$f"
    [ -f "$src" ] && [ ! -f "$dst" ] && cp "$src" "$dst"
done

[ -f "$HOME/.linkright/user_setup.md" ] && \
  cp "$HOME/.linkright/user_setup.md" "$MEM_REPO/user_setup.md" 2>/dev/null || true

cat > "$MEM_REPO/README.md" <<MD
# LinkRight Memory Vault (PRIVATE)

Contains career data: facts, signals, outcomes, pipeline, diary, decisions.
Never make this repo public.
MD

git -C "$MEM_REPO" add .
git -C "$MEM_REPO" diff --cached --quiet || \
  git -C "$MEM_REPO" commit -m "init: memory vault"
git -C "$MEM_REPO" push origin main 2>/dev/null || \
  git -C "$MEM_REPO" push --set-upstream origin main

# ── Enable GitHub Pages ────────────────────────────────────────────────────
log "Enabling GitHub Pages on linkright-resume..."
gh api "repos/$GH_USER/linkright-resume/pages" \
  --method POST \
  --field source='{"branch":"main","path":"/"}' 2>/dev/null || \
  log "Pages may already be enabled on linkright-resume"

log "Enabling GitHub Pages on linkright-portfolio..."
gh api "repos/$GH_USER/linkright-portfolio/pages" \
  --method POST \
  --field source='{"branch":"main","path":"/"}' 2>/dev/null || \
  log "Pages may already be enabled on linkright-portfolio"

# ── Store URLs in user_setup.md ────────────────────────────────────────────
RESUME_URL="https://${GH_USER}.github.io/linkright-resume/"
PORTFOLIO_URL="https://${GH_USER}.github.io/linkright-portfolio/"

if [ -f "$SETUP" ]; then
    if ! grep -q "resume_base_url" "$SETUP"; then
        cat >> "$SETUP" <<CFG

# LinkRight Push URLs (auto-generated)
resume_base_url: ${RESUME_URL}
portfolio_base_url: ${PORTFOLIO_URL}
local_resume_repo: ${REPOS_DIR}/linkright-resume
local_portfolio_repo: ${REPOS_DIR}/linkright-portfolio
local_memory_repo: ${REPOS_DIR}/linkright-memory
CFG
        log "URLs written to user_setup.md"
    fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Setup complete."
echo ""
echo "Resume URL:    $RESUME_URL"
echo "Portfolio URL: $PORTFOLIO_URL"
echo "Dashboard URL: ${PORTFOLIO_URL}dashboard/"
echo ""
echo "GitHub Pages takes 1-2 minutes to activate."
echo "Run: /linkright-push → A) Push resume to publish your first version."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
