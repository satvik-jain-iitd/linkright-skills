# linkright-interview-coach

**Sage** — LinkRight's AI interview expert. FAANG-grade PM mock interview coach.

## What it does

Conducts a personalized, signal-aware, multi-modal mock PM interview that produces an **actionable improvement playbook**.

- User picks ROUND (HR / Behavioral / Culture / Product Sense / Analytical / System Design / Bar Raiser)
- Sage rolls PROBLEM TYPE within the round (random, surprise factor)
- Variable duration per problem type (HR ~15min ... System Design ~50min)
- Autonomous timer with human-realistic patience escalation (🟢→🟡→🟠→🔴)
- 3-layer signal scoring: psychological + PM craft + executive presence
- Tradeoff-fair: personalized ceiling, not generic ideal
- Optional voice mode (Sage speaks via Kokoro TTS)
- Optional A/V coaching via Google Gemini 3 Pro offline handoff (3-stage methodology)
- LinkRight ecosystem integrated (reads profile, writes history, opt-in story bank)

## Quick start

In Claude Code:
```
/linkright-interview-coach
```
or just say:
- "mock interview"
- "Sage, run a mock interview"
- "practice PM interview"
- "FAANG mock"
- "bar raiser practice"

## What you'll need

### Required
- A Claude Code session with `/loop` + `ScheduleWakeup` support
- A LinkRight profile at `~/.linkright/profile/` (or resume PDF for fallback)

### Optional (recommended)
- Kokoro TTS installed for voice mode (`pip install kokoro`)
- Google Gemini access (gemini.google.com) for A/V coaching
- A video recording of yourself doing the mock (any Meet/Loom/phone recording)

## Workflow

1. Sage greets you (Romanized Hindi mix, warm-but-rigorous)
2. Profile loaded from `~/.linkright/profile/` (fallback: PDF or 5-Q chat)
3. You pick the round
4. Sage rolls the problem type
5. You pick text-only or voice-output mode
6. Sage announces problem + duration + difficulty bar
7. You type `/loop` to enable autonomous timer
8. Interview runs (90s timer fires, patience escalates if you over-talk)
9. Content scorecard rendered at end (3-layer signal scores)
10. (Optional) Sage gives you 3 Gemini prompts → you run them on your recording → paste JSON back → holistic scorecard
11. Improvement playbook with **strongest possible version** answers
12. Top 3 drill recommendations for next session
13. Optional: save strong stories to `~/.linkright/story-bank/`

## File structure

```
~/.claude/skills/linkright-interview-coach/
├── SKILL.md                          # main entry (loaded on invocation)
├── README.md                         # this file
├── lib/                              # reference libraries
│   ├── sage_persona.md
│   ├── round_catalogue.md
│   ├── signal_taxonomy.md
│   ├── scoring_rubric.md
│   ├── tradeoff_fairness.md
│   ├── av_projection_rubric.md
│   ├── patience_escalation.md
│   ├── improvement_playbook_template.md
│   ├── linkright_integration.md
│   └── gemini_handoff_guide.md
├── prompts/                          # in-session + Gemini prompt templates
├── state/                            # JSON schemas
└── scripts/                          # bash helpers
```

## Calibration

V1 ships with **Senior PM** difficulty bar (Meta E5 / Google L5). Calibration dial (entry / senior / principal / hostile) coming in V1.1.

## PRD

Full PRD with FRs/NFRs/architecture: `~/Documents/linkright_production/specs/sage-interview-coach-prd.md`

## Status

- V1: Core mock interview with text-only + voice-output + Gemini A/V handoff + LinkRight integration
- V1.1: Calibration dial; closed-loop signal_weights update
- V1.2: Auto-story-bank suggestions
- V2: Bi-directional voice (Whisper STT); multi-language

## Acknowledgments

Built on top of:
- `Research_Linkright/` — signal psychology + executive presence research
- `Roadmap_Linkright/` — closed-loop learning architecture (doc_12, doc_24, doc_26)
- LinkRight CLI's `signal_weights.yaml` — career-level × signal matrix
