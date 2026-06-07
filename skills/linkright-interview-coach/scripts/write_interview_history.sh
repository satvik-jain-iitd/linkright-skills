#!/usr/bin/env bash
# write_interview_history.sh — Persist final scorecard to ~/.linkright/interview-history/
# Usage: bash write_interview_history.sh <state_file_path>
# Output: Path to written history file

set -euo pipefail

STATE_FILE="${1:-}"

if [[ -z "${STATE_FILE}" ]] || [[ ! -f "${STATE_FILE}" ]]; then
    echo "ERROR: state_file required. Usage: bash write_interview_history.sh <state_file>" >&2
    exit 1
fi

if ! command -v jq &> /dev/null; then
    echo "ERROR: jq required. Install: brew install jq" >&2
    exit 1
fi

# Determine history dir (prefer ~/.linkright/, fallback ~/.claude/)
HISTORY_DIR="${HOME}/.linkright/interview-history"
if [[ ! -d "${HOME}/.linkright" ]]; then
    HISTORY_DIR="${HOME}/.claude/interview-history"
fi

mkdir -p "${HISTORY_DIR}"

# Generate timestamp + filename
TS=$(date -u +"%Y-%m-%dT%H-%M-%SZ")
SESSION_ID=$(jq -r '.session_id' "${STATE_FILE}")
HISTORY_FILE="${HISTORY_DIR}/${TS}-${SESSION_ID}.json"

# Avoid collision (extremely unlikely with TS + UUID, but defensive)
COUNTER=1
while [[ -f "${HISTORY_FILE}" ]]; do
    HISTORY_FILE="${HISTORY_DIR}/${TS}-${SESSION_ID}-${COUNTER}.json"
    COUNTER=$((COUNTER + 1))
done

# Compose history entry from state file
jq -n \
    --slurpfile state "${STATE_FILE}" \
    --arg timestamp "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
    '{
      schema_version: "1.0",
      session_id: $state[0].session_id,
      timestamp: $timestamp,
      candidate_snapshot: $state[0].candidate,
      round: $state[0].round,
      duration_seconds: (now - $state[0].timing.interview_start_ts),
      voice_mode: ($state[0].mode.voice_output // false),
      scoring_content: $state[0].scoring_content,
      scoring_gemini: $state[0].scoring_gemini,
      av_coaching_attached: (($state[0].scoring_gemini.stage1_video != null) or ($state[0].scoring_gemini.stage2_audio != null) or ($state[0].scoring_gemini.stage3_transcript != null)),
      gemini_stages_received: [
        (if $state[0].scoring_gemini.stage1_video != null then "stage1_video" else null end),
        (if $state[0].scoring_gemini.stage2_audio != null then "stage2_audio" else null end),
        (if $state[0].scoring_gemini.stage3_transcript != null then "stage3_transcript" else null end)
      ] | map(select(. != null)),
      behavior_log: $state[0].behavior_log,
      verdict: $state[0].verdict,
      improvement_playbook: $state[0].improvement_playbook
    }' > "${HISTORY_FILE}"

# Update latest symlink
LATEST_LINK="${HISTORY_DIR}/latest.json"
if [[ -L "${LATEST_LINK}" ]] || [[ -f "${LATEST_LINK}" ]]; then
    rm -f "${LATEST_LINK}"
fi
ln -s "${HISTORY_FILE}" "${LATEST_LINK}"

echo "${HISTORY_FILE}"
