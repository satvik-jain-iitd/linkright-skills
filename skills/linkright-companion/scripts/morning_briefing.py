"""
morning_briefing.py — Generate LinkRight daily brief from pipeline + setup.

Usage:
  python3 morning_briefing.py --pipeline ~/path/pipeline.json --setup ~/.linkright/user_setup.md
"""

import argparse
import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path


def load_pipeline(path: Path) -> list:
    if not path.exists():
        return []
    raw = json.loads(path.read_text())
    return raw if isinstance(raw, list) else raw.get("opportunities", [])


def load_setup(path: Path) -> dict:
    if not path.exists():
        return {}
    text = path.read_text()
    setup = {}
    for key in ("target_ctc_min", "target_ctc_target", "target_date", "target_archetype"):
        m = re.search(rf"{key}\s*:\s*(.+)", text, re.IGNORECASE)
        if m:
            setup[key] = m.group(1).strip()
    return setup


def days_since(stage_history: list) -> int:
    if not stage_history:
        return 0
    try:
        latest = sorted(stage_history, key=lambda x: x.get("date", ""))[-1]
        d = datetime.fromisoformat(str(latest.get("date", date.today()))).date()
        return (date.today() - d).days
    except Exception:
        return 0


def classify_opps(opps: list) -> dict:
    result = {"awaiting": [], "in_progress": [], "overdue": [], "saved": [], "offer": [], "rejected": []}
    for o in opps:
        stage = str(o.get("stage", "saved")).lower()
        days = days_since(o.get("stage_history", []))
        company = o.get("company", "?")
        title = o.get("title", "?")
        entry = {"company": company, "title": title, "days": days, "opp": o}

        if stage in ("offer",):
            result["offer"].append(entry)
        elif stage in ("rejected",):
            result["rejected"].append(entry)
        elif stage in ("saved",):
            result["saved"].append(entry)
        elif stage in ("applied",):
            if days > 14:
                result["overdue"].append(entry)
            else:
                result["awaiting"].append(entry)
        elif stage in ("screening", "interview"):
            result["in_progress"].append(entry)
        else:
            result["awaiting"].append(entry)
    return result


def build_actions(classified: dict, setup: dict) -> list[str]:
    actions = []

    # 1. Interview prep — highest priority
    for e in classified["in_progress"]:
        stage = str(e["opp"].get("stage", "")).lower()
        if stage == "interview":
            actions.append(f"Prep for {e['company']} interview — research JD, run /linkright-interview")

    # 2. Overdue follow-ups
    for e in sorted(classified["overdue"], key=lambda x: -x["days"])[:2]:
        actions.append(f"Follow up with {e['company']} — {e['days']}d since application, no response")

    # 3. Screening in progress
    for e in classified["in_progress"]:
        stage = str(e["opp"].get("stage", "")).lower()
        if stage == "screening" and e["days"] > 7:
            actions.append(f"Prepare for {e['company']} next round — {e['days']}d at screening stage")

    # 4. Danger zone: low pipeline
    total_active = len(classified["awaiting"]) + len(classified["in_progress"])
    if total_active < 5:
        actions.append(f"Run /linkright-hunt — only {total_active} active opps (target: ≥5)")

    # 5. Offers
    for e in classified["offer"]:
        actions.append(f"Evaluate offer from {e['company']} — run /linkright-companion → E) Offer evaluation")

    return actions[:3]


def goal_status(setup: dict, classified: dict) -> str:
    target_date = setup.get("target_date", "")
    if not target_date:
        return ""
    try:
        td = datetime.strptime(target_date, "%Y-%m-%d").date()
        days_left = (td - date.today()).days
        days_elapsed = (date.today() - (td - timedelta(days=90))).days  # assume 90-day search
        interview_count = len(classified["in_progress"])
        offer_count = len(classified["offer"])

        if offer_count > 0:
            status = "offer received"
        elif interview_count >= 3:
            status = "on track"
        elif days_left < 30 and interview_count < 2:
            status = "BEHIND — accelerate applications"
        else:
            status = "borderline"

        return f"Goal deadline: {target_date} ({days_left}d away)  Status: {status}"
    except Exception:
        return f"Target: {target_date}"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--pipeline", required=True)
    p.add_argument("--setup", default="~/.linkright/user_setup.md")
    p.add_argument("--decisions", default=None)
    p.add_argument("--format", default="text", choices=["text", "json"])
    args = p.parse_args()

    opps = load_pipeline(Path(args.pipeline).expanduser())
    setup = load_setup(Path(args.setup).expanduser())
    classified = classify_opps(opps)
    actions = build_actions(classified, setup)
    goal = goal_status(setup, classified)

    total_active = len(classified["awaiting"]) + len(classified["in_progress"])

    if args.format == "json":
        print(json.dumps({
            "date": date.today().isoformat(),
            "pipeline": {k: len(v) for k, v in classified.items()},
            "actions": actions,
            "goal": goal,
        }, indent=2))
        return

    print(f"\n{'━'*56}")
    print(f"  LINKRIGHT DAILY BRIEF — {date.today().strftime('%A, %d %b %Y')}")
    print(f"{'━'*56}")

    print(f"\nPIPELINE")
    if total_active < 5:
        print(f"  ⚠  Only {total_active} active opportunities — below minimum of 5")
    print(f"  Applied (awaiting):  {len(classified['awaiting'])}",
          f"— {', '.join(e['company'] for e in classified['awaiting'][:4])}" if classified['awaiting'] else "")
    print(f"  In progress:         {len(classified['in_progress'])}",
          f"— {', '.join(e['company'] + ' (' + e['opp'].get('stage','?') + ')' for e in classified['in_progress'])}" if classified['in_progress'] else "")
    if classified["overdue"]:
        names = ", ".join(f"{e['company']} ({e['days']}d)" for e in classified["overdue"])
        print(f"  Overdue follow-up:   {len(classified['overdue'])} ← URGENT — {names}")
    if classified["offer"]:
        print(f"  Offers:              {len(classified['offer'])} — {', '.join(e['company'] for e in classified['offer'])}")

    print(f"\nTOP 3 ACTIONS TODAY")
    if actions:
        for i, a in enumerate(actions, 1):
            print(f"  {i}. {a}")
    else:
        print("  No urgent actions. Apply to new opportunities or work on content.")

    if goal:
        print(f"\n{goal}")

    print(f"\n{'━'*56}\n")


if __name__ == "__main__":
    main()
