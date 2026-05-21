"""
fact_extractor.py — Parse resume/LinkedIn/diary text → candidate facts.
Also handles conflict detection and writing confirmed facts to facts.md.

Usage:
  python3 fact_extractor.py --input resume.pdf --format auto --output /tmp/candidate_facts.json
  python3 fact_extractor.py --mode conflicts --new-facts /tmp/candidate.json --existing facts.md
  python3 fact_extractor.py --mode write --confirmed /tmp/confirmed.json --memory facts.md
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path


def parse_facts_md(path: Path) -> list[dict]:
    if not path.exists():
        return []
    text = path.read_text()
    blocks = re.findall(r"---\n(.*?)\n---", text, re.DOTALL)
    facts = []
    for block in blocks:
        try:
            fact = {}
            for line in block.strip().split("\n"):
                if ":" in line:
                    k, _, v = line.partition(":")
                    fact[k.strip()] = v.strip()
            if "id" in fact and "text" in fact:
                facts.append(fact)
        except Exception:
            continue
    return facts


def next_fact_id(existing_facts: list[dict]) -> str:
    existing_ids = [f.get("id", "FACT_000") for f in existing_facts]
    nums = []
    for fid in existing_ids:
        m = re.search(r"\d+", fid)
        if m:
            nums.append(int(m.group()))
    next_n = (max(nums) + 1) if nums else 1
    return f"FACT_{next_n:03d}"


def detect_conflicts(new_facts: list[dict], existing_facts: list[dict]) -> list[dict]:
    conflicts = []
    for new in new_facts:
        new_text = new.get("text", "").lower()
        new_role = new.get("role", "").lower()
        for existing in existing_facts:
            ex_text = existing.get("text", "").lower()
            ex_role = existing.get("role", "").lower()
            # Same role + similar subject matter (share 3+ words) but different metrics
            new_words = set(new_text.split())
            ex_words = set(ex_text.split())
            overlap = new_words & ex_words - {"the", "a", "an", "and", "to", "for", "of", "in", "at"}
            if len(overlap) >= 3 and new_role == ex_role and new_text != ex_text:
                # Check if any number changed → likely a metric conflict
                new_nums = set(re.findall(r"\d+", new_text))
                ex_nums = set(re.findall(r"\d+", ex_text))
                if new_nums != ex_nums and new_nums and ex_nums:
                    conflicts.append({"new": new, "existing": existing})
                    break
    return conflicts


def write_facts_to_md(confirmed: list[dict], facts_md_path: Path):
    existing = facts_md_path.read_text() if facts_md_path.exists() else \
        f"# LinkRight Memory — Facts\n# Created: {datetime.now().isoformat()}\n\n"
    existing_facts = parse_facts_md(facts_md_path)
    start_id = next_fact_id(existing_facts)
    start_num = int(re.search(r"\d+", start_id).group())

    new_blocks = []
    for i, fact in enumerate(confirmed):
        fid = fact.get("id") or f"FACT_{start_num + i:03d}"
        block = f"""---
id: {fid}
text: "{fact.get('text', '')}"
role: "{fact.get('role', '')}"
period: "{fact.get('period', '')}"
evidence_refs:
  - "{fact.get('source', 'manual')}"
confidence: {fact.get('confidence', 'confirmed')}
signals_derived: []
last_updated: "{datetime.now().date()}"
---
"""
        new_blocks.append(block)

    facts_md_path.write_text(existing.rstrip() + "\n\n" + "\n".join(new_blocks))
    return len(new_blocks)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--mode", default="extract", choices=["extract", "conflicts", "write"])
    p.add_argument("--input", help="Input file path or '-' for stdin")
    p.add_argument("--format", default="auto", choices=["auto", "pdf", "text", "json"])
    p.add_argument("--output", help="Output JSON path for candidate facts")
    p.add_argument("--new-facts", help="Path to new candidate facts JSON (conflict mode)")
    p.add_argument("--existing", help="Path to existing facts.md (conflict mode)")
    p.add_argument("--confirmed", help="Path to confirmed facts JSON (write mode)")
    p.add_argument("--memory", help="Path to facts.md (write mode)")
    args = p.parse_args()

    if args.mode == "conflicts":
        new_facts = json.loads(Path(args.new_facts).read_text())
        existing_facts = parse_facts_md(Path(args.existing))
        conflicts = detect_conflicts(new_facts, existing_facts)
        print(json.dumps({"conflicts": conflicts, "count": len(conflicts)}, indent=2))

    elif args.mode == "write":
        confirmed = json.loads(Path(args.confirmed).read_text())
        written = write_facts_to_md(confirmed, Path(args.memory))
        print(f"Written {written} facts to {args.memory}")

    else:  # extract
        if args.input == "-" or not args.input:
            text = sys.stdin.read()
        else:
            p_input = Path(args.input)
            if not p_input.exists():
                print(f"ERROR: {args.input} not found", file=sys.stderr)
                sys.exit(1)
            if args.format == "pdf" or (args.format == "auto" and p_input.suffix == ".pdf"):
                try:
                    import pdfminer.high_level
                    text = pdfminer.high_level.extract_text(str(p_input))
                except ImportError:
                    print("ERROR: pdfminer not installed. Run: pip install pdfminer.six", file=sys.stderr)
                    sys.exit(1)
            else:
                text = p_input.read_text()

        # Emit text for Claude to process — extraction done inline by Claude
        # This script handles parsing/writing; Claude does the LLM extraction
        print(json.dumps({
            "mode": "extract",
            "text_length": len(text),
            "text_preview": text[:500],
            "full_text": text,
            "note": "Claude extracts candidate facts from full_text, then calls --mode write"
        }, indent=2))


if __name__ == "__main__":
    main()
