# A/V Handoff Instructions — User Guide

This is what Sage shows the user when they opt into A/V coaching at end of interview.

---

## Top-Level Message (shown by Sage)

```
═══════════════════════════════════════════════════════════════════
              A/V COACHING — OFFLINE GEMINI WORKFLOW
═══════════════════════════════════════════════════════════════════

You opted in for full A/V coaching. Here's the flow:

1. You need a recording of yourself doing this mock interview
   (Google Meet recording, Loom, phone camera — any .mp4/.mov/.webm)

2. I'll give you 3 paste-ready Gemini prompts:
   Stage 1 — Body language (video-only, audio muted)
   Stage 2 — Vocal delivery (audio-only)
   Stage 3 — Content depth (transcript-only)

3. You run each one in Google Gemini 3 Pro / 3.1 Pro on your own time.
   - Open: gemini.google.com/app
   - Upload your recording
   - Paste the prompt
   - Wait for JSON response
   - Copy and paste back to me here

4. After I receive each stage, I aggregate into the 4-source holistic
   scorecard. Cross-source asymmetries surface the highest-leverage
   drills — e.g., "you write confidently but speak hesitantly".

Estimated total time: 30-45 min (10-15 min per Gemini stage)

You can:
  - Run all 3 stages now
  - Run 1-2 stages, skip rest
  - Save for later (state will persist in /tmp; resume anytime)

Ready for Stage 1?
```

---

## Privacy Notice (shown after first "Yes")

```
🔒 PRIVACY NOTE:

Your recording stays on YOUR machine. I don't upload anything.
You upload to YOUR Gemini account when ready.

Gemini stores conversation history in your Google account per their
policy. If your recording contains sensitive content (NDAs, internal
strategy, etc.), review Google's data policy first.

For maximum privacy, use Gemini Advanced with the option to delete
data after analysis.

Proceeding with Stage 1.
```

---

## Stage 1 Delivery (Sage to user)

```
═══════════════════════════════════════════════════════════════════
              STAGE 1: VIDEO-ONLY (BODY LANGUAGE)
═══════════════════════════════════════════════════════════════════

USER STEPS:
1. Open gemini.google.com/app
2. Confirm model = Gemini 3 Pro or Gemini 3.1 Pro (top-right dropdown)
3. Click attachment icon → upload your mock-interview video
4. Paste the prompt below (your session ID is pre-filled)
5. Wait for Gemini response (30-90s typically)
6. Copy the JSON output (everything between ```json fences or the raw JSON if no fences)
7. Return here and paste

═══════════════════════════════════════════════════════════════════
              ↓ COPY EVERYTHING BELOW ↓
═══════════════════════════════════════════════════════════════════

[Full prompt from prompts/gemini_stage1_video.md, with {{session_id}} pre-filled]

═══════════════════════════════════════════════════════════════════
              ↑ COPY EVERYTHING ABOVE ↑
═══════════════════════════════════════════════════════════════════

Once Gemini returns JSON, paste it here. I'll validate + advance to Stage 2.
```

User runs Gemini, pastes JSON. Sage validates via `validate_gemini_response.sh`.

If valid: "✅ Stage 1 validated. Saved. Ready for Stage 2?"
If invalid: error message + retry instruction.

---

## Stage 2 Delivery (after Stage 1 success)

```
═══════════════════════════════════════════════════════════════════
              STAGE 2: AUDIO-ONLY (VOCAL DELIVERY)
═══════════════════════════════════════════════════════════════════

USER STEPS:
1. Same Gemini chat (or new — either works)
2. Upload the same file again (or extract audio first if preferred)
3. Paste the prompt below
4. Wait for response
5. Copy JSON → paste back here

═══════════════════════════════════════════════════════════════════

[Full prompt from prompts/gemini_stage2_audio.md, with {{session_id}} pre-filled]

═══════════════════════════════════════════════════════════════════

