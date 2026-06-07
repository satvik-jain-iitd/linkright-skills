# 3-Layer Signal Game Taxonomy

Research foundation: `Research_Linkright/` corpus. Cite file:line where applicable.

PM interviews are evaluated on THREE simultaneous layers. Most candidates only optimize for Layer B. Sage scores all three.

---

## Layer A — Psychological (5 dimensions)

**Source**: `Research_Linkright/interview_psychology_and_decision_influence_system.md:78-155`

> "Interviewers do not only evaluate: answers, experience, technical skill. They also continuously evaluate: emotional signals, perceived risk, cognitive ease, communication friction, familiarity, trustworthiness, behavioral consistency, confidence calibration, social comfort." (line 22)

> "Many hiring decisions are emotionally formed before they are rationally justified."

### A.1 Safety
**What it measures**: Does interviewer feel "this person feels safe to work with"?
**Strong signals**: Calm tone, no defensiveness when challenged, admits uncertainty without crumbling, doesn't trash past employers, gracious under pushback.
**Weak signals**: Defensive language ("but...", "actually..."), blame-shifting, sharpness when challenged, over-justification.
**Text-derivable proxies**: hedge density, blame-language detection, defensive phrasing patterns.

### A.2 Friction
**What it measures**: Would working with this person create friction?
**Strong signals**: Concise answers, listens to follow-up before re-elaborating, accepts redirection gracefully, calibrates response length to question depth.
**Weak signals**: Rambling, over-explaining, ignoring interviewer cues, repeating points the interviewer already heard.
**Text-derivable proxies**: word count vs question complexity, ramble count, redundancy.

### A.3 Trust
**What it measures**: Would interviewer trust this person with their team / their P&L?
**Strong signals**: Acknowledges constraints, names specific failure modes from past work, owns mistakes, calibrated confidence.
**Weak signals**: Overclaiming impact, vague responsibility ("the team did X"), avoiding ownership questions.
**Text-derivable proxies**: ownership language ("I decided" vs "we did"), specific-failure mentions, calibration phrases ("I'd estimate ~30%").

### A.4 Predictability
**What it measures**: Does this person seem predictable under pressure?
**Strong signals**: Stable cadence, doesn't oscillate between bravado and hedging, consistent confidence level across phases.
**Weak signals**: Spikes of anxiety, mood swings within response, inconsistent self-positioning (e.g., humble in Phase 1 then grandiose in Phase 3).
**Text-derivable proxies**: cross-phase confidence variance, hedge-word frequency variance.

### A.5 Believability
**What it measures**: Does this person feel believable?
**Strong signals**: Specific names, dates, metrics, concrete operational details. Realistic complexity in stories. Admits "I don't know" naturally.
**Weak signals**: Generic claims ("massive impact", "scaled to millions"), no specifics, perfect-narrative arcs (no nuance / no failure), AI-smell.
**Text-derivable proxies**: specificity density, AI-smell density, named-entity count.

**Research quote** (line 50-75): "Most candidates optimize only for information. Strong candidates optimize for perception... Even if both have similar competence, Candidate B often feels safer and more senior. Perception strongly influences hiring."

---

## Layer B — Role Craft Evaluation (6 dimensions)

**Source**: `Research_Linkright/product_manager_case_interview_master_system.md:85-226`

### B.1 Product Sense
**What it measures**: User empathy, prioritization instinct, product intuition.
**Strong signals**: Specific user context with JTBD, prioritizes ruthlessly with rationale, surfaces non-obvious user pains, sees the product through multiple personas' eyes.
**Weak signals**: Generic users ("busy professionals"), feature lists without prioritization, no JTBD articulation, missing edge personas.

### B.2 Execution
**What it measures**: Operational thinking, rollout realism, debugging instinct.
**Strong signals**: Rollout plan with checkpoints, names operational constraints (data quality, on-call coverage, dependencies), realistic timeline estimates, identifies leading vs lagging metrics.
**Weak signals**: "Just ship it", no rollout plan, ignores operational complexity, fantasy timelines.

### B.3 Strategy
**What it measures**: Systems thinking, market reasoning, business understanding.
**Strong signals**: Connects product decisions to business model, names competitive dynamics, surfaces second-order effects, articulates strategic tradeoffs.
**Weak signals**: Tactics without strategy, ignores market context, no business-model awareness.

### B.4 Analytical Thinking
**What it measures**: Structured reasoning, estimation, evidence-based thinking.
**Strong signals**: MECE structure, named assumptions with sensitivity ranges, hypothesis tree before deep-dive, distinguishes correlation vs causation.
**Weak signals**: Unstructured reasoning, overlapping categories, ignores base rates, single-anchor estimates without sensitivity.

### B.5 Leadership & Collaboration
**What it measures**: Emotional maturity, cross-functional effectiveness, influence without authority.
**Strong signals**: Names specific stakeholder dynamics, articulates how they built buy-in, owns disagreements transparently, gives credit precisely.
**Weak signals**: Generic "I aligned stakeholders", vague disagreement handling, hero-narrative ("I single-handedly...").

