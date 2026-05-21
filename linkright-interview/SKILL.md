---
name: linkright-interview
description: |
  LinkRight Interview Engine — two modes in one skill. BUILD mode: constructs STAR-L story
  bank from linkright-mem facts, generates layered question banks per JD/archetype, drafts
  tell-me-about-yourself intros, builds salary negotiation scripts from user_setup.md.
  SIMULATE mode: live interview simulation with OS-native TTS (plays question aloud before
  showing text), "Repeat After Me" ideal answer display for practice, Socratic follow-up
  probing, and silent coaching log written to disk per-turn. All outputs run through
  constraint validation (Truth Engine). Integrates bidirectionally with linkright-mem
  (reads facts/signals, saves finalized stories to expressions/stories/).

  Use when user says: /linkright-interview, "interview prep", "mock interview", "practice
  interview", "build story bank", "STAR stories", "prepare for interview at [company]",
  "tell me about yourself", "salary negotiation", "stress test my story",
  "simulate an interview round", or any interview preparation request.
---

# LinkRight Interview

SKILL_DIR  = `~/.claude/skills/linkright-interview`
MEM_DIR    = `~/.linkright/memory`
SETUP      = `~/.linkright/user_setup.md`
PIPELINE   = `~/Downloads/Mission Job Switch/job scraping/memory/pipeline.json`
STORIES    = `~/.linkright/memory/expressions/stories`

---

## Absolute Rules

- NEVER fabricate candidate experience — every story traces to a confirmed fact in mem or user-provided
- NEVER mark a story clean if constraint validation found violations
- ALWAYS run constraint validation (Truth Engine) before saving any story
- NEVER say "I am excited to apply" or any generic opener in TMAY scripts
- NEVER speak coaching feedback via TTS — only questions/prompts to interviewer persona
- ALWAYS check `SETUP` for `hard_constraints`, `do_not_mention`, `current_ctc` before generating salary script
- ALWAYS load mem profile before generating questions, stories, or TMAY
- NEVER deliver below the STAR-L format for any story: Situation → Task → Action → Result → Learning (L optional for delivery, mandatory for building)

---

## Gate 0 — Mode Fork

```
AskUserQuestion:
  question: "What do you need today?"
  options:
    A) BUILD — stories, question bank, TMAY intro, salary script
    B) SIMULATE — live interview with questions spoken aloud, ideal answers shown
```

---

## BUILD PATH

---

## Build Gate 1 — Load Context

```bash
# Load high-strength signals
python3 ~/.claude/skills/linkright-mem/scripts/grep_memory.py \
  --query "strength:high" \
  --memory ~/.linkright/memory \
  --format json

# Summary stats
python3 ~/.claude/skills/linkright-mem/scripts/grep_memory.py \
  --memory ~/.linkright/memory
```

If facts.md empty → ask user to paste resume text, extract bullets as raw facts, proceed.

### JD source (for question bank + story matching)
1. Active pipeline opportunity → pick ID
2. Paste JD text directly
3. Skip — build generic story bank

### Build sub-mode selection
```
AskUserQuestion:
  question: "Which do you need?"
  options:
    a) Build STAR stories from my experience
    b) Generate question bank for a specific JD
    c) Draft answer to a specific question
    d) Build tell-me-about-yourself intro
    e) Build salary negotiation script
    f) Stress-test a story I already have
    g) Run full mock (BUILD path — structured, with scoring)
```

---

## Build Gate 2 — Story Building (mode a)

### STAR-L Format (mandatory for building, L optional for delivery)

```
SITUATION:   Context — company stage, team size, period (2 sentences max)
TASK:        What was specifically yours to own (never "we")
ACTION:      What YOU specifically did — decisions, tradeoffs navigated, why
RESULT:      Quantified where possible; user_estimate OK, label it honestly
LEARNING:    One honest takeaway — mandatory for building, helps you catch weak stories
```

**Defensibility rule before saving:** Can you answer both:
1. "Why that approach specifically?"
2. "What would you do differently?"
If no → flag as needs strengthening, do NOT save yet.

