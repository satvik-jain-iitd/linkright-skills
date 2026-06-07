# Scoring Rubric — 0-5 Anchors per Dimension

Each dimension (Layer A/B/C) scored 0-5 per phase. Final phase score = weighted average per career level via `signal_weights.yaml`.

---

## Universal 0-5 Anchor Scale

| Score | Anchor | Description |
|---|---|---|
| **0** | Absent | Dimension not demonstrated at all; or actively counter-demonstrated. |
| **1** | Below junior bar | Demonstrated but with severe gaps; major rework needed. |
| **2** | Junior bar | Functional but missing senior-level depth. Acceptable for APM. |
| **3** | Mid bar | Solid mid-level execution. Senior PM would push for more. |
| **4** | Senior bar | Strong senior-PM-level demonstration. FAANG-hire material. |
| **5** | Principal bar | Exceptional — would set the bar for the team. Rare at any level. |

---

## Layer A Anchors

### A.1 Safety
- **0**: Defensive at every pushback. Trashes past employers. Visible irritation.
- **2**: Mostly calm but hedges defensively on 1-2 pushbacks.
- **3**: Calm; admits uncertainty when probed; recovers from pushback gracefully.
- **4**: Stays neutral under hard pushback. Doesn't take pushback personally.
- **5**: Welcomes pushback; visibly engages with the challenge. Anti-fragile.

### A.2 Friction
- **0**: Rambles continuously; ignores cues to wrap; repeats prior points.
- **2**: Wraps when nudged but doesn't self-calibrate.
- **3**: Calibrates length to Q depth most of the time.
- **4**: Adjusts response cadence to interviewer signals; concise by default.
- **5**: Anticipates length needs; surfaces "I'll be brief" framing.

### A.3 Trust
- **0**: Overclaims everything; no specific failures named.
- **2**: Names 1 vague failure; mostly hero narrative.
- **3**: Owns 1-2 concrete failures; calibrated language ("~30%").
- **4**: Names specific failures with context + learning; balanced ownership.
- **5**: Distinguishes "I decided" vs "team decided" sharply; multiple owned failures with high specificity.

### A.4 Predictability
- **0**: Mood / confidence oscillates wildly across phases.
- **2**: Mild inconsistency between phases.
- **3**: Mostly consistent baseline confidence.
- **4**: Stable across all phases regardless of difficulty.
- **5**: Demonstrably calm even during cutoff/interruption.

### A.5 Believability
- **0**: Generic claims throughout. AI-smell density >10%.
- **2**: Mix of specifics + generics. Some named entities.
- **3**: Specifics in 1-2 phases; AI-smell density 2-5%.
- **4**: Specifics throughout; AI-smell density <2%; named entities + metrics + dates.
- **5**: Operationally credible at FAANG-insider level; AI-smell density <0.5%.

---

## Layer B Anchors

### B.1 Product Sense
- **0**: Generic users; no JTBD; no prioritization rationale.
- **2**: Names 1 specific persona; weak JTBD.
- **3**: 2-3 segments MECE; primary segment chosen with reason; JTBD articulated.
- **4**: Multi-persona view with edge cases; JTBD context-bound (situation + struggle + progress).
- **5**: Non-obvious user pains surfaced; reverse-prioritizes obvious solutions; demonstrates taste.

### B.2 Execution
- **0**: "Just ship it." No rollout plan. Ignores operational concerns.
- **2**: Names 1-2 rollout phases. No checkpoints.
- **3**: Phased rollout with checkpoints; 1-2 operational constraints named.
- **4**: Realistic rollout with dependencies, on-call coverage, data quality checks, escalation plan.
- **5**: Demonstrates deep operational fluency; names non-obvious gotchas (e.g., DST handling, locale-specific failures).

### B.3 Strategy
- **0**: Tactics only; no business-model connection.
- **2**: Connects to one strategic lever (e.g., growth).
- **3**: Names competitive dynamics + 1 second-order effect.
- **4**: Articulates strategic tradeoffs (build vs partner, cannibalization, time-to-market vs quality).
- **5**: Frames the strategic question itself; pushes back on assumptions in the prompt.

### B.4 Analytical Thinking
- **0**: Unstructured; jumps between ideas.
- **2**: Some structure but overlapping categories.
- **3**: MECE structure; named assumptions; hypothesis tree.
- **4**: Sensitivity ranges on key estimates; distinguishes correlation/causation; surfaces base rates.
- **5**: Identifies what would falsify the hypothesis; designs experiments to invalidate own claims.

