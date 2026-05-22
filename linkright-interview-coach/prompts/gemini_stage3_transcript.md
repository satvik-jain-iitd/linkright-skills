# Gemini Stage 3 — Transcript Content Analysis Prompt

Paste-ready for Google Gemini 3 Pro / 3.1 Pro. Analyzes narrative content (transcript). Complementary to Sage's in-session text analysis — Gemini's deeper read provides validation + new insights.

---

## User Instructions (shown by Sage before pasting)

```
📝  STAGE 3: TRANSCRIPT (CONTENT DEPTH)

This stage analyzes the WORDS only — what you said, how you structured, signal density.

Step 1: Same Gemini chat. Confirm model = Gemini 3 Pro / 3.1 Pro.
Step 2: Either:
        Option A: Upload the audio/video again — Gemini will auto-transcribe
        Option B: Ask Gemini "Transcribe the audio first, then analyze per prompt"
        Option C: If you already have a transcript, paste it before the prompt
Step 3: Paste the prompt below (already filled with your context)
Step 4: Copy JSON output → paste back here
```

---

## The Prompt (to be pasted into Gemini)

```
You are a senior PM hiring manager at a FAANG company who has interviewed 1000+ PM candidates.

Below is the TRANSCRIPT of a mock PM interview. Analyze ONLY the content — IGNORE delivery (delivery is analyzed separately).

CANDIDATE CONTEXT (for personalized scoring):
- Career level: {{career_level}}
- Top demonstrable signals: {{top_signals}}
- Round: {{round_name}}
- Problem type: {{problem_type_name}}
- Question: "{{question}}"
- Transition phase: {{transition_phase}} (1 = signal accumulation, 2 = bridge narrative, 3 = identity lock, null = not transitioning)

Evaluate 8 content dimensions on a 0-5 scale, calibrated to candidate's career level (not generic ideal):

1. STORYTELLING STRUCTURE — STAR adherence, narrative arc, beginning/middle/end
2. SPECIFICITY DENSITY — concrete metrics, names, dates, places, operational details
3. AI-SMELL DETECTION — generic phrases ("leverage synergies", "drive impact", "robust solution") · polished but vague
4. CONSTRAINT ARTICULATION — were budget/time/team/data/tech/regulatory constraints named?
5. TRADEOFF ARTICULATION — were tradeoffs explicitly stated with reasoning?
6. FRAMEWORK USAGE — MECE, structured thinking, clear phases
7. AUTHENTICITY — bridge narratives where applicable · ownership · admission of failures/uncertainty
8. SIGNAL DENSITY — top PM signals demonstrated: Product Sense, Execution, Strategy, Analytical, Leadership, AI Product Judgment (0-5 per signal)

For each main dimension provide: score + 2-3 specific quoted excerpts from the transcript as evidence.

Additionally, identify 3-5 MISSED OPPORTUNITIES: moments where the candidate could have surfaced a stronger framing.

OUTPUT ONLY VALID JSON in this exact format. No prose before or after.

{
  "session_id": "{{session_id}}",
  "stage": "transcript_content",
  "scoring": {
    "storytelling_structure": {"score": 0, "evidence_quotes": ["...", "..."]},
    "specificity_density": {"score": 0, "examples_of_specifics": ["...", "..."], "density_percent": 0.0},
    "ai_smell_density": {"score": 0, "generic_phrases_found": ["...", "..."], "density_percent": 0.0},
    "constraints_named_count": 0,
    "constraints_named_examples": ["...", "..."],
    "tradeoffs_named_count": 0,
    "tradeoffs_named_examples": ["...", "..."],
    "framework_usage": {"score": 0, "evidence": "..."},
    "authenticity": {"score": 0, "evidence": "..."},
    "signal_density": {
      "product_sense": 0,
      "execution": 0,
      "strategy": 0,
      "analytical": 0,
      "leadership": 0,
      "ai_judgment": 0
    }
  },
  "top_3_strengths": ["...", "...", "..."],
  "top_3_gaps": ["...", "...", "..."],
  "content_verdict": "Content Senior | Content Mid | Content Junior | Content Generic",
  "missed_opportunities": [
    {
      "moment": "Phase N — when interviewer asked X",
      "what_was_said": "<quoted user response>",
      "what_could_have_been_said_at_their_level": "<reconstructed stronger version, using candidate's career-level-appropriate strength>"
    }
  ]
}

Replace each "..." and 0 with actual analysis.
```

---

## Variable Substitution by Sage

Before showing this prompt to user, Sage fills:
- `{{session_id}}` from state file
- `{{career_level}}` from candidate-summary
- `{{top_signals}}` from candidate-summary (array as string)
- `{{round_name}}`, `{{problem_type_name}}`, `{{question}}` from state
- `{{transition_phase}}` from candidate-summary

---

## Post-paste Validation

```bash
bash ~/.claude/skills/linkright-interview-coach/scripts/validate_gemini_response.sh stage3 <pasted_json_file>
```