### Story Types (8 — need ≥2 per type for strong bank)

| Story Type | Core Test |
|---|---|
| ambiguity_handling | Operate without clear direction |
| stakeholder_conflict | Navigate org complexity |
| data_driven_decision | Data vs intuition balance |
| failure_learning | Self-awareness + resilience |
| cross_functional_leadership | Lead without authority |
| systems_thinking | Sees whole system |
| customer_obsession | Users are real, not abstract |
| vision_prioritization | Long-term thinking under pressure |

### Story Generation Loop (per story type)

1. Find best supporting fact cluster from mem for this story type:
   ```bash
   python3 ~/.claude/skills/linkright-mem/scripts/grep_memory.py \
     --query "<story_type_keywords>" \
     --memory ~/.linkright/memory \
     --format json
   ```
2. Draft STAR-L story using only confirmed facts
3. Show draft: "Does this accurately represent what happened?"
4. User corrects factual inaccuracies — update draft
5. Run Truth Engine (Build Gate 3 — Constraint Validation)
6. If clean → save to `~/.linkright/memory/expressions/stories/<story-type>_<slug>_<YYYYMMDD>.md`

### Story File Format
```markdown
---
id: ambiguity_handling_001
story_type: ambiguity_handling
signals_demonstrated: [systems_thinking, execution_rigor]
constraint_status: clean
created: 2026-05-22
---

**STAR-L**

**Situation:** ...
**Task:** ...
**Action:** ...
**Result:** ...
**Learning:** ...

**Delivery version (L dropped):**
<natural spoken prose, 90-120 seconds>
```

---

## Build Gate 3 — Constraint Validation (Truth Engine)

Runs on every story before save.

```bash
python3 ~/.claude/skills/linkright-mem/scripts/constraint_checker.py \
  --text '<story_text>' \
  --constraints ~/.linkright/user_setup.md
```

Manual checks (if constraint_checker unavailable):

```
CHECK 1: Hard constraints
  → Read SETUP hard_constraints
  → Flag: work listed as NOT-OWNED or DO-NOT-CLAIM
  → Flag: any name in do_not_mention

CHECK 2: Metric defensibility
  → "significantly improved" without a number → flag
  → "dramatically reduced" without evidence → flag
  → Any metric user cannot defend if probed → flag

CHECK 3: Ownership clarity
  → "We built..." without specifying YOUR role → flag
  → Claiming team outcomes as personal → flag

CHECK 4: Defensibility self-test
  → Answer "Why that approach?" right now
  → Answer "What would you do differently?" right now
  → If either answer vague → flag
```

Block story save if any flag unresolved.

---

## Build Gate 4 — Question Bank (mode b)

Given JD + archetype (from Gate 1):

**Layer 1 — Universal PM (always generated):**
- Tell me about yourself
- Why this company / why this role
- Biggest product failure + what you learned
- How do you prioritize competing requests
- How do you work with engineers when they push back
- Tell me about a data-driven decision you made
- How do you know a product is successful
- Tell me about a time you led without authority
- Biggest cross-functional challenge
- Where do you see yourself in 3 years

**Layer 2 — Archetype-specific:**
- `ai_enterprise_pm`: model evaluation tradeoffs, AI trust UX, prompt system design, build-vs-buy AI infra
- `founding_pm`: zero-to-one stories, "no resources" decisions, when to pivot vs persist
- `growth_pm`: experiment design, metric tradeoffs, growth loop design, attribution problems
- `analytics_pm`: SQL/data fluency, metric definition, dashboard design philosophy
- `csm_implementation`: onboarding complex enterprise clients, handling scope creep, escalation management
- `consumer_pm`: user research methods, retention vs acquisition tradeoff, viral loop design

**Layer 3 — JD-derived:**
Extract specific scenarios from JD text → generate likely behavioral questions.
e.g. "JD: 'leading across 5+ teams'" → "Tell me about a time you aligned multiple teams on a shared priority."