### B.5 Leadership & Collaboration
- **0**: Hero narrative. Generic "I aligned stakeholders."
- **2**: Names 1 specific stakeholder dynamic.
- **3**: Articulates buy-in strategy; gives credit precisely.
- **4**: Owns specific disagreements transparently; demonstrates EQ in stakeholder management.
- **5**: Names systemic team-design decisions; long-term cultural moves.

### B.6 AI Product Judgment
- **0**: "Just add AI to everything." No failure modes.
- **2**: Names 1 failure mode (hallucination).
- **3**: Names 2-3 failure modes; proposes human-review escalation.
- **4**: Calibrates auto vs assistive; trust-building rollout; failure recovery.
- **5**: Deep AI-product fluency — eval frameworks, confidence calibration, human-AI handoff design.

---

## Layer C Anchors (text-derivable subset for V1; full via Gemini A/V)

### C.2 Cognitive Clarity (text-derivable)
- **0**: Stream-of-consciousness; no structure.
- **2**: Implicit structure but no markers.
- **3**: Numbered points; clear phase transitions.
- **4**: MECE structure with explicit signposting ("First X, then Y, finally Z").
- **5**: Anticipates next-level question; surfaces "Three things matter here: X, Y, Z. Let me deep-dive on X first."

### C.4 Pressure Management (partial text-derivable)
- **0**: Panics under pushback; defensive language; overclaims under pressure.
- **2**: Recovers slowly from pushback.
- **3**: Recovers within 1 turn; calibrated hedging.
- **4**: Acknowledges uncertainty without crumbling; "I'd estimate X but want to validate Y."
- **5**: Welcomes pushback; visibly thinks before responding.

### C.7 Interruption Handling (text-derivable when Sage interrupts mid-session)
- **0**: Talks over Sage's orange/red tier interrupt; ignores cutoff.
- **2**: Acknowledges interrupt but loses structure.
- **3**: "Got it — moving on" then advances cleanly.
- **4**: Calm acknowledgment + brief reframing.
- **5**: "Good interruption — let me adjust" + structured pivot.

### C.1, C.3, C.5, C.6 (Gemini-only)
Refer to `prompts/gemini_stage1_video.md` + `prompts/gemini_stage2_audio.md` for measurement specs. Skill defers these dimensions when no Gemini data.

---

## Career-Level Adjustment via signal_weights.yaml

Path: `context/cli/linkright/src/linkright/resume/data/signal_weights.yaml`

Schema:
```yaml
leadership:
  executive: 1.8
  senior: 1.5
  mid: 1.2
  early_career: 0.9
  fresher: 0.7
build-execution:
  executive: 0.7
  senior: 1.2
  mid: 1.3
  early_career: 1.8
  fresher: 2.0
# ... 11 more signals
```

Apply:
```
weighted_score = raw_score × signal_weights[dimension][career_level]
```

### Mapping dimensions → signal_weights keys

| Sage dim | signal_weights key |
|---|---|
| Layer B.1 Product Sense | `user-empathy` |
| Layer B.2 Execution | `build-execution` |
| Layer B.3 Strategy | `strategy-thinking` |
| Layer B.4 Analytical | `data-driven` |
| Layer B.5 Leadership | `leadership` |
| Layer B.6 AI Product Judgment | `ai-product` (V1.1 — add to signal_weights.yaml if absent) |

For Layer A dimensions, use heuristic mapping or treat as uniform (weight=1.0) for V1.

For Layer C dimensions, use `executive-presence` if defined; else weight=1.0.

---

## Personalized Ceiling Computation

For each dimension:
```
ceiling = 5.0 × signal_weights[dim][career_level] / signal_weights[dim]['senior']
```

Normalize to senior-PM baseline. A fresher demonstrating "leadership" at raw_score=3 still earns ceiling-relative recognition.

---

## Output Format (per phase)

```json
{
  "phase_name": "JTBD Articulation",
  "scores": {
    "layer_a": {
      "safety": 4, "friction": 3, "trust": 4, "predictability": 4, "believability": 3
    },
    "layer_b": {
      "product_sense": 4, "execution": 3, "strategy": 3, "analytical": 4,
      "leadership": 3, "ai_judgment": 0
    },
    "layer_c_text_derivable": {
      "cognitive_clarity": 4, "pressure_management": 3, "interruption_handling": 4
    }
  },
  "personalized_ceiling": 4.2,
  "weighted_score": 3.8,
  "tradeoff_credits": [
    "domain bridge: data-driven framing of user pain (phase line 12) carried Product Sense"
  ],
  "anti_pattern_flags": [],
  "notes": ["Strong specificity in metrics", "Weak constraint articulation"]
}
```
