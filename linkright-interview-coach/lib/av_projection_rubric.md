# A/V Projection Rubric — Text → Audio/Video Signal Projection

For V1 (text-only mock), Sage cannot directly measure vocal/visual signals. But text content **projects** A/V signals that can be estimated. Sage coaches the candidate on projected signals AFTER each phase.

(V1.x adds real A/V via Gemini handoff — see `gemini_handoff_guide.md`.)

---

## 7 Text-Derived A/V Projections

### 1. Spoken-time projection

**Formula**: `spoken_seconds = word_count / 140 * 60`

Baseline: 140 wpm (average professional speaking pace).

**Phase budget mapping**:
- 60-sec pitch (Round 4 PT 4.1 Phase 1): target 130-200 words
- 5-min phase: target 600-900 words
- 8-min phase: target 1000-1400 words

**Sage feedback**:
- "Your 280-word answer projects to 2min spoken. For a 60-sec pitch, cut by 40%."
- "Your 200-word answer is fine for a 90-sec phase but too short for the 5-min Strategy phase."

---

### 2. AI-smell density

**Method**: Detect generic / boilerplate / management-speak phrases per 100 words.

**Bad phrases** (auto-flag):
- "leverage synergies"
- "drive impact"
- "move the needle"
- "robust solution"
- "elevate the experience"
- "north star metric" (cliché unless used precisely)
- "best-in-class"
- "innovative approach"
- "stakeholder alignment" (without specifics)
- "go-to-market" (without strategy details)
- "strategic initiative"

**Score**:
- 0% generic: Authentic, 5/5
- 0-2%: Strong, 4/5
- 2-5%: Acceptable, 3/5
- 5-10%: Weak, 2/5
- >10%: AI-smell, 1/5

**Sage feedback**:
- "Density of generic phrases too high (4 in 100 words). Replace with operational specifics from your profile — e.g., instead of 'drove impact', say 'reduced onboarding from 14 to 5 steps in Q3'."

---

### 3. Specificity density

**Method**: Count specific entities per 100 words. Specific = named systems, dated events, quantified outcomes, named people, named tools.

**Specific markers**:
- Numbers + units: "30% reduction", "$2M revenue", "team of 8", "Q3 2024"
- Named tools/systems: "Snowflake pipeline", "React Native app", "Postgres replication"
- Named projects/products: "Project Atlas", "the v3 dashboard"
- Named stakeholders by role+context: "the staff engineer working on payments"
- Specific failure modes: "the rate limiter hit 429s at 1500 RPS"

**Score**:
- 15%+ specific markers: 5/5
- 10-15%: 4/5
- 6-10%: 3/5
- 3-6%: 2/5
- <3%: 1/5

**Sage feedback**:
- "Specificity density 18% — strong. This reads operationally credible."
- "Specificity density 4% — too vague. Anchor your claims with named systems / metrics / dates."

---

### 4. Tone-as-written

**Method**: Detect tone patterns from phrasing.

**Hedge density** (excessive = defensive):
- "I think maybe" / "I guess" / "kind of" / "sort of" / "perhaps"
- Score: hedges per 100 words
- 0-1%: Confident, 5/5
- 1-3%: Calibrated, 4/5
- 3-5%: Mild defensive, 3/5
- 5-8%: Defensive, 2/5
- >8%: Anxious, 1/5

**Defensive patterns**:
- "I don't have direct experience but..."
- "While I haven't done X..."
- "I might be wrong but..."

**Sage feedback**:
- "Phrase 'I don't have direct experience but...' reads defensive when spoken. Try: 'My closest analog is X — here's how it transfers.'"

---

### 5. Filler density (text → spoken projection)

**Method**: Count filler-as-written.

**Markers**:
- "um", "uh", "like", "you know", "basically", "essentially", "literally"
- "okay so", "right so", "I mean"

**Score** (per 100 words):
- 0-1 fillers: 5/5
- 1-3: 4/5
- 3-5: 3/5
- 5-8: 2/5
- >8: 1/5

**Sage feedback**:
- "5 fillers in 200 words — in spoken form, fillers convey uncertainty. Practice replacing with deliberate 2-sec pauses. Silence ≠ unsure; silence = confident."

---

### 6. Constraint mention count

**Method**: Count explicit constraint mentions per phase.

