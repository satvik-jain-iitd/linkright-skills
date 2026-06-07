"""
decision_log.py — Write and read decisions from decision_log.md.

Usage:
  python3 decision_log.py --write --title '...' --chosen '...' --reasoning '...' --assumption '...'
  python3 decision_log.py --list --log ~/.linkright/memory/decisions/decision_log.md
  python3 decision_log.py --due-today
"""

import argparse
import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

DEFAULT_LOG = Path("~/.linkright/memory/decisions/decision_log.md").expanduser()

ENTRY_SEP = "\n---\n"


def write_entry(log: Path, title: str, context: str, options: list[str],
                chosen: str, reasoning: str, assumption: str, review_days: int) -> str:
    log.parent.mkdir(parents=True, exist_ok=True)

    today = date.today().isoformat()
    review_date = (date.today() + timedelta(days=review_days)).isoformat()
    entry_id = f"dec_{today.replace('-','')}_{len(title)}"

    options_md = "\n".join(f"  - {o}" for o in options) if options else "  - (not recorded)"

    entry = f"""## {title}

**ID:** {entry_id}
**Date:** {today}
**Review date:** {review_date}
**Status:** open

**Context:**
{context}

**Options considered:**
{options_md}

**Chosen:** {chosen}

**Reasoning:** {reasoning}

**Key assumption:** {assumption}
*(What would have to be true for this to be the right call.)*
"""

    existing = log.read_text() if log.exists() else "# Decision Log\n"
    log.write_text(existing.rstrip() + ENTRY_SEP + entry)

    print(f"\n✓ Decision logged: {title}")
    print(f"  Review date: {review_date} — companion will surface this entry then.")
    return entry_id


def list_entries(log: Path) -> list[dict]:
    if not log.exists():
        return []
    text = log.read_text()
    entries = []
    blocks = text.split(ENTRY_SEP)
    for block in blocks:
        m_title = re.search(r"^## (.+)", block, re.MULTILINE)
        m_date = re.search(r"\*\*Date:\*\* (.+)", block)
        m_review = re.search(r"\*\*Review date:\*\* (.+)", block)
        m_id = re.search(r"\*\*ID:\*\* (.+)", block)
        m_status = re.search(r"\*\*Status:\*\* (.+)", block)
        if m_title:
            entries.append({
                "title":       m_title.group(1).strip(),
                "id":          m_id.group(1).strip() if m_id else "",
                "date":        m_date.group(1).strip() if m_date else "",
                "review_date": m_review.group(1).strip() if m_review else "",
                "status":      m_status.group(1).strip() if m_status else "open",
            })
    return entries


def due_today(log: Path) -> list[dict]:
    entries = list_entries(log)
    today = date.today().isoformat()
    return [e for e in entries if e.get("review_date", "") <= today and e.get("status") == "open"]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--log", default=str(DEFAULT_LOG))
    p.add_argument("--write", action="store_true")
    p.add_argument("--list", action="store_true", dest="list_mode")
    p.add_argument("--due-today", action="store_true")
    p.add_argument("--format", default="text", choices=["text", "json"])
    # Write args
    p.add_argument("--title", default="")
    p.add_argument("--context", default="")
    p.add_argument("--options", nargs="*", default=[])
    p.add_argument("--chosen", default="")
    p.add_argument("--reasoning", default="")
    p.add_argument("--assumption", default="")
    p.add_argument("--review-days", type=int, default=14)
    args = p.parse_args()

    log = Path(args.log).expanduser()

    if args.write:
        if not args.title:
            p.error("--title required for --write")
        write_entry(log, args.title, args.context, args.options,
                    args.chosen, args.reasoning, args.assumption, args.review_days)
        return

    if args.due_today:
        entries = due_today(log)
        if args.format == "json":
            print(json.dumps(entries, indent=2))
            return
        if not entries:
            print("No decisions due for review today.")
            return
        print(f"\nDECISIONS DUE FOR REVIEW ({len(entries)}):")
        for e in entries:
            print(f"  {e['date']}  {e['title']}")
            print(f"           Review date was: {e['review_date']}")
        print("\nRun /linkright-companion → H) to review each.")
        return

    if args.list_mode:
        entries = list_entries(log)
        if args.format == "json":
            print(json.dumps(entries, indent=2))
            return
        if not entries:
            print("No decisions logged yet.")
            return
        print(f"\nDECISION LOG ({len(entries)} entries):")
        for e in entries:
            marker = "⏰" if e.get("review_date", "") <= date.today().isoformat() else "  "
            print(f"  {marker} {e['date']}  {e['title']:<45}  review: {e['review_date']}")
        return

    p.print_help()


if __name__ == "__main__":
    main()
