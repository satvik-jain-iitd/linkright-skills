#!/usr/bin/env python3
"""
Signal-based Phase 2 fit score for a job vs user profile.
Usage: python3 fit_scorer.py --jd-signals '["growth_experimentation","data_fluency"]' \
         --profile ~/.linkright/memory/signals.md
Output: JSON {"fit_score": 0-100, "matched": [...], "gaps": [...], "verdict": str}
"""

import argparse
import json
import re
import sys
from pathlib import Path


SIGNAL_WEIGHTS = {
    "growth_experimentation": 1.0,
    "data_fluency": 1.0,
    "product_vision": 1.0,
    "systems_thinking": 0.8,
    "stakeholder_management": 0.8,
    "discovery_rigor": 0.8,
    "go_to_market": 0.7,
    "technical_depth": 0.7,
    "design_collaboration": 0.7,
    "metric_definition": 0.7,
    "outcome_ownership": 1.0,
    "early_stage_experience": 0.9,
    "enterprise_experience": 0.9,
    "marketplace_experience": 0.9,
    "platform_experience": 0.9,
    "b2c_experience": 0.8,
    "regulated_industry": 0.6,
    "remote_distributed_team": 0.5,
    "high_growth_stage": 0.7,
    "turnaround_context": 0.6,
    "international_products": 0.6,
    "influence_without_authority": 0.8,
    "user_empathy": 0.8,
    "ambiguity_tolerance": 0.9,
}

STRENGTH_VALUES = {"STRONG": 1.0, "MEDIUM": 0.6, "LOW": 0.2, "UNKNOWN": 0.0}


def load_profile_signals(profile_path: str) -> dict:
    """Parse signals.md → {signal_name: strength_value}"""
    path = Path(profile_path).expanduser()
    if not path.exists():
        return {}

    text = path.read_text()
    signals = {}

    # Format: "signal_name: STRONG" or "- signal_name (STRONG)"
    for line in text.splitlines():
        line = line.strip()
        # Match "signal_name: STRENGTH"
        m = re.match(r'^([\w_]+)\s*:\s*(STRONG|MEDIUM|LOW|UNKNOWN)', line, re.IGNORECASE)
        if m:
            signals[m.group(1)] = STRENGTH_VALUES.get(m.group(2).upper(), 0.0)
            continue
        # Match "- signal_name (STRENGTH)"
        m = re.match(r'^-\s*([\w_]+)\s*\((STRONG|MEDIUM|LOW|UNKNOWN)\)', line, re.IGNORECASE)
        if m:
            signals[m.group(1)] = STRENGTH_VALUES.get(m.group(2).upper(), 0.0)
            continue

    return signals


def compute_fit_score(jd_signals: list, profile: dict) -> dict:
    if not jd_signals:
        return {"fit_score": 50, "matched": [], "gaps": [], "verdict": "no JD signals provided"}

    matched = []
    gaps = []
    weighted_score = 0.0
    max_possible = 0.0

    for signal in jd_signals:
        weight = SIGNAL_WEIGHTS.get(signal, 0.5)
        max_possible += weight

        profile_strength = profile.get(signal, 0.0)
        contribution = weight * profile_strength
        weighted_score += contribution

        if profile_strength >= 0.6:
            matched.append({
                "signal": signal,
                "strength": _strength_label(profile_strength),
                "contribution": round(contribution / weight * 100) if weight else 0,
            })
        else:
            gaps.append({
                "signal": signal,
                "strength": _strength_label(profile_strength),
                "impact": "HIGH" if weight >= 0.9 else "MEDIUM" if weight >= 0.7 else "LOW",
            })

    fit_score = int((weighted_score / max_possible) * 100) if max_possible > 0 else 0

    if fit_score >= 80:
        verdict = "STRONG FIT — well-matched on required signals"
    elif fit_score >= 60:
        verdict = "GOOD FIT — matches most signals, some gaps to address"
    elif fit_score >= 40:
        verdict = "PARTIAL FIT — significant gaps but not disqualifying"
    else:
        verdict = "WEAK FIT — too many required signals at LOW or UNKNOWN"

    return {
        "fit_score": fit_score,
        "matched": matched,
        "gaps": gaps,
        "verdict": verdict,
    }


def _strength_label(value: float) -> str:
    if value >= 1.0:
        return "STRONG"
    elif value >= 0.6:
        return "MEDIUM"
    elif value >= 0.2:
        return "LOW"
    return "UNKNOWN"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jd-signals", required=True, help="JSON array of signal names from JD")
    parser.add_argument("--profile", default="~/.linkright/memory/signals.md")
    parser.add_argument("--format", choices=["json", "human"], default="json")
    args = parser.parse_args()

    try:
        jd_signals = json.loads(args.jd_signals)
    except json.JSONDecodeError:
        print(json.dumps({"error": "jd-signals must be valid JSON array"}))
        sys.exit(1)

    profile = load_profile_signals(args.profile)
    if not profile:
        print(json.dumps({"error": f"No signal profile found at {args.profile}"}))
        sys.exit(1)

    result = compute_fit_score(jd_signals, profile)

    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print(f"Fit Score: {result['fit_score']}/100 — {result['verdict']}")
        if result["matched"]:
            print(f"\nMatched ({len(result['matched'])}):")
            for m in result["matched"]:
                print(f"  ✓ {m['signal']} ({m['strength']})")
        if result["gaps"]:
            print(f"\nGaps ({len(result['gaps'])}):")
            for g in result["gaps"]:
                print(f"  ✗ {g['signal']} ({g['strength']}) — {g['impact']} impact")

    sys.exit(0 if result["fit_score"] >= 50 else 1)


if __name__ == "__main__":
    main()
