# Holistic Final Scorecard Template (4-source aggregation)

Rendered AFTER user pastes back Gemini Stage 1 + 2 + 3 (or whichever subset they ran).

Aggregates: Content (Claude session) + Video (Gemini Stage 1) + Audio (Gemini Stage 2) + Transcript (Gemini Stage 3).

---

## Template

```
═══════════════════════════════════════════════════════════════════
                HOLISTIC INTERVIEW SCORECARD
═══════════════════════════════════════════════════════════════════
Session:      {{session_id}}
Candidate:    {{name_or_anon}} · {{career_level}} · Transition Phase {{transition_phase}}
Round:        {{round_name}}
Problem:      {{problem_type_name}}
Question:     "{{question}}"
Duration:     {{actual_hhmmss}} / {{budget_hhmmss}}
Voice mode:   {{voice_mode}}
Sources received:
  {{stage1_marker}} Content (Claude session, text-projected)
  {{stage1_marker}} Video (Gemini Stage 1) — {{stage1_status}}
  {{stage2_marker}} Audio (Gemini Stage 2) — {{stage2_status}}
  {{stage3_marker}} Transcript (Gemini Stage 3) — {{stage3_status}}

═══════════════════════════════════════════════════════════════════
                   LAYER A — PSYCHOLOGICAL
                          (4-source matrix)
═══════════════════════════════════════════════════════════════════
                          Content  Video  Audio  Transcr  →  Final
  Safety:                 {{c}}/5  {{v}}/5  {{a}}/5  {{t}}/5    {{f}}/5
  Friction:               ...      ...     ...     ...        ...
  Trust:                  ...      ...     ...     ...        ...
  Predictability:         ...      ...     ...     ...        ...
  Believability:          ...      ...     ...     ...        ...
  ─────────────────────────────────────────────────────────────
  Subtotal:                                                  {{a_total}}/5

═══════════════════════════════════════════════════════════════════
                   LAYER B — PM EVALUATION
                          (4-source matrix)
═══════════════════════════════════════════════════════════════════
                          Content  Video  Audio  Transcr  →  Final
  Product Sense:          ...      —       —     ...        ...
  Execution:              ...      —       —     ...        ...
  Strategy:               ...      —       —     ...        ...
  Analytical Thinking:    ...      —       —     ...        ...
  Leadership:             ...      —       —     ...        ...
  AI Product Judgment:    ...      —       —     ...        ...
  ─────────────────────────────────────────────────────────────
  Subtotal:                                                  {{b_total}}/5

═══════════════════════════════════════════════════════════════════
                   LAYER C — EXECUTIVE PRESENCE
                          (4-source matrix)
═══════════════════════════════════════════════════════════════════
                          Content  Video  Audio  Transcr  →  Final
  Behavioral Stability:   —        {{v}}    {{a}}    —          {{f}}/5
  Cognitive Clarity:      {{c}}    —       —     {{t}}        {{f}}/5
  Social Calibration:     {{c}}    {{v}}    {{a}}    —          {{f}}/5
  Pressure Management:    {{c}}    {{v}}    {{a}}    —          {{f}}/5
  Vocal Presence:         —        —       {{a}}    —          {{f}}/5
  Remote Behavior:        —        {{v}}    —     —          {{f}}/5
  Interruption Handling:  {{c}}    —       {{a}}    —          {{f}}/5
  ─────────────────────────────────────────────────────────────
  Subtotal:                                                  {{c_total}}/5

═══════════════════════════════════════════════════════════════════
OVERALL:                                                     {{overall}}/15
PERSONALIZED CEILING (for your career level + phase):       {{ceiling}}/15
DELTA:                                                       {{delta}}
═══════════════════════════════════════════════════════════════════

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
                   GEMINI RAW METRICS
═══════════════════════════════════════════════════════════════════

VIDEO (Stage 1):
  Posture:                 {{stage1.posture.score}}/5
  Hand gestures:           {{stage1.hand_gestures.score}}/5
  Eye contact:             {{stage1.eye_contact.score}}/5
  Facial expressions:      {{stage1.facial_expressions.score}}/5
  Energy projection:       {{stage1.energy_projection.score}}/5
  Environment:             {{stage1.environment.score}}/5
  Confidence cues:         {{stage1.confidence_cues.score}}/5
  → Visual verdict:        {{stage1.visual_verdict}}

AUDIO (Stage 2):
  Pace WPM:                {{stage2.pace_wpm}}  (target 130-150)
  Pace variation:          {{stage2.pace_variation.score}}/5
  Pause quality:           {{stage2.pause_quality.score}}/5
  Filler density:          {{stage2.filler_density_per_min}}/min
  Filler top-3:            {{stage2.filler_top_3}}
  Verbosity:               {{stage2.verbosity.score}}/5
  Tone modulation:         {{stage2.tone_modulation.score}}/5
  Energy projection:       {{stage2.energy_projection_vocal.score}}/5
  Authority:               {{stage2.authority.score}}/5
  Breath control:          {{stage2.breath_control.score}}/5
  Volume stability:        {{stage2.volume_stability.score}}/5
  → Vocal verdict:         {{stage2.vocal_verdict}}

TRANSCRIPT (Stage 3):
  Storytelling structure:  {{stage3.storytelling_structure.score}}/5
  Specificity density:     {{stage3.specificity_density.score}}/5
  AI-smell density:        {{stage3.ai_smell_density.score}}/5
  Constraints named:       {{stage3.constraints_named_count}}
  Tradeoffs named:         {{stage3.tradeoffs_named_count}}
  Framework usage:         {{stage3.framework_usage.score}}/5
  Authenticity:            {{stage3.authenticity.score}}/5
  Signal density:          {{stage3.signal_density}}
  → Content verdict:       {{stage3.content_verdict}}

═══════════════════════════════════════════════════════════════════
                   CROSS-SOURCE ASYMMETRIES
                          (Highest-leverage feedback)
═══════════════════════════════════════════════════════════════════

{{#each asymmetries}}
  - {{description}}
    What it means: {{interpretation}}
    Drill: {{specific_drill}}
{{/each}}

[Example asymmetry: "Content rated authority 4/5, Audio rated authority 2/5.
You phrase confidently but speak with rising intonation. Drill: read your
strongest written paragraph out loud with falling intonation at sentence
ends; record + listen back daily for 7 days."]

═══════════════════════════════════════════════════════════════════
                   STRENGTHS (top 3, multi-source)
═══════════════════════════════════════════════════════════════════
  1. {{strength_1}}
     Sources: {{strength_1_sources}}
     Quoted: "{{strength_1_quote}}"

  2. {{strength_2}}
     Sources: ...
     Quoted: "..."

  3. {{strength_3}}
     Sources: ...
     Quoted: "..."

═══════════════════════════════════════════════════════════════════
                IMPROVEMENT PLAYBOOK (top 3 gaps)
═══════════════════════════════════════════════════════════════════
[Each gap uses lib/improvement_playbook_template.md format with cross-source
attribution: WHERE OBSERVED includes all source stages that flagged the gap]

{{playbook_gap_1}}
───────────────────────────────────────────────────────────────────
{{playbook_gap_2}}
───────────────────────────────────────────────────────────────────
{{playbook_gap_3}}

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
              NEXT-SESSION DRILL PLAN
═══════════════════════════════════════════════════════════════════
  Drill 1 (same round, different PT):
    Round: {{round_name}} · PT: {{drill_pt}}
    Target: {{drill_target}}
    Time: {{drill_time_min}} min

  Drill 2 (different round, same weak dimension):
    Round: {{drill_2_round}} · PT: {{drill_2_pt}}
    Target: {{drill_2_target}}

  Drill 3 (A/V drill):
    Record 60s answer to: "{{drill_av_question}}"
    Run Gemini Stage 2 on recording
    Target: pace 140 ± 10 wpm · fillers < 2/min · falling intonation

  Daily solo drill (5 min):
    {{daily_drill_description}}

═══════════════════════════════════════════════════════════════════
              TRANSITION PHASE GUIDANCE (if applicable)
═══════════════════════════════════════════════════════════════════
{{transition_phase_guidance}}

═══════════════════════════════════════════════════════════════════
              SAVED TO LINKRIGHT
═══════════════════════════════════════════════════════════════════
  Interview history: ~/.linkright/interview-history/{{ts}}.json
  Latest pointer:    ~/.linkright/interview-history/latest.json
  Gemini A/V data:   embedded in interview-history file
  Story bank:        {{stories_saved_status}}

═══════════════════════════════════════════════════════════════════
              SAGE SIGNS OFF
═══════════════════════════════════════════════════════════════════
  {{sage_signoff_in_character}}
═══════════════════════════════════════════════════════════════════
```