**Layer 4 — Company-stage:**
- Early-stage: "How do you prioritize with no data?" / "Tell me about working with limited resources"
- Enterprise: "How do you drive change in a complex org?" / "Tell me about managing stakeholder politics"

For each question: show best matching story from existing story bank. Flag if no good match → story gap.

---

## Build Gate 5 — Tell Me About Yourself (mode d)

Structure (90-120 seconds spoken):
```
PAST:    "[X] years in [domain] — brief thread of what you've been building toward"
PRESENT: "Currently/most recently — [strongest signal] at [company]"
TARGET:  "I'm specifically interested in [company] because [real specific reason — not 'mission']]"
HOOK:    "[One sentence connecting your past to this exact opportunity + invites follow-up you're ready for]"
```

Rules:
- Must signal target archetype in first 2 sentences
- Must cite something specific about the company (product, decision, challenge — never "I admire your mission")
- Hook must invite a follow-up you have a strong story ready for
- Speak it aloud → if > 120 seconds → cut ruthlessly

Generate one version per active archetype in user_setup.md (or per active application if pipeline provided).

---

## Build Gate 6 — Salary Negotiation (mode e)

Load from SETUP:
- `current_ctc`
- `target_ctc_min`
- `target_ctc_target`

Never hardcode numbers. Never invent if SETUP missing — ask user directly.

**Opening (when asked "what are your expectations?"):**
```
"I'm currently at [current_ctc]. For this role and seniority level,
I'm targeting [target_ctc_target]. Does that work within your range?"
```

**If pushed below target_min:**
```
"I appreciate the context. Before I can say whether there's flexibility,
could you walk me through the full package — base, equity, and bonus?
I want to evaluate total compensation."
```

**If they reveal range first:**
- Range includes target → anchor at TOP of range
- Range below target_min → "That's a bit below what I was targeting — is there flexibility, or should we talk about other parts of the package?"

**Hard rules:**
- NEVER volunteer a lower number to "seem reasonable"
- NEVER say "I'm flexible" without anchoring first
- NEVER negotiate against yourself before they've made an offer

---

## Build Gate 7 — Stress Test (mode f)

User provides an existing story. Run it through:

1. **Constraint validation** (Build Gate 3)
2. **Follow-up simulation** (2 rounds):
   - "Why that approach specifically?"
   - "What would you do differently?"
   - "Can you walk me through the data behind that result?"
   - "Who else was involved — what was your specific contribution?"
3. **Weakness finder:** "What's the weakest claim in this story?"
4. **Rewrite offer:** If story fails under pressure — offer targeted rewrite

Show pass/fail verdict per check. No flattery. Specific fixes only.

---

## BUILD PATH DELIVERY

Show complete story bank status:
```
STORY BANK STATUS
Total stories: X / 16 minimum (2 per type × 8 types)

ambiguity_handling:    2 ✓
stakeholder_conflict:  1 ✗ (need 1 more)
data_driven_decision:  0 ✗ (need 2)
...

Strong bank threshold: 16 stories. Current: X.
```

---

## SIMULATE PATH

---

## Simulate Gate 1 — Pre-flight

Load profile:
```bash
python3 ~/.claude/skills/linkright-mem/scripts/grep_memory.py \
  --query "strength:high" \
  --memory ~/.linkright/memory \
  --format json

python3 ~/.claude/skills/linkright-mem/scripts/consistency_scorer.py \
  --signals ~/.linkright/memory/signals.md \
  --archetype "<detected_or_asked>" \
  --format json
```

Load story bank:
```bash
ls ~/.linkright/memory/expressions/stories/
```

Load JD (same sources as Build Gate 1).

Render setup summary (≤7 lines on screen, full analysis in coaching log):
```
Candidate: <Name> → <Target Role> at <Company>
Archetype: <detected>  Level: <IC3/4/5/6>
Signals: <top 3>       Gaps: <missing>
Story bank: <N stories loaded>
Log path: interview_session/coaching_log_<YYYYMMDD-HHMM>.md

Rounds: 1) HR Screen  2) Hiring Manager  3) Case/Analytical  4) Technical/CTO  5) Founder/Exec
Type round number to begin.
```