Paste the JSON here when ready.
```

---

## Stage 3 Delivery (after Stage 2 success)

```
═══════════════════════════════════════════════════════════════════
              STAGE 3: TRANSCRIPT (CONTENT DEPTH)
═══════════════════════════════════════════════════════════════════

USER STEPS:
1. Same Gemini chat
2. Either:
   - Upload same file (Gemini auto-transcribes), OR
   - Ask Gemini: "Transcribe the audio first, then analyze per the prompt"
3. Paste the prompt below — includes your career context for personalized scoring
4. Wait for response
5. Copy JSON → paste back

═══════════════════════════════════════════════════════════════════

[Full prompt from prompts/gemini_stage3_transcript.md, with all {{*}} placeholders pre-filled]

═══════════════════════════════════════════════════════════════════

Paste the JSON here when ready.
```

---

## After All Stages Received

```
═══════════════════════════════════════════════════════════════════
              ALL STAGES RECEIVED — AGGREGATING
═══════════════════════════════════════════════════════════════════

✅ Content (Claude session)
✅ Video (Gemini Stage 1) — Visual verdict: {{stage1_verdict}}
✅ Audio (Gemini Stage 2) — Vocal verdict: {{stage2_verdict}}
✅ Transcript (Gemini Stage 3) — Content verdict: {{stage3_verdict}}

Aggregating into holistic 4-source scorecard. One second.

[Holistic scorecard renders per prompts/final_scorecard_holistic.md]
```

---

## Partial Submission Handling

User can skip stages. Sage handles:

### "I don't have a video"
```
OK. Skipping Stage 1 (Visual). You can still run:
  - Stage 2 (Audio-only) if you have audio
  - Stage 3 (Transcript) if you have either audio or text

Proceeding to Stage 2 — confirm you have audio?
```

### "I don't have any recording"
```
OK. Content-only scorecard already rendered.

Suggestion for next session: record yourself (phone camera is fine).
Then we can run full A/V coaching.

For now, focus on the improvement playbook from content scorecard.
```

### "Skip Stage 3"
```
OK. Aggregating Content + Video + Audio into 3-source scorecard.

Note: Transcript stage gives the deepest narrative analysis; consider
running it next session for full feedback.
```

---

## Resume Flow (if user starts but pauses)

State file `/tmp/mock-interview-state-<uuid>.json` persists Gemini responses already received:

```json
{
  "scoring_gemini": {
    "stage1_video": {...},     // received
    "stage2_audio": null,      // pending
    "stage3_transcript": null  // pending
  },
  "received_ts": {
    "stage1": 1747143500,
    "stage2": null,
    "stage3": null
  }
}
```

User can return hours later, type "resume interview coach" — Sage:
1. Reads state
2. Sees Stage 1 already done
3. Picks up at Stage 2 prompt

---

## Cost Communication

```
💰 COST NOTE:

Gemini 3 Pro free tier covers typical use (3 stages × 1 interview/day).
If you hit limits, you can:
  - Skip Stage 1 (most token-heavy due to video)
  - Wait for daily quota reset
  - Upgrade to Gemini Advanced

This skill itself (Claude side) is part of your existing session — no additional cost.
```

---

## When User Asks "Why 3 Stages?"

```
Why not just 1 combined analysis?

Professional vocal/presentation coaches isolate channels:

1. Video-only (mute audio): forces analysis of ONLY visual cues.
   Eliminates "halo effect" where good vocal masks weak body language.

2. Audio-only (no video): forces ONLY vocal cues. Same logic.

3. Transcript-only (text): forces ONLY content. Same logic.

Aggregating later catches ASYMMETRIES across channels — e.g.,
"Content-Senior + Vocally-Junior" means you write confidently but
speak hesitantly. That specific asymmetry implies a specific drill
that 1-shot analysis would hide.

Cross-source agreement = high-confidence signal.
Cross-source disagreement = highest-leverage feedback.
```
