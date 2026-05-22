# Orange Tier Interrupt Prompt Template

Fires when: `phase_budget + 60s < elapsed ≤ phase_budget + 180s`

Sage interrupts mid-stream: acknowledges first key point, then forces phase advance.

---

## Template

```
[Brief acknowledgment of first 1-2 substantive points from user's latest reply, if any]
{{brief_acknowledgment}}

🟠 ORANGE — Phase exceeded by {{over_seconds}}s. Pause there, moving us forward.

═══════════════════════════════════════════════════════════════════

Phase {{N+1}} of {{phase_count}}: {{next_phase_name}}
Budget: {{next_phase_budget_min}} minutes

{{next_phase_question}}

╭─────────────────────────────────────────────────────────────────╮
│  ⏱  Phase {{N}} ended at: {{phase_n_end_hhmmss}} (🟠 ORANGE)     │
│  ⏱  Phase {{N+1}} start:   {{phase_start_hhmmss}}                │
│  ⏱  Soft cutoff:           {{soft_cutoff_hhmmss}}                │
│  ⏱  Hard cutoff:           {{hard_cutoff_hhmmss}}                │
│  ⏱  Total elapsed:         {{total_elapsed}}/{{total_budget}}    │
│  ⏱  Status:                🟢 GREEN                              │
╰─────────────────────────────────────────────────────────────────╯
```

---

## Acknowledgment Examples

### If user's latest reply had substantive content
> "Tu Phase 3 mein 'first-time freelancer' point acha bole — that's a strong JTBD anchor. Moving on."

### If user's reply was rambling
> "Point 1 (segmentation by retention cohort) was useful. Rest deferred to scorecard. Moving on."

### If no new user reply since last fire (orange fired due to clock alone)
> "No new message; phase budget exhausted. Advancing."

---

## State Update on Orange Fire

```json
{
  "timing": {
    "patience_tier": "orange",
    "tier_entered_ts": {{now_ts}},
    "current_phase_idx": {{N+1}},
    "phases": [
      ...
      {"name": "{{phase_n_name}}", "end_ts": {{now_ts}}, "status": "orange_cutoff"}
    ]
  },
  "behavior_log": {
    "orange_interrupts": {{incremented_count}}
  }
}
```

---

## Scoring Impact

Phase ended at Orange tier:
- Layer A.2 Friction: capped at 3
- Layer C.4 Pressure Management: capped at 3
- Note added: "Phase X ended at Orange tier — interrupt fired at +{{over_seconds}}s"

---

## Variable Substitution

- `{{brief_acknowledgment}}` — 1-2 sentence acknowledgment
- `{{over_seconds}}` — seconds over budget at moment of orange transition
- `{{N}}` — phase index ending
- `{{N+1}}` — phase index starting
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
- `{{incremented_count}}` — orange_interrupts count after increment
