# Content-Only Final Scorecard Template

Rendered at end of interview, BEFORE A/V coaching offer. Based ONLY on text-derived signals (Content + A/V Projection from text).

Use this when:
- User opts NOT to do A/V coaching, OR
- Before A/V handoff (then upgraded to holistic scorecard)

For full 4-source scorecard with Gemini A/V, see `final_scorecard_holistic.md`.

---

## Template

```
═══════════════════════════════════════════════════════════════════
              CONTENT-ONLY SCORECARD
═══════════════════════════════════════════════════════════════════
Session:      {{session_id}}
Candidate:    {{name_or_anon}} · {{career_level}} · Transition Phase {{transition_phase}}
Round:        {{round_name}}
Problem:      {{problem_type_name}}
Question:     "{{question}}"
Duration:     {{actual_hhmmss}} / {{budget_hhmmss}}
Source:       ✅ Content (Claude session, text-projected)
              ⬜ Video (Gemini Stage 1 — not yet run)
              ⬜ Audio (Gemini Stage 2 — not yet run)
              ⬜ Transcript (Gemini Stage 3 — not yet run)

═══════════════════════════════════════════════════════════════════
                   LAYER A — PSYCHOLOGICAL
═══════════════════════════════════════════════════════════════════
  Safety:                  {{score}}/5    vs ceiling {{ceil}}/5
  Friction:                {{score}}/5    vs ceiling {{ceil}}/5
  Trust:                   {{score}}/5    vs ceiling {{ceil}}/5
  Predictability:          {{score}}/5    vs ceiling {{ceil}}/5
  Believability:           {{score}}/5    vs ceiling {{ceil}}/5
  ─────────────────────────────────────────
  Subtotal:                {{a_total}}/5  (weighted, career-level adjusted)

═══════════════════════════════════════════════════════════════════
                   LAYER B — PM EVALUATION
═══════════════════════════════════════════════════════════════════
  Product Sense:           {{score}}/5    vs ceiling {{ceil}}/5
  Execution:               {{score}}/5    vs ceiling {{ceil}}/5
  Strategy:                {{score}}/5    vs ceiling {{ceil}}/5
  Analytical Thinking:     {{score}}/5    vs ceiling {{ceil}}/5
  Leadership:              {{score}}/5    vs ceiling {{ceil}}/5
  AI Product Judgment:     {{score}}/5    {{na_if_not_applicable}}
  ─────────────────────────────────────────
  Subtotal:                {{b_total}}/5

═══════════════════════════════════════════════════════════════════
            LAYER C — EXECUTIVE PRESENCE (text-derived subset)
═══════════════════════════════════════════════════════════════════
  Behavioral Stability:    — (Gemini Stage 1 + 2 required)
  Cognitive Clarity:       {{score}}/5    vs ceiling {{ceil}}/5
  Social Calibration:      — (Gemini required)
  Pressure Management:     {{score}}/5    (text-projected subset)
  Vocal Presence:          — (Gemini Stage 2 required)
  Remote Behavior:         — (Gemini Stage 1 required)
  Interruption Handling:   {{score}}/5    (from your handling of my orange-tier cuts)
  ─────────────────────────────────────────
  Subtotal (partial):      {{c_partial_total}}/5

═══════════════════════════════════════════════════════════════════
OVERALL (Content-only):    {{overall}}/15  (Layer A + B + partial C)
PERSONALIZED CEILING:      {{personalized_ceiling}}/15
DELTA:                     {{delta}}

═══════════════════════════════════════════════════════════════════
                   TIME DISCIPLINE
═══════════════════════════════════════════════════════════════════
  Per-phase timing:
  {{#each phases}}
    Phase {{idx}}: {{name}}            {{actual_min}}m / {{budget_min}}m  [{{tier_emoji}}]
  {{/each}}

  Yellow nudges:           {{yellow_nudges}}
  Orange interrupts:       {{orange_interrupts}}
  Hard cutoffs (red):      {{hard_cutoffs}}
  Ramble interrupts:       {{ramble_count}}

═══════════════════════════════════════════════════════════════════
              A/V PROJECTION SUMMARY (text-derived)
═══════════════════════════════════════════════════════════════════
  Avg spoken-time per phase:   {{avg_spoken_s}}s / {{avg_target_s}}s
  AI-smell density:            {{ai_smell_pct}}%   (low = good)
  Specificity density:         {{specificity_pct}}%   (high = authentic)
  Hedge density:               {{hedge_pct}}%
  Filler-as-written density:   {{filler_per_100w}} per 100w
  Constraints named (avg):     {{constraints_avg}} per phase
  Tradeoffs named (avg):       {{tradeoffs_avg}} per phase

  Projected vocal verdict:     {{projected_vocal_verdict}}
  (For real audio analysis, run Gemini Stage 2)

═══════════════════════════════════════════════════════════════════
                   STRENGTHS (top 3, with quotes)
═══════════════════════════════════════════════════════════════════
  1. {{strength_1}}
     Quoted: "{{strength_1_quote}}"

  2. {{strength_2}}
     Quoted: "{{strength_2_quote}}"

  3. {{strength_3}}
     Quoted: "{{strength_3_quote}}"

═══════════════════════════════════════════════════════════════════
                IMPROVEMENT PLAYBOOK (top 3 gaps)
═══════════════════════════════════════════════════════════════════
{{playbook_gap_1}}
───────────────────────────────────────────────────────────────────
{{playbook_gap_2}}
───────────────────────────────────────────────────────────────────
{{playbook_gap_3}}

[Each gap follows format from lib/improvement_playbook_template.md]

═══════════════════════════════════════════════════════════════════
              TRADEOFF-FAIRNESS CREDITS APPLIED
═══════════════════════════════════════════════════════════════════
{{tradeoff_credits_list}}

═══════════════════════════════════════════════════════════════════
                   VERDICT (calibrated to {{difficulty_bar}})
═══════════════════════════════════════════════════════════════════
  [{{verdict}}]

  Reasoning:
  {{verdict_reasoning_2_3_sentences}}

═══════════════════════════════════════════════════════════════════
              NEXT-SESSION DRILL RECOMMENDATIONS
═══════════════════════════════════════════════════════════════════
  1. {{drill_1}}
  2. {{drill_2}}
  3. {{drill_3}}

  Daily solo drill (5 min): {{daily_drill}}

═══════════════════════════════════════════════════════════════════
              WANT A/V COACHING?
═══════════════════════════════════════════════════════════════════
  Recorded yourself doing this interview? (Meet / Loom / phone camera)

  If yes, I can give you 3 paste-ready Gemini prompts that will analyze:
    Stage 1: Body language (video-only, audio muted)
    Stage 2: Vocal delivery (audio-only)
    Stage 3: Content depth (transcript-only)

  You'll run them in gemini.google.com on your own time and paste
  results back. I'll aggregate into a 4-source holistic scorecard.

  Yes / No / Later?

═══════════════════════════════════════════════════════════════════
              SAVED TO LINKRIGHT
═══════════════════════════════════════════════════════════════════
  Interview history: ~/.linkright/interview-history/{{ts}}.json
  Latest pointer:    ~/.linkright/interview-history/latest.json
  Story bank:        (none saved yet — Sage will offer specific stories shortly)

═══════════════════════════════════════════════════════════════════
              SAGE SIGNS OFF
═══════════════════════════════════════════════════════════════════
  Sage hu — interview done. Tumhari biggest gap is {{biggest_gap}}.
  Drill that in next session via {{recommended_next_drill}}.
  Keep showing up.
═══════════════════════════════════════════════════════════════════
```

