"""
signal_deriver.py — Given confirmed facts, derive candidate signals.
Loads existing signals.md, finds new signal opportunities, outputs candidates for Claude review.

Usage:
  python3 signal_deriver.py --facts facts.md --existing-signals signals.md --output /tmp/candidates.json
  python3 signal_deriver.py --mode write --confirmed /tmp/confirmed_signals.json --memory signals.md
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

# Signal taxonomy — keywords that map to signals
SIGNAL_KEYWORD_MAP = {
    "systems_thinking": [
        "redesign", "workflow", "architecture", "interconnect", "end-to-end",
        "system", "pipeline", "process", "framework", "infrastructure",
        "orchestrat", "integrat", "complex", "cross-functional",
    ],
    "stakeholder_leadership": [
        "stakeholder", "align", "executive", "leadership", "manage upward",
        "cross-functional", "partner", "collaborate", "present", "influence",
        "without authority", "ministry", "c-suite", "vp", "director",
    ],
    "execution_rigor": [
        "deliver", "ship", "launch", "on time", "sprint", "pi ", "roadmap",
        "milestone", "zero spillover", "deployment", "release", "agile",
        "scrum", "velocity", "OKR", "metric", "track",
    ],
    "data_fluency": [
        "data", "analytics", "sql", "dashboard", "insight", "metric",
        "kpi", "report", "analysis", "query", "model", "dataset",
        "a/b test", "experiment", "measure",
    ],
    "ambiguity_handling": [
        "ambiguous", "undefined", "0 to 1", "zero to one", "new market",
        "first principles", "greenfield", "pioneer", "define scope",
        "uncertain", "early stage", "no playbook",
    ],
    "ai_workflow_design": [
        "ai", "llm", "genai", "generative", "nlp", "machine learning",
        "ml", "rag", "embedding", "prompt", "model evaluation", "agent",
        "automation", "root cause", "taxonomy", "classification",
    ],
    "enterprise_workflow_ownership": [
        "enterprise", "b2b", "saas", "onboarding", "implementation",
        "client", "customer success", "account", "workflow", "adoption",
        "time to value", "ttv", "platform", "integration",
    ],
    "growth_experimentation": [
        "growth", "experiment", "a/b", "funnel", "conversion", "retention",
        "activation", "acquisition", "churn", "cohort", "north star",
        "dau", "mau", "engagement", "viral",
    ],
    "user_empathy": [
        "user research", "usability", "interview", "feedback", "pain point",
        "user need", "customer", "persona", "journey", "ux", "delight",
    ],
    "communication_clarity": [
        "present", "communicate", "write", "document", "spec", "prd",
        "brief", "narrative", "story", "explain", "translate", "simplif",
    ],
    "zero_to_one_execution": [
        "found", "built from scratch", "created", "launched", "solo",
        "0 to 1", "zero to one", "startup", "mvp", "first version",
    ],
    "implementation_management": [
        "implement", "deploy", "onboard", "configure", "integrate",
        "rollout", "go-live", "setup", "migration", "transition",
    ],
}


def parse_facts_md(path: Path) -> list[dict]:
    if not path.exists():
        return []
    text = path.read_text()
    blocks = re.findall(r"---\n(.*?)\n---", text, re.DOTALL)
    facts = []
    for block in blocks:
        fact = {"signals_derived": [], "evidence_refs": []}
        lines = block.strip().split("\n")
        i = 0
        while i < len(lines):
            line = lines[i]
            if ":" in line and not line.startswith("  "):
                k, _, v = line.partition(":")
                k, v = k.strip(), v.strip()
                if v.startswith("["):
                    items = []
                    i += 1
                    while i < len(lines) and lines[i].startswith("  - "):
                        items.append(lines[i][4:].strip('"'))
                        i += 1
                    fact[k] = items
                    continue
                else:
                    fact[k] = v.strip('"')
            i += 1
        if "id" in fact and "text" in fact:
            facts.append(fact)
    return facts


def parse_signals_md(path: Path) -> list[dict]:
    if not path.exists():
        return []
    text = path.read_text()
    blocks = re.findall(r"---\n(.*?)\n---", text, re.DOTALL)
    signals = []
    for block in blocks:
        sig = {}
        for line in block.strip().split("\n"):
            if ":" in line:
                k, _, v = line.partition(":")
                sig[k.strip()] = v.strip().strip('"')
        if "id" in sig and "name" in sig:
            signals.append(sig)
    return signals


def score_fact_for_signal(fact_text: str, keywords: list[str]) -> int:
    text_lower = fact_text.lower()
    return sum(1 for kw in keywords if kw in text_lower)


def derive_candidates(facts: list[dict], existing_signals: list[dict]) -> list[dict]:
    existing_signal_names = {s["name"] for s in existing_signals}
    signal_fact_map: dict[str, list[str]] = {}

    for fact in facts:
        text = fact.get("text", "")
        for signal_name, keywords in SIGNAL_KEYWORD_MAP.items():
            if score_fact_for_signal(text, keywords) >= 1:
                signal_fact_map.setdefault(signal_name, []).append(fact["id"])

    candidates = []
    existing_signal_map = {s["name"]: s for s in existing_signals}

    for signal_name, fact_ids in signal_fact_map.items():
        if len(fact_ids) == 0:
            continue
        if signal_name in existing_signal_map:
            # Strengthen existing signal
            existing = existing_signal_map[signal_name]
            current_facts = existing.get("supporting_facts", [])
            new_facts = [f for f in fact_ids if f not in current_facts]
            if new_facts:
                candidates.append({
                    "action": "strengthen",
                    "signal_name": signal_name,
                    "existing_id": existing["id"],
                    "new_supporting_facts": new_facts,
                    "current_strength": existing.get("strength", "medium"),
                })
        else:
            # New signal
            strength = "high" if len(fact_ids) >= 3 else "medium" if len(fact_ids) >= 2 else "low"
            sig_num = len(existing_signals) + len(candidates) + 1
            candidates.append({
                "action": "new",
                "id": f"SIG_{sig_num:03d}",
                "name": signal_name,
                "supporting_facts": fact_ids,
                "strength": strength,
            })

    return candidates


def write_signals_to_md(confirmed: list[dict], signals_md_path: Path):
    existing_text = signals_md_path.read_text() if signals_md_path.exists() else \
        f"# LinkRight Memory — Signals\n# Created: {datetime.now().isoformat()}\n\n"

    new_blocks = []
    for sig in confirmed:
        if sig.get("action") == "new":
            facts_yaml = "\n".join(f"  - {f}" for f in sig.get("supporting_facts", []))
            block = f"""---
