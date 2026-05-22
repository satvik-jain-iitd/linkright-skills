# ref_02 — Decision Journal

## Entry Format

```markdown
---
id: dec_YYYY-MM-DD_NNN
date: YYYY-MM-DD
title: [Short descriptive title]
context: |
  [What was the situation? What prompted this decision?]
options_considered:
  - [Option A]
  - [Option B]
  - [Option C if applicable]
chosen: [Which option was selected]
reasoning: |
  [Why this option over the others]
key_assumption: |
  [What must be true for this to be the right call?]
review_date: YYYY-MM-DD
reviewed: false
---
```

## Entry Examples

```markdown
---
id: dec_2026-03-15_001
date: 2026-03-15
title: Apply to Series B startup vs FAANG PM role
context: |
  Two applications ready. Limited time this week. Had to prioritize one to tailor properly.
options_considered:
  - Apply to Stripe (FAANG-adjacent, high bar, needs 2h tailoring)
  - Apply to Figma Series B role (archetype match, lower competition)
chosen: Figma Series B
reasoning: |
  Archetype match higher at Figma. Stripe PM role required 3+ years growth experimentation
  signal which is currently LOW in profile. Better ROI to tailor Figma application.
key_assumption: |
  Figma Series B role is still open and not already in late-stage hiring for internal candidate.
review_date: 2026-03-29
reviewed: false
---
```

## Review Prompt (surfaces on review_date)

```
DECISION REVIEW — [title]
Date decided: [date] | Review date: today

Original key assumption:
  "[key_assumption]"

Does this assumption still hold? (y / n / partially)

→ If no/partially: What changed? Log an update.
→ If yes: No action needed. Mark reviewed.
```

## Decision Categories

Tag decisions to spot patterns:

| Tag | Example |
|---|---|
| `application_prioritization` | Which roles to apply to this week |
| `tailoring_investment` | How much time to spend customizing |
| `offer_decision` | Accept / negotiate / decline |
| `pipeline_management` | When to drop a stalled opportunity |
| `networking_bet` | Which relationship to invest in |
| `skill_investment` | Which gap to close this quarter |

## Review Cadence Rules

- Default review: +14 days from decision date
- Offer decisions: review in 7 days if still in negotiation
- Application prioritization: review after outcome known (or 30d max)
- Skill investment: review +90 days

## Review Log Append Format

When a reviewed decision has an update, append:

```markdown
review_YYYY-MM-DD: |
  Assumption held/broke. [What actually happened.]
  [Updated reasoning if behavior changes going forward.]
```
