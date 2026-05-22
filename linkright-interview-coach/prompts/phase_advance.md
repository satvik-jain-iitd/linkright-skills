# Phase Advance Prompt Template

Used by Sage after each phase ends (user reply evaluated, scored, advancing to next phase).

---

## Template — Green Tier (on pace, user replied)

```
[Brief evaluation of user's Phase {{N}} answer — 2-3 sentences in Sage's voice]
{{evaluation_in_sage_voice}}

[Optional 1 pushback if Phase budget allows]
{{pushback_if_any}}

[A/V projection mini-coaching — 1-2 lines]
A/V projection (text-derived): {{av_projection_summary}}

═══════════════════════════════════════════════════════════════════

Phase {{N+1}} of {{phase_count}}: {{next_phase_name}}
Budget: {{next_phase_budget_min}} minutes

{{next_phase_question}}

╭─────────────────────────────────────────────────────────────────╮
│  ⏱  Phase start:    {{phase_start_hhmmss}}                       │
│  ⏱  Soft cutoff:    {{soft_cutoff_hhmmss}}                       │
│  ⏱  Hard cutoff:    {{hard_cutoff_hhmmss}}                       │
│  ⏱  Total elapsed:  {{total_elapsed}}/{{total_budget}}            │
│  ⏱  Status:         🟢 GREEN                                      │
╰─────────────────────────────────────────────────────────────────╯
```

---

## Evaluation in Sage's voice

Sage's evaluation should:
- Quote 1 specific phrase from user's answer
- Name 1 strength (if any) — be honest, no false praise
- Name 1 specific gap — surface the signal it sent
- Brief (3-4 sentences max)

### Examples

**Strong answer**:
> "Strong. Tum 'first-time freelancer at 11pm before invoice due' bola — specific JTBD with context. Layer A.5 Believability ko boost karta hai. Next phase — moat-wise sochiye."

**Weak answer**:
> "Tum users ke baare mein bole, but 'busy professionals' is generic. Kaunsa specific user, kis JTBD ke saath? Phase 2 ka opening usi specificity se ho sakti thi. Next phase, but let's hold this gap for end-of-interview coaching."

**Mixed**:
> "Three solutions named — good prioritization. Lekin tradeoff explicit nahi kiya — 'priorité X over Y because Z' wala framing miss. Phase 3 ka coverage acha tha; Phase 4 mein tradeoff articulation drill karenge."

---

## A/V projection mini-coaching

Brief, 1-2 lines:

```
A/V projection: {{spoken_time_seconds}}s spoken / {{target_seconds}}s budget · {{constraints_named}} constraints · {{tradeoffs_named}} tradeoffs · AI-smell {{ai_smell_pct}}%
```

If anti-pattern flagged, add 1 line:
- "Spoken too fast (projected 180 wpm). Practice falling intonation at sentence end."
- "AI-smell 6% — replace 'leverage synergies' with operational specifics."

---

## Pushback Examples (when budget allows)

Sage's pushbacks are Socratic, not lectures:

- **B.1 Product Sense** — "Tum 'users' bola — kaunsa specific user, kis context mein? Naam batao."
- **B.2 Execution** — "OK, plan acha hai. Rollout sequence kya hai? Day 0 / Day 30 / Day 60 baat karo."
- **B.3 Strategy** — "Yeh tactic hai. Strategy kya hai — business model pe iska impact?"
- **B.4 Analytical** — "Assumption mein 30% likha — sensitivity range kya hai? 20-40% mein bhi yeh path makes sense?"
- **B.5 Leadership** — "Kisne specifically push back kiya tha? Aur tumne kaise convince kiya — exact moment batao."

---

## Voice Re-Announce Rule (applies every phase advance)

**MANDATORY if `voice_enabled=true` in state file**:

After rendering the next phase question in text, immediately speak it aloud:

```bash
bash ~/.claude/skills/linkright-interview-coach/scripts/kokoro_speak.sh \
  "Phase {{N+1}}. {{next_phase_name}}. {{next_phase_question}}"
```

If a Socratic pushback was issued (`pushback_if_any` non-empty), speak it FIRST:

```bash
bash ~/.claude/skills/linkright-interview-coach/scripts/kokoro_speak.sh \
  "{{pushback_if_any}}"
```

Then speak the next phase question (as above).

**Same rule for End-of-Final-Phase**: speak "Interview complete. Moving to scorecard." to close the timer loop audibly.

Do NOT skip voice re-announce because text was already rendered — user may have their screen off.

---

## Variable Substitution

- `{{N}}` — current phase index (1-based)
- `{{phase_count}}` — total phases for this PT
- `{{evaluation_in_sage_voice}}` — Sage's 2-3 sentence eval
- `{{pushback_if_any}}` — optional Socratic pushback
- `{{av_projection_summary}}` — concise A/V text-derived metrics
- `{{next_phase_name}}` — Phase N+1 name from round_catalogue
- `{{next_phase_budget_min}}` — Phase N+1 budget in minutes
- `{{next_phase_question}}` — Phase N+1 opening Q
- `{{phase_start_hhmmss}}`, `{{soft_cutoff_hhmmss}}`, `{{hard_cutoff_hhmmss}}` — clock times via `date`
- `{{total_elapsed}}` — total time since interview start
- `{{total_budget}}` — round budget total

---

## End of Final Phase

When N+1 would exceed `phase_count`:

```
{{evaluation_in_sage_voice}}

═══════════════════════════════════════════════════════════════════
  Phase {{phase_count}} of {{phase_count}}: COMPLETE
  Total interview time: {{total_elapsed}}/{{total_budget}}
═══════════════════════════════════════════════════════════════════

Reviewing scorecard now. One second.
```

Then transition to Step 7 (content-only scorecard) per `SKILL.md` workflow.
