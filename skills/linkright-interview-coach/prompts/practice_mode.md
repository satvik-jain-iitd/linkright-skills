# Practice Mode — Repeat After Me + Best Version + Retry Loop

Triggered when user accepts practice mode offer at the end of Step 9.

Goal: give the candidate two ways to build fluency. In **Repeat After Me mode**, the ideal answer appears on screen immediately after the question is spoken aloud — the candidate reads it, internalizes it, and practices speaking it so they build muscle memory for their own best thinking before any real interview. In **simulation mode**, the candidate answers first in their own words, then sees the ideal answer as the comparison point and receives structured feedback on the gap. Both modes use the same TTS-first question delivery. The candidate chooses which mode at the start of each practice session, or can switch mid-question by typing **show answer** to reveal the ideal version immediately.

---

## Step 10.0 — Mode Selection

Before picking a gap, ask which mode the candidate wants:

```
═══════════════════════════════════════════════════════════════════
              PRACTICE MODE — REPEAT AFTER ME
═══════════════════════════════════════════════════════════════════

How do you want to practice?

  1. REPEAT AFTER ME — Question spoken aloud → ideal answer shown
     immediately on screen → you read and practice saying it.
     Best for: building fluency, internalizing strong structure.

  2. SIMULATION — Question spoken aloud → you answer in your own
     words → ideal answer shown after for comparison + feedback.
     Best for: stress-testing readiness, finding gaps.

  Type 1 or 2 (or switch mid-question with "show answer"):
```

Store selection as `practice_mode_type` in state (`ram` or `sim`).

---

---

## Step 10.1 — Pick Focus Question

Ask user which gap to practice on:

```
═══════════════════════════════════════════════════════════════════
                    PRACTICE MODE
═══════════════════════════════════════════════════════════════════
Retry attempt: {{practice_retries + 1}} / 3

Kis gap pe focus karna hai?

  1. GAP #1 — {{gap_1_name}}  ({{gap_1_phase}}, {{gap_1_layer}})
  2. GAP #2 — {{gap_2_name}}  ({{gap_2_phase}}, {{gap_2_layer}})
  3. GAP #3 — {{gap_3_name}}  ({{gap_3_phase}}, {{gap_3_layer}})
  4. Full interview — sab kuch fresh (same question set, same clock)

Pick 1 / 2 / 3 / 4:
```

Increment `practice_retries` in state file before re-answer begins.

---

## Step 10.2 — Reveal Best Version

Show the "YOUR STRONGEST POSSIBLE VERSION" section from the selected gap's playbook entry (from `lib/improvement_playbook_template.md`). Present it in a distinct block:

```
═══════════════════════════════════════════════════════════════════
       BEST VERSION — RECONSTRUCTED FROM YOUR PROFILE
═══════════════════════════════════════════════════════════════════
(Using: career_level={{career_level}}, top_signals={{top_signals}},
        resume bullets from ~/.linkright/profile/highlights.jsonl)

"{{strongest_possible_version_answer}}"

── WHY THIS WORKS ──────────────────────────────────────────────
  Layer A signal: {{psychological_signal_name}} — {{why}}
  Layer B hit:    {{pm_dimension_name}} — {{why}}
  Layer C shows:  {{presence_dimension_name}} — {{why}}

── KEY MOVES TO INTERNALIZE ────────────────────────────────────
  • {{move_1}} — e.g., "Name constraint BEFORE proposing solution"
  • {{move_2}} — e.g., "Anchor to specific resume bullet: '<quote>'"
  • {{move_3}} — e.g., "One named tradeoff, not two vague ones"

Take a moment to read this. When you're ready, type "ready".
═══════════════════════════════════════════════════════════════════
```

If `voice_enabled=true` → speak: "Yeh hai tumhara best possible version. Padho, internalize karo. Jab ready ho, 'ready' likho."

---

## Step 10.3 — Re-Attempt (Repeat After Me delivery)

When user types "ready":

1. Speak the question via TTS first — always, regardless of mode:
   ```bash
   bash ~/.claude/skills/linkright-interview-coach/scripts/kokoro_speak.sh \
     "{{original_question}}"
   ```

2. Then display the question on screen:
   ```
   ─────────────────────────────────────────────────────────────────
   "{{original_question}}"
   ─────────────────────────────────────────────────────────────────
   ```

