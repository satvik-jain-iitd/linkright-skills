#!/usr/bin/env bash
# load_profile.sh — Load LinkRight profile + build candidate-summary.json
#
# Reads ~/.linkright/profile/ (metadata.yaml + nuggets.jsonl + highlights.jsonl)
# Extracts top_3_signals from `tags` field (comma-separated string in each nugget)
# Computes transition_phase + absent_signals
# Output: candidate-summary JSON on stdout
#
# Usage: bash load_profile.sh

set -eu

PROFILE_DIR="${HOME}/.linkright/profile"

if [ ! -d "${PROFILE_DIR}" ] || [ ! -f "${PROFILE_DIR}/metadata.yaml" ]; then
    cat >&2 << EOF
PROFILE_MISSING: ${PROFILE_DIR}/metadata.yaml not found.

Fallback options:
  - Path A: User provides resume PDF path (parse via markitdown/pypdf)
  - Path B: 5-Q conversational capture
EOF
    exit 1
fi

# Delegate to Python — robust JSON/YAML parsing + signal extraction
python3 << 'PYEOF'
import json
import os
import sys
from collections import Counter
from pathlib import Path

PROFILE = Path.home() / ".linkright" / "profile"

# --- Read metadata.yaml (minimal — only fields we need) ---
def read_yaml_field(path: Path, key: str, default=None):
    """Naive YAML reader for top-level scalar fields. Robust enough for our use."""
    if not path.exists():
        return default
    for line in path.read_text().splitlines():
        line = line.strip()
        if line.startswith(f"{key}:"):
            value = line.split(":", 1)[1].strip().strip('"').strip("'")
            return value
    return default

meta = PROFILE / "metadata.yaml"
career_level = read_yaml_field(meta, "career_level", "mid")
career_years_raw = read_yaml_field(meta, "career_years", "0")
domain_arc = read_yaml_field(meta, "domain_arc", "") or ""

try:
    career_years = int(career_years_raw)
except (ValueError, TypeError):
    career_years = 0

# --- Read nuggets.jsonl + extract tag frequencies ---
nuggets_path = PROFILE / "nuggets.jsonl"
tag_counter = Counter()
leadership_modes = Counter()
nuggets_count = 0

if nuggets_path.exists():
    for line in nuggets_path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            n = json.loads(line)
        except json.JSONDecodeError:
            continue
        nuggets_count += 1

        # tags: comma-separated string
        tags_str = n.get("tags", "") or ""
        if isinstance(tags_str, str):
            tags = [t.strip().lower() for t in tags_str.split(",") if t.strip()]
            for tag in tags:
                tag_counter[tag] += 1

        # leadership: separate signal
        ldr = n.get("leadership", "") or ""
        if ldr and isinstance(ldr, str):
            leadership_modes[ldr.strip().lower()] += 1

# Top 3 signals by frequency, filtered to PM-relevant tags
# Drop tags that are too generic / not signals
GENERIC_DROP = {"p1", "p2", "p3", "work_experience", "side_project", "education",
                 "experience", "general", "misc", "other"}
top_signals_pool = [(tag, ct) for tag, ct in tag_counter.most_common(20)
                     if tag not in GENERIC_DROP]
top_3_signals = [t for t, _ in top_signals_pool[:3]]

# Absent signals: canonical PM signals not in top tags
# Map from signal_weights.yaml convention (kebab-case) to common tag variants
CANONICAL_SIGNALS = {
    "leadership": ["leadership", "team_lead", "leading"],
    "build-execution": ["product_development", "build", "execution", "shipping", "delivery"],
    "user-empathy": ["ux_research", "user_research", "product_design", "user_empathy"],
    "data-driven": ["data", "analytics", "data_engineering", "data_pipeline", "ml"],
    "strategy-thinking": ["strategy", "roadmap", "vision", "product_strategy"],
    "revenue-impact": ["revenue", "growth", "monetization", "growth_strategy"],
    "ai-product": ["ai", "ml", "llm", "ai_product"],
    "executive-influence": ["executive", "c_suite", "leadership_influence", "stakeholder"],
}

present_canonical = set()
for canonical, variants in CANONICAL_SIGNALS.items():
    for v in variants:
        if v in tag_counter or v in top_3_signals:
            present_canonical.add(canonical)
            break

absent_signals = sorted(set(CANONICAL_SIGNALS.keys()) - present_canonical)[:5]

# --- Read highlights.jsonl count ---
highlights_path = PROFILE / "highlights.jsonl"
story_count = 0
if highlights_path.exists():
    story_count = sum(1 for line in highlights_path.read_text().splitlines() if line.strip())

# --- Compute transition_phase from heuristic ---
# Phase 1: <1 yr in target domain (heavy signal accumulation)
# Phase 2: 1-3 yrs (bridge narrative)
# Phase 3: 3+ yrs or no transition (identity lock OR linear career)
if domain_arc:
    if career_years < 1:
        transition_phase = 1
    elif career_years < 3:
        transition_phase = 2
    else:
        transition_phase = 3
else:
    transition_phase = None

# --- Personalized ceiling per dimension (career-level adjusted baseline) ---
LEVEL_MULTIPLIERS = {
    "fresher":      {"product_sense": 3.0, "execution": 3.5, "strategy": 2.5,
                     "analytical":    3.5, "leadership": 2.5, "ai_judgment": 2.5},
    "early_career": {"product_sense": 3.5, "execution": 4.0, "strategy": 3.0,
                     "analytical":    4.0, "leadership": 3.0, "ai_judgment": 3.0},
    "mid":          {"product_sense": 4.0, "execution": 4.0, "strategy": 3.5,
                     "analytical":    4.0, "leadership": 3.5, "ai_judgment": 3.0},
    "senior":       {"product_sense": 4.5, "execution": 4.0, "strategy": 4.5,
                     "analytical":    4.0, "leadership": 4.5, "ai_judgment": 4.0},
    "executive":    {"product_sense": 4.5, "execution": 3.5, "strategy": 5.0,
                     "analytical":    4.0, "leadership": 5.0, "ai_judgment": 4.0},
}
ceilings = LEVEL_MULTIPLIERS.get(career_level, LEVEL_MULTIPLIERS["mid"])

# --- Compose output JSON ---
summary = {
    "schema_version": "1.0",
    "profile_source": "linkright",
    "career_level": career_level,
    "career_years": career_years,
    "transition_phase": transition_phase,
    "domain_arc": domain_arc,
    "top_3_signals": top_3_signals,
    "absent_signals": absent_signals,
    "story_inventory_count": story_count,
    "nuggets_count": nuggets_count,
    "leadership_modes": dict(leadership_modes.most_common(3)),
    "personalized_ceilings": ceilings,
    "signal_weights_path": str(Path.home() / "Documents" / "linkright_production" /
                                 "context" / "cli" / "linkright" / "src" / "linkright" /
                                 "resume" / "data" / "signal_weights.yaml"),
}

print(json.dumps(summary, indent=2))
PYEOF
