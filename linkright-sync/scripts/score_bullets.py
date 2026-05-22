#!/usr/bin/env python3
"""
BRS (Bullet Relevance Score) — score a fact/bullet against JD signals.
Usage: python3 score_bullets.py --facts facts.md --signals signals.md --jd-signals '["systems_thinking","ai_workflow_design"]'
Output: JSON list of {fact_id, text, brs, signals_matched, signals_missing}
"""

import argparse
import json
import re
import sys
from pathlib import Path


def load_facts(facts_path: str) -> list:
    path = Path(facts_path).expanduser()
    if not path.exists():
        return []
    text = path.read_text()
    facts = []
    blocks = re.split(r'^---\s*$', text, flags=re.MULTILINE)
    for block in blocks:
        if 'id:' not in block:
            continue
        fact = {}
        for line in block.strip().splitlines():
            line = line.strip()
            if m := re.match(r'^id:\s*(.+)', line):
                fact['id'] = m.group(1).strip()
            elif m := re.match(r'^text:\s*"?(.+?)"?\s*$', line):
                fact['text'] = m.group(1).strip().strip('"')
            elif m := re.match(r'^signals_derived:\s*\[(.+)\]', line):
                fact['signals'] = [s.strip() for s in m.group(1).split(',')]
        if 'id' in fact and 'text' in fact:
            fact.setdefault('signals', [])
            facts.append(fact)
    return facts


def load_signals_from_facts_file(facts_path: str) -> dict:
    """Build signal→facts map from facts.md."""
    facts = load_facts(facts_path)
    signal_map = {}
    for f in facts:
        for sig in f.get('signals', []):
            signal_map.setdefault(sig, []).append(f['id'])
    return signal_map


def score_fact(fact: dict, jd_signals: list) -> dict:
    """Score a single fact against JD signal list."""
    matched = [s for s in jd_signals if s in fact.get('signals', [])]
    missing = [s for s in jd_signals if s not in fact.get('signals', [])]

    # BRS = (matched signals / total jd signals) * 100, min 10 if any match
    if not jd_signals:
        brs = 50
    elif matched:
        brs = max(10, int((len(matched) / len(jd_signals)) * 100))
    else:
        brs = 0

    return {
        'fact_id': fact['id'],
        'text': fact['text'],
        'brs': brs,
        'signals_matched': matched,
        'signals_missing': missing,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--facts", default="~/.linkright/memory/facts.md")
    parser.add_argument("--signals", default="~/.linkright/memory/signals.md")
    parser.add_argument("--jd-signals", required=True, help="JSON array of required signal names")
    parser.add_argument("--top", type=int, default=10, help="Return top N by BRS")
    parser.add_argument("--format", choices=["json", "human"], default="json")
    args = parser.parse_args()

    try:
        jd_signals = json.loads(args.jd_signals)
    except json.JSONDecodeError:
        print(json.dumps({"error": "jd-signals must be valid JSON array"}))
        sys.exit(1)

    facts = load_facts(args.facts)
    if not facts:
        print(json.dumps({"error": f"No facts loaded from {args.facts}"}))
        sys.exit(1)

    scored = [score_fact(f, jd_signals) for f in facts]
    scored.sort(key=lambda x: x['brs'], reverse=True)
    top = scored[:args.top]

    if args.format == "json":
        print(json.dumps(top, indent=2))
    else:
        print(f"Top {len(top)} facts by BRS (JD signals: {', '.join(jd_signals)})\n")
        for item in top:
            matched_str = ', '.join(item['signals_matched']) or 'none'
            print(f"  [{item['brs']:3d}] {item['fact_id']}: {item['text'][:80]}")
            print(f"       Signals matched: {matched_str}")


if __name__ == "__main__":
    main()
