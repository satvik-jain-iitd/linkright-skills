# TTS Execution Protocol

Loaded when: wiring up the actual Bash TTS call before any question/greeting/closing, or when the candidate types `slower`, `faster`, or `change voice`.

## Table of contents

- [Core rule](#core-rule) — silent execution discipline
- [macOS commands](#macos-default) — `say` command with quoting rules
- [Rate adjustments](#rate-adjustments) — slower / faster / change voice handlers
- [Windows commands](#windows-fallback) — PowerShell SAPI
- [Linux commands](#linux-fallback) — espeak-ng / spd-say / pico2wave / festival cascade

## Core rule

You are running inside Claude Code CLI, which has direct Bash tool access. You MUST execute every TTS command yourself using the Bash tool — never display a command for the user to paste. The audio must play automatically, without any action from the candidate. Never show the `say` command in chat. Never ask the candidate to run anything.

## macOS default

This session runs on macOS. Default voice: Samantha.

Every question, every time — execute in this exact order:

1. Construct the question as plain text. Strip all markdown. No asterisks, no hashes, no backticks.
2. Escape single quotes: replace each `'` with `'\''` (end-quote, escaped-quote, re-open-quote).
3. Execute via Bash tool (silent — do not display this command in chat):
   ```
   say -v Samantha 'question text here'
   ```
4. After Bash confirms execution, display the question text on screen so the candidate can read along while it plays.
5. Then show ideal answer (practice mode) or wait for candidate response (simulation mode).

Always construct TTS commands dynamically per question. Never hard-code a fixed command.

The same protocol applies to the dynamic round-opener greeting and the dynamic round-closing prompts — not just questions. Anything the interviewer "says" must go through TTS first, then be rendered on screen.

## Rate adjustments

Execute via Bash, store the new rate/voice as the session default for all subsequent TTS calls until the candidate changes it again:

- `slower` typed → `say -v Samantha -r 130 'question text here'`
- `faster` typed → `say -v Samantha -r 210 'question text here'`
- `change voice` typed → `say -v Alex 'question text here'`

Never revert to defaults mid-session — once changed, the new rate/voice sticks.

## Windows fallback

If macOS commands fail (detected via Bash error) or the candidate identifies they are on Windows, execute via Bash tool:

```
powershell -Command "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('question text here')"
```

Same silent execution protocol — never shown to user.

## Linux fallback

If on Linux (detected), try in order via Bash tool until one exits 0:

1. `espeak-ng -s 150 'question text here'`
2. `spd-say 'question text here'`
3. `pico2wave -w /tmp/q.wav 'question text here' && aplay /tmp/q.wav`
4. `echo 'question text here' | festival --tts`

First one that exits 0 is the TTS for this session — store the choice for subsequent calls.

If all four fail: fall back to text-only delivery, notify the candidate once that audio is unavailable, and continue the session without TTS.
