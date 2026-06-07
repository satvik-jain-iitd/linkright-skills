# Gemini A/V Handoff Guide + Kokoro TTS Setup

## Why offline Gemini handoff?

Claude (Sage) is text-native. Google Gemini 3 Pro / 3.1 Pro is multi-modal. Sage delegates A/V analysis to Gemini via structured prompts. User runs Gemini themselves; pastes JSON results back. Sage aggregates.

**Privacy**: A/V files stay on user's machine. User uploads to their own Gemini account on their terms.

---

## Prerequisites (user-side)

### For A/V coaching
- Google account with Gemini access (gemini.google.com/app)
- Gemini 3 Pro or Gemini 3.1 Pro (whichever latest at impl time)
- Video recording of mock interview (Meet, Loom, Zoom, phone camera — any .mp4/.mov/.webm)
- Audio extracted (optional — Gemini accepts video and ignores video track if instructed)
- ~30 minutes for 3 stages of analysis

### For voice mode (Sage speaks via Kokoro)
- Kokoro TTS installed locally
- macOS: `afplay` (built-in) for playback
- Linux: `aplay` (alsa-utils) for playback

---

## Sage Voice — 5-Tier Engine Cascade (Free-Local First)

Sage's voice uses a free-first cascade: try local-zero-cost engines BEFORE paid-quota engines. Engine dispatcher: `scripts/kokoro_speak.sh`.

| Tier | Engine | Cost | Setup | Quality |
|---|---|---|---|---|
| **1** | **kokoro-onnx** (default) | Free, local | `pip install kokoro-onnx soundfile` (wheel-only, Python 3.13 compatible) | Very good |
| 2 | kokoro full | Free, local | May require Python 3.12 venv (heavier compile deps) | Excellent |
| 3 | OS-native (`say` macOS / `espeak-ng` Linux) | Free, local | Zero install | OK ("good enough" baseline) |
| 4 | Gemini API native TTS | Uses `GEMINI_API_KEY` quota (free tier exists) | Add key to `~/.linkright/.env`; same key as A/V analysis | Excellent (30 voices) |
| 5 | pyttsx3 | Free, local | `pip install pyttsx3` | Mediocre but always-on |

Sage dispatcher tries 1 → 2 → 3 → 4 → 5 in order; first success wins.