3. **If `practice_mode_type = ram` (Repeat After Me mode):**
   Show the ideal answer immediately after the question — on screen, right now, before the candidate says anything. This is the Repeat After Me mechanism: they hear the question, they see the best answer, they read it aloud, they internalize it. Display it as:
   ```
   ═══════════════════════════════════════════════════════════════════
        YOUR BEST VERSION — read this aloud, make it yours
   ═══════════════════════════════════════════════════════════════════
   "{{strongest_possible_version_answer}}"

   ── KEY MOVES ────────────────────────────────────────────────────
     • {{move_1}}
     • {{move_2}}
     • {{move_3}}

   Read it. Say it aloud. When ready for next question, type "next".
   ═══════════════════════════════════════════════════════════════════
   ```
   Do not wait for an answer. Do not score. Move to next question on "next".

4. **If `practice_mode_type = sim` (simulation mode):**
   Do NOT show the ideal answer yet. Show only:
   ```
   Clock: {{practice_budget_min}} min  |  Type "show answer" anytime to reveal ideal version.
   ```
   Wait for the candidate's answer. After they answer, reveal the ideal version for comparison, then go to Step 10.4 for scoring.

5. **If candidate types "show answer" at any point during sim mode:**
   Switch to RAM mode for this question: show the ideal answer immediately, skip scoring for this attempt. Candidate can type "retry" to re-attempt the same question in simulation mode.

6. Start a fresh practice clock via `ScheduleWakeup(delaySeconds=90, ...)` with reason "Practice Mode timer — retry {{practice_retries}}".

7. Patience escalation still active (same tiers from `lib/patience_escalation.md`). Ramble interrupt still active (sim mode only — RAM mode has no answer to interrupt).

---

## Step 10.4 — Re-Score + Delta

After user answers:

Evaluate using same rubrics (`lib/scoring_rubric.md`). Compare against original scores from state. Render delta card:

```
═══════════════════════════════════════════════════════════════════
             PRACTICE MODE — BEFORE vs AFTER
═══════════════════════════════════════════════════════════════════
Gap practiced:   {{gap_name}}
Retry:           {{practice_retries}} / 3

                        BEFORE        AFTER         DELTA
  ─────────────────────────────────────────────────────────────
  {{dim_1}}:          {{b1}}/5       {{a1}}/5       {{d1:+0.0}}
  {{dim_2}}:          {{b2}}/5       {{a2}}/5       {{d2:+0.0}}
  {{dim_3}}:          {{b3}}/5       {{a3}}/5       {{d3:+0.0}}
  ─────────────────────────────────────────────────────────────
  Overall:            {{before_total}}/5  {{after_total}}/5  {{delta_total:+0.0}}

Verdict shift:  {{before_verdict}} → {{after_verdict}}

═══════════════════════════════════════════════════════════════════
```

Then Sage gives 2-3 sentence honest eval:
- What improved (quote the specific phrase that showed it)
- What's still the gap (if any)
- What to do next

If `voice_enabled=true` → speak the delta summary (not the table, just the narrative eval).

---

## Step 10.5 — Loop Decision

After delta card:

```
Ek aur try? (retries left: {{3 - practice_retries}})

  1. Same gap, try again
  2. Different gap — pick another
  3. Full fresh interview
  4. Done — end session
```

- Options 1/2/3 → go back to Step 10.1 (if retries < 3)
- Option 4 OR retries = 3 → end Practice Mode → Sage signs off

If retries = 3, don't offer more — say:
> "3 retries done. Enough for one session — spacing effect works better across days. Save this to story-bank and come back tomorrow."

---

## Variables

- `{{practice_retries}}` — from state file `practice_retries` key (int, starts 0)
- `{{gap_N_name}}`, `{{gap_N_phase}}`, `{{gap_N_layer}}` — from scorecard's playbook entries
- `{{strongest_possible_version_answer}}` — from playbook entry "YOUR STRONGEST POSSIBLE VERSION"
- `{{original_question}}` — from state `current_phase_question`
- `{{practice_budget_min}}` — same as original phase budget
- `{{before_*}}`, `{{after_*}}`, `{{delta_*}}` — computed from original vs re-scored signals

---

## Rules

1. **Never fabricate resume facts** — reconstruction uses ONLY `highlights.jsonl` + `nuggets.jsonl`.
2. **Same rubric, same rigor** — no "nice try" scoring. Be honest about delta.
3. **Voice follows user through practice loop** — every question, every re-announce.
4. **3-retry hard cap** — spacing effect is real; more retries same-session = diminishing returns.
5. **Positive delta ≥ 0.5 on any dim = win** — explicitly call it out. Confidence signal matters.