---

## Source Marker Conventions

- ✅ Source received and valid
- ⚠️ Source partial (e.g., Gemini returned incomplete JSON)
- ⬜ Source not run
- — Source not applicable to this dimension

---

## Aggregation Logic (per dimension)

For Layer C dimensions where multiple sources apply:
```
final_score = weighted_avg of source_scores
  where weights:
    Content  : 1.0
    Video    : 2.0   (most direct for visual signals)
    Audio    : 2.0   (most direct for vocal signals)
    Transcript: 1.5  (richer than Content for text-derived)
```

Skip sources marked `—` for that dimension.

If only Content source available (no Gemini), Layer C subset score same as content-only scorecard. Indicate clearly.

---

## Asymmetry Detection Logic

For each dimension scored by 2+ sources:
- Compute `max_source_score - min_source_score`
- If delta ≥ 2 → flag as asymmetry
- Generate specific drill explaining the asymmetry

Common patterns:
- **Content high, Audio low**: writes confidently, speaks hesitantly
- **Content high, Video low**: writes confidently, body shows anxiety
- **Video high, Content low**: looks senior, content is shallow
- **Audio high, Video low**: voice steady, body language nervous

---

## Verdict Bands (4-source variant)

| Overall / 15 | Time discipline | A/V quality | Verdict |
|---|---|---|---|
| ≥ 12 | Clean | All sources strong | STRONG HIRE |
| 10-12 | 1-2 issues | Mixed but solid | HIRE |
| 8-10 | 2-3 issues | One weak source | LEAN HIRE |
| 6-8 | Multiple | Multiple weak sources | NO HIRE |
| < 6 | Severe | Severe | STRONG NO |

Anti-pattern overrides:
- Gemini Stage 2 vocal_verdict = "Vocally Anxious" → cap at LEAN HIRE
- Gemini Stage 1 visual_verdict = "Visually Anxious" → cap at LEAN HIRE
- Gemini Stage 3 ai_smell_density.score ≤ 2 → cap at LEAN HIRE

---

## Variable Substitution

All placeholders filled from `/tmp/mock-interview-state-<uuid>.json` after merging Gemini stage data. See `state/state-schema.json` for full schema.
