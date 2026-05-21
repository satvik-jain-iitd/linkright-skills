---
name: linkright-push
description: |
  GitHub backbone for the entire LinkRight system. Manages three repos: linkright-resume
  (public — versioned resume hosting + GitHub Pages URLs), linkright-portfolio (public —
  portfolio site + live Kanban dashboard), linkright-memory (private — facts, signals,
  outcomes, pipeline). Push workflows: validate HTML → generate PDF → commit → tag with
  company+role+date → push → return permanent URL. Pull workflow: retrieve any specific
  resume version by tag. Memory push: diff → confirm → commit. Dashboard: auto-generated
  from pipeline.json, no server required. First-time setup creates all 3 repos via gh CLI.

  Use when user says: /linkright-push, "push my resume", "publish resume", "push memory",
  "sync pipeline", "create resume repo", "GitHub pages resume", "share my resume URL",
  "pull resume for editing", "view dashboard", or any GitHub/publishing request.
---

# LinkRight Push

SKILL_DIR   = `~/.claude/skills/linkright-push`
SETUP       = `~/.linkright/user_setup.md`
MEM_DIR     = `~/.linkright/memory`
PIPELINE    = `~/Downloads/Mission Job Switch/job scraping/memory/pipeline.json`

---

## Absolute Rules

- NEVER push to public repos without user seeing exactly what's being published
- ALWAYS validate HTML (ATS scan + width check) before public resume push
- ALWAYS generate PDF alongside HTML on every resume push
- ALWAYS tag every resume push: `resume-<company-slug>-<role-slug>-<YYYY-MM-DD>`
- NEVER make linkright-memory repo public — contains salary targets, rejections, hard constraints
- ALWAYS show `git diff --stat` before any memory commit
- NEVER push unvalidated content — constraint check must pass first
- ALWAYS check `gh auth status` before any git/gh operations
- NEVER commit `.env` files, API keys, or `user_setup.md` to public repos

---

## Gate 0 — Prerequisites Check

```bash
# Git available?
git --version

# gh CLI available?
gh --version || echo "MISSING: install via brew install gh"

# gh authenticated?
gh auth status

# user_setup.md exists?
ls ~/.linkright/user_setup.md
```

If gh missing → show install instructions, stop.
If not authenticated → `gh auth login`, wait for completion.

---

## Gate 1 — Action Selection

```
AskUserQuestion:
  question: "What do you want to do?"
  options:
    A) Push resume — publish new or updated version to GitHub Pages
    B) Pull resume — retrieve a version for editing
    C) Push memory vault — commit facts/signals/outcomes to private repo
    D) Sync pipeline — push pipeline.json, rebuild dashboard
    E) View dashboard / resume URL
    F) First-time setup — create all 3 repos
```

---

## Gate 2 — Execute (branch per action)

---

### Action A — Push Resume

**Inputs:** company name + role title (required). Resume file path (HTML).

If file path not provided: scan `~/Downloads` and current dir for `resume_*.html` files, ask user to confirm.

```bash
# Step 1: Validate
python3 ~/.claude/skills/linkright-push/scripts/validate_html.py '<html_path>'
python3 ~/.claude/skills/linkright-mem/scripts/constraint_checker.py \
  --text "$(cat '<html_path>')" \
  --constraints ~/.linkright/user_setup.md

# If validation fails → show violations → stop. NEVER push invalid resume.

# Step 2: Slugify
COMPANY_SLUG="<company-name-lowercase-hyphenated>"
ROLE_SLUG="<role-title-lowercase-hyphenated>"
DATE="$(date +%Y-%m-%d)"
TAG="resume-${COMPANY_SLUG}-${ROLE_SLUG}-${DATE}"

# Step 3: Generate PDF
python3 ~/.claude/skills/linkright-push/scripts/generate_pdf.py '<html_path>'
# Output: same dir as HTML, same name + .pdf

# Step 4: Push
bash ~/.claude/skills/linkright-push/scripts/push_resume.sh \
  '<html_path>' \
  '<pdf_path>' \
  "${COMPANY_SLUG}" \
  "${ROLE_SLUG}" \
  "${DATE}"
```

Show user:
```
✓ Pushed: roles/<company>-<role>/index.html
✓ Pushed: roles/<company>-<role>/resume.pdf
✓ Tagged: resume-<company>-<role>-<date>

Public URL: https://<username>.github.io/linkright-resume/roles/<company>-<role>/
Latest:     https://<username>.github.io/linkright-resume/
```

