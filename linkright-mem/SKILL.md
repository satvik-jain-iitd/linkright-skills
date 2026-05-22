---
name: linkright-mem
description: |
  LinkRight's memory and profile intelligence engine. Ingests career material (resume,
  LinkedIn, diary, notes), extracts confirmed facts, derives professional signals, and
  maintains the canonical 5-layer memory graph. All other LinkRight skills draw from
  this memory — without it they work from raw paste every time.

  Use when user says: /linkright-mem, "update my profile", "ingest my resume",
  "add to memory", "what signals do I have", "consistency score", "onboard",
  "search my profile", "add a new fact", "edit a fact", "I joined X", "diary entry",
  "weekly reflection", "what does my profile say about", or any profile/memory update.
---

# LinkRight Memory

MEMORY_DIR = `~/.linkright/memory`
SKILL_DIR  = `~/.claude/skills/linkright-mem`

---

## Core Rules

1. NEVER write to `facts.md` or `signals.md` without explicit user confirmation
2. NEVER delete a fact — only mark `stale: true` (preserve history)
3. NEVER let a signal exist with 0 supporting facts
4. ALWAYS show diff before any write
5. ALWAYS tag every write: timestamp + source document
6. ALWAYS surface conflicts — never silently overwrite
7. NEVER generate resume bullets or stories here — that's linkright-sync/interview/portfolio
8. One fact = one specific, grounded claim. No superlatives. No vague generalizations.

---

## Gate 1 — Intent Detection

If invoked with clear intent (e.g., `/linkright-mem ingest`, `/linkright-mem search X`), go directly to that gate.

Otherwise check: does `~/.linkright/memory/facts.md` exist and have content?
- No → **go to Gate 2 (Onboard)**
- Yes → ask:

```
Use AskUserQuestion:
  question: "What do you want to do?"
  options:
    a) Ingest new material   — resume, LinkedIn, diary, notes
    b) Search memory         — find facts/signals by query
    c) Review profile state  — fact count, signal strengths, consistency score
    d) Audit                 — stale facts, weak signals, archetype gaps
    e) Edit a fact or signal — correct something wrong
    f) Add diary entry       — reflect on recent work
    g) Version snapshot      — tag current memory state
```

---

## Gate 2 — Onboard (first-time setup)

```bash
ls ~/.linkright/memory/facts.md 2>/dev/null || echo "MISSING"
```

If missing, run first-time setup:

1. Check for user_setup.md:
```bash
ls ~/.linkright/user_setup.md 2>/dev/null || echo "MISSING"
```

2. If missing — ask user:
```
I need a few things to set up your profile:
1. Paste your resume text (or give file path)
2. What roles are you targeting? (e.g. "Senior Engineer at fintech startups" or "PM at Series B consumer apps")
3. What sectors/industries? (e.g. FINTECH, CONSUMER_AI, ALL)
4. Anything you never want mentioned? (companies, projects, anything off-limits)
```

Then create `~/.linkright/user_setup.md` from the answers using this schema:

```yaml
# ~/.linkright/user_setup.md
user:
  name: ""
  email: ""
  current_title: ""          # e.g. "Senior PM", "Staff Engineer", "Data Scientist"
  current_company: ""
  years_experience: 0
  current_ctc: ""            # format: "X LPA" or "$Xk/yr"

target:
  roles: []                  # e.g. ["PM", "Engineering Manager", "Data Scientist"]
  sectors: []                # e.g. ["FINTECH", "CONSUMER_AI", "ALL"] — drives hunt sector filter
  locations: []              # e.g. ["India", "Remote"]
  target_ctc_min: ""
  target_ctc_target: ""

paths:
  jobs_dir: "~/.linkright/jobs"    # all hunt + sync scripts use this

constraints:
  hard_constraints: []       # e.g. ["no relocate", "no night shifts"]
  do_not_mention: []         # companies, projects, people — never surface in any output
  topics_to_avoid_in_posts: []
  companies_not_to_comment_on: []
```

3. If found — load it, proceed with ingestion of resume mentioned inside.

4. Run ingestion (Gate 3) on the provided resume.

5. After facts confirmed, derive signals (Gate 3, Step 5).

6. Compute first consistency score for stated target role.

7. Create initial memory files:
```bash
python3 ~/.claude/skills/linkright-mem/scripts/init_memory.py ~/.linkright/memory
```

