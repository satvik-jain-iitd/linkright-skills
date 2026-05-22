---
name: linkright-hunt
description: |
  LinkRight's job discovery and opportunity intelligence layer. Finds jobs across
  ATS APIs, job boards, and free APIs; scores against user's profile; analyzes JDs through
  signal taxonomy; tracks opportunities through pipeline; adapts recommendations from
  application outcomes.

  Two modes:
    Mode A — Batch Discovery: NL description → param interpretation → run scrapers → ranked results
    Mode B — JD Intelligence: paste URL or text → signal extraction → fit score → pipeline save

  Use when user says: /linkright-hunt, "find jobs", "search jobs", "analyze this JD",
  "save to pipeline", "record outcome", "view pipeline", "probe this company's ATS",
  "what should I apply to", "job search", or any job-hunting request.

  Target sectors loaded from user_setup.md (target_sectors field). Default: ALL.
  NEVER automate LinkedIn account interaction. NEVER apply on behalf of user.
---

# LinkRight Hunt

Job discovery and opportunity intelligence. Covers the full loop: find → analyze → track → learn.

JOBS_DIR = `~/.linkright/jobs`
MEMORY_DIR = `$JOBS_DIR/memory`
HUNT_SCRIPTS = `~/.claude/skills/linkright-hunt/scripts`

---

## Core Rules

1. NEVER automate LinkedIn account login, apply, connect, or DM — ban risk is severe
2. NEVER apply on behalf of user — surface, score, and show only
3. NEVER write to pipeline.json without showing summary first
4. ALWAYS show both scores separately (fit score + shortlist probability)
5. ALWAYS explain score components — "78% fit: 4/5 primary signals matched"
6. ALWAYS preserve full JD text in pipeline (needed by linkright-sync downstream)
7. Sectors filter — read target_sectors from user_setup.md (default: ALL)

---

## Gate 1 — Mode Detection

If user invoked with a clear intent (e.g., `/linkright-hunt search ...` or `/linkright-hunt analyze ...`),
detect mode directly from the phrase and skip to the relevant gate.

Otherwise, ask:

```
Use AskUserQuestion:
  question: "What do you want to do?"
  options:
    a) Search for new jobs         — describe in plain language what you're looking for
    b) Analyze a specific JD       — paste URL or text
    c) Save / update an opportunity — add context or change stage
    d) Record an application outcome — shortlisted / rejected / ghosted
    e) View pipeline               — all tracked opportunities by stage
    f) Probe a company's ATS       — get live job listings for any company
```

---

## Gate 2 — Batch Discovery (mode=a)

### Step 1 — Interpret NL Description

User gives free-form description. Derive these params:

| Signal in description | Derived param |
|---|---|
| Role type / title keywords | `--search-terms` (see mapping table below) |
| Industry / domain | `--sectors` (from user_setup.md target_sectors, or user-specified; default: ALL) |
| "India", "remote", "US open" | `--location` + `--remote` flag |
| "recent", "last week", "today" | `--hours-old` (24 / 72 / 168) |
| "founding", "early-stage", "startup" | hours-old → 168 (founding roles are rare, wider window) |
| Seniority cues ("senior", "lead") | add senior variants to search_terms |

**Search term mapping** (canonical → CLI value):

| User says | `--search-terms` value | `--workday-search` |
|---|---|---|
| founding PM, early-stage PM | founding product manager,chief of staff,ai product manager | product manager |
| AI PM, LLM product, genAI PM | ai product manager,ai builder,llm product | ai product |
| growth PM, growth manager | growth manager,growth product manager,product growth | growth |
| CSM, customer success | customer success manager,implementation manager,solutions architect | customer success |
| PMM, product marketing | product marketing manager,pmm | product marketing |
| TPM, program manager | technical program manager,program manager | program manager |
| chief of staff | chief of staff | chief of staff |
| general PM, product manager | product manager,senior product manager,product owner | product manager |

Default (no role type): use all terms from `DEFAULT_SEARCH_TERMS` in jobspy_scrape.py.

### Step 2 — Confirm Interpretation

Show before running:

```
Interpreted as:
  Search terms   : [list]
  Sectors        : [CONSUMER_AI | ALL | etc.]
  Location       : India (default)
  Remote         : yes / no
  Hours old      : 72 (default) / 168 (founding/rare)
  Workday filter : [term]

Run with these params? (y to confirm, or adjust)
```

Wait for y / adjustment before running.

### Step 3 — Run Scripts

```bash
JOBS_DIR=$(grep -E 'jobs_dir:' ~/.linkright/user_setup.md 2>/dev/null | head -1 | sed 's/.*jobs_dir: *//;s/["\x27]//g;s/ *$//' | sed "s|~|$HOME|g")
JOBS_DIR="${JOBS_DIR:-$HOME/.linkright/jobs}"
cd "$JOBS_DIR"

HUNT_SCRIPTS="$HOME/.claude/skills/linkright-hunt/scripts"

# Tier 2: job boards (LinkedIn guest + Indeed + Google + Naukri)
python3 "$HUNT_SCRIPTS/jobspy_scrape.py" \
  --search-terms "<derived_terms>" \
  --sectors "<derived_sectors>" \
  --location "India" \
  [--remote] \
  --hours-old <derived_hours_old> \
  --results 25

# Tier 1: ATS direct APIs (598 target companies)
python3 "$HUNT_SCRIPTS/scrape_jobs.py" --workday-search "<derived_workday_search>"

# Score new jobs (unscored only)
python3 "$HUNT_SCRIPTS/score_jobs.py" --top 20
```

If any script errors: show the exact error message + continue with remaining scripts. Do NOT abort the full run.

### Step 4 — Present Results

After scoring, query and display top 20:

```bash
JOBS_DIR=$(grep -E 'jobs_dir:' ~/.linkright/user_setup.md 2>/dev/null | head -1 | sed 's/.*jobs_dir: *//;s/["\x27]//g;s/ *$//' | sed "s|~|$HOME|g")
JOBS_DIR="${JOBS_DIR:-$HOME/.linkright/jobs}"
cd "$JOBS_DIR"
sqlite3 db/jobs.db "
  SELECT title, company, location, sector, role_category,
         relevance_score, is_remote, job_url
  FROM jobs
  WHERE is_ghost=0 AND relevance_score IS NOT NULL
  ORDER BY relevance_score DESC
  LIMIT 20
"
```

Display as a clean table. Flag: [R] = remote, sector tag, score.

Then ask: "Want to analyze any of these JDs in depth? (paste number or 'done')"

---

## Gate 3 — JD Analysis (mode=b)

### Step 1 — Get JD

Accept URL or pasted text.
- If URL: use `agent-browser` to fetch the page text (not WebFetch)
- If text: use as-is

### Step 2 — Signal Extraction (inline Claude analysis)

Analyze the JD text against the PM signal taxonomy. Run all 5 steps mentally:

**Step 2a — Archetype Detection**
Which archetype best fits this role?
Options: `growth | 0to1 | enterprise | platform | consumer | data_ai | design_led | marketplace`
Output: primary_archetype, secondary_archetype (if mixed)

**Step 2b — Signal Requirement Extraction**
Against Tier 1 (core PM), Tier 2 (archetype), Tier 3 (domain), Tier 4 (contextual) signals, identify:
- Primary signals: emphasized repeatedly or in JD headline
- Secondary signals: mentioned once, important
- Mentioned signals: present but not core
- Negative signals: role explicitly de-emphasizes these

See `~/.claude/skills/linkright-mem/references/ref_02_signal_taxonomy.md` for full taxonomy (load when available).

**Step 2c — Domain + Context**
- Industry domain: AI / fintech / saas / consumer / gaming / etc.
- Company stage signal: startup / scaleup / enterprise
- Seniority signal: IC / hybrid / manager

**Step 2d — Recruiter Language**
- Extract verbatim phrases that reveal true priorities
- Flag weasel language ("wear many hats", "startup pace" = often unclear ownership)
- Flag red flags ("manage support escalations" in PM role = degraded scope)
- Mirror vocabulary: exact terms to use in resume/cover letter