Create coaching log:
```bash
mkdir -p interview_session
# Write frontmatter + Session Profile section with full analysis
```

---

## Simulate Gate 2 — Round Setup

On round selection: write pre-round inference log to coaching log (background bash, never on screen).

```
AskUserQuestion:
  question: "Mode?"
  options:
    Practice — ideal answer shown after each question. Read it aloud, type 'next'.
    Simulation — you answer first. Feedback written silently to log. I ask follow-ups.
```

Deliver interviewer greeting via TTS before text appears.

Round durations:
- HR screen: 20-30 min
- Hiring Manager: 45-60 min
- Technical/CTO: 45-60 min
- Founder/Exec: 30-45 min
- Case: 45-60 min

---

## Simulate Gate 3 — TTS Protocol

**Speak via TTS (mandatory — before text appears):**
- Interviewer greeting
- Interview questions
- Follow-up probes
- Round-closing question

**Never speak via TTS:**
- Session status, nav prompts, mode confirmations
- Anything coaching-flavored
- The ideal answer (candidate reads it aloud themselves)

macOS:
```bash
say -v Samantha '<question text with '\'' escaped>'
# Commands: slower → -r 130, faster → -r 210, change voice → -v Alex
```

---

## Simulate Gate 4 — Interview Loop

### Practice mode (per question)

1. Generate question (reason internally about signal coverage, remaining time, last answer)
2. TTS speaks question
3. Display question text
4. Display ideal answer as **verbatim spoken prose** — 1-3 short paragraphs, natural speech, no tables, no labels, no structural annotations
   - If answer uses info NOT on resume: `⚑ Note: this answer uses info not on your resume — they'll probe it fresh.`
5. Background bash append to coaching log (structured two-column format + inference update)
6. Wait for `next` (or command)

### Simulation mode (per question)

1. Generate question
2. TTS speaks question
3. Display question text
4. Wait for candidate answer
5. On receipt: background bash append (candidate answer + KEEP/CUT/ADD/GOLD/TONE/TIME + structured ideal + inference update)
6. On screen: nothing — next question IS the acknowledgement
7. ~50% probability follow-up after substantive answers (probe weakest claim or vaguest moment)

### Interviewer thinking (before each question, internal only)

- Primary goal of this round right now
- Which hiring risk: capability / execution / interpersonal / organizational
- Which signals still absent or unconfirmed
- What the last answer revealed → what to probe
- Which resume claim needs pressure testing
- Remaining time budget (manage privately, never tell candidate)

### Follow-up rules

- After any claim: probe with "Why that approach specifically?" or "What was your contribution vs the team's?"
- If signal absent after 2 attempts: go after it directly
- Watch for operational specificity vs polished vagueness — call it out in follow-up

---

## Simulate Gate 5 — Ideal Answer Construction

Every ideal answer = strongest version of what THIS candidate can truthfully say. Never fabricated. Every story traces to mem facts or user-provided.

**Structure (prose delivery version):**
1. Direct declarative sentence — main point first, no hedging
2. One sentence: situation context
3. One sentence: tension / stakes / what was at risk
4. 2-3 sentences: specific actions in "I" (candidate's decisions, not team's)
5. One sentence: result with metric (user_estimate OK, label it)
6. One sentence: bridge to this company's specific context

**On screen (practice mode):** plain prose only — no tables, no labels, no intent annotations  
**In coaching log:** two-column table (Structural intent | Script) + additional-info flags in left column

---

## Simulate Gate 6 — Coaching Log Protocol

**File:** `interview_session/coaching_log_<YYYY-MM-DD-HHMM>.md`

Create on session start with frontmatter + `## Session Profile` (full analysis).

Per-turn append (background bash, `run_in_background: true`):
```bash
cat >> "interview_session/coaching_log_<timestamp>.md" <<'EOF'

### Q<n>: <question>
**Asked:** <question text>
**Candidate answer:** <text or "(skipped — practice mode)">
**Feedback:** KEEP: ... | CUT: ... | ADD: ... | GOLD: ... | TONE: ... | TIME: ...
**Ideal (structured):** <two-column table>
**Inference:** <2-4 lines assessor note, first-person>
EOF
```