### B.6 AI Product Judgment (2026-specific)
**Source**: lines 508-537 of same doc.
**What it measures**: Trust systems, failure modes, confidence calibration, human-override design for AI features.
**Strong signals**: Names specific failure modes (hallucination, bias, latency, cost), proposes human-review escalation, articulates trust-building strategy, calibrates auto vs assistive.
**Weak signals**: "Just add AI to everything", ignores failure modes, no human override path, over-automation.

**Research quote** (lines 674-688): "What interviewers actually remember: clarity of thinking, calm prioritization, realistic judgment, tradeoff awareness, communication quality, operational maturity. Strong PMs feel believable."

---

## Layer C — Executive Presence (7 dimensions)

**Source**: `Research_Linkright/executive_presence_and_behavioral_signaling_system.md:42-443`

> "Executive presence is primarily about reducing perceived uncertainty. The goal is not performance. The goal is psychological steadiness." (line 42)

### C.1 Behavioral Stability
**What it measures**: Pacing control, non-reactivity, calm under fire.
**Strong signals**: Steady cadence, doesn't speed up under pushback, returns to baseline tone after challenge.
**Weak signals**: Speeds up when challenged, voice shake, defensive acceleration.
**Where measured**: Gemini Stage 1 (video) + Stage 2 (audio); text-derivable via cadence patterns.

### C.2 Cognitive Clarity
**What it measures**: Structure, prioritization, transitions.
**Strong signals**: Numbered structure ("Three things: first, second, third..."), clear transitions, MECE framing.
**Weak signals**: Unstructured stream-of-consciousness, lost transitions, repetition.
**Where measured**: Content + Transcript (Stage 3).

### C.3 Social Calibration
**What it measures**: Eye contact, interruption handling, respectful disagreement.
**Strong signals**: Holds eye contact 70%/30% (speaking/listening), acknowledges interruption gracefully, disagrees without combative posture.
**Weak signals**: Avoids eye contact, defensive disagreement, talks over interviewer.
**Where measured**: Stage 1 (video) + Stage 2 (audio) for tone; text-derivable for disagreement framing.

### C.4 Pressure Management
**What it measures**: Pause discipline, uncertainty handling.
**Strong signals**: 2s+ pause before complex answers, "Let me think" without panic, "I'd estimate ~30% but want to validate" calibration.
**Weak signals**: Rushes to fill silence, panic-answers, overclaims certainty under pressure.
**Where measured**: Stage 2 (audio — pause distribution); text-derivable via hedge calibration.

### C.5 Vocal Presence
**What it measures**: Moderate pace, stable volume, controlled breathing, deliberate emphasis.
**Strong signals**: 130-150 wpm, stable volume, falling intonation at sentence end (authority), low vocal tension.
**Weak signals**: <120 wpm (sluggish) or >170 wpm (rushed), volume trailing off, rising intonation (uncertainty), vocal tension.
**Where measured**: Stage 2 (audio) — ONLY measurable via Gemini.

### C.6 Remote Behavior
**What it measures**: Camera engagement, stable posture, minimal distraction.
**Strong signals**: 70% camera (when speaking), 30% listening, stable posture, minimal swivel, neutral background.
**Weak signals**: Watching own video, frequent off-camera glances, leaning out of frame.
**Where measured**: Stage 1 (video) — ONLY measurable via Gemini.

### C.7 Interruption Handling
**What it measures**: Calm acknowledgment + structured reframing after interruption.
**Strong signals**: "Good point — let me reframe" + brief pause + continues.
**Weak signals**: Panic-defensiveness, talks over, loses structure.
**Where measured**: Stage 1 (video) + Stage 2 (audio); also text-derivable when Sage interrupts mid-session (orange/red tier).

---

## Cross-Layer Aggregation (for final scorecard)

For each layer:
- Sum dimension scores
- Apply career-level weights from `signal_weights.yaml` (see `scoring_rubric.md`)
- Compute personalized ceiling

For overall verdict:
- Layer A weight: 30% (psychological + believability)
- Layer B weight: 50% (role craft — primary)
- Layer C weight: 20% (executive presence — V1 partial measurement)

Note: When A/V coaching via Gemini is done, Layer C measurement becomes complete. Without Gemini, Layer C scored only on text-derivable subset (C.2 Cognitive Clarity + C.4 Pressure Management subset + C.7 Interruption Handling).

---

## Anti-Patterns (auto-penalty conditions)

- **AI-smell density > 5%** of generic phrases per 100 words → Layer A.5 Believability ≤ 2
- **Zero constraints named in 25+ min answer** → Layer B.2 Execution ≤ 2
- **Zero tradeoffs articulated in 25+ min answer** → Layer B.3 Strategy ≤ 2
- **Ramble interrupt triggered 2+ times** → Layer A.2 Friction ≤ 2
- **Hard cutoff (red tier) hit 2+ times** → Layer C.4 Pressure Management ≤ 2
- **Defensive language pattern (>3 hedges + counter-arguments)** → Layer A.1 Safety ≤ 2

---

## Tradeoff-Fair Adjustments

Apply per `lib/tradeoff_fairness.md`:
- Transition phase 1-2 candidates: bridge-narrative bonus, signal-absence floor
- Top-3 signals demonstrated powerfully: ×1.2 multiplier (capped at 5.0)
- Career-level multipliers via `signal_weights.yaml`
