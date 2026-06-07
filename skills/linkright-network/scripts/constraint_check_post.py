"""
constraint_check_post.py — Check a LinkedIn post or email against user_setup.md constraints.

Usage:
  python3 constraint_check_post.py --text '<post>' --setup ~/.linkright/user_setup.md
  python3 constraint_check_post.py --text '<post>' --format json
"""

import argparse
import json
import re
import sys
from pathlib import Path


def parse_setup(path: Path) -> dict:
    if not path.exists():
        return {}
    text = path.read_text()
    setup = {}
    for key in ("do_not_mention", "companies_not_to_comment_on", "topics_to_avoid_in_posts"):
        block = re.search(rf"{key}[:\s]*\n((?:\s+[-*•].+\n?)+)", text, re.IGNORECASE)
        if block:
            items = re.findall(r"[-*•]\s+(.+)", block.group(1))
            setup[key] = [i.strip() for i in items]
    return setup


def check(text: str, setup: dict) -> list[dict]:
    flags = []
    text_lower = text.lower()

    for item in setup.get("do_not_mention", []):
        if item.lower() in text_lower:
            flags.append({"check": "do_not_mention", "severity": "BLOCK",
                          "detail": f"Mentions '{item}' which is in do_not_mention list.",
                          "fix": f"Remove all references to '{item}'."})

    for item in setup.get("companies_not_to_comment_on", []):
        if item.lower() in text_lower:
            flags.append({"check": "company_constraint", "severity": "BLOCK",
                          "detail": f"Comments on '{item}' which is in companies_not_to_comment_on.",
                          "fix": f"Remove all commentary about '{item}'."})

    for item in setup.get("topics_to_avoid_in_posts", []):
        if item.lower() in text_lower:
            flags.append({"check": "topic_constraint", "severity": "WARN",
                          "detail": f"Touches topic '{item}' in topics_to_avoid.",
                          "fix": f"Rephrase to avoid '{item}'."})

    return flags


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--text", required=True)
    p.add_argument("--setup", default="~/.linkright/user_setup.md")
    p.add_argument("--format", default="text", choices=["text", "json"])
    args = p.parse_args()

    setup = parse_setup(Path(args.setup).expanduser())
    flags = check(args.text, setup)
    blocks = [f for f in flags if f["severity"] == "BLOCK"]
    status = "BLOCKED" if blocks else ("WARN" if flags else "CLEAN")

    if args.format == "json":
        print(json.dumps({"status": status, "flags": flags}, indent=2))
        sys.exit(1 if blocks else 0)

    print(f"\nCONSTRAINT CHECK — {status}")
    if status == "CLEAN":
        print("  No constraint violations.")
        return
    for f in flags:
        print(f"  [{f['severity']}] {f['detail']}")
        print(f"    Fix: {f['fix']}")
    if blocks:
        sys.exit(1)


if __name__ == "__main__":
    main()