---

## Verdict Bands (with Phase-Aware Floors)

| Layer A + B subtotal | Time discipline | Verdict band |
|---|---|---|
| ≥ 8/10 | ≤ 1 yellow nudge, 0 orange, 0 red, 0-1 ramble | STRONG HIRE |
| 7-8/10 | ≤ 2 yellow, ≤ 1 orange, 0 red | HIRE |
| 6-7/10 | ≤ 3 yellow, ≤ 2 orange, ≤ 1 red | LEAN HIRE |
| 4-6/10 | Any | NO HIRE |
| < 4/10 | Any | STRONG NO |

Anti-pattern overrides:
- Hard cutoff fired 2+ times → cap at LEAN HIRE
- Ramble cut 3+ times → cap at LEAN HIRE
- AI-smell density > 10% → cap at LEAN HIRE

---

## Variable Substitution

All `{{*}}` placeholders filled from `/tmp/mock-interview-state-<uuid>.json`:
- `{{session_id}}`, `{{name_or_anon}}`, `{{career_level}}`, `{{transition_phase}}` — from candidate-summary
- `{{round_name}}`, `{{problem_type_name}}`, `{{question}}`, `{{difficulty_bar}}` — from round config
- `{{actual_hhmmss}}`, `{{budget_hhmmss}}` — from timing
- `{{score}}`, `{{ceil}}` — per-dimension scores + personalized ceilings
- `{{a_total}}`, `{{b_total}}`, `{{c_partial_total}}`, `{{overall}}` — aggregates
- `{{phases}}` array — per-phase timing rows
- `{{yellow_nudges}}` etc — behavior_log counts
- `{{strength_*}}`, `{{playbook_gap_*}}`, `{{drill_*}}` — derived per `improvement_playbook_template.md`
- `{{verdict}}` — calibrated band
- `{{verdict_reasoning_2_3_sentences}}` — Sage's narrative explanation
