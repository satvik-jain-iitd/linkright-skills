# Gemini Stage 1 — Video-Only Analysis Prompt

Paste-ready prompt for user to run in Google Gemini 3 Pro / 3.1 Pro after uploading their mock-interview video.

Sage renders this with `{{session_id}}` pre-filled before showing user.

---

## User Instructions (shown by Sage before pasting)

```
🎬 STAGE 1: VIDEO-ONLY (BODY LANGUAGE)

Step 1: Open gemini.google.com/app
Step 2: Confirm model = Gemini 3 Pro or Gemini 3.1 Pro (check model dropdown)
Step 3: Click attachment / upload icon → upload your mock-interview video (.mp4/.mov/.webm)
Step 4: Paste the prompt below (already filled with your session ID)
Step 5: Wait for Gemini response — usually 30-90 seconds
Step 6: Copy the JSON output (everything inside the ```json ... ``` fence if present)
Step 7: Return here and paste

Important: Gemini may ask clarifying questions. If it does, tell it "Just analyze
the video per the prompt and output the JSON; ignore any ambiguity by setting
fields to 'unverifiable'."
```

---

## The Prompt (to be pasted into Gemini)

```
You are a senior executive presence coach with 20+ years coaching FAANG PMs.

I have uploaded a VIDEO RECORDING of a mock PM interview. **IGNORE THE AUDIO COMPLETELY. Analyze ONLY visual content** — treat as if the audio is muted.

Evaluate 7 visual dimensions on a 0-5 scale:

1. POSTURE — upright vs slouched · lean-in vs lean-back · head position · shoulder set
2. HAND GESTURES — purposeful framing vs fidgeting / hiding · frequency · congruence with speech beats
3. EYE CONTACT — camera-locked vs wandering vs note-reading · sustained vs darting
4. FACIAL EXPRESSIONS — engagement · neutrality default · micro-expressions (anxiety / contempt / surprise)
5. ENERGY PROJECTION — vitality · "psychological steadiness" · presence vs absence
6. ENVIRONMENT — background tidiness · lighting (face lit vs shadowed) · camera framing · distractions
7. CONFIDENCE CUES — chest open vs closed · brow tension · jaw set · swallowing / throat clearing

For each dimension provide:
- score (integer 0-5; use 0 if unable to confidently identify)
- 2-3 specific timestamp-anchored observations as evidence (e.g., "at 0:23, shoulders dropped noticeably before answering"; if you cannot confidently identify a timestamp, set evidence to "unverifiable" rather than inventing one)

OUTPUT ONLY VALID JSON in this exact format. No prose before or after. No commentary. No code fence preamble.

{
  "session_id": "{{session_id}}",
  "stage": "video_only",
  "scoring": {
    "posture": {"score": 0, "evidence": "..."},
    "hand_gestures": {"score": 0, "evidence": "..."},
    "eye_contact": {"score": 0, "evidence": "..."},
    "facial_expressions": {"score": 0, "evidence": "..."},
    "energy_projection": {"score": 0, "evidence": "..."},
    "environment": {"score": 0, "evidence": "..."},
    "confidence_cues": {"score": 0, "evidence": "..."}
  },
  "top_3_strengths": ["...", "...", "..."],
  "top_3_gaps": ["...", "...", "..."],
  "visual_verdict": "Visually Senior | Visually Mid | Visually Junior | Visually Anxious",
  "specific_drills": [
    {"problem": "...", "drill_30s": "..."},
    {"problem": "...", "drill_30s": "..."},
    {"problem": "...", "drill_30s": "..."}
  ]
}

Replace each "..." with your actual analysis. Replace each 0 with your actual score.
```

---

## Session ID Pre-fill

Before showing this to user, Sage replaces `{{session_id}}` with the actual session ID from state file.

---

## Post-paste Validation

After user pastes JSON back, Sage runs:

```bash
bash ~/.claude/skills/linkright-interview-coach/scripts/validate_gemini_response.sh stage1 <pasted_json_file>
```

Schema check (`state/gemini-response-schemas.json`):
- Required fields present
- Scores within 0-5 range
- `visual_verdict` matches enum
- All 7 dimensions present

If invalid:
> "Gemini returned invalid JSON. Common issues: missing session_id, wrong stage value (must be 'video_only'), missing dimension. Re-run Gemini and tell it: 'You returned invalid JSON; the schema requires fields X, Y, Z. Output only valid JSON.'"

---

## What Gemini's Output Looks Like (example)

```json
{
  "session_id": "abc123",
  "stage": "video_only",
  "scoring": {
    "posture": {
      "score": 3,
      "evidence": "Upright in first 2 minutes; shoulders dropped at 4:15 during product-sense pushback; recovered by 5:00"
    },
    "hand_gestures": {
      "score": 2,
      "evidence": "Hands hidden below frame for most of interview; visible only at 6:30 when explaining diagram"
    },
    "eye_contact": {
      "score": 4,
      "evidence": "Consistent camera-engagement; brief downward glances around 3:20 and 8:45 likely note-checks"
    },
    "facial_expressions": {
      "score": 3,
      "evidence": "Neutral default; brief brow furrow at 5:30; slight smile when discussing strong story at 9:10"
    },
    "energy_projection": {
      "score": 3,
      "evidence": "Steady energy in Phase 1-2; visible fatigue dip at 12:00 onward"
    },
    "environment": {
      "score": 4,
      "evidence": "Clean background; even face lighting; camera at eye level; minor: ceiling light reflection on glasses at 7:00"
    },
    "confidence_cues": {
      "score": 3,
      "evidence": "Open chest posture; mild jaw tension at 4:15 + 11:30 (pushback moments); brow tension brief"
    }
  },
  "top_3_strengths": [
    "Strong eye contact throughout — camera-engaged 80%+ of session",
    "Clean environment with professional lighting and framing",
    "Open body posture in opening phases — projects confidence"
  ],
  "top_3_gaps": [
    "Hands hidden below frame — limits expressiveness and reads as nervous",
    "Energy dropped in second half — visible fatigue affected presence",
    "Brief shoulder slump under pushback moments — signals defensiveness"
  ],
  "visual_verdict": "Visually Mid",
  "specific_drills": [
    {"problem": "Hands hidden", "drill_30s": "Practice answering 1 question with hands at chest level, visible, occasionally gesturing. Record. Watch back."},
    {"problem": "Energy fatigue", "drill_30s": "Pre-interview: 10 minutes of standing posture + breathing exercises to baseline energy. Sit 30s before record."},
    {"problem": "Defensive shoulder posture", "drill_30s": "When you hear pushback, deliberately roll shoulders back + take 2-sec pause. Practice with 5 pushback prompts."}
  ]
}
```

---

## Common Failure Modes

| Gemini behavior | Cause | Fix |
|---|---|---|
| Returns prose instead of JSON | Didn't follow "OUTPUT ONLY JSON" | "Output ONLY valid JSON. No prose. Restart." |
| Invents timestamps | Confusing or short clip | Tell Gemini: "use 'unverifiable' instead of guessing timestamps" |
| Refuses to analyze | Content policy concern | Confirm no PII / shorten clip / try Gemini API directly |
| Skips dimensions | Truncated response | "Output the full JSON. All 7 dimensions required." |
| Wrong session_id | User edit | Re-paste with correct ID |
