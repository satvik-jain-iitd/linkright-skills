#!/usr/bin/env bash
# compute_elapsed.sh — Compute elapsed seconds since a unix timestamp
# Usage: bash compute_elapsed.sh <start_ts>
# Output: JSON with elapsed_s, elapsed_human, now_ts

set -euo pipefail

START_TS="${1:-}"

if [[ -z "${START_TS}" ]]; then
    echo "ERROR: start_ts required. Usage: bash compute_elapsed.sh <unix_ts>" >&2
    exit 1
fi

if ! [[ "${START_TS}" =~ ^[0-9]+$ ]]; then
    echo "ERROR: start_ts must be a unix timestamp (integer)" >&2
    exit 1
fi

NOW_TS=$(date +%s)
NOW_HHMMSS=$(date +"%H:%M:%S")
ELAPSED_S=$((NOW_TS - START_TS))

# Format human-readable
ELAPSED_MIN=$((ELAPSED_S / 60))
ELAPSED_SEC=$((ELAPSED_S % 60))
ELAPSED_HUMAN=$(printf "%dm%02ds" "${ELAPSED_MIN}" "${ELAPSED_SEC}")

cat << EOF
{
  "start_ts": ${START_TS},
  "now_ts": ${NOW_TS},
  "now_hhmmss": "${NOW_HHMMSS}",
  "elapsed_s": ${ELAPSED_S},
  "elapsed_human": "${ELAPSED_HUMAN}"
}
EOF
