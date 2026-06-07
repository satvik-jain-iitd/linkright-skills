#!/usr/bin/env bash
# build.sh — assemble the unified `linkright` plugin bundle from canonical sources.
#
# Sources stay canonical in their own repos. This script copies them into
# dist/linkright/ (gitignored) so nothing is duplicated in git on main.
#
#   - The 10 linkright-* skills:   this repo's root (discovered dynamically)
#   - The 5 content-engine skills: the LinkedIn Content repo's plugin-source/skills
#     (renamed with a content- prefix to namespace them)
#   - The content engine:          that same plugin-source/engine
#
# Usage:
#   bash build.sh              assemble + validate dist/linkright/ (no network)
#   bash build.sh --publish    assemble, then force-push the bundle to the
#                              `release` branch root (needs push rights)
#
# The marketplace.json on main points the plugin source at the `release` branch,
# so `release` always holds the full, committed, installable bundle while main
# stays clean and duplication-free.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIST="$REPO_DIR/dist/linkright"
PLUGIN_NAME="linkright"

# --- locate the content-engine source -------------------------------------
# Override with: LINKRIGHT_CONTENT_SRC=/path/to/plugin-source bash build.sh
DEFAULT_CONTENT_SRC="$HOME/Downloads/Mission Job Switch/LinkedIn Content/LinkRight-Research/plugin-source"
CONTENT_SRC="${LINKRIGHT_CONTENT_SRC:-$DEFAULT_CONTENT_SRC}"

if [ ! -d "$CONTENT_SRC/skills" ] || [ ! -d "$CONTENT_SRC/engine" ]; then
    echo "ERROR: content-engine source not found at:" >&2
    echo "  $CONTENT_SRC" >&2
    echo "" >&2
    echo "Set the real path and re-run, e.g.:" >&2
    echo "  LINKRIGHT_CONTENT_SRC=\"/path/to/LinkRight-Research/plugin-source\" bash build.sh" >&2
    exit 1
fi

# content-engine skill rename map: <source-dir>:<bundle-dir>
CONTENT_MAP=(
    "daily-post:content-daily-post"
    "optimize:content-optimize"
    "profile-search:content-profile-search"
    "topic-hunt:content-topic-hunt"
    "setup:content-voice-setup"
)

# junk never copied into the bundle
EXCLUDES=(--exclude='.DS_Store' --exclude='__pycache__' --exclude='*.pyc'
          --exclude='.tmp_*' --exclude='.git' --exclude='.env')

echo "==> Assembling $PLUGIN_NAME bundle"
echo "    repo:    $REPO_DIR"
echo "    content: $CONTENT_SRC"

# --- clean slate ----------------------------------------------------------
rm -rf "$DIST"
mkdir -p "$DIST/.claude-plugin" "$DIST/skills"

# --- plugin manifest ------------------------------------------------------
# No "version" on purpose: every push to the release branch is a fresh commit,
# so Claude Code treats each release-branch SHA as a new version automatically.
cat > "$DIST/.claude-plugin/plugin.json" <<'JSON'
{
  "name": "linkright",
  "description": "LinkRight, a local-first career OS. One install for resume tailoring, interview prep, job hunt, LinkedIn content and outreach, portfolio, and a shared career memory that every skill reads and writes.",
  "author": { "name": "Satvik Jain" },
  "homepage": "https://github.com/satvik-jain-iitd/linkright-skills",
  "repository": "https://github.com/satvik-jain-iitd/linkright-skills",
  "keywords": ["career", "resume", "interview", "job-search", "linkedin", "personal-branding", "career-memory"]
}
JSON

# --- the 10 linkright-* skills (canonical here, copy as-is) ----------------
linkright_count=0
for src in "$REPO_DIR"/linkright-*/; do
    [ -d "$src" ] || continue
    name="$(basename "$src")"
    if [ ! -f "$src/SKILL.md" ]; then
        echo "WARNING: $name has no SKILL.md, skipping" >&2
        continue
    fi
    rsync -a "${EXCLUDES[@]}" "$src" "$DIST/skills/$name/"
    linkright_count=$((linkright_count + 1))
    echo "    + skills/$name"
