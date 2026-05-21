"""
story_saver.py — Save finalized STAR-L story to linkright-mem expressions/stories/.

Usage:
  python3 story_saver.py --interactive
  python3 story_saver.py --story-type ambiguity_handling --text '<STAR-L text>' --signals systems_thinking,execution_rigor
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

STORIES_DIR = Path("~/.linkright/memory/expressions/stories").expanduser()

STORY_TYPES = [
    "ambiguity_handling",
    "stakeholder_conflict",
    "data_driven_decision",
    "failure_learning",
    "cross_functional_leadership",
    "systems_thinking",
    "customer_obsession",
    "vision_prioritization",
]


def next_id(story_type: str) -> str:
    STORIES_DIR.mkdir(parents=True, exist_ok=True)
    existing = list(STORIES_DIR.glob(f"{story_type}_*.md"))
    idx = len(existing) + 1
    return f"{story_type}_{idx:03d}"


def slug(text: str) -> str:
    words = re.sub(r"[^\w\s]", "", text.lower()).split()[:4]
    return "_".join(words)


def save(story_type: str, text: str, signals: list[str], constraint_status: str = "clean") -> Path:
    STORIES_DIR.mkdir(parents=True, exist_ok=True)
    story_id = next_id(story_type)
    title_slug = slug(text[:80])
    filename = f"{story_id}_{title_slug}.md"
    path = STORIES_DIR / filename

    content = f"""---
id: {story_id}
story_type: {story_type}
signals_demonstrated: [{", ".join(signals)}]
constraint_status: {constraint_status}
created: {date.today().isoformat()}
---

{text.strip()}
"""
    path.write_text(content)
    return path


def list_stories() -> dict:
    STORIES_DIR.mkdir(parents=True, exist_ok=True)
    counts = {t: 0 for t in STORY_TYPES}
    for f in STORIES_DIR.glob("*.md"):
        for t in STORY_TYPES:
            if f.name.startswith(t):
                counts[t] += 1
    return counts


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--story-type", choices=STORY_TYPES)
    p.add_argument("--text", default=None)
    p.add_argument("--signals", default="")
    p.add_argument("--constraint-status", default="clean", choices=["clean", "blocked", "warn"])
    p.add_argument("--status", action="store_true", help="Show story bank status")
    p.add_argument("--format", default="text", choices=["text", "json"])
    args = p.parse_args()

    if args.status:
        counts = list_stories()
        total = sum(counts.values())
        if args.format == "json":
            print(json.dumps({"total": total, "minimum": 16, "by_type": counts}))
        else:
            print("\nSTORY BANK STATUS")
            print(f"  Total: {total} / 16 minimum  (24 = strong bank)")
            print()
            for t, n in counts.items():
                mark = "✓" if n >= 2 else ("△" if n == 1 else "✗")
                print(f"  {mark}  {t:<35} {n}")
        return

    if not args.story_type:
        p.error("--story-type required (unless --status)")

    if args.constraint_status == "blocked":
        print("Error: cannot save a BLOCKED story. Resolve all Truth Engine violations first.", file=sys.stderr)
        sys.exit(1)

    text = args.text or sys.stdin.read()
    signals = [s.strip() for s in args.signals.split(",") if s.strip()]

    path = save(args.story_type, text, signals, args.constraint_status)
    if args.format == "json":
        print(json.dumps({"saved": str(path), "story_type": args.story_type}))
    else:
        print(f"\nStory saved: {path}")


if __name__ == "__main__":
    main()
