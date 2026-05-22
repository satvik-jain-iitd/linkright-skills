#!/usr/bin/env python3
"""
gemini_tts.py — Generate audio via Gemini API native TTS

Per adversarial review #5: API key now sent via x-goog-api-key HEADER (not URL
query string), and redacted in any error path. Previous version embedded key
in URL and leaked it via urlopen error messages.

Usage:
    python3 gemini_tts.py "<text>" "<voice_id>" "<output_path>"

Env vars:
    GEMINI_API_KEY — Required. From ~/.linkright/.env or shell env.
    GEMINI_TTS_MODEL — Optional. Default: gemini-2.5-flash-preview-tts

Returns:
    Exit 0 on success (audio written to output_path)
    Exit 1 on failure (error logged to stderr with key redacted)
"""

import os
import re
import sys
import json
import base64
import wave
import urllib.request
import urllib.error
from pathlib import Path


GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
_KEY_REGEX = re.compile(r'AIza[0-9A-Za-z\-_]{20,}')


def redact(text: str) -> str:
    """Redact any Google API key (AIza...) from log output."""
    return _KEY_REGEX.sub("AIza...[REDACTED]", text)


def load_env_from_file(env_path: Path) -> None:
    """Load KEY=VALUE pairs from a .env file into os.environ (if not already set)."""
    if not env_path.exists():
        return
    try:
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            # Strip whitespace + quotes + whitespace-inside-quotes
            value = value.strip().strip('"').strip("'").strip()
            if key and key not in os.environ:
                os.environ[key] = value
    except Exception as e:
        print(f"WARN: Could not load env file {env_path}: {e}", file=sys.stderr)


def main():
    if len(sys.argv) < 4:
        print("Usage: python3 gemini_tts.py <text> <voice_id> <output_path>", file=sys.stderr)
        return 1

    text = sys.argv[1]
    voice_id = sys.argv[2]
    output_path = sys.argv[3]

    home = Path.home()
    load_env_from_file(home / ".linkright" / ".env")

    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not set. Add to ~/.linkright/.env or shell env.", file=sys.stderr)
        return 1

    # Sanity-validate key shape before sending (prevents control chars / spaces in URL/header)
    if not re.match(r'^AIza[0-9A-Za-z\-_]{20,}$', api_key):
        print("ERROR: GEMINI_API_KEY has unexpected format (should start with 'AIza' + alphanumeric/_/-).", file=sys.stderr)
        return 1

    model = os.environ.get("GEMINI_TTS_MODEL", "gemini-2.5-flash-preview-tts")

    payload = {
        "contents": [{
            "parts": [{"text": text}]
        }],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "voiceConfig": {
                    "prebuiltVoiceConfig": {
                        "voiceName": voice_id
                    }
                }
            }
        }
    }

    # API key in header (NOT URL query), per security review
    url = f"{GEMINI_API_BASE}/{model}:generateContent"

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key,
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            response_data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        print(f"ERROR: Gemini API HTTP {e.code}: {redact(error_body)}", file=sys.stderr)
        return 1
    except urllib.error.URLError as e:
        print(f"ERROR: Network error: {redact(str(e))}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"ERROR: Unexpected: {redact(str(e))}", file=sys.stderr)
        return 1

    try:
        candidates = response_data.get("candidates", [])
        if not candidates:
            print(f"ERROR: No candidates in response: {redact(json.dumps(response_data))[:500]}", file=sys.stderr)
            return 1
        parts = candidates[0].get("content", {}).get("parts", [])
        audio_part = None
        for part in parts:
            inline_data = part.get("inlineData") or part.get("inline_data")
            if inline_data and inline_data.get("data"):
                audio_part = inline_data
                break
        if not audio_part:
            print(f"ERROR: No audio data in response: {redact(json.dumps(response_data))[:500]}", file=sys.stderr)
            return 1

        audio_b64 = audio_part["data"]
        mime_type = audio_part.get("mimeType") or audio_part.get("mime_type", "audio/L16;rate=24000")
        audio_bytes = base64.b64decode(audio_b64)
    except Exception as e:
        print(f"ERROR: Could not parse audio from response: {redact(str(e))}", file=sys.stderr)
        return 1

    sample_rate = 24000
    if "rate=" in mime_type:
        try:
            sample_rate = int(mime_type.split("rate=")[1].split(";")[0])
        except Exception:
            pass

    try:
        with wave.open(output_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(audio_bytes)
    except Exception as e:
        print(f"ERROR: Could not write WAV: {e}", file=sys.stderr)
        return 1

    print(f"OK: Generated {output_path} ({len(audio_bytes)} bytes raw PCM, {sample_rate} Hz)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
