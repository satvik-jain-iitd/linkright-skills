#!/usr/bin/env bash
# kokoro_speak.sh — Sage's TTS engine dispatcher
#
# Default voice: Rishi (Indian English male, macOS native — ships free).
# Engine cascade (native-first, paid always last):
#   Tier 1: macOS say / espeak-ng / Windows PowerShell — OS native, zero setup
#   Tier 2: kokoro-onnx (free local neural — better quality than pyttsx3, needs model download)
#   Tier 3: pyttsx3 (Python wrapper around OS native — lower quality fallback)
#   Tier 4: Gemini API (PAID, opt-in only — always last)
#
# Usage: bash kokoro_speak.sh "<text>" [voice_id]

set -eu

TEXT="${1:-}"
VOICE_ID_ARG="${2:-}"

if [ -z "${TEXT}" ]; then
    echo "ERROR: text required. Usage: bash kokoro_speak.sh \"<text>\" [voice_id]" >&2
    exit 1
fi

OUT_DIR="/tmp/sage-tts"
mkdir -p "${OUT_DIR}"

if command -v shasum >/dev/null 2>&1; then
    TEXT_HASH=$(echo -n "${TEXT}${VOICE_ID_ARG}" | shasum -a 256 | awk '{print substr($1, 1, 12)}')
else
    TEXT_HASH=$(echo -n "${TEXT}${VOICE_ID_ARG}" | md5 -q 2>/dev/null || echo -n "${TEXT}${VOICE_ID_ARG}" | md5sum | awk '{print substr($1, 1, 12)}')
fi

CONFIG_FILE="${HOME}/.linkright/sage-voice.yaml"
CONFIG_TIER=""
CONFIG_VOICE=""
if [ -f "${CONFIG_FILE}" ]; then
    CONFIG_TIER=$(grep -E "^preferred_tier:" "${CONFIG_FILE}" 2>/dev/null | head -1 | awk -F': ' '{print $2}' | tr -d ' "')
    CONFIG_VOICE=$(grep -E "^voice_id:" "${CONFIG_FILE}" 2>/dev/null | head -1 | awk -F': ' '{print $2}' | tr -d ' "')
fi

if [ -n "${VOICE_ID_ARG}" ]; then
    VOICE_ID="${VOICE_ID_ARG}"
elif [ -n "${CONFIG_VOICE}" ]; then
    VOICE_ID="${CONFIG_VOICE}"
else
    VOICE_ID="Rishi"
fi

TIER="${SAGE_TTS_TIER:-${CONFIG_TIER}}"

play_wav() {
    local wav_path="$1"
    if command -v afplay >/dev/null 2>&1; then
        afplay "${wav_path}"
        return 0
    elif command -v aplay >/dev/null 2>&1; then
        aplay "${wav_path}"
        return 0
    elif command -v ffplay >/dev/null 2>&1; then
        ffplay -nodisp -autoexit -loglevel quiet "${wav_path}"
        return 0
    fi
    return 1
}

# Tier 1: OS-native TTS — macOS say, Windows PowerShell, Linux espeak-ng/espeak (zero setup)
try_tier_1() {
    if command -v say >/dev/null 2>&1; then
        say -v "${VOICE_ID}" -r 165 "${TEXT}"
        echo "PLAYED tier-1 macOS say (${VOICE_ID})" >&2
        return 0
    fi
    # Windows PowerShell (Git Bash / MSYS2 / WSL boundary check)
    if command -v powershell.exe >/dev/null 2>&1; then
        powershell.exe -Command "Add-Type -AssemblyName System.Speech; \$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; \$s.Rate = 2; \$s.Speak('${TEXT}')" 2>/dev/null && {
            echo "PLAYED tier-1 Windows PowerShell SpeechSynthesizer" >&2
            return 0
        }
    fi
    if command -v espeak-ng >/dev/null 2>&1; then
        espeak-ng -s 165 "${TEXT}"
        echo "PLAYED tier-1 espeak-ng" >&2
        return 0
    elif command -v espeak >/dev/null 2>&1; then
        espeak -s 165 "${TEXT}"
        echo "PLAYED tier-1 espeak" >&2
        return 0
    fi
    return 1
}

# Tier 2: kokoro-onnx (neural local, better quality — delegates via argv — no shell injection)
try_tier_2() {
    if ! python3 -c "import kokoro_onnx" 2>/dev/null; then
        return 1
    fi
    local out_wav="${OUT_DIR}/sage-kokoro-onnx-${TEXT_HASH}.wav"
    local script_dir
    script_dir="$(dirname "$0")"
    if [ ! -f "${out_wav}" ]; then
        python3 "${script_dir}/sage_tts_runner.py" kokoro_onnx "${TEXT}" "${VOICE_ID}" "${out_wav}" 2>/dev/null || return 1
    fi
    if [ -f "${out_wav}" ] && play_wav "${out_wav}"; then
        echo "PLAYED tier-2 kokoro-onnx" >&2
        return 0
    fi
    return 1
}

# Tier 3: pyttsx3 (Python wrapper around OS-native — delegates via argv — no shell injection)
try_tier_3() {
    if ! python3 -c "import pyttsx3" 2>/dev/null; then
        return 1
    fi
    local script_dir
    script_dir="$(dirname "$0")"
    python3 "${script_dir}/sage_tts_runner.py" pyttsx3 "${TEXT}" "${VOICE_ID}" 2>/dev/null && {
        echo "PLAYED tier-3 pyttsx3 (${VOICE_ID})" >&2
        return 0
    }
    return 1
}

# Tier 4: Gemini API (PAID, opt-in via gemini.enabled: true — always last)
try_tier_4() {
    local gemini_enabled=""
    if [ -f "${CONFIG_FILE}" ]; then
        gemini_enabled=$(grep -A 5 "^gemini:" "${CONFIG_FILE}" 2>/dev/null | grep -E "^\s+enabled:" | awk -F': ' '{print $2}' | tr -d ' "')
    fi
    if [ "${gemini_enabled}" != "true" ] && [ "${SAGE_TTS_TIER:-}" != "4" ]; then
        echo "Tier 4 (Gemini, PAID) skipped: opt-in only. Set gemini.enabled: true in ${CONFIG_FILE}" >&2
        return 1
    fi
    local out_wav="${OUT_DIR}/sage-gemini-${TEXT_HASH}.wav"
    local script_dir
    script_dir="$(dirname "$0")"
    if [ ! -f "${out_wav}" ]; then
        python3 "${script_dir}/gemini_tts.py" "${TEXT}" "Fenrir" "${out_wav}" >&2 2>&1 || return 1
    fi
    if play_wav "${out_wav}"; then
        echo "PLAYED tier-4 Gemini TTS" >&2
        return 0
    fi
    return 1
}

# Dispatch: forced tier OR native-first cascade
if [ -n "${TIER}" ]; then
    case "${TIER}" in
        1) try_tier_1 && exit 0 ;;
        2) try_tier_2 && exit 0 ;;
        3) try_tier_3 && exit 0 ;;
        4) try_tier_4 && exit 0 ;;
    esac
    echo "WARN: Forced tier ${TIER} unavailable, attempting cascade" >&2
fi

# Cascade: OS-native → kokoro-onnx (neural, needs model) → pyttsx3 → Gemini (PAID, always last)
try_tier_1 && exit 0
try_tier_2 && exit 0
try_tier_3 && exit 0
try_tier_4 && exit 0

cat >&2 << EOF
ERROR: No TTS engine available. Run setup:

  bash ~/.claude/skills/linkright-interview-coach/scripts/sage_setup.sh

Text was: ${TEXT}
EOF
exit 1
