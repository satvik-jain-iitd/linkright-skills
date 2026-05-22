"""
grep_memory.py — Multi-query grep across facts.md + signals.md.
Returns ranked results for skills querying profile memory.

Usage:
  python3 grep_memory.py --query "stakeholder alignment" --memory ~/.linkright/memory --top 10
  python3 grep_memory.py --signal "systems_thinking" --memory ~/.linkright/memory --format json
  python3 grep_memory.py --archetype "growth" --memory ~/.linkright/memory --format json
  python3 grep_memory.py --query "strength:high" --memory ~/.linkright/memory
"""

import argparse
import json
import re
from pathlib import Path


# Names aligned with ref_02_signal_taxonomy.md, ref_03_archetype_requirements.md
ARCHETYPE_SIGNALS = {
    "growth":      ["growth_experimentation", "data_fluency", "metric_definition",
                    "product_vision", "user_empathy", "systems_thinking"],
    "0to1":        ["early_stage_experience", "product_vision", "discovery_rigor",
                    "ambiguity_tolerance", "systems_thinking", "stakeholder_management"],
    "platform":    ["platform_experience", "technical_depth", "systems_thinking",
                    "stakeholder_management", "data_fluency", "outcome_ownership"],
    "enterprise":  ["enterprise_experience", "stakeholder_management", "go_to_market",
                    "outcome_ownership", "data_fluency", "systems_thinking"],
    "consumer":    ["user_empathy", "growth_experimentation", "discovery_rigor",
                    "data_fluency", "product_vision", "design_collaboration"],
    "data_ai":     ["data_fluency", "technical_depth", "systems_thinking",
                    "metric_definition", "product_vision", "outcome_ownership"],
    "design_led":  ["design_collaboration", "discovery_rigor", "product_vision",
                    "user_empathy", "systems_thinking", "outcome_ownership"],
    "marketplace": ["marketplace_experience", "growth_experimentation", "data_fluency",
                    "systems_thinking", "outcome_ownership", "metric_definition"],
}


def parse_facts_md(path: Path) -> list[dict]:
    if not path.exists():
        return []
    text = path.read_text()
    blocks = re.findall(r"---\n(.*?)\n---", text, re.DOTALL)
    facts = []
    for block in blocks:
        fact = {}
        for line in block.strip().split("\n"):
            if ":" in line and not line.startswith("  "):
                k, _, v = line.partition(":")
                fact[k.strip()] = v.strip().strip('"')
        if "id" in fact and "text" in fact:
            facts.append(fact)
    return facts


def parse_signals_md(path: Path) -> list[dict]:
    if not path.exists():
        return []
    text = path.read_text()
    blocks = re.findall(r"---\n(.*?)\n---", text, re.DOTALL)
    sigs = []
    for block in blocks:
        sig = {}
        lines = block.strip().split("\n")
        i = 0
        while i < len(lines):
            line = lines[i]
            if ":" in line and not line.startswith("  "):
                k, _, v = line.partition(":")
                k, v = k.strip(), v.strip().strip('"')
                if i + 1 < len(lines) and lines[i + 1].startswith("  - "):
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
            sigs.append(sig)
    return sigs


def score_relevance(text: str, query_terms: list[str]) -> int:
    text_lower = text.lower()
    return sum(1 for t in query_terms if t.lower() in text_lower)


def search(query: str, facts: list[dict], signals: list[dict], top: int = 10) -> dict:
    # Handle special queries
    if query.startswith("strength:"):
        strength_filter = query.split(":")[1].strip()
        matched_signals = [s for s in signals if s.get("strength") == strength_filter]
        return {"facts": [], "signals": matched_signals[:top]}

    terms = query.lower().split()
    scored_facts = []
    for f in facts:
        score = score_relevance(f.get("text", "") + " " + f.get("role", ""), terms)
        if score > 0:
            scored_facts.append((score, f))
    scored_facts.sort(key=lambda x: -x[0])

    scored_signals = []
    for s in signals:
        sig_text = s.get("name", "") + " " + s.get("description", "") + " " + s.get("label", "")
        score = score_relevance(sig_text, terms)
        if score > 0:
            scored_signals.append((score, s))
    scored_signals.sort(key=lambda x: -x[0])

    return {
        "facts":   [f for _, f in scored_facts[:top]],
        "signals": [s for _, s in scored_signals[:top]],
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--query", default=None)
    p.add_argument("--signal", default=None, help="Get facts for a specific signal")
    p.add_argument("--archetype", default=None, help="Get all signals for an archetype")
    p.add_argument("--memory", required=True)
    p.add_argument("--top", type=int, default=10)
    p.add_argument("--format", default="text", choices=["text", "json"])
    args = p.parse_args()

    memory = Path(args.memory)
    facts   = parse_facts_md(memory / "facts.md")
    signals = parse_signals_md(memory / "signals.md")
    signal_map = {s["name"]: s for s in signals}

    if args.archetype:
        required = ARCHETYPE_SIGNALS.get(args.archetype, [])
        result_signals = [signal_map[s] for s in required if s in signal_map]
        missing = [s for s in required if s not in signal_map]
        result = {"archetype": args.archetype, "signals": result_signals, "missing": missing}
        if args.format == "json":
            print(json.dumps(result, indent=2))
        else:
            print(f"\nSignals for archetype: {args.archetype}")
            for s in result_signals:
                print(f"  {s.get('strength','?'):6}  {s['name']}")
            if missing:
                print(f"\nMissing: {', '.join(missing)}")
        return

    if args.signal:
        sig = signal_map.get(args.signal)
        if not sig:
            print(json.dumps({"error": f"Signal '{args.signal}' not found"}))
            return
        fact_ids = sig.get("supporting_facts", [])
        supporting = [f for f in facts if f.get("id") in fact_ids]
        result = {"signal": sig, "supporting_facts": supporting}
        if args.format == "json":
            print(json.dumps(result, indent=2))
        else:
            print(f"\nSignal: {args.signal}  strength={sig.get('strength','?')}")
            for f in supporting:
                print(f"  {f['id']}: {f['text']}")
        return

    if args.query:
        result = search(args.query, facts, signals, args.top)
        if args.format == "json":
            print(json.dumps(result, indent=2))
        else:
            print(f"\nFACTS matching '{args.query}':")
            for f in result["facts"]:
                print(f"  {f['id']}: {f['text']}  ({f.get('role','')})")
            print(f"\nSIGNALS matching '{args.query}':")
            for s in result["signals"]:
                print(f"  {s['name']}  strength={s.get('strength','?')}")
        return

    # Default: show summary
    print(f"\nMEMORY SUMMARY")
    print(f"  Facts  : {len(facts)}")
    print(f"  Signals: {len(signals)}")
    by_strength = {}
    for s in signals:
        k = s.get("strength", "unknown")
        by_strength[k] = by_strength.get(k, 0) + 1
    for k, v in sorted(by_strength.items()):
        print(f"    {k}: {v}")


if __name__ == "__main__":
    main()
