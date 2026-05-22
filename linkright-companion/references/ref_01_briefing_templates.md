# ref_01 — Briefing Templates

## Morning Brief Format

```
LINKRIGHT DAILY BRIEF — [YYYY-MM-DD]

PIPELINE:
  Applied (awaiting):   [N] — [company1, company2, ...]
  In progress:          [N] — [company | stage | Xd elapsed]
  Overdue follow-up:    [N] — [company names] ← URGENT if >14d

TOP 3 ACTIONS TODAY:
  1. [Specific, immediately actionable]
  2. [Specific, immediately actionable]
  3. [Specific, immediately actionable]

OPTIONAL (if energy allows):
  [Lower-leverage item]

GOAL PROGRESS:
  [Goal from user_setup.md] — [Xd elapsed / Yd to deadline]
  Status: [on track / borderline / behind]
```

### Action Priority Rules

1. **Interview prep** → always #1 if interview within 7 days
2. **Overdue follow-up** → #2 if company >14d no response
3. **Active pipeline tasks** → resume to tailor, cover letter due, application deadline today
4. **Content / networking** → only if no urgent pipeline item

Never output more than 3 "highest leverage" items. Never a 10-item list.

### Pipeline Stage Labels

Use exact labels from pipeline.json `stage` field:
- `applied` — submitted, awaiting response
- `phone_screen` — scheduled or completed
- `interview_r1` / `interview_r2` / `interview_final`
- `offer_received` — offer extended
- `rejected` / `ghosted` — closed

### Follow-up Urgency Thresholds

| Days since last activity | Flag |
|---|---|
| 8-13d | (none) |
| 14-20d | Overdue |
| 21d+ | CRITICAL — add to action #1 or #2 |

---

## Weekly Review Format

```
WEEKLY REVIEW — [Mon YYYY-MM-DD] to [Sun YYYY-MM-DD]

ACTIVITY:
  Applications:       [N]
  Interviews/calls:   [N] — [company names]
  Outcomes recorded:  [N]
  Posts published:    [N]
  Cold emails sent:   [N]
  New opps found:     [N]

PIPELINE:
  [stage label]: [count]
  [stage label]: [count]

WHAT WORKED:
  [1-2 specific observations from this week]

WHAT TO IMPROVE:
  [1-2 specific, actionable gaps — never "apply to more jobs"]

SHORTLIST MODEL:
  [N] total outcomes — confidence: [none/low/medium/high]
  [If new outcomes this week]: "Added [N] data points."

NEXT WEEK FOCUS:
  1. [Specific priority]
  2. [Specific priority]
  3. [Specific priority]
```

### Confidence Scale for Shortlist Model

| Total outcomes | Confidence |
|---|---|
| 0-4 | none |
| 5-9 | low |
| 10-19 | medium |
| 20+ | high |

### "What to Improve" Rules

- Must be specific and actionable
- NEVER output: "apply to more jobs", "be more proactive", "network more"
- Example good: "3 applications this week had no cover letter — add a 3-sentence note to every app"
- Example good: "2 follow-ups overdue >14d — set calendar reminders day 7 and day 14"

---

## Goal Progress Format

```
GOAL PROGRESS — [YYYY-MM-DD]

Target: receive offer ≥ [target_ctc_target] at [archetype] role by [target_date]
Days elapsed:   [N]
Days remaining: [N]

CHECKPOINTS:
  [✓/✗] Memory built (facts: N, signals: N)
  [✓/✗] Pipeline populated (N active opps, target: 10+)
  [✓/✗] 3+ companies in interview simultaneously — currently: N
  [✓/✗] Offer received
  [✓/✗] Offer meets CTC floor

ON TRACK: [on track / borderline / behind]
Key risk: [one sentence]
```

### On-Track Heuristics

- **On track**: 3+ active interviews OR offer in hand
- **Borderline**: Pipeline exists (5-9 opps) but no interviews yet after 4+ weeks
- **Behind**: Pipeline <5 opps, 0 interviews after 3+ weeks, or deadline <30d with no offer
