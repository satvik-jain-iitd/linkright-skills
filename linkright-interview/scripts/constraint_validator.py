"""
constraint_validator.py — Truth Engine for STAR story validation.

Usage:
  python3 constraint_validator.py --text '<story_text>' --setup ~/.linkright/user_setup.md
  python3 constraint_validator.py --file story.md --setup ~/.linkright/user_setup.md
"""

import argparse
import json
import re
import sys
from pathlib import Path


WEAK_METRIC_PATTERNS = [
    r"\bsignificantly\s+(?:improved|reduced|increased|decreased|enhanced|boosted)\b",
    r"\bdramatically\s+(?:improved|reduced|increased|decreased)\b",
    r"\bsubstantially\s+(?:improved|reduced|increased)\b",
    r"\bgreatly\s+(?:improved|reduced|increased)\b",
    r"\bmajorly\s+\w+",
    r"\bmany\s+(?:users|customers|clients)\b(?!\s+\()",
    r"\bnumerous\s+(?:stakeholders|teams|partners)\b",
]

OWNERSHIP_PATTERNS = [
    r"\bwe\s+built\b(?!\s+a\s+team)",
    r"\bwe\s+launched\b",
    r"\bwe\s+shipped\b",
    r"\bwe\s+created\b",
    r"\bour\s+team\s+(?:built|launched|shipped|created|developed)\b",
]


def parse_setup(path: Path) -> dict:
    if not path.exists():
        return {}
    text = path.read_text()
    setup = {}

    hard_block = re.search(r"hard_constraints?[:\s]*\n((?:\s+[-*•].+\n?)+)", text, re.IGNORECASE)
    if hard_block:
        items = re.findall(r"[-*•]\s+(.+)", hard_block.group(1))
        setup["hard_constraints"] = [i.strip() for i in items]

    dont_block = re.search(r"do_not_mention[:\s]*\n((?:\s+[-*•].+\n?)+)", text, re.IGNORECASE)
    if dont_block:
        items = re.findall(r"[-*•]\s+(.+)", dont_block.group(1))
        setup["do_not_mention"] = [i.strip() for i in items]

    not_owned = re.search(r"not_owned[:\s]*\n((?:\s+[-*•].+\n?)+)", text, re.IGNORECASE)
    if not_owned:
        items = re.findall(r"[-*•]\s+(.+)", not_owned.group(1))
        setup["not_owned"] = [i.strip() for i in items]

    return setup


def validate(text: str, setup: dict) -> list[dict]:
    flags = []
    text_lower = text.lower()

    # Check 1: do_not_mention
    for item in setup.get("do_not_mention", []):
        if item.lower() in text_lower:
            flags.append({
                "check": "hard_constraint",
                "severity": "BLOCK",
                "detail": f"References '{item}' which is in do_not_mention list.",
                "fix": f"Remove or replace any reference to '{item}'.",
            })

    # Check 2: not_owned claims
    for item in setup.get("not_owned", []):
        if item.lower() in text_lower:
            flags.append({
                "check": "hard_constraint",
                "severity": "BLOCK",
                "detail": f"References '{item}' which is marked not_owned.",
                "fix": f"Remove claim about '{item}' or clarify your specific contributing role.",
            })

    # Check 3: weak/unquantified metrics
    for pattern in WEAK_METRIC_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            flags.append({
                "check": "metric_defensibility",
                "severity": "WARN",
                "detail": f"Vague metric: '{match}' — no number attached.",
                "fix": "Replace with specific number, percentage, or label as 'estimated' if unsure.",
            })

    # Check 4: ownership clarity (we-language without role spec)
    for pattern in OWNERSHIP_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            flags.append({
                "check": "ownership_clarity",
                "severity": "WARN",
                "detail": f"'We' language without specifying your individual role.",
                "fix": "Replace with 'I' + your specific action, or add '(my role: [X])'.",
            })

    # Check 5: no quantified result at all
    has_metric = bool(re.search(
        r"\b\d+\s*(?:%|percent|x|times|hours?|days?|weeks?|months?|users?|customers?|k|M|crore|lakh|LPA|USD|INR|\$|₹)\b",
        text, re.IGNORECASE
    ))
    if not has_metric:
        flags.append({
            "check": "metric_defensibility",
            "severity": "WARN",
            "detail": "No quantified metric found in story.",
            "fix": "Add at least one number (%, time, count, $, or label as user_estimate).",
        })

    return flags


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--text", default=None)
    p.add_argument("--file", default=None)
    p.add_argument("--setup", default="~/.linkright/user_setup.md")
    p.add_argument("--format", default="text", choices=["text", "json"])
    args = p.parse_args()

    if args.text:
        text = args.text
    elif args.file:
        f = Path(args.file).expanduser()
        if not f.exists():
            print(f"Error: file not found: {f}", file=sys.stderr)
            sys.exit(1)
        text = f.read_text()
    else:
        text = sys.stdin.read()

    setup = parse_setup(Path(args.setup).expanduser())
    flags = validate(text, setup)

    blocks = [f for f in flags if f["severity"] == "BLOCK"]
    warns  = [f for f in flags if f["severity"] == "WARN"]
    status = "BLOCKED" if blocks else ("WARN" if warns else "CLEAN")

    if args.format == "json":
        print(json.dumps({"status": status, "blocks": blocks, "warnings": warns}, indent=2))
        return

    print(f"\nTRUTH ENGINE — {status}")
    if status == "CLEAN":
        print("  All checks passed. Story is ready to save.")
        return

    if blocks:
        print(f"\nBLOCKERS ({len(blocks)}) — must resolve before saving:")
        for i, f in enumerate(blocks, 1):
            print(f"  {i}. [{f['check']}] {f['detail']}")
            print(f"     Fix: {f['fix']}")

    if warns:
        print(f"\nWARNINGS ({len(warns)}) — recommended to resolve:")
        for i, f in enumerate(warns, 1):
            print(f"  {i}. [{f['check']}] {f['detail']}")
            print(f"     Fix: {f['fix']}")

    if blocks:
        sys.exit(1)


if __name__ == "__main__":
    main()
