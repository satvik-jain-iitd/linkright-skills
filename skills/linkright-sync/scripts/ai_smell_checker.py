#!/usr/bin/env python3
"""
Detect AI-generated language patterns in resume text.
Usage: python3 ai_smell_checker.py '<text>'
Output: JSON {"flagged": [...], "clean": bool, "count": N}
"""

import argparse
import json
import re
import sys

# Patterns that scream "written by AI" — exact phrases and regex
AI_SMELL_PATTERNS = [
    # Generic superlatives
    (r'\bexceptional\b', "generic superlative"),
    (r'\bexcellent\b', "generic superlative"),
    (r'\boutstanding\b', "generic superlative"),
    (r'\bimpactful\b', "AI buzzword"),
    (r'\bseamlessly\b', "AI filler"),
    (r'\brobust\b', "overused adjective"),
    (r'\bscalable solution', "AI boilerplate"),
    (r'\bleverage[d]?\b', "corporate jargon"),
    (r'\butilize[d]?\b', "prefer 'use'"),
    (r'\bfacilitate[d]?\b', "prefer 'led' or 'drove'"),
    (r'\bsynergize[d]?\b', "jargon"),
    (r'\bsynergy\b', "jargon"),
    (r'\bholistic(ally)?\b', "vague"),
    (r'\bparadigm shift\b', "cliché"),
    (r'\bthought leader', "cliché"),
    (r'\bdiverse stakeholder', "AI filler"),
    (r'\bkey stakeholders\b', "vague — name them"),
    (r'\bcross-functional teams\b', "vague — specify teams"),
    (r'\bdrove significant\b', "unquantified claim"),
    (r'\bsignificantly improved\b', "vague — add metric"),
    (r'\bdramatically (improved|reduced|increased)\b', "vague — add metric"),
    (r'\bsignificant impact\b', "vague — add metric"),
    (r'\ba wide range of\b', "AI filler"),
    (r'\bvast array of\b', "AI filler"),
    (r'\bin a fast-paced environment\b', "cliché"),
    (r'\bpassionate about\b', "cliché"),
    (r'\bresults-driven\b', "cliché"),
    (r'\bgo-getter\b', "cliché"),
    (r'\bteam player\b', "cliché"),
    (r'\bself-starter\b', "cliché"),
    (r'\bhard-working\b', "cliché"),
    (r'\bdetail-oriented\b', "cliché"),
    (r'\bstrong work ethic\b', "cliché"),
    (r'\bproactive\b', "overused — show don't tell"),
    (r'\bensured\b', "passive — use active verb"),
    (r'\bresponsible for\b', "passive — use active verb"),
    (r'\bassisted (in|with)\b', "weak — led/built/drove"),
    (r'\bhelped (to|with)?\b', "weak — led/built/drove"),
    (r'\bworked (with|on|to)\b', "vague — specify action"),
    (r'\bcontributed to\b', "vague — specify contribution"),
    (r'\bplayed a (key|pivotal|critical) role\b', "vague — show what you did"),
    (r'\bto the best of my ability\b', "filler"),
    (r'\bI am excited to\b', "cover letter cliché"),
    (r'\bI believe I would be\b', "cover letter cliché"),
    (r'\bin today\'s (fast-paced|ever-changing|dynamic)\b', "AI opener"),
    (r'\bwhereby\b', "legalese"),
    (r'\bthereafter\b', "legalese"),
    (r'\bwherein\b', "legalese"),
    (r'\bone-stop(-shop)?\b', "marketing cliché"),
    (r'\bend-to-end\b', "overused — be specific"),
    (r'\bstate-of-the-art\b', "marketing"),
    (r'\bcutting-edge\b', "marketing"),
    (r'\bworld-class\b', "marketing"),
    (r'\bpivotal role\b', "vague — show what you did"),
    (r'\bkey (driver|contributor|factor)\b', "vague"),
]


def check_text(text: str) -> list:
    findings = []
    text_lower = text.lower()
    for pattern, reason in AI_SMELL_PATTERNS:
        matches = list(re.finditer(pattern, text_lower))
        for m in matches:
            findings.append({
                "phrase": text[m.start():m.end()],
                "reason": reason,
                "position": m.start(),
            })
    # Deduplicate by phrase
    seen = set()
    unique = []
    for f in findings:
        key = f["phrase"].lower()
        if key not in seen:
            seen.add(key)
            unique.append(f)
    return unique


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("text", nargs="?", help="Text to check")
    parser.add_argument("--file", help="File path to check")
    parser.add_argument("--format", choices=["json", "human"], default="json")
    args = parser.parse_args()

    if args.file:
        from pathlib import Path
        text = Path(args.file).expanduser().read_text()
    elif args.text:
        text = args.text
    else:
        text = sys.stdin.read()

    findings = check_text(text)
    result = {"flagged": findings, "clean": len(findings) == 0, "count": len(findings)}

    if args.format == "json":
        print(json.dumps(result))
    else:
        if result["clean"]:
            print("✓ CLEAN — no AI-smell patterns detected")
        else:
            print(f"✗ {result['count']} AI-smell phrase(s) found:")
            for f in findings:
                print(f"  \"{f['phrase']}\" — {f['reason']}")

    sys.exit(0 if result["clean"] else 1)


if __name__ == "__main__":
    main()