8. Output:
```
Memory initialized.
  Facts confirmed : [N]
  Signals derived : [N]
  Memory path     : ~/.linkright/memory/

Run /linkright-sync to generate your first tailored resume.
```

---

## Gate 3 — Ingest New Material

### Step 1 — Detect format

Accept: resume text/PDF path, LinkedIn export JSON path, plain text, diary/reflection text.

```bash
# If PDF path given:
python3 ~/.claude/skills/linkright-mem/scripts/fact_extractor.py \
  --input "<path_or_text>" \
  --format auto \
  --output /tmp/linkright_candidate_facts.json
```

If script unavailable or input is pasted text: extract inline (Step 2).

### Step 2 — Extract candidate facts (inline)

For each role/achievement block in the input:
- Extract one fact per specific, grounded claim
- Strip superlatives ("exceptional", "outstanding", "key")
- Keep metrics as-is but flag as `confidence: user_estimate`
- Format per schema:

```yaml
id: FACT_<NNN>          # next available number from facts.md
text: "<terse, specific claim>"
role: "<job title, company>"
period: "<year or year range>"
evidence_refs:
  - "<source doc>:<approximate location>"
confidence: confirmed    # start as 'confirmed' if user provides it directly
signals_derived: []      # filled after signal derivation
last_updated: "<today>"
```

Show facts in batches of 5-8. For each batch:
```
Here are candidate facts from [source]:

FACT_001: "Led cross-functional onboarding redesign for enterprise clients"
FACT_002: "Reduced time-to-first-value from 14 days to 6 days"
FACT_003: "Managed stakeholder alignment across engineering, support, success"

[c]onfirm all  [e]dit one  [r]eject one  [s]kip batch
```

Only confirmed facts proceed to Step 3.

### Step 3 — Conflict detection

```bash
python3 ~/.claude/skills/linkright-mem/scripts/fact_extractor.py \
  --mode conflicts \
  --new-facts /tmp/linkright_candidate_facts.json \
  --existing ~/.linkright/memory/facts.md
```

If conflicts found — surface BOTH versions:
```
CONFLICT DETECTED:
  Existing: "Reduced onboarding from 14 to 6 days (FACT_023)"
  New:      "Reduced onboarding from 14 to 4 days"
  Source:   new resume v3

Which is correct? (keep existing / use new / keep both as separate facts)
```

Never resolve silently.

### Step 4 — Write confirmed facts

```bash
python3 ~/.claude/skills/linkright-mem/scripts/fact_extractor.py \
  --mode write \
  --confirmed /tmp/linkright_confirmed_facts.json \
  --memory ~/.linkright/memory/facts.md
```

Show diff before writing. Confirm. Then write.

### Step 5 — Signal derivation

```bash
python3 ~/.claude/skills/linkright-mem/scripts/signal_deriver.py \
  --facts ~/.linkright/memory/facts.md \
  --existing-signals ~/.linkright/memory/signals.md \
  --output /tmp/linkright_candidate_signals.json
```

Show candidate signals to user:
```
From these new facts, I derived these signals:

SIG_XXX: systems_thinking
  Supported by: FACT_001 + FACT_007 + FACT_012
  "You redesigned interconnected workflows across multiple teams with
   measurable outcome. This is a clear systems_thinking signal."
  Strength: high

Confirm? [y/n/edit]
```

Write only confirmed signals.

---

## Gate 4 — Search Memory

Accept free-text query. Run multi-query search:

```bash
python3 ~/.claude/skills/linkright-mem/scripts/grep_memory.py \
  --query "<user query>" \
  --memory ~/.linkright/memory \
  --top 10
```

Return ranked results: matching facts + signals + any cached expressions.

Format:
```
FACTS matching "stakeholder alignment":
  FACT_003: "Managed alignment across engineering, support, success" (role: [TITLE] @ [CURRENT_COMPANY], 2023) — signal: stakeholder_leadership
  FACT_019: "Presented roadmap to 40+ ministry stakeholders" (role: [TITLE] @ [PREVIOUS_PROJECT], 2023)

SIGNALS with strength ≥ medium:
  stakeholder_leadership (high) — 4 supporting facts
```

---

## Gate 5 — Review Profile State

