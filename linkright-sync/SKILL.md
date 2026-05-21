---
name: linkright-sync
description: |
  Build pixel-perfect, brand-customized, ATS-safe resumes and cover letters tailored
  to a specific job opportunity. Pulls profile from linkright-mem (facts + signals).
  Pulls JD from linkright-hunt pipeline or paste. Two output paths: HTML (Tailwind,
  GitHub Pages) or Overleaf/LaTeX (FAANGPath template, XeLaTeX).

  Use when user says: /linkright-sync, "tailor my resume", "build resume for [company]",
  "optimize my resume", "cover letter", "job application", "I'm applying to [X]",
  "resume for this JD", or any resume/CV creation request.
---

# LinkRight Sync — Resume & Cover Letter

SKILL_DIR  = `~/.claude/skills/linkright-sync`
MEM_DIR    = `~/.linkright/memory`
JOBS_DB    = `~/Downloads/Mission Job Switch/job scraping/db/jobs.db`
PIPELINE   = `~/Downloads/Mission Job Switch/job scraping/memory/pipeline.json`

---

## Absolute Rules (read before every gate)

- ALWAYS ask HTML vs Overleaf as the VERY FIRST question — no exceptions
- ALWAYS generate all content in B&W (Gates 0–5) — colors ONLY at Gate 6
- ALWAYS run width measurement on every bullet — never eyeball
- NEVER set `height: 1.2em; overflow: hidden` on any bullet container
- NEVER use `measure_width.py` on LaTeX — wrong font metrics
- NEVER add `\usepackage{xcolor}` before Gate 6
- NEVER deliver a resume with any Overfull \hbox (LaTeX) or >100% fill (HTML)
- NEVER guess dates, titles, companies — ask if missing
- NEVER repeat the same action verb anywhere in the resume
- NEVER open a cover letter with "I am excited to apply" or "I believe I would be a great fit"
- NEVER deliver below Grade B (quality grade system, Gate 7)
- ALWAYS run constraint validation before delivery

---

## Gate 0 — Format Fork (ALWAYS FIRST)

```
AskUserQuestion:
  question: "Which output format?"
  options:
    A) HTML — browser-rendered, Tailwind CSS, pixel-perfect, GitHub Pages ready
    B) Overleaf/LaTeX — FAANGPath template, XeLaTeX, compiles to PDF
```

Document format choice. All downstream behavior branches from this.

---

## Gate 1 — Input Collection

### JD Source (pick one)
1. **From pipeline** — "Do you have a saved opportunity ID from linkright-hunt?"
   ```bash
   cat "$PIPELINE" 2>/dev/null | python3 -c "
   import json,sys
   data=json.load(sys.stdin)
   opps=data if isinstance(data,list) else data.get('opportunities',[])
   for o in opps:
     print(f\"{o.get('id')} | {o.get('company')} | {o.get('title')} | stage={o.get('stage')}\")
   "
   ```
2. **From jobs.db** — search by company/title
3. **Paste URL** → fetch JD text
4. **Paste text directly**

### Profile Source (v2.1.0 — linkright-mem)
```bash
python3 ~/.claude/skills/linkright-mem/scripts/grep_memory.py \
  --query "strength:high" \
  --memory ~/.linkright/memory \
  --format json
```

If `facts.md` empty → fallback: "Paste your current resume text." (v2.0.0 mode)

If using mem: load signals + supporting facts. Skip raw resume paste entirely.

### Target Archetype
Infer from JD (Gate 2 output) or ask user to confirm.

---

## Gate 2 — JD Analysis

Analyze JD inline (same pipeline as linkright-hunt Gate 3):

**Step 1 — Archetype Detection**
Which PM archetype? `ai_pm | enterprise_pm | growth_pm | platform_pm | consumer_pm | founding_pm | analytics_pm | csm_implementation`

**Step 2 — Signal Extraction**
- Primary signals: emphasized repeatedly or in headline
- Secondary signals: mentioned once
- Negative signals: role explicitly de-emphasizes
- Red flags: "manage support escalations" in PM role, etc.

**Step 3 — Recruiter Vocabulary**
Extract exact phrases to mirror in resume bullets. These are the keywords.

**Step 4 — Career Level Detection**
IC3 / IC4 / IC5 / IC6 / Director — drives section order and bullet depth.

Show analysis to user. Confirm archetype + level before proceeding.

---

## Gate 3 — Signal Coverage Map

Pull profile signals from mem, map against JD requirements:

```bash
python3 ~/.claude/skills/linkright-mem/scripts/consistency_scorer.py \
  --signals ~/.linkright/memory/signals.md \
  --archetype "<detected_archetype>" \
  --format json
```

Show coverage map:
```
SIGNAL COVERAGE MAP — <company> (<archetype>)

JD Primary Signals:
  systems_thinking        → Profile: STRONG (6 facts) ✓
  ai_workflow_design      → Profile: MEDIUM (2 facts) △
  stakeholder_leadership  → Profile: STRONG (5 facts) ✓

JD Secondary Signals:
  data_fluency            → Profile: LOW (1 fact)    ✗ ← gap
  execution_rigor         → Profile: STRONG (3 facts) ✓

GAP SIGNALS: data_fluency
→ "I see data_fluency is required but your profile has only 1 fact.
   Do you have any data-related work I should know about before I write?"
```