Schema check:
- All 8 dimensions present
- `signal_density` has all 6 sub-fields
- `missed_opportunities` is array (≥3 entries preferred)
- `content_verdict` matches enum

---

## Example Output (excerpt)

```json
{
  "session_id": "abc123",
  "stage": "transcript_content",
  "scoring": {
    "storytelling_structure": {
      "score": 3,
      "evidence_quotes": [
        "Phase 1 had clear STAR setup: 'In Q3 2024, we were facing 40% drop in onboarding completion...'",
        "Phase 3 lost narrative thread; jumped between solutions without grounding in user pain"
      ]
    },
    "specificity_density": {
      "score": 4,
      "examples_of_specifics": [
        "'Snowflake pipeline'",
        "'team of 6 engineers'",
        "'Q3 2024 launch'",
        "'reduced p99 latency from 800ms to 120ms'"
      ],
      "density_percent": 14.2
    },
    "ai_smell_density": {
      "score": 4,
      "generic_phrases_found": ["drive impact"],
      "density_percent": 0.8
    },
    "constraints_named_count": 2,
    "constraints_named_examples": [
      "6-engineer team capacity",
      "no labeled preference data yet"
    ],
    "tradeoffs_named_count": 1,
    "tradeoffs_named_examples": [
      "'I chose mobile-only over web to ship faster, sacrificing reach for speed'"
    ],
    "framework_usage": {
      "score": 4,
      "evidence": "MECE in Phase 1 (3 segments named clearly); structured tradeoff framing in Phase 4"
    },
    "authenticity": {
      "score": 4,
      "evidence": "Admitted uncertainty on Phase 5 metrics ('I'd estimate ~30%, want to validate'); owned Phase 3 launch failure"
    },
    "signal_density": {
      "product_sense": 4,
      "execution": 3,
      "strategy": 3,
      "analytical": 4,
      "leadership": 3,
      "ai_judgment": 0
    }
  },
  "top_3_strengths": [
    "High specificity density (14%) anchors answers in operational reality",
    "Authentic admission of uncertainty + owned failures — Believability signal strong",
    "MECE structure in Phase 1 — Cognitive Clarity clear from text alone"
  ],
  "top_3_gaps": [
    "Only 1 tradeoff named in 45-min interview — Strategy signal under-demonstrated",
    "Narrative thread lost in Phase 3 — Cognitive Clarity drop mid-interview",
    "AI Product Judgment dimension absent — Q didn't directly require it but bridge-narrative chance missed"
  ],
  "content_verdict": "Content Mid",
  "missed_opportunities": [
    {
      "moment": "Phase 2 — when asked about user segmentation",
      "what_was_said": "Users are busy professionals trying to manage their finances",
      "what_could_have_been_said_at_their_level": "Given my data-analyst background, I'd start by segmenting on retention-cohort behavior — specifically the 7-30 day cohort where onboarding completion correlates with first-deposit conversion. Within that cohort, the highest-LTV sub-segment is salaried professionals between 25-35 who use 3+ payment apps. That's my primary user."
    },
    {
      "moment": "Phase 4 — when proposing solutions",
      "what_was_said": "We could add personalized recommendations and improve the welcome flow",
      "what_could_have_been_said_at_their_level": "Two improvements, both within Q4 with our 6-eng team. First, v0 personalization using existing Snowflake events (~2wk build), constraint: no labeled data so v0 ranks by cohort behavior not personal signal. Second, A/B test welcome flow against current 24-hr activation — target +5% over 8 weeks. I'd hold the line on adding steps; my data-analyst instinct says friction reduction beats personalization for Phase 1."
    }
  ]
}
```

---

## Why This Stage Is Distinct from Sage's In-Session Analysis

Sage already evaluates content during the interview. Why also run Gemini Stage 3?

Reasons:
1. **Cross-validation** — Gemini's independent read catches what Sage missed mid-flow
2. **Deeper specificity computation** — Gemini computes density % over full transcript, more accurate than Sage's running estimate
3. **Missed-opportunity reconstruction** — Gemini specifically generates the "what could have been said" alternative for each weak moment, anchored to candidate's career level
4. **Signal density across 6 PM dimensions** — Gemini gives fine-grained scoring per dimension on full transcript context

Cross-source agreement (Content + Transcript both flag a gap) → higher-confidence playbook entry.
Cross-source disagreement (Sage flagged, Gemini didn't) → investigate; might be Sage false-positive.

---

## Common Failure Modes

| Issue | Fix |
|---|---|
| Returns analysis but no transcript | Ask: "Transcribe first, then analyze per the prompt" |
| Skips signal_density sub-fields | "All 6 signal_density fields required: product_sense, execution, strategy, analytical, leadership, ai_judgment" |
| Density % missing | "Include density_percent field for specificity and ai_smell" |
| missed_opportunities empty | "Provide at least 3 missed opportunity entries" |
