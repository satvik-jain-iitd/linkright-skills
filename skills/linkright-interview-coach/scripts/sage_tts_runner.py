#!/usr/bin/env python3
"""
sage_tts_runner.py — Safe Python TTS runner for kokoro_speak.sh.

Replaces inline `python3 -c "..."` heredocs in kokoro_speak.sh that interpolated
shell variables ${TEXT} / ${VOICE_ID} / ${out_wav} directly into Python source.
That pattern enabled arbitrary code execution via apostrophe injection in user
text (verified PoC by adversarial reviewer):

    SAGE_TTS_TIER=1 bash kokoro_speak.sh "x', voice='am_adam'); __import__('os').system('touch /tmp/PWNED'); a=kokoro.create('y"

This script accepts text/voice/output_path via argv (no shell interpolation),
so user text cannot escape into Python source.

Usage:
    python3 sage_tts_runner.py <engine> <text> <voice_id> <output_path>

    engine: kokoro_onnx | pyttsx3

Exit codes:
    0 = success (audio written)
    1 = engine unavailable or error
    2 = invalid arguments
"""

import os
import sys
from pathlib import Path


def run_kokoro_onnx(text: str, voice_id: str, output_path: str) -> int:
    """Tier 1: kokoro-onnx (neural local)."""
    try:
        from kokoro_onnx import Kokoro
        import soundfile as sf
    except ImportError as e:
        print(f"kokoro-onnx unavailable: {e}", file=sys.stderr)
        return 1

    model_path = str(Path.home() / ".cache" / "kokoro" / "kokoro-v0_19.onnx")
    voices_path = str(Path.home() / ".cache" / "kokoro" / "voices.bin")
    if not Path(model_path).exists() or not Path(voices_path).exists():
        print(f"Kokoro model files missing at {Path(model_path).parent}", file=sys.stderr)
        return 1

    # Kokoro v0.19 has no Indian voices; map common Sage voices to closest neural
    voice_map = {
        "Rishi": "am_adam",
        "Veena": "af_nicole",
        "Lekha": "af_nicole",
        "Samantha": "af_nicole",
        "Daniel": "am_adam",
        "Karen": "bf_emma",
    }
    kokoro_voice = voice_map.get(voice_id, voice_id)
    if not kokoro_voice.startswith(("af_", "am_", "bf_", "bm_")):
        kokoro_voice = "af_nicole"

    try:
        kokoro = Kokoro(model_path, voices_path)
        samples, sample_rate = kokoro.create(
            text, voice=kokoro_voice, speed=1.0, lang="en-us"
        )
        sf.write(output_path, samples, sample_rate)
    except Exception as e:
        print(f"kokoro-onnx synthesis failed: {e}", file=sys.stderr)
        return 1

    return 0


def run_pyttsx3(text: str, voice_id: str) -> int:
    """Tier 3: pyttsx3 (wraps OS-native TTS)."""
    try:
        import pyttsx3
    except ImportError as e:
        print(f"pyttsx3 unavailable: {e}", file=sys.stderr)
        return 1

    # voice_id passed through to OS-native engine name (Daniel/Samantha/Rishi/Veena)
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 165)
        # Try to find matching voice by name
        for v in engine.getProperty("voices"):
            v_name = getattr(v, "name", "") or ""
            v_id_str = getattr(v, "id", "") or ""
            if voice_id and (voice_id in v_name or voice_id.lower() in v_id_str.lower()):
                engine.setProperty("voice", v.id)
                break
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"pyttsx3 synthesis failed: {e}", file=sys.stderr)
        return 1

    return 0


def main() -> int:
    if len(sys.argv) < 3:
        print(
            "Usage: python3 sage_tts_runner.py <engine> <text> [voice_id] [output_path]",
            file=sys.stderr,
        )
        return 2

    engine = sys.argv[1]
    text = sys.argv[2]
    voice_id = sys.argv[3] if len(sys.argv) > 3 else ""
    output_path = sys.argv[4] if len(sys.argv) > 4 else ""

    if engine == "kokoro_onnx":
        if not output_path:
            print("kokoro_onnx requires output_path argument", file=sys.stderr)
            return 2
        return run_kokoro_onnx(text, voice_id, output_path)
    elif engine == "pyttsx3":
        return run_pyttsx3(text, voice_id)
    else:
        print(f"Unknown engine: {engine}. Use kokoro_onnx | pyttsx3", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