### Why this ordering
- **Tier 1 default**: wheel-only install dodges Python 3.13's `_PyLong_AsByteArray` API breakage that affects spaCy/thinc/blis chain in full kokoro install. Same quality voices, no compile.
- **Tier 3 fallback**: macOS `say` + Linux `espeak-ng` ship with OS. Zero-setup safety net.
- **Tier 4 Gemini**: uses your existing `GEMINI_API_KEY` (same key as Sage's A/V analysis Stages 1/2/3). 30 voices (Kore, Puck, Fenrir, Enceladus, Sulafat, +25 more), 70+ languages, free tier covers daily practice. But uses quota — only fires if all local engines fail.

### Install commands (run once)

**Tier 1 (recommended)**:
```bash
pip install kokoro-onnx soundfile
# Download model weights (one-time, ~330MB):
curl -L -o kokoro-v0_19.onnx https://huggingface.co/hexgrad/Kokoro-82M/resolve/main/kokoro-v0_19.onnx
curl -L -o voices.bin https://huggingface.co/hexgrad/Kokoro-82M/resolve/main/voices.bin
```

**Tier 4 (Gemini TTS)**:
- Already configured if `~/.linkright/.env` has `GEMINI_API_KEY`
- Same key used for A/V Stage 1/2/3 prompts

### Voice profile config

File: `~/.linkright/sage-voice.yaml` — full schema in `state/sage-voice-config-schema.yaml`. Key fields:

```yaml
preferred_tier: 1           # 1-5; cascades downward on failure
voice_id: am_adam           # auto-maps across engines (am_adam → Daniel on macOS / Kore on Gemini)
speed: 1.0
pause_before_pushback_seconds: 2.0
gemini:
  model: gemini-2.5-flash-preview-tts
  api_key_env_var: GEMINI_API_KEY
```

Force-override tier via env: `SAGE_TTS_TIER=4 bash kokoro_speak.sh "..."`

---

## Gemini A/V Workflow (3 stages)

After content-only interview ends, Sage offers A/V coaching. If user says Yes:

### Stage 1 — Video-only (body language)

**User instructions**:
1. Open `gemini.google.com/app` in browser
2. Start new chat
3. Click attachment / upload icon
4. Upload your mock interview video file
5. Paste the prompt Sage gave you (with `{{session_id}}` pre-filled)
6. Wait for Gemini response
7. Copy the JSON output (Gemini may wrap in ```json fences — copy everything between fences, exclude fences themselves)
8. Return to Claude Code and paste

**What Gemini analyzes**: posture, hand gestures, eye contact, facial expressions, energy projection, environment, confidence cues. Audio MUTED in analysis.

**Output**: JSON with 7 scored dimensions + verdict + drills.

### Stage 2 — Audio-only (vocal delivery)

**User instructions**:
1. Same Gemini chat (or new one)
2. Upload same file (or audio-extracted version)
3. Paste Stage 2 prompt
4. Copy JSON output → back to Sage

**What Gemini analyzes**: pace WPM, pace variation, pause quality, filler density, verbosity, tone modulation, energy, authority, breath, volume. Visual IGNORED.

**Output**: JSON with 10 vocal metrics + verdict + drills.

### Stage 3 — Transcript-only (narrative content)

**User instructions**:
1. Gemini auto-transcribes the audio (most reliable)
2. Paste Stage 3 prompt — includes candidate context (career level, signals, round/PT)
3. Copy JSON output → back to Sage

**What Gemini analyzes**: storytelling structure, specificity density, AI-smell, constraints, tradeoffs, framework usage, authenticity, signal density.

**Output**: JSON with 8 content dimensions + missed opportunities + verdict.

---

## Pasting JSON Back to Sage

### Format expected
Sage expects valid JSON. Two acceptable formats:

**Format A**: pure JSON
```
{"session_id": "abc123", "stage": "video_only", "scoring": {...}}
```

**Format B**: with code fence
````
```json
{"session_id": "abc123", "stage": "video_only", "scoring": {...}}
```
````

Sage strips fences if present.

### Validation
Sage validates against `state/gemini-response-schemas.json`. On failure:
- Sage tells user: "JSON didn't match expected schema — common issues: missing session_id, wrong stage name, missing fields. Re-run Gemini with: '<corrective instruction>'."
- User retries

### Partial submission
User can submit subsets:
- Only Stage 2 + 3 (no video recording)
- Only Stage 3 (only transcript)
- All 3 stages

Sage adapts holistic scorecard based on which stages received.

---

## Troubleshooting

### Gemini returns invalid JSON
- Tell Gemini: "Output ONLY valid JSON. No prose before or after. Use the exact schema specified."
- Or: "Try again — JSON failed validation. The schema requires field X."

### Gemini hallucinates timestamps
- Tell Gemini: "If you cannot confidently identify a specific timestamp, set evidence to 'unverifiable' instead of inventing a time."

### Gemini refuses video upload (policy)
- Switch to extracted audio + transcript modes (Stages 2 + 3 only)
- Skip Stage 1

### Kokoro install fails on macOS
- Common cause: missing `espeak` or similar dependency
- Fallback: `pyttsx3` — Sage handles this automatically
- For best quality: install via Docker (`docker pull hexgrad/kokoro`)

### Voice playback silent
- Check system volume + output device
- Test: `afplay /System/Library/Sounds/Glass.aiff` (macOS)
- If Kokoro generates WAV but no playback: check `afplay` permission

---

## Why 3 Stages (and not 1 combined)?

Professional vocal/presentation coaching practice isolates channels:

1. **Video-only (audio muted)**: Forces analyst to evaluate ONLY visual cues. Eliminates "halo effect" where good vocal masks weak body language.
2. **Audio-only (video off)**: Forces analyst to evaluate ONLY vocal cues. Same logic.
3. **Transcript-only (text)**: Forces analyst to evaluate ONLY content. Same logic.

Aggregating later catches **asymmetries**:
- Content-Senior + Vocally-Junior → "you write confidently but speak hesitantly"
- Vocally-Senior + Visually-Anxious → "voice is steady but body shows nerves"
- Visually-Senior + Content-Generic → "you look senior but answers are surface-level"

Each asymmetry implies a different drill. Combined analysis would hide these signals.

---

## When to use voice mode vs A/V mode

| Mode | When to use |
|---|---|
| **Text-only** (default) | Quick practice, no setup, async-friendly |
| **Voice-output (Kokoro)** | Listen to Sage's Qs aloud; practice composing oral answers; lower-friction immersion |
| **A/V handoff (Gemini)** | Full-fidelity coaching; user records themselves on Meet/Loom and gets body-language + vocal + transcript analysis |

These compose:
- Text-only + A/V handoff = strong middle path
- Voice-output + A/V handoff = closest to real interview feel
- Voice-output alone (no recording) = practice without rigorous A/V scoring

---

## Cost considerations

| Item | Cost (user-side) |
|---|---|
| Sage skill itself | Free (text via Claude session) |
| Kokoro TTS | Free (local, no API) |
| Gemini 3 Pro free tier | Typically sufficient for 3 stages per interview |
| Gemini paid tier | Optional; needed only for high-volume practice |
| Storage for recordings | User's local disk (~50-200MB per interview) |

---

## V2 path

When Whisper STT is integrated (V2), Sage can:
- Accept user's spoken answers via mic
- Transcribe in real-time
- Score Layer C vocal dimensions natively (no Gemini handoff needed for audio)
- Real-time bi-directional voice conversation with Sage

V2 still benefits from Gemini for video analysis (until Claude gains multimodal video).
