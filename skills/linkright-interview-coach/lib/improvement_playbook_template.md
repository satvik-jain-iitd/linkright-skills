# Improvement Playbook — Output Format

The **playbook IS the product**, not the score. After interview, candidate gets a playbook that shows what their **strongest possible version** answer would have looked like, with concrete drills.

---

## Playbook Generation Rules

### Rule 1 — Reconstruct using ONLY candidate's profile facts
Never invent experience. The "strongest possible version" reconstruction must use:
- Bullets from `~/.linkright/profile/highlights.jsonl`
- Nuggets from `~/.linkright/profile/nuggets.jsonl`
- Existing story-bank entries if present

If candidate's profile lacks the raw material for a strong answer, the playbook must say: "You don't have the experience to answer this way today. Build it: <specific suggestion>."

### Rule 2 — Anchor to specific quotes from user's actual answer
Every gap entry must quote the candidate's actual phrase. Specificity is what makes the playbook actionable.

### Rule 3 — Top 3 gaps only
More than 3 dilutes the message. Pick highest-leverage gaps based on:
- Cross-layer signal (gap visible in multiple layers)
- High-multiplier dimension for career level
- Anti-pattern flags

### Rule 4 — Each gap has 4 sections
- WHAT it was
- WHY it matters
- WHAT IT COULD HAVE BEEN (your strongest version using your facts)
- HOW TO PRACTICE

### Rule 5 — Quantify the expected lift
Each gap should specify: "If fixed at ceiling: +X.X on Layer Y dimension Z" so candidate sees what fixing yields.

---

## Playbook Format

```
═══════════════════════════════════════════════════════════════════
                IMPROVEMENT PLAYBOOK (Top 3 Gaps)
═══════════════════════════════════════════════════════════════════

GAP #1: {{name_of_gap}}
  Severity: {{High|Medium|Low}}
  Layer / Dimension affected: {{Layer X.Y}}
  Cross-source consensus: {{Content + Video + Audio agree | Only Content flagged}}

WHAT IT LOOKED LIKE:
  Phase {{N}} — your actual phrasing:
    "{{quote from user reply}}"

  Sage interpretation:
    {{1-2 sentences on what this signal projected}}

WHY IT MATTERS:
  In real FAANG interview:
    - {{specific psychological-layer impact}}
    - {{specific PM-evaluation impact}}
    - {{verdict-band shift if uncorrected}}

YOUR STRONGEST POSSIBLE VERSION:
  (Reconstructed from YOUR profile facts — career_level: {{X}}, top_signals: {{Y, Z}})

  "{{Full reconstructed strong-version answer using candidate's actual experience}}"

  Why this works:
    - Sends Layer A signal: {{specific psychological signal}}
    - Hits Layer B dimension: {{specific PM dimension}}
    - Demonstrates Layer C: {{specific presence dimension}}

HOW TO PRACTICE:

  30-SECOND DRILL (repeat daily for 7 days):
    {{Specific exercise — e.g., "Pick a moment from your resume bullet '<bullet>'. Practice articulating it with 1 named constraint and 1 named tradeoff in under 60 seconds. Record yourself. Listen back. Repeat."}}

  TRIGGER PHRASE (mental cue during real interview):
    When you hear "{{JD-signal phrase}}", respond with "{{constraint-surfacing or tradeoff-naming phrase}}"

  STORY BANK ENTRY TO ADD:
    Theme: {{theme}}
    Source: {{specific bullet from candidate's resume}}
    Adapts to: {{1-2 question types}}

EXPECTED LIFT IF FIXED:
  Layer X.Y: +{{N.N}} → final ceiling-relative score moves from {{X}} to {{Y}}
  Verdict band shift: {{e.g., "LEAN HIRE → HIRE"}}

───────────────────────────────────────────────────────────────────

GAP #2: ... (same structure)

───────────────────────────────────────────────────────────────────

GAP #3: ... (same structure)

═══════════════════════════════════════════════════════════════════
```

---

## Concrete Example (illustrative)

