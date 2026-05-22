#!/usr/bin/env bash
# sage_setup.sh — One-shot installer for Sage voice dependencies
#
# Called from `linkright setup` wizard (V1.1+). Run idempotently.
#
# Provisions:
#   1. Python deps (kokoro-onnx, soundfile, pyttsx3) via pyenv-aware pip
#   2. Kokoro model files (~330MB) to ~/.cache/kokoro/
#   3. macOS Rishi voice (Indian English male — Sage default) verification + download trigger
#   4. Default ~/.linkright/sage-voice.yaml with Rishi as voice
#   5. Per-tier verification
#
# Usage: bash ~/.claude/skills/linkright-interview-coach/scripts/sage_setup.sh

set -eu

G='\033[0;32m'; Y='\033[0;33m'; R='\033[0;31m'; B='\033[1m'; N='\033[0m'
log()  { printf "${B}==>${N} %s\n" "$*"; }
ok()   { printf "${G}  ✓${N} %s\n" "$*"; }
warn() { printf "${Y}  !${N} %s\n" "$*"; }
err()  { printf "${R}  ✗${N} %s\n" "$*"; }

PYTHON_BIN="$(command -v python3 || true)"
if [ -z "${PYTHON_BIN}" ]; then
    err "python3 not found. Install Python 3.10+ via brew (brew install python@3.13) or pyenv."
    exit 1
fi
log "Using python: ${PYTHON_BIN} ($(${PYTHON_BIN} --version 2>&1))"

# ── Step 1: Python deps ──────────────────────────────────────────
log "Installing Python TTS dependencies..."

install_py_dep() {
    local pkg="$1"
    local import_name="${2:-$1}"
    if "${PYTHON_BIN}" -c "import ${import_name}" 2>/dev/null; then
        ok "${pkg} already installed"
    else
        "${PYTHON_BIN}" -m pip install "${pkg}" --quiet 2>&1 | tail -3 || true
        if "${PYTHON_BIN}" -c "import ${import_name}" 2>/dev/null; then
            ok "${pkg} installed"
        else
            warn "${pkg} install failed or not importable"
        fi
    fi
}

install_py_dep "kokoro-onnx" "kokoro_onnx"
install_py_dep "soundfile" "soundfile"
install_py_dep "pyttsx3" "pyttsx3"

# ── Step 2: Kokoro model files ───────────────────────────────────
log "Provisioning Kokoro model files to ~/.cache/kokoro/..."

KOKORO_DIR="${HOME}/.cache/kokoro"
mkdir -p "${KOKORO_DIR}"

download_if_missing() {
    local file="$1"
    local url="$2"
    local min_size="$3"
    local target="${KOKORO_DIR}/${file}"
    local size
    if [ -f "${target}" ]; then
        size=$(stat -f%z "${target}" 2>/dev/null || stat -c%s "${target}" 2>/dev/null || echo 0)
        if [ "${size}" -gt "${min_size}" ]; then
            ok "${file} already present ($(du -h "${target}" | cut -f1))"
            return 0
        fi
    fi
    log "Downloading ${file}..."
    if curl -L --progress-bar -o "${target}" "${url}"; then
        ok "Downloaded ${file} ($(du -h "${target}" | cut -f1))"
    else
        warn "Download failed for ${file}"
    fi
}

download_if_missing "kokoro-v0_19.onnx" \
    "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/kokoro-v0_19.onnx" \
    100000000

download_if_missing "voices.bin" \
    "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/voices.bin" \
    1000000

# ── Step 3: macOS Rishi voice (default Sage voice) ───────────────
log "Verifying Sage's default voice (Rishi — Indian English male)..."

PLATFORM="$(uname -s)"
RISHI_OK=false

if [ "${PLATFORM}" = "Darwin" ]; then
    if say -v "?" 2>/dev/null | grep -qE "^Rishi\s+en_IN"; then
        RISHI_OK=true
        ok "Rishi (en_IN, Indian English male) installed"
    fi

    if [ "${RISHI_OK}" = "false" ]; then
        warn "Rishi voice not installed. Opening macOS Settings to download..."
        echo ""
        cat << 'EOF'
  ┌──────────────────────────────────────────────────────────────┐
  │  ONE-TIME MANUAL STEP — DOWNLOAD RISHI VOICE                 │
  │                                                              │
  │  macOS Settings is opening to: Accessibility → Spoken Content│
  │                                                              │
  │  Steps:                                                      │
  │     1. Click "System Voice" dropdown                         │
  │     2. Scroll to bottom, click "Manage Voices..."            │
  │     3. Find "English (India)" section                        │
  │     4. Check "Rishi"                                         │
  │     5. Click OK — download (~50MB, ~1 min)                   │
  │     6. Press Enter here when done                            │
  │                                                              │
  │  Optional voices to add (now or later):                      │
  │     - Veena (en_IN female)                                   │
  │     - Lekha (hi_IN female, Hindi)                            │
  │     - Allison / Ava (premium en_US female)                   │
  │     Change voice_id in ~/.linkright/sage-voice.yaml          │
  └──────────────────────────────────────────────────────────────┘
