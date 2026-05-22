#!/usr/bin/env bash
# roll_problem_type.sh — Randomly roll a problem type within picked round
# Usage: bash roll_problem_type.sh <round_id>
# Output: JSON with PT id + name + budget_s on stdout
# POSIX-compatible (works with macOS bash 3.x)

set -eu

ROUND_ID="${1:-}"

if [ -z "${ROUND_ID}" ]; then
    echo "ERROR: round_id required. Usage: bash roll_problem_type.sh <round_id>" >&2
    exit 1
fi

# Problem type count per round
case "${ROUND_ID}" in
    1) PT_COUNT=3; ROUND_NAME="HR Screening"; DIFFICULTY="Recruiter screen" ;;
    2) PT_COUNT=6; ROUND_NAME="Behavioral / STAR"; DIFFICULTY="Senior PM" ;;
    3) PT_COUNT=4; ROUND_NAME="Culture Fit / Values"; DIFFICULTY="Hiring manager" ;;
    4) PT_COUNT=5; ROUND_NAME="Product Sense"; DIFFICULTY="Senior PM" ;;
    5) PT_COUNT=4; ROUND_NAME="Analytical / Diagnostic"; DIFFICULTY="Senior PM" ;;
    6) PT_COUNT=5; ROUND_NAME="Technical PM / System Design"; DIFFICULTY="Tech PM / Principal" ;;
    7) PT_COUNT=4; ROUND_NAME="Bar Raiser"; DIFFICULTY="Principal / E7" ;;
    *) echo "ERROR: Invalid round_id '${ROUND_ID}'. Must be 1-7." >&2; exit 1 ;;
esac

# Roll
if command -v shuf >/dev/null 2>&1; then
    ROLL=$(shuf -i 1-${PT_COUNT} -n 1)
elif command -v jot >/dev/null 2>&1; then
    ROLL=$(jot -r 1 1 ${PT_COUNT})
else
    # POSIX fallback: $RANDOM
    ROLL=$(( (RANDOM % PT_COUNT) + 1 ))
fi

PT_ID="${ROUND_ID}.${ROLL}"

# PT name + budget lookup (POSIX case statement)
case "${PT_ID}" in
    "1.1") PT_NAME="Standard intro screen"; PT_BUDGET=900 ;;
    "1.2") PT_NAME="Recruiter referral screen"; PT_BUDGET=900 ;;
    "1.3") PT_NAME="Cold-applied screen"; PT_BUDGET=900 ;;
    "2.1") PT_NAME="Leadership without authority"; PT_BUDGET=1500 ;;
    "2.2") PT_NAME="Conflict with engineering / cross-functional"; PT_BUDGET=1500 ;;
    "2.3") PT_NAME="Biggest product failure + learning"; PT_BUDGET=1500 ;;
    "2.4") PT_NAME="Influencing a senior stakeholder"; PT_BUDGET=1500 ;;
    "2.5") PT_NAME="Handling ambiguity"; PT_BUDGET=1500 ;;
    "2.6") PT_NAME="Disagree-and-commit"; PT_BUDGET=1500 ;;
    "3.1") PT_NAME="Resume deep-dive narrative"; PT_BUDGET=1200 ;;
    "3.2") PT_NAME="Values challenge"; PT_BUDGET=1200 ;;
    "3.3") PT_NAME="Why this company specifically"; PT_BUDGET=1200 ;;
    "3.4") PT_NAME="Reverse interview"; PT_BUDGET=1200 ;;
    "4.1") PT_NAME="Favourite product"; PT_BUDGET=1800 ;;
    "4.2") PT_NAME="Improve X"; PT_BUDGET=2100 ;;
    "4.3") PT_NAME="Design X for Y"; PT_BUDGET=2700 ;;
    "4.4") PT_NAME="Diagnose drop"; PT_BUDGET=1800 ;;
    "4.5") PT_NAME="Market sizing"; PT_BUDGET=1500 ;;
    "5.1") PT_NAME="Metric design"; PT_BUDGET=1800 ;;
    "5.2") PT_NAME="A/B test critique"; PT_BUDGET=1800 ;;
    "5.3") PT_NAME="Diagnose unexpected drop"; PT_BUDGET=1800 ;;
    "5.4") PT_NAME="Prioritize 5 features with limited engineering"; PT_BUDGET=1800 ;;
    "6.1") PT_NAME="Design URL shortener at 100M req/day"; PT_BUDGET=3000 ;;
    "6.2") PT_NAME="Design Instagram Stories backend (500M DAU)"; PT_BUDGET=3000 ;;
    "6.3") PT_NAME="Design recommendation engine for OTT"; PT_BUDGET=3000 ;;
    "6.4") PT_NAME="Design search ranking for marketplace"; PT_BUDGET=3000 ;;
    "6.5") PT_NAME="Design notification system at scale"; PT_BUDGET=3000 ;;
    "7.1") PT_NAME="Hard product Q + Ownership LP"; PT_BUDGET=2100 ;;
    "7.2") PT_NAME="Strategy under uncertainty"; PT_BUDGET=2100 ;;
    "7.3") PT_NAME="Curveball"; PT_BUDGET=2100 ;;
    "7.4") PT_NAME="Customer obsession deep-dive"; PT_BUDGET=2100 ;;
    *) PT_NAME="Unknown"; PT_BUDGET=1800 ;;
esac

# Output JSON
cat << EOF
{
  "round_id": ${ROUND_ID},
  "round_name": "${ROUND_NAME}",
  "pt_id": "${PT_ID}",
  "pt_name": "${PT_NAME}",
  "budget_seconds": ${PT_BUDGET},
  "difficulty_bar": "${DIFFICULTY}",
  "roll_value": ${ROLL},
  "roll_max": ${PT_COUNT}
}
EOF