id: {sig['id']}
name: "{sig['name']}"
label: "{sig['name'].replace('_', ' ').title()}"
description: ""
supporting_facts:
{facts_yaml}
strength: {sig.get('strength', 'medium')}
confidence: confirmed
market_relevance: high
last_updated: "{datetime.now().date()}"
---
"""
            new_blocks.append(block)

    signals_md_path.write_text(existing_text.rstrip() + "\n\n" + "\n".join(new_blocks))
    return len(new_blocks)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--mode", default="derive", choices=["derive", "write"])
    p.add_argument("--facts", help="Path to facts.md")
    p.add_argument("--existing-signals", help="Path to signals.md")
    p.add_argument("--output", help="Output path for candidate signals JSON")
    p.add_argument("--confirmed", help="Confirmed signals JSON (write mode)")
    p.add_argument("--memory", help="Path to signals.md (write mode)")
    args = p.parse_args()

    if args.mode == "write":
        confirmed = json.loads(Path(args.confirmed).read_text())
        written = write_signals_to_md(confirmed, Path(args.memory))
        print(f"Written {written} new signals to {args.memory}")
        return

    facts = parse_facts_md(Path(args.facts)) if args.facts else []
    existing = parse_signals_md(Path(args.existing_signals)) if args.existing_signals else []

    candidates = derive_candidates(facts, existing)

    result = {"candidates": candidates, "count": len(candidates)}
    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
