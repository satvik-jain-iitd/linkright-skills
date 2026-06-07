# Yellow Tier Nudge Prompt Template

Fires when: `phase_budget < elapsed ≤ phase_budget + 60s`

Sage delivers a gentle wrap nudge appended to next response.

---

## Template Variants

### Variant 1 (formal Hindi-mix)
```
[Sage's eval + pushback if user replied]

⏱  YELLOW tier — 1 min left on this phase. Last sentence?

╭─────────────────────────────────────────────────────────────────╮
│  ⏱  Elapsed: {{elapsed_human}} / {{budget_human}}                │
│  ⏱  Status:  🟡 YELLOW (wrap up)                                 │
╰─────────────────────────────────────────────────────────────────╯
```

### Variant 2 (casual Hindi-mix)
```
[Sage's eval]

Phase budget ka edge aa gaya — 30 seconds aur. Final thought.

╭─ Status: 🟡 YELLOW ─╮
```

### Variant 3 (terse)
```
{{eval if any}}

Wrap karo — 30s. Last point.

🟡 YELLOW · {{elapsed_human}}
```

---

## Selection Heuristic

Pick variant based on phase intensity:

- **Round 1 (HR)** — Variant 1 (formal)
- **Round 2 (Behavioral)** — Variant 2 (casual)
- **Round 4 (Product Sense)** — Variant 2
- **Round 6 (System Design)** — Variant 1 (formal, structured)
- **Round 7 (Bar Raiser)** — Variant 3 (terse, time-pressure)

---

## State Update on Yellow Fire

```json
{
  "timing": {
    "patience_tier": "yellow",
    "tier_entered_ts": {{now_ts}}
  },
  "behavior_log": {
    "yellow_nudges": {{incremented_count}}
  }
}
```

Increment `yellow_nudges` only on first transition into yellow per phase (not every fire while in yellow).

---

## Behavior During Yellow

- Continue to evaluate user replies if they arrive
- Compress pushback to 1 line (don't extend the phase)
- If user keeps responding past nudge, transition to Orange at +60s
- Don't repeat nudge multiple times — one nudge per phase

---

## Variable Substitution

- `{{eval if any}}` — Sage's eval of user's last reply (if any)
- `{{elapsed_human}}` — formatted "Xm YYs"
- `{{budget_human}}` — phase budget formatted
- `{{now_ts}}` — unix timestamp
- `{{incremented_count}}` — yellow_nudges count after increment
