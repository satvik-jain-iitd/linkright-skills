# Red Tier Hard Cutoff Prompt Template

Fires when: `elapsed > phase_budget + 180s`

Sage hard-cuts the phase regardless of user reply state. Forces advance. Logs `hard_cutoff` for scorecard.

---

## Template

```
🔴 RED — HARD CUTOFF. Phase {{N}} exceeded budget by {{over_seconds}}s. Time discipline is part of the test.

═══════════════════════════════════════════════════════════════════

Phase {{N+1}} of {{phase_count}}: {{next_phase_name}}
Budget: {{next_phase_budget_min}} minutes

{{next_phase_question}}

╭─────────────────────────────────────────────────────────────────╮
│  ⏱  Phase {{N}} ended at: {{phase_n_end_hhmmss}} (🔴 RED CUTOFF) │
│  ⏱  Phase {{N+1}} start:   {{phase_start_hhmmss}}                │
│  ⏱  Soft cutoff:           {{soft_cutoff_hhmmss}}                │
│  ⏱  Hard cutoff:           {{hard_cutoff_hhmmss}}                │
│  ⏱  Total elapsed:         {{total_elapsed}}/{{total_budget}}    │
│  ⏱  Status:                🟢 GREEN                              │
╰─────────────────────────────────────────────────────────────────╯

Note: Hard cutoff logged. In real FAANG interview, this would be a verdict-band drop. Reviewing in end-of-interview scorecard.
```

---

## Sage's Internal Tone

Red tier is **professional finality** — no anger, no sarcasm, just discipline.

Variants:
- "Hard stop. Time exceeded. Next phase: <Q>."
- "Phase end. 3-min overrun. Real interview mein selection penalty hota. Moving on."
- "Cutoff. Recording for scorecard. Next: <Q>."

NEVER:
- Apologize for cutting off
- Negotiate ("OK, give me 30 more seconds")
- Re-extend the phase

---

## State Update on Red Fire

```json
{
  "timing": {
    "patience_tier": "red",
    "tier_entered_ts": {{now_ts}},
    "current_phase_idx": {{N+1}},
    "phases": [
      ...
      {"name": "{{phase_n_name}}", "end_ts": {{now_ts}}, "status": "red_cutoff"}
    ]
  },
  "behavior_log": {
    "hard_cutoffs": {{incremented_count}}
  }
}
```

---

## Scoring Impact (red cutoff)

Phase ended at Red tier:
- Layer A.2 Friction: capped at 2
- Layer C.4 Pressure Management: capped at 2
- Anti-pattern flag: "hard_cutoff_red_tier" added to phase
- Overall verdict band: cannot exceed LEAN HIRE if 2+ red cutoffs

---

## If Final Phase Red Cutoff

If Phase N is the LAST phase and red cutoff fires:

```
🔴 RED — Final phase exceeded. Wrapping interview now.

[Scorecard transitions to Step 7]
```

Don't advance to a non-existent Phase N+1. Jump to scorecard.

---

## Variable Substitution

- `{{over_seconds}}` — seconds over budget when red fired
- `{{N}}` — phase index ending
- `{{N+1}}` — phase index starting (or "—" if final)
- `{{phase_count}}` — total phases
- `{{next_phase_name}}` — Phase N+1 name
- `{{next_phase_budget_min}}` — Phase N+1 budget
- `{{next_phase_question}}` — Phase N+1 opening Q
- `{{phase_n_end_hhmmss}}` — when Phase N ended
- `{{phase_start_hhmmss}}` — when Phase N+1 starts
- `{{soft_cutoff_hhmmss}}` — Phase N+1 soft cutoff
- `{{hard_cutoff_hhmmss}}` — Phase N+1 hard cutoff
- `{{total_elapsed}}` — total interview elapsed
- `{{total_budget}}` — round budget total
- `{{incremented_count}}` — hard_cutoffs count after increment
