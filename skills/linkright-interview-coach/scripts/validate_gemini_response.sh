#!/usr/bin/env bash
# validate_gemini_response.sh — Thin wrapper around validate_gemini_response.py
#
# Per adversarial review #3 + refactor: delegates to separate Python file so
# stdin isn't consumed by bash heredoc. Schema validation now real.
#
# Usage:
#   bash validate_gemini_response.sh <stage> <json_file_or_->
#     stage: stage1 | stage2 | stage3
#
# Exit codes pass through from Python validator (0=valid, 1=invalid, 2=args)

set -eu

STAGE="${1:-}"
JSON_INPUT="${2:-}"

if [ -z "${STAGE}" ] || [ -z "${JSON_INPUT}" ]; then
    echo "ERROR: Usage: bash validate_gemini_response.sh <stage1|stage2|stage3> <json_file_or_->" >&2
    exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCHEMA_FILE="${SCRIPT_DIR}/../state/gemini-response-schemas.json"

# Normalize "-" → /dev/stdin for Python clarity
[ "${JSON_INPUT}" = "-" ] && JSON_INPUT="/dev/stdin"

python3 "${SCRIPT_DIR}/validate_gemini_response.py" "${STAGE}" "${SCHEMA_FILE}" "${JSON_INPUT}"
