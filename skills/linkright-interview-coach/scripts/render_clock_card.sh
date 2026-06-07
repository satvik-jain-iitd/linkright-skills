#!/usr/bin/env bash
# render_clock_card.sh — Render the clock card from current state
# Usage: bash render_clock_card.sh <state_file_path>
# Output: Clock card markdown on stdout

set -euo pipefail

STATE_FILE="${1:-}"

if [[ -z "${STATE_FILE}" ]] || [[ ! -f "${STATE_FILE}" ]]; then
    echo "ERROR: State file required and must exist. Usage: bash render_clock_card.sh /tmp/mock-interview-state-<uuid>.json" >&2
    exit 1
fi

# Require jq for JSON parsing
if ! command -v jq &> /dev/null; then
    echo "ERROR: jq required for state parsing. Install via 'brew install jq' on macOS." >&2
    exit 1
fi

# Extract fields
ROUND_NAME=$(jq -r '.round.name' "${STATE_FILE}")
PT_NAME=$(jq -r '.round.problem_type.name' "${STATE_FILE}")
DIFFICULTY=$(jq -r '.round.difficulty_bar' "${STATE_FILE}")
PHASE_IDX=$(jq -r '.timing.current_phase_idx' "${STATE_FILE}")
PHASE_COUNT=$(jq -r '.timing.phases | length' "${STATE_FILE}")
PHASE_NAME=$(jq -r ".timing.phases[${PHASE_IDX}].name" "${STATE_FILE}")
PHASE_START_TS=$(jq -r ".timing.phases[${PHASE_IDX}].start_ts" "${STATE_FILE}")
PHASE_BUDGET_S=$(jq -r ".timing.phases[${PHASE_IDX}].budget_s" "${STATE_FILE}")
INTERVIEW_START_TS=$(jq -r '.timing.interview_start_ts' "${STATE_FILE}")
TOTAL_BUDGET_S=$(jq -r '.round.budget_seconds' "${STATE_FILE}")
TIER=$(jq -r '.timing.patience_tier' "${STATE_FILE}")

# Compute time fields
NOW_TS=$(date +%s)
NOW_HHMMSS=$(date +"%H:%M:%S")

PHASE_START_HHMMSS=$(date -r "${PHASE_START_TS}" +"%H:%M:%S" 2>/dev/null || \
                    date -d "@${PHASE_START_TS}" +"%H:%M:%S" 2>/dev/null || \
                    echo "??:??:??")

SOFT_CUTOFF_TS=$((PHASE_START_TS + PHASE_BUDGET_S))
SOFT_CUTOFF_HHMMSS=$(date -r "${SOFT_CUTOFF_TS}" +"%H:%M:%S" 2>/dev/null || \
                     date -d "@${SOFT_CUTOFF_TS}" +"%H:%M:%S" 2>/dev/null || \
                     echo "??:??:??")

HARD_CUTOFF_TS=$((SOFT_CUTOFF_TS + 180))
HARD_CUTOFF_HHMMSS=$(date -r "${HARD_CUTOFF_TS}" +"%H:%M:%S" 2>/dev/null || \
                     date -d "@${HARD_CUTOFF_TS}" +"%H:%M:%S" 2>/dev/null || \
                     echo "??:??:??")

ELAPSED_PHASE_S=$((NOW_TS - PHASE_START_TS))
ELAPSED_PHASE_HUMAN=$(printf "%dm%02ds" "$((ELAPSED_PHASE_S / 60))" "$((ELAPSED_PHASE_S % 60))")

REMAINING_PHASE_S=$((PHASE_BUDGET_S - ELAPSED_PHASE_S))
if (( REMAINING_PHASE_S < 0 )); then
    REMAINING_PHASE_HUMAN="overrun by $(printf "%dm%02ds" "$((-REMAINING_PHASE_S / 60))" "$((-REMAINING_PHASE_S % 60))")"
else
    REMAINING_PHASE_HUMAN=$(printf "%dm%02ds" "$((REMAINING_PHASE_S / 60))" "$((REMAINING_PHASE_S % 60))")
fi

ELAPSED_TOTAL_S=$((NOW_TS - INTERVIEW_START_TS))
ELAPSED_TOTAL_HUMAN=$(printf "%dm%02ds" "$((ELAPSED_TOTAL_S / 60))" "$((ELAPSED_TOTAL_S % 60))")
TOTAL_BUDGET_HUMAN=$(printf "%dm%02ds" "$((TOTAL_BUDGET_S / 60))" "$((TOTAL_BUDGET_S % 60))")

# Tier emoji + status text
case "${TIER}" in
    "green")  TIER_LINE="🟢 GREEN  (on pace)";;
    "yellow") TIER_LINE="🟡 YELLOW  (1 min left — wrap up)";;
    "orange") TIER_LINE="🟠 ORANGE  (interrupting — advancing)";;
    "red")    TIER_LINE="🔴 RED  (HARD CUTOFF — advancing)";;
    *)        TIER_LINE="⚪️ UNKNOWN";;
esac

# Render
PHASE_DISPLAY=$((PHASE_IDX + 1))
cat << EOF

╭─────────────────────────────────────────────────────────────────╮
│  ⏱  ROUND: ${ROUND_NAME}  │  Difficulty: ${DIFFICULTY}
│  ⏱  PHASE: ${PHASE_DISPLAY} of ${PHASE_COUNT} — ${PHASE_NAME}
│  ───────────────────────────────────────────────────────────────
│  ⏱  Phase start:   ${PHASE_START_HHMMSS}
│  ⏱  Soft cutoff:   ${SOFT_CUTOFF_HHMMSS}  ($((PHASE_BUDGET_S / 60))m budget)
│  ⏱  Hard cutoff:   ${HARD_CUTOFF_HHMMSS}  (+3m grace)
│  ⏱  Now:           ${NOW_HHMMSS}
│  ⏱  Elapsed phase: ${ELAPSED_PHASE_HUMAN}    │  Remaining: ${REMAINING_PHASE_HUMAN}
│  ⏱  Total elapsed: ${ELAPSED_TOTAL_HUMAN}    │  Round budget: ${TOTAL_BUDGET_HUMAN}
│  ───────────────────────────────────────────────────────────────
│  STATUS: ${TIER_LINE}
╰─────────────────────────────────────────────────────────────────╯

EOF