```
═══════════════════════════════════════════════════════════════════
GAP #1: Constraint Articulation Absent
  Severity: HIGH
  Layer / Dimension: Layer B.2 Execution + Layer A.5 Believability
  Cross-source consensus: Content + Transcript (Stage 3) both flag

WHAT IT LOOKED LIKE:
  Phase 4 (Solutions) — your actual phrasing:
    "We could improve onboarding by adding personalized recommendations
    and a better welcome flow."

  Sage interpretation:
    No team size, no timeline, no budget, no data dependency named.
    Reads as ideation without operational constraint awareness.

WHY IT MATTERS:
  In real FAANG interview:
    - Layer A.5 Believability: -1.5 (interviewer codes as "shallow operator")
    - Layer B.2 Execution: -1.0 (no rollout realism)
    - Verdict shift: HIRE → LEAN HIRE

YOUR STRONGEST POSSIBLE VERSION:
  (Reconstructed using your career_level=mid, top_signals=[data-driven, build-execution])

  "Two improvements, both within Q4 budget assuming a 4-engineer team:
   First, personalized recommendations — I'd start with a v0 that uses
   the existing user-event pipeline (Snowflake, ~2 weeks build) before
   investing in a real-time ML serving stack. Constraint: we don't have
   labeled preference data yet, so v0 ranks by cohort behavior, not
   personal signal. Second, welcome flow — A/B test against current
   24-hour activation rate, target +5% over 8 weeks. I'd hold the line
   on adding more steps; my data-analyst instinct says reducing friction
   beats adding personalization for a Phase 1 onboarding fix."

  Why this works:
    - Layer A.5: Specific tech stack (Snowflake), timelines (2wk, 8wk), team size (4 eng), target metric (+5% activation) = high specificity density = believable
    - Layer B.2: Phased rollout + clear constraint (no labeled data yet) + sensible v0 = senior-PM execution thinking
    - Layer B.3: Strategic restraint ("hold the line on adding steps") = product-thinking maturity
    - Bridge-narrative: explicit reference to "data-analyst instinct" = honest transition framing

HOW TO PRACTICE:

  30-SECOND DRILL (repeat daily for 7 days):
    Pick one bullet from your resume. In 60 seconds, narrate it with:
    - 1 named constraint (team / time / data / tech / regulatory)
    - 1 named tradeoff
    - 1 quantified outcome
    Record yourself. Listen back. Aim for natural cadence by Day 7.

  TRIGGER PHRASE (mental cue):
    When you hear "How would you...", IMMEDIATELY name 1 constraint
    BEFORE proposing the solution. Make it muscle memory.

  STORY BANK ENTRY TO ADD:
    Theme: phased-rollout-under-constraint
    Source: your Q3 data-pipeline rebuild bullet
    Adapts to: PT 4.2 (Improve X), PT 4.3 (Design X for Y), PT 6.1 (System Design)

EXPECTED LIFT IF FIXED:
  Layer B.2: +1.5 → ceiling-relative score 3.0 → 4.5
  Layer A.5: +1.0 → ceiling-relative score 3.5 → 4.5
  Verdict band shift: LEAN HIRE → HIRE (and approaching STRONG HIRE)

═══════════════════════════════════════════════════════════════════
```

---

## Edge Case: When Profile Lacks Raw Material

If candidate's profile has NO bullet matching the question's domain:

```
YOUR STRONGEST POSSIBLE VERSION:
  Honest note: Your profile doesn't currently have experience in
  large-scale launch execution. You're in Phase 1 (signal accumulation)
  for this signal.

  To build this:
    - Add: 1 quantifiable shipped feature with rollout phases
    - Position: bridge-narrative — "From my data-analyst background,
      I'd approach the rollout by..."
    - Practice: 5 mock answers WITHOUT relying on launch-execution
      framing; use data-analyst framing instead

  Once you have the experience, re-run this PT — your strongest
  version will look different (and better).
```

This converts the playbook into a career-development artifact for Phase 1 candidates.

---

## Cross-Layer Disagreement Surfacing

When 4-source aggregation shows disagreement (e.g., Transcript says high authority, Audio says rising intonation), the playbook surfaces this:

```
CROSS-SOURCE INSIGHT:
  - Transcript content: rated Layer C.5 (Vocal Presence) NOT MEASURABLE
  - Audio analysis (Gemini Stage 2): rated 2/5 — rising intonation throughout, hedging tone
  - Content analysis: your phrasing was confident in text

  Interpretation:
    You PHRASE confidently but SPEAK hesitantly. Common pattern for
    candidates rehearsing scripts mentally.

  Drill:
    Pick your strongest-written paragraph from this transcript.
    Practice saying it OUT LOUD with falling intonation at sentence
    ends. Record yourself. Goal: spoken-confidence matches written-
    confidence by week's end.
```

This is the **highest-leverage feedback** the playbook can give — the asymmetry between channels reveals specific drills no single-channel analysis would surface.

---

## End-of-Playbook Drill Plan (next session)

```
═══════════════════════════════════════════════════════════════════
                   NEXT SESSION DRILL PLAN
═══════════════════════════════════════════════════════════════════

Based on top 3 gaps + your career level + transition phase:

DRILL 1 — Same round, different PT
  Round: {{X}} (you picked) — PT: {{rolled, different from last}}
  Target: improve Layer {{Y.Z}} from {{score}} to {{score + 1.5}}
  Time: ~{{N}} min

DRILL 2 — Different round, similar weak dimension
  Round: {{X}}
  PT: {{Y}}
  Target: practice {{specific dim}} in different context
  Time: ~{{N}} min

DRILL 3 — A/V drill (if not done yet)
  Record yourself answering: "{{strongest possible version from Gap #1}}"
  Run Gemini Stage 2 (audio) prompt on your recording
  Target: pace_wpm 140 ± 10, fillers <2/min, falling intonation

DAILY DRILL (solo, 5 min/day):
  {{Specific exercise from Gap #1 → "How to practice" → 30-sec drill}}

═══════════════════════════════════════════════════════════════════
```