**Six feedback codes (KEEP/CUT/ADD/GOLD/TONE/TIME):**
- KEEP: quote specific line/metric that landed + why
- CUT: filler, defensive phrasing, tangent, over-explanation
- ADD: missing metric, missing tradeoff, missing company bridge
- GOLD: single most quotable sentence to own by real interview
- TONE: pace, hedging, trailing endings, defensive opens
- TIME: over/under appropriate length for seniority

---

## Simulate Gate 7 — Round Close + Debrief

Every round ends with TTS closing question:
- HR: "...any questions about the role, the team, or the process?"
- HM: "...about the team or how we actually work?"  
- Founder: "...about the company, the vision, or what comes next?"
- CTO: "...about the architecture, the stack, or how engineering operates?"

If candidate says "no questions" → note in log (at mid+ levels reads as disengaged).

On screen after round:
```
Strength: <one sentence>
Risk: <one sentence>
Fix before real interview: <one specific action>
Full debrief: interview_session/coaching_log_<timestamp>.md#round-<n>-debrief
```

Full debrief written to coaching log under `### Debrief`.

Close menu:
```
1. Practice another round
2. End session and generate final scorecard
```

---

## Simulate Gate 8 — Final Scorecard

On screen only:
```
Answer Quality:
  Signal coverage:     <Strong / Solid / Developing / Needs Work>
  Specificity:         <...>
  Ownership clarity:   <...>
  Narrative structure: <...>
  Authenticity:        <...>

Strongest asset: <one sentence>
Primary risk: <one sentence>
Pre-interview action: <one specific action>

Full scorecard: interview_session/coaching_log_<timestamp>.md#final-scorecard
```

### Save to story bank offer
"Want to save any answer as a STAR story for linkright-sync? Yes / No"

If yes:
1. User picks which answer
2. Run Truth Engine (Build Gate 3)
3. If clean → save to `~/.linkright/memory/expressions/stories/`

---

## Simulate Commands

| Command | Action |
|---------|--------|
| `next` | Move to next question |
| `skip` | Skip this question, no feedback |
| `again` | Re-execute TTS for last question |
| `easier` | Scaffold before re-asking |
| `harder` | Force follow-up after next answer |
| `show answer` | Display ideal answer (switches to practice for this Q) |
| `slower` | TTS at -r 130 |
| `faster` | TTS at -r 210 |
| `change voice` | Switch to -v Alex |
| `pause` | Hold |
| `resume` | Continue |
| `debrief` | Surface 3-line debrief now |
| `show log` | Print coaching log path |
| `stop` | Jump to scorecard immediately |

---

## Cost Policy

- ZERO extra Claude API billing — stay within Claude Code subscription
- No subagent dispatches via Agent() tool
- No external Anthropic API calls
- State in coaching log file — read deltas, not full history

---

## Scripts Reference

| Script | Purpose |
|---|---|
| `scripts/constraint_validator.py` | Truth Engine for story validation |
| `scripts/story_saver.py` | Save finalized STAR-L story to expressions/stories/ |
| `scripts/question_bank_generator.py` | Generate layered question bank from JD + archetype |

---

## Phase Status

| Feature | Status |
|---|---|
| BUILD path (story bank, Q bank, TMAY, salary, stress-test) | ✅ This SKILL.md |
| SIMULATE path (TTS interview, coaching log, practice/sim modes) | ✅ This SKILL.md |
| linkright-mem integration (load facts/signals, save stories) | ✅ |
| linkright-hunt pipeline.json integration | ✅ |
| constraint_validator.py | ⏳ build |
| story_saver.py | ⏳ build |
| question_bank_generator.py | ⏳ build |
| references/ref_01_story_bank.md | ⏳ auto-generated on first story save |
| references/ref_02_question_bank.md | ⏳ build |