```bash
python3 ~/.claude/skills/linkright-mem/scripts/consistency_scorer.py \
  --signals ~/.linkright/memory/signals.md \
  --facts ~/.linkright/memory/facts.md \
  --memory ~/.linkright/memory
```

Show:
```
PROFILE STATE
  Facts      : [N] confirmed, [N] stale, [N] user_estimate
  Signals    : [N] total — [N] high, [N] medium, [N] low
  Evidence   : [N] source documents ingested

CONSISTENCY SCORES (by target archetype):
  ai_enterprise_pm     : 78%  (3/5 fully met, 1 partial, 1 missing)
  growth_pm            : 45%  (2/5 met, 1 partial, 2 missing)
  founding_pm          : 61%  (3/5 met, 1 partial, 1 missing)

TOP SIGNALS:
  systems_thinking           — high  (6 facts)
  stakeholder_leadership     — high  (5 facts)
  enterprise_workflow_ownership — high (4 facts)
  ambiguity_handling         — medium (3 facts)

GAP SIGNALS (for ai_enterprise_pm):
  data_fluency       — LOW (only 1 fact)
  ai_native_tooling  — MEDIUM (can strengthen)
```

---

## Gate 6 — Audit

Run stale + weak signal detection:

```bash
python3 ~/.claude/skills/linkright-mem/scripts/stale_detector.py \
  --memory ~/.linkright/memory \
  --stale-days 180
```

Show:
- Facts not updated in >6 months → "Still accurate?"
- Signals with <2 supporting facts → "Needs more evidence or remove?"
- Archetypes with consistency <50% → "Gap worth addressing?"

---

## Gate 7 — Diary / Reflection Ingestion

Accept free-text work reflection. Extract:
1. New fact candidates (specific claims with date)
2. Signal evidence additions (which existing signals this supports)
3. Potential interview story flag (if a clear challenge→action→result emerges)
4. Learning/pattern note (personal, not for outputs)

Show extracted items. User confirms. Write to facts.md + signals.md.

If interview story detected:
```
This reflection contains a strong interview story candidate:
  Challenge: [X]
  Action: [Y]
  Result: [Z]

Save to story bank? (linkright-interview will use this)
```

If yes → save to `~/.linkright/memory/expressions/stories/<date>_<slug>.md`

---

## Gate 8 — Edit Fact or Signal

1. Ask: which fact or signal? (ID or search by text)
2. Show current value + all evidence_refs
3. Show downstream impact: which signals/expressions reference this fact
4. Show proposed edit
5. Confirm
6. Write with `last_updated` + `edited_from` reference

---

## Gate 9 — Version Snapshot

```bash
cp -r ~/.linkright/memory ~/.linkright/memory_snapshots/snapshot_$(date +%Y%m%d_%H%M%S)
echo "Snapshot saved."
```

---

## Phase Status

| Feature | Status |
|---|---|
| facts.md + signals.md schema | ✅ Defined |
| Memory directory structure | ✅ Created |
| Gate 1-9 orchestration | ✅ This SKILL.md |
| `fact_extractor.py` | ✅ Built |
| `signal_deriver.py` | ✅ Built |
| `consistency_scorer.py` | ✅ Built |
| `grep_memory.py` | ✅ Built |
| `stale_detector.py` | ✅ Built |
| `init_memory.py` | ✅ Built |
| `ref_01_ingestion_rules.md` | ⏳ Load inline until built |
| `ref_02_signal_taxonomy.md` | ⏳ Shared with linkright-hunt |
| `ref_03_archetype_requirements.md` | ⏳ Used inline by consistency_scorer |
| sqlite-vec embeddings (>200 facts) | ⏳ Phase 2 |

---

## Cross-Skill API

When other skills call `linkright-mem`:

```bash
# Get signals for archetype
python3 ~/.claude/skills/linkright-mem/scripts/grep_memory.py \
  --archetype "ai_enterprise_pm" \
  --memory ~/.linkright/memory \
  --format json

# Get facts supporting a signal
python3 ~/.claude/skills/linkright-mem/scripts/grep_memory.py \
  --signal "systems_thinking" \
  --memory ~/.linkright/memory \
  --format json

# Get all high-strength signals
python3 ~/.claude/skills/linkright-mem/scripts/grep_memory.py \
  --query "strength:high" \
  --memory ~/.linkright/memory \
  --format json
```

Returns JSON — skills parse and use without loading full memory context.