**Step 2e — Gap Analysis**
Load user's signal strengths from linkright-mem:
```bash
JOBS_DIR=$(python3 -c "
import re, pathlib
f = pathlib.Path.home() / '.linkright/user_setup.md'
m = re.search(r'jobs_dir:\s*[\"\'"]?(.+?)[\"\'"]?\s*$', f.read_text(), re.M) if f.exists() else None
print(m.group(1).strip() if m else str(pathlib.Path.home() / '.linkright/jobs'))
")
python3 ~/.claude/skills/linkright-mem/scripts/grep_memory.py \
  --query "strength:high strength:medium strength:low" \
  --memory ~/.linkright/memory \
  --format json
```
Map each required signal → HIGH/MEDIUM/LOW/UNKNOWN based on returned signals.

### Step 3 — Phase 1 Fit Score

Embed this JD against profile embedding:

```bash
JOBS_DIR=$(grep -E 'jobs_dir:' ~/.linkright/user_setup.md 2>/dev/null | head -1 | sed 's/.*jobs_dir: *//;s/["\x27]//g;s/ *$//' | sed "s|~|$HOME|g")
JOBS_DIR="${JOBS_DIR:-$HOME/.linkright/jobs}"
cd "$JOBS_DIR"
# Insert JD into DB temporarily, score it, show result
python3 -c "
import sqlite3, numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

BASE = Path('.')
db = sqlite3.connect('db/jobs.db')
profile = np.load('db/profile_embedding.npy')
model = SentenceTransformer('all-MiniLM-L6-v2')

jd_text = '''<PASTE JD TEXT HERE — first 2000 chars>'''
vec = model.encode(jd_text, normalize_embeddings=True)
score = float(np.dot(vec, profile) / (np.linalg.norm(vec) * np.linalg.norm(profile))) * 100
print(f'Phase 1 fit score: {score:.1f}/100')
db.close()
"
```

If sentence-transformers unavailable, skip score and note "install sentence-transformers to compute fit score".

### Step 4 — Output

