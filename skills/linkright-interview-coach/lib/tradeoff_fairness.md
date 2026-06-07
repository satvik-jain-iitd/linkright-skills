# Tradeoff-Fair Scoring Rules

Core principle: **Score against candidate's strongest possible version given THEIR background**, not against a generic ideal. Missing X is OK if Y is strong. Reward potential, not perfection.

Research basis: `Research_Linkright/cross_domain_career_transitions_guide.md:31-82` (3-phase transition model) + `signal_weights.yaml` career-level matrix.

---

## Transition Phase Model

Every candidate is in ONE of 3 phases when interviewing for a NEW domain (e.g., IC→PM, B2B→B2C, traditional→AI):

### Phase 1 — Signal Accumulation
**Definition**: Candidate is actively building demonstrable artifacts in the new domain but has yet to ship them at scale or accumulate clear positioning.

**Signals**: 1-2 side projects, 1-2 internal-rotation experiences, < 6 months in target domain.

**Fair expectations**:
- Bridge-narrative articulation expected
- Some absent signals expected and forgiven
- Strong transferable signals from prior domain should be CREDITED, not penalized

### Phase 2 — Bridge Narrative
**Definition**: Candidate has 6-18 months in target domain. Has artifacts but is still positioning vs. seasoned operators.

**Signals**: 1-2 shipped projects in target domain, can articulate bridge narrative confidently.

**Fair expectations**:
- Should articulate WHAT transfers and WHAT they had to learn
- Some hesitation on advanced-domain Qs acceptable
- Should demonstrate growth trajectory (Phase 1 → Phase 2 evidence)

### Phase 3 — Identity Lock
**Definition**: Market sees candidate as a domain practitioner, not a transitioner.

**Signals**: 18+ months at target-domain seniority; resume reads native; references confirm.

**Fair expectations**:
- Full-bar evaluation (no transition adjustments)
- Bridge narrative no longer needed
- Hold to senior-PM standard for their stated level

---

## Bridge-Narrative Bonus

**When applied**: Candidate is in Phase 1 or 2 AND demonstrates HOW prior-domain signal transferred to new-domain question.

**Example**:
- Candidate background: 8 years data analyst → 6 months PM (Phase 1)
- Phase 4 Product Sense Q: "Improve YouTube Premium"
- Weak answer: "Users want X" (generic)
- Bridge-narrative strong: "From my data-analyst background, I'd start by segmenting users by retention cohort — and the 7-30 day cohort has the steepest drop. So my hypothesis is that the value-prop messaging mismatches what users do in week 2-3."

**Scoring impact**: +1.0 raw score on relevant dimension (B.1 Product Sense + B.4 Analytical) before weight applied.

**Caps**:
- Bridge bonus cannot push raw_score above 4.5 (only senior-PM-level analysis with full domain depth earns 5)
- Bonus applies once per phase, not per dimension

---

## Signal-Absence Floor

**When applied**: Candidate is in Phase 1 AND the missing signal is REASONABLE-given-background.

**Example**:
- Candidate background: data-analyst→PM, 6 months in PM role
- Phase Question requires demonstrating large-scale launch experience (B.2 Execution)
- Candidate has no large-scale launch yet — they're in Phase 1

**Scoring impact**: Floor weighted_score for that dimension at 3.0 (instead of 1-2).

**Rationale**: At Phase 1, signal absence is expected, not a defect. Penalize only if Phase 2-3 candidate lacks the signal.

**Limits**:
- Floor applies only to up-to-2 absent signals per session (otherwise becomes "everything's fair")
- Does NOT apply to core PM skills (Cognitive Clarity, Pressure Management) which are level-agnostic

---

## Top-Signal Demonstration Bonus

**When applied**: Candidate demonstrates one of their TOP-3 signals (from `candidate-summary.json`) with high specificity.

**Example**:
- Candidate top signals: `data-driven`, `user-empathy`, `build-execution`
- Phase Q answer demonstrates data-driven thinking with named metrics, sensitivity analysis, and segmentation rigor
- Score impact: ×1.2 multiplier on `data-driven` dimension (B.4 Analytical) — capped at 5.0

**Rationale**: Reward what they're best at; they should over-index on their strengths in interviews.

---

## Career-Level Adjustments (via signal_weights.yaml)

| Career Level | Adjustment philosophy |
|---|---|
| Fresher | Heavy bonus on build-execution, user-empathy, data-driven; heavy discount on leadership, revenue-impact-scale, executive-influence |
| Early career | Moderate bonus on build-execution; moderate discount on executive signals |
| Mid (default) | Balanced; no major adjustment |
| Senior | Bonus on leadership + strategy; expectation of demonstrated execution |
| Executive | Heavy bonus on executive-influence + leadership + revenue-impact; expectation of strategy fluency |

Applied as: `weighted_score = raw_score × signal_weights[dim][career_level]`

---

## Career-Arc Special Cases

### Returner / Career-Re-Entrant
- 1-3 year gap (parental / sabbatical / health / pivot)
- **Adjustment**: Treat as Phase 2 in their stated domain; don't penalize gap-related signal absence
- **What to look for**: How they explain the gap; what they learned in it; how they're re-acclimating

### Startup-to-FAANG transition
- Strong build-execution + user-empathy
- Often weak on scale-execution + cross-functional + measurement rigor
- **Adjustment**: Reward systems thinking emerging from constraint; expect them to learn scale
- **What to look for**: Awareness of what FAANG-scale changes vs. startup-scale

### FAANG-to-startup transition
- Strong measurement + strategy + cross-functional
- Often weak on resourcefulness + multi-hat execution
- **Adjustment**: Reward strategic clarity; expect them to demonstrate operational humility
- **What to look for**: How they handle "we don't have the data" or "no analytics team"

### Consultant-to-PM
- Strong structure + communication + analytical
- Often weak on ownership + execution depth
- **Adjustment**: Reward MECE thinking; expect them to demonstrate end-to-end ownership

---

## Anti-Tradeoff-Abuse Rules

Tradeoff-fair scoring is NOT:
- "Everyone gets a passing grade"
- Generic "potential bonus" without specific transferable signal
- Excusing core PM skill gaps (Cognitive Clarity, Pressure Management)
- Forgiving fabrication or AI-smell (those penalize ALL levels equally)
- Forgiving anti-patterns (defensive responses, blame-shifting)

---

## Output: Tradeoff Credits in Scorecard

For each phase, scorecard lists:

```
TRADEOFF-FAIRNESS CREDITS APPLIED:
- Phase 3 (JTBD): Bridge-narrative bonus +1.0 on B.1 Product Sense — your data-analyst framing of "retention cohort segmentation" transferred well
- Phase 4 (Solutions): Signal-absence floor on B.2 Execution because you're in Phase 1 (6mo PM); large-scale launch absence not penalized
- Phase 5 (Metrics): Top-signal bonus on B.4 Analytical — your sensitivity-analysis instinct earned ×1.2
```

This transparency lets candidate understand WHY their score is what it is, and where they got fair credit for non-traditional background.

---

## End-of-Interview Phase-Progression Coaching

If candidate is Phase 1 or 2:

```
TRANSITION PHASE GUIDANCE:

You're in Phase {{N}}: {{phase_name}}.

To progress to Phase {{N+1}}:
- Ship: <specific artifact suggestion based on absent signals>
- Position: <specific bridge-narrative refinement>
- Practice: <specific drill — e.g., "answer 3 product-sense questions where you DON'T rely on data-analyst framing">

Estimated time to Phase {{N+1}}: <X> months at current pace.
```

This converts the scorecard into a career-development tool, not just an interview verdict.
