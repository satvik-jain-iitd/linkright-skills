---
name: linkright-companion
description: |
  Daily operating layer for LinkRight — synthesizes pipeline, memory, and outcomes into
  situational awareness and prioritized action. Six modules: Morning Briefing (top 3
  actionable priorities, pipeline status, goal progress), Weekly Review (activity summary,
  pattern analysis, next week focus), Decision Journal (log decisions with key assumption +
  review date — surfaces on schedule), Rejection Analysis (probabilistic cause, confounders,
  model update routing), Offer Evaluation (auto-runs compensation check against user_setup.md,
  pipeline context, decision framework questions), Diary Ingestion (free-text reflection →
  extract fact/signal/story candidates → route to linkright-mem after confirmation).
  Needs data from all other skills to be meaningful — build last.

  Use when user says: /linkright-companion, "morning briefing", "daily brief", "weekly review",
  "log a decision", "rejected by", "got an offer", "analyze rejection", "diary entry",
  "how is my job search going", "what should I do today", or any daily review/tracking request.
---

# LinkRight Companion

SKILL_DIR   = `~/.claude/skills/linkright-companion`
SETUP       = `~/.linkright/user_setup.md`
MEM_DIR     = `~/.linkright/memory`
PIPELINE    = `~/.linkright/jobs/memory/pipeline.json`
DECISIONS   = `~/.linkright/memory/decisions/decision_log.md`

---

## Absolute Rules

- ALWAYS load user_setup.md before any compensation evaluation — never hardcode numbers
- ALWAYS flag if pipeline has fewer than 5 active opportunities — danger zone
- ALWAYS surface decision journal entries on their stated review date
- NEVER interpret a rejection as definitive — always list confounders
- NEVER route diary entries to memory without user confirmation
- NEVER recommend accepting an offer without checking target_ctc_min first
- ALWAYS run compensation check automatically on offer evaluation — user shouldn't need to ask
- Max 3 "highest leverage" actions in morning briefing — never a 10-item list

---

## Gate 0 — Load State (all modes)

```bash
# Pipeline
cat "$PIPELINE" 2>/dev/null | python3 -c "
import json,sys
data=json.load(sys.stdin)
opps=data if isinstance(data,list) else data.get('opportunities',[])
for o in opps: print(o.get('stage','?'),'|',o.get('company','?'),'|',o.get('title','?'))
" 2>/dev/null || echo "pipeline not found"

# Memory summary
python3 ~/.claude/skills/linkright-mem/scripts/grep_memory.py \
  --memory ~/.linkright/memory 2>/dev/null || echo "memory empty"

# Pending decision reviews
python3 ~/.claude/skills/linkright-companion/scripts/decision_log.py \
  --due-today --log ~/.linkright/memory/decisions/decision_log.md 2>/dev/null || true
```

---

## Gate 1 — Mode Selection

```
AskUserQuestion:
  question: "What do you need today?"
  options:
    A) Morning briefing — pipeline status + top 3 priorities
    B) Weekly review — activity summary + patterns + next week focus
    C) Log a decision — record with key assumption + review date
    D) Rejection / ghosting analysis — what likely happened + confounder list
    E) Offer evaluation — compensation check + pipeline context + decision questions
    F) Diary entry — reflection → extract facts/signals/stories
    G) Goal progress check — where you stand vs target + checkpoints
    H) Decision review — surface entries due for review
```

---

## Module A — Morning Briefing

```bash
python3 ~/.claude/skills/linkright-companion/scripts/morning_briefing.py \
  --pipeline "$PIPELINE" \
  --setup "$SETUP" \
  --decisions "$DECISIONS"
```