**Constraint markers**:
- Budget: "limited budget", "Q4 budget", "$2M cap"
- Time: "8-week sprint", "Q4 launch deadline"
- Team: "team of 4 engineers", "no design support"
- Data: "no labeled data yet", "limited user research"
- Tech: "iOS only", "must work offline", "<200ms latency required"
- Regulatory: "GDPR-bound", "HIPAA scope"

**Score per 25min phase**:
- 3+ constraints: 5/5
- 2 constraints: 4/5
- 1 constraint: 3/5
- 0 constraints: 2/5

**Sage feedback**:
- "Zero constraints named in this 25-min answer. Senior PMs surface constraints in opening 30s. Add: 'I'll assume <X budget>, <Y timeline>, <Z team size>.'"

---

### 7. Tradeoff articulation count

**Method**: Count explicit tradeoff statements per phase.

**Tradeoff markers**:
- "I'm prioritizing X over Y because Z, even though it costs us W"
- "We chose A which means we sacrifice B"
- "The cost of X is Y — but we accept that because Z"

**Score per 25min phase**:
- 3+ tradeoffs: 5/5
- 2 tradeoffs: 4/5
- 1 tradeoff: 3/5
- 0 tradeoffs: 2/5

**Sage feedback**:
- "No explicit tradeoff articulated. Add: 'I'm prioritizing X over Y because Z, even though it costs us W.' Real operators name what they're giving up."

---

## Combined A/V Projection Output (per phase)

```json
{
  "phase_name": "JTBD",
  "av_projection": {
    "word_count": 280,
    "spoken_time_seconds": 120,
    "spoken_time_target_seconds": 300,
    "spoken_time_status": "under_budget",
    "ai_smell_density_pct": 1.8,
    "ai_smell_phrases_found": ["drive impact"],
    "specificity_density_pct": 16.0,
    "specificity_examples": ["Q3 2024 launch", "team of 6", "30% retention lift"],
    "hedge_density_pct": 2.1,
    "hedge_phrases_found": ["I think maybe"],
    "defensive_pattern_count": 0,
    "filler_density_per_100w": 1.4,
    "constraints_named": 2,
    "constraints_examples": ["6-engineer team", "Q4 deadline"],
    "tradeoffs_named": 1,
    "tradeoffs_examples": ["chose mobile-only over web to ship faster"]
  }
}
```

---

## In-Session A/V Coaching (after each phase)

Sage delivers brief A/V coaching tied to projected signals:

```
A/V PROJECTION FOR THIS PHASE:
  Spoken time: ~2min (target: 5min) — answer too short, expand on Phase 4
  AI-smell: low (1.8%) — strong
  Specificity: high (16%) — operationally credible
  Constraint mentions: 2 — strong
  Tradeoffs: 1 — could surface one more

SPEAKING TIP:
  Phrase "I think maybe X would help" — spoken, this reads as hedging.
  Replace with: "My read is X helps, and here's why."

  Practice this: when you have a strong intuition, state it confidently
  with the reasoning, not as a question.
```

This is the in-session coaching that fires AFTER each phase, before next phase begins. Brief enough to not derail interview cadence.

---

## End-of-Interview A/V Projection Summary

Aggregated across all phases:

```
A/V PROJECTION SUMMARY (text-derived; full A/V via Gemini available separately):

Avg spoken time per phase:    180s / 300s target  (under-utilized — expand answers)
AI-smell density (overall):   1.6%                  (strong — operationally credible)
Specificity density:          14%                   (strong)
Hedge density:                3.4%                  (mild defensive)
Filler-as-written:            2.1 per 100w          (good)
Constraints named per phase:  1.8 avg               (could improve to 3+)
Tradeoffs named per phase:    1.2 avg               (could improve to 2+)

PROJECTED VOCAL VERDICT (text-based):  Vocally Competent
  → For real audio verdict, run Gemini Stage 2 prompt

SPEAKING DRILLS:
  1. Increase per-answer length by 30% (you're under-utilizing time)
  2. Replace "I think maybe" with "My read is" (×3 occurrences observed)
  3. Surface 1 more tradeoff per phase
```

---

## Caveat: Text-Projection vs Real A/V

Text projection is a PROXY for spoken delivery. Real audio/video analysis via Gemini (Stage 1 + 2 + 3) provides ground truth.

When user has real A/V data, the holistic scorecard uses ACTUAL Gemini scores for Layer C dimensions. Text projection becomes secondary input. When user has no A/V data, text projection is the only signal source for Layer C.
