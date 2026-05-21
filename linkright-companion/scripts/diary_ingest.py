"""
diary_ingest.py — Extract fact/signal/story candidates from a free-text reflection.

Usage:
  python3 diary_ingest.py --text 'Today I led the quarterly roadmap review...'
  echo 'reflection...' | python3 diary_ingest.py --stdin
  python3 diary_ingest.py --text '...' --format json
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

SIGNAL_KEYWORDS = {
    "stakeholder_leadership": ["stakeholder", "vp", "c-suite", "leadership", "alignment", "executive",
                                "cross-functional", "buy-in", "director", "sponsor"],
    "systems_thinking":       ["architecture", "system", "end-to-end", "downstream", "upstream",
                                "dependency", "pipeline", "infrastructure", "platform", "scale"],
    "execution_rigor":        ["shipped", "launched", "delivered", "deadline", "sprint", "roadmap",
                                "milestone", "on time", "scope", "cut", "prioritize"],
    "ambiguity_handling":     ["unclear", "ambiguous", "no process", "undefined", "figure out",
                                "from scratch", "first time", "nobody knew", "new territory"],
    "data_fluency":           ["metric", "data", "sql", "analytics", "dashboard", "kpi", "okr",
                                "measure", "track", "experiment", "a/b", "conversion", "retention"],
    "user_empathy":           ["user", "customer", "feedback", "interview", "survey", "pain point",
                                "insight", "research", "journey", "persona"],
    "ai_workflow_design":     ["ai", "llm", "prompt", "model", "ml", "generative", "api", "claude",
                                "chatgpt", "automation", "workflow"],
    "communication_clarity":  ["presentation", "wrote", "explained", "communicated", "document",
                                "spec", "prd", "brief", "email", "narrative"],
}

STORY_TYPE_KEYWORDS = {
    "ambiguity_handling":         ["no direction", "unclear", "from scratch", "undefined"],
    "stakeholder_conflict":       ["disagreed", "pushed back", "conflict", "tension", "politics"],
    "data_driven_decision":       ["data showed", "metric", "experiment", "chose based on"],
    "failure_learning":           ["failed", "didn't work", "wrong", "mistake", "learned"],
    "cross_functional_leadership":["across teams", "without authority", "aligned", "led without"],
    "systems_thinking":           ["end-to-end", "system design", "trade-off", "architecture"],
    "customer_obsession":         ["user insight", "changed direction", "customer said"],
    "vision_prioritization":      ["prioritize", "cut", "said no", "focus on", "trade-off"],
}

FACT_PATTERNS = [
    r"(?:led|ran|owned|drove|shipped|launched|built|created|managed|coordinated)\s+.{10,80}",
    r"(?:reduced|increased|improved|grew|cut|saved)\s+.{5,60}(?:\d+|%|percent|x\b)",
    r"\d+\s*(?:%|percent|x\b|users?|customers?|k\b|million|teams?|stakeholders?)\s+.{5,50}",
]


def extract_signals(text: str) -> list[dict]:
    text_lower = text.lower()
    found = []
    for signal, keywords in SIGNAL_KEYWORDS.items():
        matches = [k for k in keywords if k in text_lower]
        if len(matches) >= 2:
            found.append({"signal": signal, "evidence_keywords": matches, "confidence": "HIGH" if len(matches) >= 3 else "MEDIUM"})
        elif matches:
            found.append({"signal": signal, "evidence_keywords": matches, "confidence": "LOW"})
    return sorted(found, key=lambda x: {"HIGH":0,"MEDIUM":1,"LOW":2}[x["confidence"]])


def extract_facts(text: str) -> list[str]:
    found = []
    for pat in FACT_PATTERNS:
        for m in re.finditer(pat, text, re.IGNORECASE):
            candidate = m.group(0).strip().rstrip(",;.")
            if len(candidate) > 15:
                found.append(candidate)
    # Deduplicate by first 30 chars
    seen = set()
    result = []
    for f in found:
        key = f[:30].lower()
        if key not in seen:
            seen.add(key)
            result.append(f)
    return result[:5]


def detect_story(text: str) -> list[dict]:
    text_lower = text.lower()
    found = []
    for story_type, keywords in STORY_TYPE_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                found.append({"story_type": story_type, "trigger_phrase": kw})
                break
    return found


def write_diary(text: str) -> Path:
    diary_dir = Path("~/.linkright/memory/diary").expanduser()
    diary_dir.mkdir(parents=True, exist_ok=True)
    path = diary_dir / f"{date.today().isoformat()}.md"
    existing = path.read_text() if path.exists() else ""
    separator = "\n\n---\n\n" if existing else ""
    path.write_text(existing + separator + text.strip())
    return path


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--text", default=None)
    p.add_argument("--stdin", action="store_true")
    p.add_argument("--no-diary-write", action="store_true")
    p.add_argument("--format", default="text", choices=["text", "json"])
    args = p.parse_args()

    if args.stdin or args.text is None:
        text = sys.stdin.read().strip()
    else:
        text = args.text.strip()

    if not text:
        p.error("No reflection text provided")

    signals = extract_signals(text)
    facts = extract_facts(text)
    stories = detect_story(text)

    # Always write diary
    if not args.no_diary_write:
        diary_path = write_diary(text)

    if args.format == "json":
        print(json.dumps({
            "date": date.today().isoformat(),
            "fact_candidates": facts,
            "signal_evidence": signals,
            "story_candidates": stories,
        }, indent=2))
        return

    print(f"\nDIARY EXTRACTION — {date.today().strftime('%d %b %Y')}")
    if not args.no_diary_write:
        print(f"  Diary written: {diary_path}\n")

    if facts:
        print("FACT CANDIDATES:")
        for f in facts:
            print(f"  → \"{f}\"")
        print()

    if signals:
        print("SIGNAL EVIDENCE:")
        high = [s for s in signals if s["confidence"] == "HIGH"]
        med  = [s for s in signals if s["confidence"] == "MEDIUM"]
        for s in high + med:
            print(f"  → {s['signal']}  [{s['confidence']}]  ({', '.join(s['evidence_keywords'][:3])})")
        print()

    if stories:
        print("INTERVIEW STORY CANDIDATES:")
        for s in stories:
            print(f"  → story_type: {s['story_type']}  (trigger: '{s['trigger_phrase']}')")
        print()

    if facts or signals or stories:
        print("ROUTING:")
        if facts or signals:
            print("  Send fact/signal candidates to linkright-mem? (y/n)")
        if stories:
            print("  Send story candidates to linkright-interview? (y/n)")
        print("  Nothing persists until you confirm.")
    else:
        print("  No clear fact/signal/story candidates found.")
        print("  Diary saved. Add more specific details for richer extraction.")


if __name__ == "__main__":
    main()
