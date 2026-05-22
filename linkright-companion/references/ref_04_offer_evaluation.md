# ref_04 — Offer Evaluation Framework

## Required Inputs

Before running evaluation, load from user_setup.md:
- `target_ctc_min` — hard floor, non-negotiable
- `target_ctc_target` — aspirational target
- `current_ctc` — baseline for comparison
- `target_role` / `target_archetype`

If any of these fields are missing from user_setup.md, stop and ask before continuing.

---

## CTC Calculation Rules

Total comp = base + (equity vested per year) + target_bonus

### Equity Vesting

- Standard: 4-year vest, 1-year cliff → annualized = total_equity / 4
- Accelerated schedules: use stated schedule, not 4-year
- Unvested equity at current company (golden handcuffs): note separately, don't add to offer

### Bonus

- "Target bonus X%" → use target, not max
- "Discretionary bonus" → do not count. Note it separately.
- Signing bonus → one-time, do not annualize into CTC

---

## Compensation Verdict Labels

| Condition | Verdict |
|---|---|
| Total comp ≥ target_ctc_target | ABOVE TARGET |
| target_ctc_min ≤ total comp < target_ctc_target | WITHIN RANGE |
| total comp < target_ctc_min | BELOW FLOOR |

### BELOW FLOOR Response

Always output:
```
This offer is below your stated minimum of [target_ctc_min].
Do not accept without negotiating first.

Suggested negotiating opening:
  "I'm excited about this opportunity. Based on my research and the scope of the role,
   I was expecting [target_ctc_target or midpoint]. Is there flexibility on [base/equity]?"

If they say no room: "Can we revisit in [90 days] based on performance?"
If still no: walk away or document the decision clearly in the decision journal.
```

---

## Role Fit Analysis

Map offer role to user archetype signals from user_setup.md.

| Fit level | Condition |
|---|---|
| Strong fit | ≥3 of user's top signals required by role |
| Partial fit | 1-2 overlap, rest new territory |
| Weak fit | <1 overlap, role would require building new signals |

Career trajectory:
- **Forward**: role title or scope is a clear step up from current
- **Neutral**: same level/scope, different domain
- **Lateral**: different domain, similar seniority — may be ok if strategic
- **Backward**: lower scope or seniority — document why before accepting

---

## Decision Framework Questions

Always surface all 4. Never skip.

1. Does this role move you toward or away from your target archetype?
2. What signal does taking this role send to your next employer in 2-3 years?
3. What concrete thing would you have to give up to accept? (time, other opps, equity unvested)
4. Would you regret not taking it in 2 years?

Never recommend accepting or rejecting. These questions are for the user to answer.

---

## Pipeline Context Check

Pull from pipeline.json:
- Count of opps currently in `interview_r1` / `interview_r2` / `interview_final`
- Any offers already in `offer_received`
- Any deadline conflicts (other companies with exploding offers)

Output:
```
PIPELINE CONTEXT:
  In-interview now: [N] — [company names]
  Other offers: [none / yes: company name]
  Deadline pressure: [yes/no + note if yes]
```

If deadline pressure exists: "You have [X] days to decide. [Company Y] is in interview R2 — consider requesting an extension."

---

## Full Output Template

```
OFFER EVALUATION — [Company] — [Role]
Date: [YYYY-MM-DD]

COMPENSATION:
  Base:         [amount]
  Equity/yr:    [amount] ([total] over [N]yr vest)
  Bonus (tgt):  [amount]
  Total comp:   [sum]
  ─────────────────────
  Your floor:   [target_ctc_min]
  Your target:  [target_ctc_target]
  Verdict:      [ABOVE TARGET / WITHIN RANGE / BELOW FLOOR]

  [If BELOW FLOOR: negotiation script]

ROLE FIT:
  Archetype match: [strong / partial / weak]
  Top signals required by role: [list]
  Your signal gaps: [list or "none"]
  Career trajectory: [forward / neutral / lateral / backward]

PIPELINE CONTEXT:
  In-interview now: [N] — [companies]
  Other offers: [none / company name]
  Deadline pressure: [none / note]

DECISION FRAMEWORK QUESTIONS:
  1. Does this role move you toward or away from your target archetype?
  2. What signal does taking this role send to your next employer?
  3. What concrete thing would you have to give up to accept?
  4. Would you regret not taking it in 2 years?

This evaluation is analytical input, not a recommendation.
The decision is yours.
```

---

## Negotiation Paths

### Path 1 — Below Floor

Open with target. If rejected:
- Ask for equity top-up (less visible in budget than base)
- Ask for sign-on bonus (one-time, budget-friendly for company)
- Ask for earlier first review + performance bonus trigger
- If all denied: walk away or document decision clearly

### Path 2 — Within Range, Want Target

"I'm very interested. The offer is close to where I need to be. Is there room to get to [target_ctc_target] in base or equity to make this an easy yes?"

### Path 3 — Above Target

No negotiation needed unless terms have unfavorable clauses (non-compete, clawback, cliff mismatch). Review those before accepting.