User addresses gaps or confirms they don't have them. Proceed only after gap resolution.

Also check vertical space budget:
```bash
python3 ~/.claude/skills/linkright-sync/scripts/validate_page_fit.py  # HTML only
```

---

## Gate 4 — Strategy

Based on archetype + signal map + career level, recommend:

| Strategy | When |
|---|---|
| Signal-Forward | Strong signal match — lead with impact stories |
| Gap-Bridging | 1-2 key gaps — reframe existing facts to address them |
| Narrative-Pivot | Career transition — emphasize transferable signals |
| Depth-First | Senior/Staff — show systems ownership over breadth |
| Breadth-Display | Mid-level generalist — show range across signal tiers |

Show: recommended strategy + BRS scores for candidate bullets from mem.

```bash
python3 ~/.claude/skills/linkright-sync/scripts/score_bullets.py \
  --facts ~/.linkright/memory/facts.md \
  --signals ~/.linkright/memory/signals.md \
  --jd-signals '<primary_signals_json>' \
  --output /tmp/brs_scores.json
```

User approves strategy or overrides.

---

## Gate 5 — Content Generation (B&W Mode)

Generate ALL content before any color. Every pixel utilized. No blank areas.

### Bullet Rules (every bullet, no exceptions)
- Lead with strong specific action verb (never repeated across resume)
- X-Y-Z format: "Accomplished [X] as measured by [Y] by doing [Z]"
- Every claim traceable to a confirmed fact in mem (or user-provided)
- Quantify outcomes — user_estimate is OK, own it
- Mirror recruiter vocabulary from Gate 2
- NO orphaned words: final line ≥3 words
- NO AI-smell phrases (see `references/ref_03_bullet_quality.md`)

### Bullet Grouping (HTML only)
- Splitting: 2→[2], 3→[3], 4→[2+2], 5→[3+2], 6→[3+3]
- Separator: `<li class="bullet-group-spacer" aria-hidden="true"></li>`
- NEVER fewer than 2 or more than 3 per group
- NEVER more than 6 total per company

### Width Loop (runs on EVERY bullet)

**HTML path:**
```bash
python3 ~/.claude/skills/linkright-sync/scripts/measure_width.py '<bullet_text>'
# BULLET_BUDGET = 158.07mm (Roboto 10px, A4)
# Target: 95-100%
# <85%: expand | 95-100%: ship | >100%: trim
# Max 3 attempts, then rewrite from scratch
```

**LaTeX path:**
```
Compile → parse .log
No hbox + badness 0-200: ship
Overfull hbox: trim
Underfull badness 201-1000: expand if possible
Badness >1000: rewrite
Max 3 compile cycles, then rewrite
```

### HTML Section Patterns

**Experience:**
```html
<ul>
  <li><span class="li-content">Bullet with <b>keyword</b> and result.</span></li>
  <li><span class="li-content">Second bullet same group.</span></li>
  <li class="bullet-group-spacer" aria-hidden="true"></li>
  <li><span class="li-content">First bullet second group.</span></li>
</ul>
```

**Contact Bar:**
```html
<span><b>Email:</b> <a href="mailto:x@y.com" style="color:inherit;text-decoration:none;">x@y.com</a></span>
<span><b>LinkedIn:</b> <a href="https://linkedin.com/in/x" style="color:inherit;text-decoration:none;">LinkedIn</a></span>
```

### LaTeX Section Patterns

```latex
\documentclass[a4paper,10pt]{resume}   % ALWAYS a4paper, NEVER letterpaper

\begin{rSection}{EXPERIENCE}
  {\bf Senior Associate PM} \hfill {Jan 2023 -- Present} \\
  {\it American Express} \hfill {\it Gurugram, India}
  \begin{itemize}
    \itemsep -3pt {}
    \item {Bullet with \textbf{keyword} and result.}
  \end{itemize}
\end{rSection}
```

### Page Fit — After Every Company (HTML)
```bash
python3 ~/.claude/skills/linkright-sync/scripts/validate_page_fit.py '<html_so_far>'
# A4 = 271.6mm usable. If overflow: trim lowest-BRS bullet immediately.
```

Show complete resume section by section. User approves or requests edits.

Run constraint validation:
```bash
python3 ~/.claude/skills/linkright-mem/scripts/constraint_checker.py \
  --text '<resume_text>' \
  --constraints ~/.linkright/user_setup.md
```

Block delivery if any violation found.

---

## Gate 6 — Design Application (Color)

**ONLY after Gate 5 is 100% approved.**

