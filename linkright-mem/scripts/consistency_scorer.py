"""
consistency_scorer.py — Score profile signals against PM archetypes.

Usage:
  python3 consistency_scorer.py --signals signals.md --facts facts.md --memory ~/.linkright/memory
  python3 consistency_scorer.py --signals signals.md --archetype ai_enterprise_pm
"""

import argparse
import json
import re
from pathlib import Path

# Archetype required signals: {archetype: {signal: weight}}
# weight: 1.0 = required, 0.6 = important, 0.3 = nice-to-have
ARCHETYPE_SIGNALS = {
    "ai_enterprise_pm": {
        "systems_thinking":              1.0,
        "ai_workflow_design":            1.0,
        "enterprise_workflow_ownership": 1.0,
        "stakeholder_leadership":        0.6,
        "data_fluency":                  0.6,
        "ambiguity_handling":            0.3,
        "execution_rigor":               0.3,
    },
    "growth_pm": {
        "growth_experimentation":        1.0,
        "data_fluency":                  1.0,
        "user_empathy":                  0.6,
        "execution_rigor":               0.6,
        "communication_clarity":         0.3,
        "systems_thinking":              0.3,
    },
    "founding_pm": {
        "zero_to_one_execution":         1.0,
        "ambiguity_handling":            1.0,
        "systems_thinking":              0.6,
        "stakeholder_leadership":        0.6,
        "execution_rigor":               0.6,
        "data_fluency":                  0.3,
    },
    "csm_implementation": {
        "enterprise_workflow_ownership": 1.0,
        "implementation_management":     1.0,
        "stakeholder_leadership":        0.6,
        "user_empathy":                  0.6,
        "communication_clarity":         0.3,
        "execution_rigor":               0.3,
    },
    "analytics_pm": {
        "data_fluency":                  1.0,
        "systems_thinking":              0.6,
        "execution_rigor":               0.6,
        "communication_clarity":         0.6,
        "user_empathy":                  0.3,
    },
    "consumer_pm": {
        "user_empathy":                  1.0,
        "growth_experimentation":        1.0,
        "communication_clarity":         0.6,
        "execution_rigor":               0.6,
        "data_fluency":                  0.3,
    },
    "general_pm": {
        "execution_rigor":               1.0,
        "stakeholder_leadership":        1.0,
        "systems_thinking":              0.6,
        "data_fluency":                  0.6,
        "user_empathy":                  0.3,
        "communication_clarity":         0.3,
    },
}

STRENGTH_VALUE = {"high": 1.0, "medium": 0.6, "low": 0.2}


def parse_signals_md(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    text = path.read_text()
    blocks = re.findall(r"---\n(.*?)\n---", text, re.DOTALL)
    signals = {}
    for block in blocks:
        sig = {}
        lines = block.strip().split("\n")
        i = 0
        while i < len(lines):
            line = lines[i]
            if ":" in line and not line.startswith("  "):
                k, _, v = line.partition(":")
                k, v = k.strip(), v.strip().strip('"')
                if v.startswith("[") or (i + 1 < len(lines) and lines[i + 1].startswith("  -")):
                    items = []
                    i += 1
                    while i < len(lines) and lines[i].startswith("  - "):
                        items.append(lines[i][4:].strip())
                        i += 1
                    sig[k] = items
                    continue
                sig[k] = v
            i += 1
        if "name" in sig:
            signals[sig["name"]] = sig
    return signals


def score_archetype(signals: dict[str, dict], archetype: str) -> dict:
    required = ARCHETYPE_SIGNALS.get(archetype, {})
    if not required:
        return {"error": f"Unknown archetype: {archetype}"}

    total_weight = sum(required.values())
    earned_weight = 0.0
    signal_breakdown = []

    for sig_name, req_weight in required.items():
        if sig_name in signals:
            sig = signals[sig_name]
            strength = sig.get("strength", "medium")
            user_val = STRENGTH_VALUE.get(strength, 0.3)
            contribution = req_weight * user_val
            earned_weight += contribution
            signal_breakdown.append({
                "signal": sig_name,
                "required_weight": req_weight,
                "user_strength": strength,
                "status": "✓ strong" if user_val >= 0.8 else "△ partial" if user_val >= 0.5 else "△ weak",
                "contribution": round(contribution, 2),
            })
        else:
            signal_breakdown.append({
                "signal": sig_name,
                "required_weight": req_weight,
                "user_strength": "absent",
                "status": "✗ missing",
                "contribution": 0.0,
            })

    score_pct = round((earned_weight / total_weight) * 100) if total_weight > 0 else 0
    gaps = [s for s in signal_breakdown if s["status"] == "✗ missing"]
    partials = [s for s in signal_breakdown if "partial" in s["status"] or "weak" in s["status"]]

    return {
        "archetype": archetype,
        "score": score_pct,
        "earned": round(earned_weight, 2),
        "total": round(total_weight, 2),
        "breakdown": signal_breakdown,
        "gaps": [g["signal"] for g in gaps],
        "partials": [p["signal"] for p in partials],
        "label": "STRONG FIT" if score_pct >= 75 else "GOOD FIT" if score_pct >= 55 else "STRETCH" if score_pct >= 35 else "MISMATCH",
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--signals", required=True)
    p.add_argument("--facts", default=None)
    p.add_argument("--memory", default=None)
    p.add_argument("--archetype", default=None, help="Score one archetype only")
    p.add_argument("--format", default="text", choices=["text", "json"])
    args = p.parse_args()

    signals = parse_signals_md(Path(args.signals))

    archetypes = [args.archetype] if args.archetype else list(ARCHETYPE_SIGNALS.keys())
    results = [score_archetype(signals, a) for a in archetypes]
    results.sort(key=lambda x: x.get("score", 0), reverse=True)

    if args.format == "json":
        print(json.dumps(results, indent=2))
        return

    # Text output
    print("\nCONSISTENCY SCORES")
    print(f"  {'Archetype':<28}  {'Score':>5}  {'Label'}")
    print(f"  {'-'*28}  {'-'*5}  {'-'*12}")
    for r in results:
        if "error" not in r:
            print(f"  {r['archetype']:<28}  {r['score']:>4}%  {r['label']}")

    if args.archetype:
        r = results[0]
        print(f"\nDETAIL: {r['archetype']}")
        for b in r["breakdown"]:
            print(f"  {b['status']:12}  {b['signal']:<32}  weight={b['required_weight']}  strength={b['user_strength']}")
        if r["gaps"]:
            print(f"\nGAP SIGNALS: {', '.join(r['gaps'])}")
        if r["partials"]:
            print(f"WEAK SIGNALS: {', '.join(r['partials'])}")


if __name__ == "__main__":
    main()