Output format:
```
LINKRIGHT DAILY BRIEF — [date]

PIPELINE:
  Applied (awaiting): [N] — [company names]
  In progress: [N] — [company | stage | days elapsed]
  Overdue follow-up (>14d): [N] — [names] ← URGENT

TOP 3 ACTIONS TODAY:
  1. [Specific, immediately actionable — e.g., "Tailor resume for Figma PM JD (interview next week)"]
  2. [e.g., "Follow up with Anthropic — 16 days since application, no response"]
  3. [e.g., "Add diary entry from yesterday's stakeholder review"]

OPTIONAL (if energy allows):
  [Lower leverage item]

GOAL PROGRESS:
  [Goal from setup] — [days elapsed / days to deadline]
  Status: [on track / borderline / behind]
```

Priority rules for action ranking:
1. Interview prep (if interview within 7 days) → always #1
2. Overdue follow-ups (>14 days no response) → #2
3. Active pipeline actions (resume to tailor, cover letter due) → #3
4. Content/networking (post to publish before company interview) → optional

---

## Module B — Weekly Review

Ask: "What week are you reviewing? What activities happened this week?"
User provides activity counts (or script reads from outcomes.json if populated).

Output:
```
WEEKLY REVIEW — [date range]

ACTIVITY:
  Applications:       [N]
  Interviews/calls:   [N] — [which companies]
  Outcomes recorded:  [N]
  Posts published:    [N]
  Cold emails sent:   [N]
  New opps found:     [N]

PIPELINE:
  [stage: count] for each stage

WHAT WORKED: [1-2 specific things from this week's activity]

WHAT TO IMPROVE: [1-2 specific, actionable gaps — not "apply to more jobs"]

SHORTLIST MODEL:
  [N] total outcomes — confidence: [none/low/medium/high]
  [If new outcomes: "This week added [N] data points. Model updated."]

NEXT WEEK FOCUS:
  1. [Specific priority]
  2. [Specific priority]
  3. [Specific priority]
```

---

## Module C — Decision Journal

Ask: "What's the decision? Give me context."

Record:
```bash
python3 ~/.claude/skills/linkright-companion/scripts/decision_log.py \
  --write \
  --title '<brief title>' \
  --context '<situation>' \
  --chosen '<what you chose>' \
  --reasoning '<why>' \
  --assumption '<key assumption>' \
  --review-days 14 \
  --log ~/.linkright/memory/decisions/decision_log.md
```

Every entry includes:
- Decision title
- Date + context
- Options considered (at least 2 — user provides)
- Chosen option + reasoning
- **Key assumption:** what would have to be true for this to be the right call
- **Review date:** +14 days by default, adjustable

On review date: surface entry → "Does the key assumption still hold?"

---

## Module D — Rejection / Ghosting Analysis

Inputs: company, role, stage where it failed (no response / early screen reject / post-interview reject).

Output:
```
OUTCOME ANALYSIS — [Company] — [Role]
Outcome: [Ghosted / Early Reject / Post-Interview Reject]
Stage: [where it ended]

LIKELY CAUSE (probabilistic):
  [Based on JD signal analysis vs profile signals]
  e.g. "JD emphasized growth_experimentation as primary signal (weight 1.0).
        Your profile has this at LOW strength.
        Plausible fit gap — not definitive."

CONFOUNDERS (factors we cannot control):
  - Internal candidate preference
  - Hiring freeze / headcount cut
  - Timing vs other candidates
  - ATS keyword filter before human review
  - Role requirements changed after posting

PATTERN CHECK:
  "This is rejection [N] at similar stage. [Pattern note if N≥3]."

MEMORY UPDATE OFFER:
  "Record this outcome to update the shortlist model? (y/n)"
  → If yes: routes to linkright-hunt outcomes tracking

ACTION ITEM: [0 or 1 specific action — not a 5-point plan]
```

Rules:
- Never assign definitive blame
- Always list confounders — rejection has many causes
- Analytical framing only — no emotional amplification

---

## Module E — Offer Evaluation

Inputs: company, role, compensation breakdown (base + equity + bonus).
Load from SETUP: `target_ctc_min`, `target_ctc_target`, `current_ctc`.

