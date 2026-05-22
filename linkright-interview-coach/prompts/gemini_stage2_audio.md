# Gemini Stage 2 — Audio-Only Analysis Prompt

Paste-ready for Google Gemini 3 Pro / 3.1 Pro. Analyzes vocal delivery from audio (or video with visuals ignored).

---

## User Instructions (shown by Sage before pasting)

```
🎙  STAGE 2: AUDIO-ONLY (VOCAL DELIVERY)

Step 1: Same Gemini chat (or new one) — gemini.google.com/app
Step 2: Confirm model = Gemini 3 Pro / 3.1 Pro
Step 3: Upload the SAME file (or extracted audio — Gemini accepts both)
Step 4: Paste the prompt below
Step 5: Wait for response
Step 6: Copy JSON output → paste back here

If Gemini transcribes silently or runs out of context, ask: "Output ONLY the
JSON per the schema; don't transcribe or commentate."
```

---

## The Prompt (to be pasted into Gemini)

```
You are a senior vocal coach who has trained 500+ executives for high-stakes interviews and earnings calls.

I have uploaded an AUDIO RECORDING (or video — IGNORE VISUALS COMPLETELY; analyze ONLY audio track).

Evaluate 10 vocal dimensions. For some, provide raw numbers. For all, provide 0-5 score.

1. PACE — words per minute (estimate over entire recording). Target 130-150 wpm.
2. PACE VARIATION — does speaker change pace deliberately for emphasis vs monotone speed?
3. PAUSE QUALITY — strategic pauses (2s+ before answering) vs nervous gaps vs zero pauses (rushed)
4. FILLER DENSITY — count "um", "uh", "like", "you know", "basically", "kind of", "sort of" per minute. Provide the 3 most-used fillers.
5. VERBOSITY — answer length proportional to question complexity, or rambling/under-utilizing?
6. TONE MODULATION — pitch variation, monotone vs sing-songy vs balanced
7. ENERGY PROJECTION (vocal) — vitality, audible engagement, tension or release
8. AUTHORITY — falling intonation at sentence-end (assertive) vs rising (uncertain) · decisive vs hedge
9. BREATH CONTROL — controlled breathing vs audible gasping vs shallow chest breathing
10. VOLUME STABILITY — consistent vs trailing-off-at-sentence-end

For each dimension provide:
- score (integer 0-5)
- 2-3 specific time-anchored observations or pattern descriptions (if you cannot confidently identify timestamps, describe the pattern instead)

OUTPUT ONLY VALID JSON in this exact format. No prose before or after.

{
  "session_id": "{{session_id}}",
  "stage": "audio_only",
  "scoring": {
    "pace_wpm": 0,
    "pace_variation": {"score": 0, "evidence": "..."},
    "pause_quality": {"score": 0, "evidence": "..."},
    "filler_density_per_min": 0.0,
    "filler_top_3": ["um", "like", "you know"],
    "verbosity": {"score": 0, "evidence": "..."},
    "tone_modulation": {"score": 0, "evidence": "..."},
    "energy_projection_vocal": {"score": 0, "evidence": "..."},
    "authority": {"score": 0, "evidence": "..."},
    "breath_control": {"score": 0, "evidence": "..."},
    "volume_stability": {"score": 0, "evidence": "..."}
  },
  "top_3_strengths": ["...", "...", "..."],
  "top_3_gaps": ["...", "...", "..."],
  "vocal_verdict": "Vocally Senior | Vocally Mid | Vocally Junior | Vocally Anxious",
  "specific_drills": [
    {"problem": "...", "drill_30s": "..."},
    {"problem": "...", "drill_30s": "..."},
    {"problem": "...", "drill_30s": "..."}
  ]
}

Replace each "..." with actual analysis. Replace numeric placeholders with actual numbers.
```

---

## Session ID Pre-fill

Sage replaces `{{session_id}}` before showing user.

---

## Post-paste Validation

```bash
bash ~/.claude/skills/linkright-interview-coach/scripts/validate_gemini_response.sh stage2 <pasted_json_file>
```

Schema check (`state/gemini-response-schemas.json`):
- All 10 dimension fields present
- `pace_wpm` is integer or float
- `filler_density_per_min` is float
- `filler_top_3` is array of 3 strings
- `vocal_verdict` matches enum

---

## Example Output

```json
{
  "session_id": "abc123",
  "stage": "audio_only",
  "scoring": {
    "pace_wpm": 168,
    "pace_variation": {
      "score": 2,
      "evidence": "Mostly uniform pace at 168 wpm throughout; brief slowdown to ~140 wpm at 3:20 during clarification request"
    },
    "pause_quality": {
      "score": 2,
      "evidence": "Few deliberate pauses; tends to start answering within 0.5s of question end; nervous gap at 7:15 (4-second silence after pushback)"
    },
    "filler_density_per_min": 4.2,
    "filler_top_3": ["like", "basically", "you know"],
    "verbosity": {
      "score": 3,
      "evidence": "Phase 1-2 answers proportional; Phase 4 over-extended; Phase 5 under-utilized"
    },
    "tone_modulation": {
      "score": 3,
      "evidence": "Some variation; tends toward monotone in technical phases; lifts when discussing user impact"
    },
    "energy_projection_vocal": {
      "score": 3,
      "evidence": "Steady energy first half; visible vocal fatigue from 12:00 onward"
    },
    "authority": {
      "score": 2,
      "evidence": "Rising intonation at sentence-ends consistently (e.g., 4:30, 6:15, 9:50); hedge density high"
    },
    "breath_control": {
      "score": 3,
      "evidence": "Mostly controlled; audible breath at 5:20 + 11:30 (pushback moments)"
    },
    "volume_stability": {
      "score": 3,
      "evidence": "Stable in first half; trailing off at sentence-end pattern from 10:00 onward"
    }
  },
  "top_3_strengths": [
    "Stable volume in opening 10 minutes",
    "Pace slowed appropriately during clarification request — shows responsiveness",
    "Energy lifts noticeably when discussing user impact — authentic engagement signal"
  ],
  "top_3_gaps": [
    "Pace too fast (168 wpm — target 140); reads as rushed",
    "Rising intonation at sentence-end consistently — undermines authority",
    "Filler density 4.2/min — practice replacing with deliberate 1-2 sec pauses"
  ],
  "vocal_verdict": "Vocally Junior",
  "specific_drills": [
    {"problem": "Pace too fast", "drill_30s": "Read your strongest paragraph at 140 wpm metronome cue; record + listen + adjust; daily for 7 days"},
    {"problem": "Rising intonation", "drill_30s": "Pick 5 declarative sentences; practice with deliberate falling intonation at sentence-end; record + compare to confident reference speaker"},
    {"problem": "Filler density", "drill_30s": "Practice 60-sec answer with deliberate 2-sec pauses replacing 'like'/'basically'; silence > filler"}
  ]
}
```

---

## Common Failure Modes

| Issue | Fix |
|---|---|
| WPM seems off | Ask Gemini: "Verify your WPM estimate — count words spoken and divide by audio minutes" |
| Filler list missing | "List the top 3 most-used fillers exactly as heard" |
| Verdict not from enum | "Verdict must be one of: Vocally Senior, Vocally Mid, Vocally Junior, Vocally Anxious" |
| Filler density string instead of number | "filler_density_per_min must be a number, not a string" |
