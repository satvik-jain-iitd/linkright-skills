#!/usr/bin/env python3
"""
Check text against user_setup.md hard_constraints and do_not_mention list.
Usage: python3 constraint_checker.py --text '<text>' --constraints ~/.linkright/user_setup.md
Exit 0 = clean. Exit 1 = violations found (violations printed to stdout as JSON).
"""

import argparse
import json
import re
import sys
from pathlib import Path


def load_constraints(setup_path: str) -> dict:
    path = Path(setup_path).expanduser()
    if not path.exists():
        return {"hard_constraints": [], "do_not_mention": [], "topics_to_avoid_in_posts": [], "companies_not_to_comment_on": []}

    text = path.read_text()
    result = {"hard_constraints": [], "do_not_mention": [], "topics_to_avoid_in_posts": [], "companies_not_to_comment_on": []}

    # Parse YAML-ish list items under each key
    for key in result:
        pattern = rf'{key}:\s*\n((?:\s+-[^\n]+\n?)*)'
        m = re.search(pattern, text)
        if m:
            items = re.findall(r'-\s*(.+)', m.group(1))
            result[key] = [i.strip().strip('"\'') for i in items if i.strip()]

    return result


def check_text(text: str, constraints: dict) -> list:
    violations = []
    text_lower = text.lower()

    for item in constraints.get("do_not_mention", []):
        if item and item.lower() in text_lower:
            violations.append({
                "type": "do_not_mention",
                "item": item,
                "message": f"'{item}' is in your do-not-mention list"
            })

    for item in constraints.get("companies_not_to_comment_on", []):
        if item and item.lower() in text_lower:
            violations.append({
                "type": "companies_not_to_comment_on",
                "item": item,
                "message": f"'{item}' is in your companies-not-to-comment-on list"
            })

    for item in constraints.get("topics_to_avoid_in_posts", []):
        if item and item.lower() in text_lower:
            violations.append({
                "type": "topics_to_avoid_in_posts",
                "item": item,
                "message": f"'{item}' is a topic to avoid in posts"
            })

    return violations


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True, help="Text to check")
    parser.add_argument("--constraints", default="~/.linkright/user_setup.md", help="Path to user_setup.md")
    parser.add_argument("--format", choices=["json", "human"], default="human")
    args = parser.parse_args()

    constraints = load_constraints(args.constraints)
    violations = check_text(args.text, constraints)

    if args.format == "json":
        print(json.dumps({"violations": violations, "clean": len(violations) == 0}))
    else:
        if not violations:
            print("CLEAN — no constraint violations found.")
        else:
            print(f"VIOLATIONS FOUND ({len(violations)}):")
            for v in violations:
                print(f"  [{v['type']}] {v['message']}")

    sys.exit(0 if not violations else 1)


if __name__ == "__main__":
    main()
