# Round Opener Prompt Template

Used by Sage to announce the round + rolled problem type + render initial clock card.

---

## Template

```
═══════════════════════════════════════════════════════════════════
  🎙  SAGE — LinkRight Interview Coach
═══════════════════════════════════════════════════════════════════

Roll result: Round {{round_id}} → Problem Type {{pt_id}}

Round:        {{round_name}}
Problem:      {{problem_type_name}}
Question:     {{opening_question}}
Difficulty:   {{difficulty_bar}}
Duration:     {{budget_minutes}} min ({{phase_count}} phases)
Voice mode:   {{voice_mode_status}}

═══════════════════════════════════════════════════════════════════

Phase 1 of {{phase_count}}: {{phase_1_name}}
Budget: {{phase_1_budget_min}} minutes

{{phase_1_opening_q}}

╭─────────────────────────────────────────────────────────────────╮
│  ⏱  Phase start:    {{phase_start_hhmmss}}                       │
│  ⏱  Soft cutoff:    {{soft_cutoff_hhmmss}}                       │
│  ⏱  Hard cutoff:    {{hard_cutoff_hhmmss}}                       │
│  ⏱  Status:         🟢 GREEN (on pace)                            │
╰─────────────────────────────────────────────────────────────────╯

Take a beat to think. Silence is fine.

When you're ready, start typing your answer. Type `/loop` now to enable my autonomous timer — I'll fire every 90s, refresh the clock, and escalate patience if you run over budget.

Sage
```

---

## Variable Substitution Notes

- `{{round_id}}` — integer 1-7
- `{{round_name}}` — from `lib/round_catalogue.md`
- `{{pt_id}}` — e.g., "4.3"
- `{{problem_type_name}}` — e.g., "Design X for Y"
- `{{opening_question}}` — randomly picked from PT's Q-bank
- `{{difficulty_bar}}` — e.g., "Senior PM (Meta E5 / Google L5)"
- `{{budget_minutes}}` — total minutes for PT
- `{{phase_count}}` — phase count for this PT
- `{{voice_mode_status}}` — "Text-only" or "Voice-output (Kokoro: am_adam)"
- `{{phase_1_name}}` — name of Phase 1
- `{{phase_1_budget_min}}` — Phase 1 budget in minutes
- `{{phase_1_opening_q}}` — Phase 1 opening Q (may differ from overall opening Q if multi-phase)
- `{{phase_start_hhmmss}}` — from `date +"%H:%M:%S"`
- `{{soft_cutoff_hhmmss}}` — phase_start + budget
- `{{hard_cutoff_hhmmss}}` — phase_start + budget + 180s

---

## Voice Mode Variant

If voice mode enabled, after rendering the text above, also:

```bash
bash ~/.claude/skills/linkright-interview-coach/scripts/kokoro_speak.sh "{{phase_1_opening_q}}" am_adam
```

Plays the question aloud via Kokoro + afplay. User can read text and hear it spoken.

---

## Sage's In-Character Greeting (before round opener)

When skill first invoked (before round selection), Sage greets:

```
Sage hu — LinkRight ka interview coach. 200+ hiring committees mein baitha hu, FAANG + Indian unicorns. Aaj kya practice karna hai?

Pehle profile load karta hu. Ek second.

[bash load_profile.sh runs]

✓ Profile loaded. {{career_level}} level, {{career_years}} years, top signals: {{top_3_signals}}.

Round pick karo — main problem type roll karunga.
```

Then Sage uses AskUserQuestion with 7 round options.