Output:
```
OFFER EVALUATION — [Company] — [Role]

COMPENSATION:
  Offered:  [base + equity + bonus] = [total comp estimate]
  Floor:    [target_ctc_min from setup]
  Target:   [target_ctc_target from setup]
  Verdict:  [ABOVE TARGET / WITHIN RANGE / BELOW FLOOR]

  [If below floor]:
  "This is below your stated minimum. Negotiate before any decision."
  "Suggested opening: [pull from linkright-interview salary script]"

ROLE FIT:
  [Match signals covered vs archetype requirements]
  Career trajectory: [forward / neutral / lateral / backward]

PIPELINE CONTEXT:
  Active opportunities: [N]
  In-interview: [list]
  Decision urgency: [any deadline conflicts?]

DECISION FRAMEWORK QUESTIONS:
  1. Does this role move you toward or away from your target archetype?
  2. What signal does taking this role send to your next employer?
  3. What would you have to give up to accept?
  4. Would you regret not taking it in 2 years?

This evaluation is analytical input, not a recommendation.
The decision is yours.
```

NEVER recommend accepting or rejecting. Provide analysis, not advice.

---

## Module F — Diary Ingestion

User pastes free-text reflection (any length, any style).

```bash
python3 ~/.claude/skills/linkright-companion/scripts/diary_ingest.py \
  --text '<reflection text>'
```

Extracts and shows candidates:
```
DIARY EXTRACTION — [date]

FACT CANDIDATES:
  → "Led quarterly roadmap review with 4 VP-level stakeholders"
     Confidence: HIGH (specific, verifiable, role-appropriate)

SIGNAL EVIDENCE:
  → stakeholder_leadership (3 signals from this entry)
  → real-time decision-making under pressure

INTERVIEW STORY CANDIDATE:
  → "Scope cuts under executive pressure — story type: stakeholder_conflict"

ROUTING:
  [ ] Send fact candidates to linkright-mem? (y/n)
  [ ] Send story candidate to linkright-interview? (y/n)

Nothing persists until you confirm.
```

Also write reflection to `~/.linkright/memory/diary/YYYY-MM-DD.md` (raw, always — no confirmation needed for the diary itself, only for extracted memory updates).

---

## Module G — Goal Progress

Read SETUP goals section + pipeline data. Output:

```
GOAL PROGRESS — [date]

Target: [receive offer ≥ target_ctc at archetype role by target_date]
Days elapsed: [N]  Days remaining: [N]

CHECKPOINTS:
  ✓ Memory built (facts: N, signals: N)
  ✓ Pipeline populated (N active opps)
  ✗ 3+ companies in interview simultaneously — currently: N  [BEHIND]
  ✗ Offer received — none yet
  ✗ Offer meets CTC floor

ON TRACK: borderline
Key risk: Low interview-stage density. Increase application rate or improve response rate.
```

---

## Module H — Decision Reviews Due

```bash
python3 ~/.claude/skills/linkright-companion/scripts/decision_log.py \
  --due-today \
  --log ~/.linkright/memory/decisions/decision_log.md
```

For each due entry, show:
- Original decision + key assumption
- "Does the key assumption still hold? (y/n/partially)"
- If not: "What changed? Log an update."

---

## Scripts Reference

| Script | Purpose |
|---|---|
| `scripts/morning_briefing.py` | Generate morning brief from pipeline + setup |
| `scripts/decision_log.py` | Read/write decision journal entries |
| `scripts/diary_ingest.py` | Extract fact/signal/story candidates from reflection text |

---

## Phase Status

| Feature | Status |
|---|---|
| SKILL.md (orchestrator) | ✅ |
| morning_briefing.py | ✅ |
| decision_log.py | ✅ |
| diary_ingest.py | ✅ |
| All 6 modules | ✅ |
| ref_01_briefing_templates.md | ✅ |
| ref_02_decision_journal.md | ✅ |
| ref_03_rejection_framework.md | ✅ |
| ref_04_offer_evaluation.md | ✅ |