### HTML Path
1. Present 4 color swatches (Primary, Secondary, Tertiary, Quaternary) with hex + contrast ratio
2. Wait for explicit user approval
3. Apply CSS variables:
```css
:root {
  --brand-primary-color: #0F766E;
  --brand-secondary-color: #0D9488;
  --brand-tertiary-color: #5EEAD4;
  --brand-quaternary-color: #042F2E;
}
```
4. Add metric emphasis: `<b style="color: var(--brand-primary-color)">↑40%</b>`
5. Validate contrast:
```bash
python3 ~/.claude/skills/linkright-sync/scripts/validate_contrast.py '<hex_color>'
# WCAG AA = 4.5:1 minimum. NEVER deliver failing colors.
```
6. Run ONE final measure_width.py pass — verify widths didn't shift after styling

### LaTeX Path
1. Same color approval step
2. Add to preamble:
```latex
\usepackage{xcolor}
\definecolor{primary}{HTML}{0F766E}
\definecolor{secondary}{HTML}{0D9488}
```
3. Add `\textbf{\textcolor{primary}{↑40\%}}` to all metric segments
4. Recompile — verify no new hbox/vbox from color additions

---

## Gate 7 — Cover Letter (Optional)

Ask: "Want a cover letter for this application?"

If yes:

**Structure (max 300 words):**
1. **Opening** — Why this company, why this role. Must cite something specific: a product, a decision, a challenge. NOT generic.
2. **Evidence** — 2-3 sentences: strongest signals → their stated requirements. Verbatim from recruiter vocabulary.
3. **Ask** — Clear, confident close with specific ask.

**Hard rules:**
- NEVER open with "I am excited to apply" or "I believe I would be a great fit"
- ALWAYS cite something specific about the company (not "I admire your mission")
- ALWAYS mirror 2-3 exact phrases from the JD
- Max 300 words — cut ruthlessly

---

## Gate 8 — Delivery

Run final checklist:

```
[ ] ATS scan: no tables/text boxes/columns that break parsing
[ ] AI-smell scan: no flagged phrases
[ ] One-page confirmed (or senior two-page explicitly approved)
[ ] Constraint validation: zero violations
[ ] Width: all bullets 95-100% (HTML) or badness ≤200 (LaTeX)
[ ] Identity consistency: signals match target archetype
[ ] Verb dedup: zero repeated action verbs
[ ] Color contrast: WCAG AA (HTML)
```

**Quality Grade:**
| Check | Weight |
|---|---|
| Keyword Coverage | 30% |
| Width Fill | 25% |
| Verb Dedup | 15% |
| Page Fit | 15% |
| Color Contrast | 10% |
| ATS Compliance | 5% |

Grade A ≥ 90. NEVER deliver below Grade B (≥75).

**Output files:**
- HTML: `resume_<company-slug>_<YYYYMMDD>.html`
- LaTeX: `resume_<company-slug>_<YYYYMMDD>.tex`

**Save to pipeline:**
```bash
# Update opportunity stage in pipeline.json
python3 -c "
import json
from pathlib import Path
from datetime import datetime

p = Path('$PIPELINE')
data = json.loads(p.read_text()) if p.exists() else {'opportunities': []}
opps = data if isinstance(data, list) else data.get('opportunities', [])
for o in opps:
    if o.get('id') == '<OPP_ID>':
        o['stage'] = 'applied'
        o['resume_version'] = 'resume_<company-slug>_<YYYYMMDD>.html'
        o['stage_history'].append({'stage': 'applied', 'date': str(datetime.now().date())})
p.write_text(json.dumps(data, indent=2))
print('Pipeline updated.')
"
```

**PDF export (HTML path):**
> Chrome → ⌘P → Save as PDF → Background graphics: ON → Margins: None

---

## Scripts Reference

| Script | Purpose | Gate |
|---|---|---|
| `measure_width.py` | HTML bullet width vs 158.07mm budget | 5 (every bullet) |
| `score_bullets.py` | BRS scoring of candidate facts | 4 |
| `validate_contrast.py` | WCAG AA color contrast | 6 |
| `validate_page_fit.py` | A4 vertical budget check (HTML) | 5 (after each company) |
| `suggest_synonyms.py` | Width-calibrated word swaps | 5 (trimming) |
| `assemble_html.py` | Final HTML from template | 8 |
| `ai_smell_checker.py` | Flag AI-generated phrases | 8 |
| `ats_scanner.py` | ATS-hostile formatting check | 8 |

Template: `assets/template.html`

---

## Phase Status

| Feature | Status |
|---|---|
| 7-gate pipeline | ✅ This SKILL.md |
| HTML path (full) | ✅ |
| LaTeX/Overleaf path (full) | ✅ |
| Cover letter (Gate 7) | ✅ |
| linkright-mem integration (Gate 1+3) | ✅ — falls back to paste if mem empty |
| linkright-hunt pipeline.json integration | ✅ |
| `measure_width.py` | ⏳ copy from skill-updates/sync/ |
| `score_bullets.py` | ⏳ |
| `validate_contrast.py` | ⏳ |
| `validate_page_fit.py` | ⏳ |
| `ref_03_bullet_quality.md` (banned phrases) | ⏳ |
| `constraint_checker.py` from linkright-mem | ✅ shared |