---

### Action B — Pull Resume

User provides: company slug + role slug (or picks from tag list).

```bash
# List all resume tags
cd ~/linkright-resume && git tag | grep "^resume-" | sort -r

# Pull specified version
bash ~/.claude/skills/linkright-push/scripts/pull_resume.sh \
  '<company-slug>' '<role-slug>' '<date-or-latest>'
```

Opens file locally. Offers to load into linkright-sync for editing.

---

### Action C — Push Memory Vault

```bash
bash ~/.claude/skills/linkright-push/scripts/push_memory.sh
```

Script shows:
```
MEMORY DIFF
  facts.md:    +3 new facts, 1 modified
  signals.md:  +1 new signal
  outcomes.json: 2 new outcomes

Commit this? (y/n)
```

User confirms → commit + push → return commit hash.

---

### Action D — Sync Pipeline

```bash
# Build fresh dashboard from pipeline.json
python3 ~/.claude/skills/linkright-push/scripts/build_dashboard.py \
  --pipeline "$PIPELINE" \
  --output ~/linkright-portfolio/dashboard/index.html

# Commit + push
cd ~/linkright-portfolio
git add dashboard/index.html
git commit -m "dashboard: sync $(date +%Y-%m-%d)"
git push origin main
```

Show: pipeline stage breakdown + dashboard URL.

---

### Action E — View URLs

Read `resume_base_url` and `portfolio_base_url` from SETUP. Display:
```
Resume:    https://<username>.github.io/linkright-resume/
Dashboard: https://<username>.github.io/linkright-portfolio/dashboard/
Portfolio: https://<username>.github.io/linkright-portfolio/
```

Also list recent resume tags for quick reference.

---

### Action F — First-Time Setup

```bash
bash ~/.claude/skills/linkright-push/scripts/scaffold_repos.sh
```

Steps shown on screen:
1. Check gh auth
2. `gh repo create linkright-resume --public`
3. `gh repo create linkright-portfolio --public`
4. `gh repo create linkright-memory --private`
5. Enable Pages on resume + portfolio repos
6. Initialize folder structure + push placeholder index.html
7. Test: verify Pages URLs respond (wait up to 120s)
8. Write `resume_base_url` + `portfolio_base_url` to user_setup.md

After setup: run Action A with a sample resume to confirm end-to-end.

---

## Gate 3 — Confirm + Report

Every action ends with:
- What was committed (files changed, lines added)
- URL(s) updated
- Any warnings or failures

---

## Scripts Reference

| Script | Purpose |
|---|---|
| `scripts/push_resume.sh` | validate → PDF → commit → tag → push |
| `scripts/pull_resume.sh` | retrieve specified resume version |
| `scripts/push_memory.sh` | diff → confirm → commit memory vault |
| `scripts/scaffold_repos.sh` | first-time: create 3 repos + Pages setup |
| `scripts/build_dashboard.py` | generate Kanban HTML from pipeline.json |
| `scripts/validate_html.py` | HTML validation pre-push |
| `scripts/generate_pdf.py` | headless Chrome HTML → PDF |

---

## Repo Architecture

```
linkright-resume/ (PUBLIC — GitHub Pages)
├── index.html                    ← latest resume
├── roles/
│   └── <company-slug>-<role-slug>/
│       ├── index.html
│       └── resume.pdf
└── README.md

linkright-portfolio/ (PUBLIC — GitHub Pages)
├── index.html                    ← portfolio home
├── cases/
├── dashboard/
│   └── index.html               ← auto-generated Kanban
└── README.md

linkright-memory/ (PRIVATE)
├── user_setup.md
├── memory/
│   ├── facts.md
│   ├── signals.md
│   ├── outcomes.json
│   ├── evidence/
│   └── expressions/
├── pipeline.json
├── diary/
└── decisions/
    └── decision_log.md
```

---

## Phase Status

| Feature | Status |
|---|---|
| SKILL.md (orchestrator) | ✅ |
| scaffold_repos.sh | ✅ |
| push_resume.sh | ✅ |
| pull_resume.sh | ✅ |
| push_memory.sh | ✅ |
| build_dashboard.py (Kanban HTML) | ✅ |
| validate_html.py | ✅ |
| generate_pdf.py | ✅ |
| GitHub Actions (diary/weekly/health) | ⏳ ref_03_actions_templates.md |