EOF
        open "x-apple.systempreferences:com.apple.preference.universalaccess?Speech" 2>/dev/null \
            || open "x-apple.systempreferences:com.apple.Speech-Settings.extension" 2>/dev/null \
            || true
        echo ""
        read -r -p "  Press Enter when Rishi download finishes (or skip with fallback)... " _
        echo ""

        if say -v "?" 2>/dev/null | grep -qE "^Rishi\s+en_IN"; then
            RISHI_OK=true
            ok "Rishi now installed"
        else
            warn "Rishi still not detected. Sage will use system default voice as fallback."
        fi
    fi
elif [ "${PLATFORM}" = "Linux" ]; then
    if ! command -v espeak-ng >/dev/null 2>&1; then
        warn "espeak-ng not found. Install via: sudo apt-get install -y espeak-ng"
    else
        ok "espeak-ng installed"
    fi
fi

# ── Step 4: Write ~/.linkright/sage-voice.yaml ───────────────────
log "Writing ~/.linkright/sage-voice.yaml..."

LR_DIR="${HOME}/.linkright"
mkdir -p "${LR_DIR}"
CONFIG_FILE="${LR_DIR}/sage-voice.yaml"

if [ -f "${CONFIG_FILE}" ]; then
    warn "${CONFIG_FILE} already exists — preserving (edit manually if needed)"
else
    DEFAULT_VOICE="Rishi"
    [ "${RISHI_OK}" = "false" ] && DEFAULT_VOICE="Daniel"  # fallback to en_US male

    cat > "${CONFIG_FILE}" << EOF
# ~/.linkright/sage-voice.yaml — auto-generated $(date +"%Y-%m-%d")
# Edit voice_id to switch voices. Run \`say -v "?"\` to list installed voices.

preferred_tier: 2

voice_id: ${DEFAULT_VOICE}   # Default Sage voice. Rishi = Indian English male.

speed: 1.0
pitch: 0.0
pause_before_pushback_seconds: 2.0

emphasis_words:
  - specifically
  - tradeoff
  - concrete
  - constraint
  - signal

kokoro:
  model_path: ~/.cache/kokoro/kokoro-v0_19.onnx
  voices_path: ~/.cache/kokoro/voices.bin
  language: en-us

gemini:
  enabled: false              # PAID quota; opt-in only.
  model: gemini-2.5-flash-preview-tts
  api_key_env_var: GEMINI_API_KEY
EOF
    ok "Wrote ${CONFIG_FILE} (default voice: ${DEFAULT_VOICE})"
fi

# ── Step 5: Per-tier verification ────────────────────────────────
log "Verifying each tier..."

SKILL_DIR="$(dirname "$0")"

verify_tier() {
    local tier_num="$1"
    local name="$2"
    if SAGE_TTS_TIER="${tier_num}" bash "${SKILL_DIR}/kokoro_speak.sh" "Setup test." >/dev/null 2>&1; then
        ok "Tier ${tier_num} (${name}) — working"
    else
        warn "Tier ${tier_num} (${name}) — unavailable"
    fi
}

verify_tier 1 "kokoro-onnx"
verify_tier 2 "macOS say / espeak-ng"
verify_tier 3 "pyttsx3"

echo ""
log "${B}Sage voice setup complete.${N}"
echo ""
echo "  Default voice:    Rishi (Indian English male) — or system default if not installed"
echo "  Config:           ${CONFIG_FILE}"
echo "  Model cache:      ${KOKORO_DIR}"
echo ""
echo "  Test Sage's voice:"
echo "    bash ${SKILL_DIR}/kokoro_speak.sh \"Sage hu. Interview coach. Ready to practice?\""
echo ""
echo "  To use a different voice, edit voice_id in ${CONFIG_FILE}."
echo "  List installed voices: say -v \"?\""
echo ""