Present in this order:
1. Archetype: [primary] (+ [secondary] if mixed)
2. Fit score: [N]/100 (Phase 1 semantic)
3. Primary signals required: [list with user's strength level: HIGH/MEDIUM/LOW/UNKNOWN]
4. Gap signals: [signals role requires but user is weak on or unknown]
5. Red flags: [any found]
6. Recruiter vocabulary to mirror: [key phrases verbatim]
7. Recommendation: STRONG FIT / GOOD FIT / STRETCH / MISMATCH with 1-sentence reason

### Step 5 — Save to Pipeline

Ask: "Save this to your opportunity pipeline? (y/n)"

On y:

```bash
JOBS_DIR=$(grep -E 'jobs_dir:' ~/.linkright/user_setup.md 2>/dev/null | head -1 | sed 's/.*jobs_dir: *//;s/["\x27]//g;s/ *$//' | sed "s|~|$HOME|g")
JOBS_DIR="${JOBS_DIR:-$HOME/.linkright/jobs}"
mkdir -p "$JOBS_DIR/memory"
```

Write opportunity to `memory/pipeline.json` (append to array or create file):

```json
{
  "id": "OPP_<timestamp>",
  "title": "<title>",
  "company": "<company>",
  "source_url": "<url>",
  "date_seen": "<today>",
  "stage": "saved",
  "fit_score": <score>,
  "shortlist_probability": null,
  "jd_raw": "<full jd text>",
  "jd_analyzed": {
    "archetype": "<archetype>",
    "primary_signals": [],
    "secondary_signals": [],
    "negative_signals": [],
    "red_flags": [],
    "recruiter_language": []
  },
  "manual_signals": [],
  "enrichment_notes": "",
  "applied_date": null,
  "outcome": null,
  "stage_history": [{"stage": "saved", "date": "<today>"}]
}
```

Show confirmation: "Saved as OPP_<id>. Use `/linkright-sync` to tailor resume for this role."

---

## Gate 4 — Record Outcome (mode=d)

Load `memory/pipeline.json`. Show opportunities where `stage` is `applied` and `outcome` is null.

For each, ask outcome:
- `shortlisted` — got a call/screen
- `cleared_stage` — advanced past initial screen
- `offer` — received offer
- `early_reject` — rejected before screen
- `ghosted` — no response after 14 days

Update the opportunity record: `outcome`, `outcome_date`, optional `notes`.

After update:
```
Outcome recorded. [N] total outcomes in model.
Model confidence: [none/low/medium/high based on N: 0-4/5-9/10-14/15+]
```

Note: `shortlist_model.py` not yet built. Outcomes are stored now; model runs when script is built.

---

## Gate 5 — Pipeline View (mode=e)

```bash
JOBS_DIR=$(grep -E 'jobs_dir:' ~/.linkright/user_setup.md 2>/dev/null | head -1 | sed 's/.*jobs_dir: *//;s/["\x27]//g;s/ *$//' | sed "s|~|$HOME|g")
JOBS_DIR="${JOBS_DIR:-$HOME/.linkright/jobs}"
cat "$JOBS_DIR/memory/pipeline.json" 2>/dev/null || echo "Pipeline empty — no opportunities saved yet."
```

Render by stage with days-in-stage. Flag any application >14 days with no outcome.

Stages in order: saved → applied → screening → phone_screen → interview → final → offer / rejected / archived

---

## Gate 6 — ATS Probe (mode=f)

User gives company name. Try common slugs (company name lowercased, dashes for spaces) against ATS APIs:

```bash
python3 -c "
import httpx, json, sys

slug = '<company_slug>'
endpoints = [
    ('greenhouse',      f'https://boards-api.greenhouse.io/v1/boards/{slug}/jobs'),
    ('lever',           f'https://api.lever.co/v0/postings/{slug}?limit=10'),
    ('ashby',           f'https://api.ashbyhq.com/posting-api/job-board/{slug}'),
    ('smartrecruiters', f'https://api.smartrecruiters.com/v1/companies/{slug}/postings?limit=10'),
    ('workable',        f'https://apply.workable.com/api/v3/accounts/{slug}/jobs'),
]

for ats, url in endpoints:
    try:
        r = httpx.get(url, timeout=8)
        if r.status_code == 200:
            print(f'ATS: {ats}  URL: {url}')
            # parse and show PM-relevant jobs
            break
    except Exception as e:
        pass
else:
    print('ATS not detected via standard probes. Try find_career_urls.py for full discovery.')
"
```

Show: ATS type found + list of PM-relevant open roles.

---

## Hard Rules

| Rule | Detail |
|---|---|
| NO LinkedIn account automation | Never use auth LinkedIn API, headless browser with session, or any account-level action |
| NO applying on behalf | Surface and score only — user applies manually |
| NO pipeline write without preview | Always show summary before writing to pipeline.json |
| Sectors filter | loaded from user_setup.md target_sectors (default: ALL) |
| LinkedIn guest OK | `linkedin.com/jobs-guest/` via JobSpy only — stop if rate limited |
| Both scores always separate | Never merge fit + shortlist into one opaque score |
| Full JD preserved | Don't truncate in pipeline.json — linkright-sync needs the full text |
| Shortlist model is a signal | Not a verdict. "20% probability" ≠ "don't apply" |

---

## Phase Status

| Feature | Status |
|---|---|
| Tier 1 ATS scraping (9 ATS types, 598 companies) | ✅ Built — scrape_jobs.py |
| Tier 2 job board (LinkedIn/Indeed/Google/Naukri) | ✅ Built — jobspy_scrape.py |
| Title filtering + sector tagging | ✅ Built — filter_pm_jobs.py |
| Phase 1 semantic fit score (sentence-transformers) | ✅ Built — score_jobs.py |
| Passive browser capture import | ✅ Built — import_browser_csv.py |
| Excel export | ✅ Built — update_excel.py |
| Tier 3 free APIs (Remotive/RemoteOK/YC WaaS) | ✅ tier3_search.py |
| JD signal extraction script | ✅ jd_analyzer.py |
| Phase 2 signal-based fit score | ✅ fit_scorer.py |
| Pipeline CRUD script | ✅ pipeline_update.py |
| Shortlist probability model | ⏳ shortlist_model.py |
| ATS probe script | ⏳ ats_probe.py (Gate 6 uses inline probe until built) |

---

## Cross-Skill Integration

```
linkright-hunt  (this skill)
    │ saves opportunity to memory/pipeline.json
    ▼
linkright-sync  — reads pipeline.json → tailors resume for the role
linkright-interview — reads pipeline.json → builds question bank for the company
linkright-companion — reads pipeline.json → daily briefing on active applications
```