done

# --- the 5 content-engine skills (rename-mapped) --------------------------
content_count=0
for pair in "${CONTENT_MAP[@]}"; do
    s="${pair%%:*}"; d="${pair##*:}"
    if [ ! -d "$CONTENT_SRC/skills/$s" ]; then
        echo "ERROR: expected content skill not found: $CONTENT_SRC/skills/$s" >&2
        exit 1
    fi
    rsync -a "${EXCLUDES[@]}" "$CONTENT_SRC/skills/$s/" "$DIST/skills/$d/"
    content_count=$((content_count + 1))
    echo "    + skills/$d  (from $s)"
done

# --- the content engine ---------------------------------------------------
rsync -a "${EXCLUDES[@]}" "$CONTENT_SRC/engine/" "$DIST/engine/"
echo "    + engine/"

# --- bundle README --------------------------------------------------------
cat > "$DIST/README.md" <<'MD'
# LinkRight

One local-first career OS, installed as a single plugin. Every skill reads and
writes one shared career memory at `~/.linkright`, so your resume, interviews,
content, and outreach all stand on the same confirmed facts about your work.

## Install (marketplace)

```
/plugin marketplace add satvik-jain-iitd/linkright-skills
/plugin install linkright@linkright
```

First run: `/linkright-setup`, then `/linkright-mem` to onboard your resume.

## What's inside

Memory is the foundation: `linkright-mem` owns the shared Evidence, Facts, and
Signals store. Get the job: `linkright-sync` (ATS-safe resume), `linkright-hunt`
(role search), `linkright-push` (publish to GitHub Pages), `linkright-portfolio`
(proof of work). Prep: `linkright-interview` (story bank), `linkright-interview-coach`
(Sage, full mock with scoring). Be seen: the content engine in `engine/` driven by
`content-daily-post`, `content-topic-hunt`, `content-profile-search`,
`content-optimize`, and `content-voice-setup`. Reach out: `linkright-network`
(one-to-one outreach). Run it: `linkright-setup` (first-run wizard),
`linkright-companion` (daily briefing).

All skills point at `~/.linkright`. The `linkright` CLI on PyPI writes the
canonical store; the skills read the derived view and refresh it on use.
MD

# --- validate -------------------------------------------------------------
echo "==> Validating bundle"
fail=0
python3 -c "import json,sys; json.load(open('$DIST/.claude-plugin/plugin.json')); print('    plugin.json: valid JSON')" || fail=1

skill_total=0
for d in "$DIST"/skills/*/; do
    [ -d "$d" ] || continue
    skill_total=$((skill_total + 1))
    if [ ! -f "$d/SKILL.md" ]; then
        echo "    MISSING SKILL.md: $(basename "$d")" >&2
        fail=1
    fi
done
[ -d "$DIST/engine" ] || { echo "    MISSING engine/" >&2; fail=1; }

echo "    linkright skills: $linkright_count   content skills: $content_count   total: $skill_total"
if [ "$skill_total" -ne 15 ]; then
    echo "    WARNING: expected 15 skills (10 linkright + 5 content), got $skill_total" >&2
fi
if [ "$fail" -ne 0 ]; then
    echo "==> BUILD FAILED validation" >&2
    exit 1
fi
echo "==> Bundle ready at: $DIST"

# --- publish (optional) ---------------------------------------------------
if [ "${1:-}" = "--publish" ]; then
    echo "==> Publishing bundle to the 'release' branch (force)"
    WT="$(mktemp -d)"
    git -C "$REPO_DIR" worktree add --force --detach "$WT" >/dev/null
    (
        cd "$WT"
        git checkout --orphan release
        git rm -rf . >/dev/null 2>&1 || true
        rsync -a "$DIST/" ./
        git add -A
        git commit -q -m "release: linkright plugin bundle $(date -u +%FT%TZ)"
        git push -f origin release
    )
    git -C "$REPO_DIR" worktree remove --force "$WT"
    echo "==> Published. Users get it via the marketplace 'release' ref."
fi
