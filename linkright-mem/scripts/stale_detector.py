"""
stale_detector.py — Find stale facts, weak signals, archetype gaps.

Usage:
  python3 stale_detector.py --memory ~/.linkright/memory --stale-days 180
"""

import argparse
import json
import re
from datetime import datetime, timedelta
from pathlib import Path


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
        if "id" in fact:
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


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--memory", required=True)
    p.add_argument("--stale-days", type=int, default=180)
    p.add_argument("--format", default="text", choices=["text", "json"])
    args = p.parse_args()

    memory = Path(args.memory)
    facts = parse_facts_md(memory / "facts.md")
    signals = parse_signals_md(memory / "signals.md")
    cutoff = datetime.now() - timedelta(days=args.stale_days)

    stale_facts = []
    for f in facts:
        if f.get("stale") == "true":
            continue
        updated_str = f.get("last_updated", "")
        if updated_str:
            try:
                updated = datetime.fromisoformat(updated_str)
                if updated < cutoff:
                    stale_facts.append(f)
            except ValueError:
                pass

    weak_signals = [s for s in signals if s.get("strength") == "low"]
    orphan_signals = [s for s in signals if not s.get("supporting_facts")]

    report = {
        "stale_facts":      [{"id": f["id"], "text": f.get("text",""), "last_updated": f.get("last_updated","")} for f in stale_facts],
        "weak_signals":     [{"name": s["name"], "strength": s.get("strength","")} for s in weak_signals],
        "orphan_signals":   [{"name": s["name"]} for s in orphan_signals],
        "stale_days_threshold": args.stale_days,
        "total_facts":      len(facts),
        "total_signals":    len(signals),
    }

    if args.format == "json":
        print(json.dumps(report, indent=2))
        return

    print(f"\nAUDIT REPORT  (stale threshold: {args.stale_days} days)")
    print(f"  Total facts  : {len(facts)}")
    print(f"  Total signals: {len(signals)}")

    if stale_facts:
        print(f"\nSTALE FACTS ({len(stale_facts)}) — not updated in {args.stale_days}+ days:")
        for f in stale_facts:
            print(f"  {f['id']}: {f.get('text','')}  (last: {f.get('last_updated','')})")

    if weak_signals:
        print(f"\nWEAK SIGNALS ({len(weak_signals)}) — strength=low:")
        for s in weak_signals:
            print(f"  {s['name']}")

    if orphan_signals:
        print(f"\nORPHAN SIGNALS ({len(orphan_signals)}) — 0 supporting facts:")
        for s in orphan_signals:
            print(f"  {s['name']}")

    if not stale_facts and not weak_signals and not orphan_signals:
        print("\n  Memory is clean. No issues found.")


if __name__ == "__main__":
    main()
