#!/usr/bin/env python3
"""
CRUD operations on pipeline.json.
Usage:
  python3 pipeline_update.py --list
  python3 pipeline_update.py --add --company Stripe --role "PM, Payments" --stage applied --url https://...
  python3 pipeline_update.py --update --id <id> --stage phone_screen
  python3 pipeline_update.py --close --id <id> --outcome rejected
  python3 pipeline_update.py --get --id <id>
  python3 pipeline_update.py --stats
"""

import argparse
import json
import sys
import uuid
from datetime import datetime
from pathlib import Path

PIPELINE_PATH = Path("~/.linkright/jobs/memory/pipeline.json").expanduser()

VALID_STAGES = [
    "applied", "phone_screen", "interview_r1", "interview_r2",
    "interview_final", "offer_received", "rejected", "ghosted", "withdrawn",
]


def load_pipeline() -> list:
    if not PIPELINE_PATH.exists():
        return []
    try:
        data = json.loads(PIPELINE_PATH.read_text())
        return data if isinstance(data, list) else data.get("opportunities", [])
    except (json.JSONDecodeError, KeyError):
        return []


def save_pipeline(opps: list) -> None:
    PIPELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
    PIPELINE_PATH.write_text(json.dumps(opps, indent=2))


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def add_opportunity(company: str, role: str, stage: str, url: str = "", jd_signals: list = None) -> dict:
    opps = load_pipeline()
    opp = {
        "id": str(uuid.uuid4())[:8],
        "company": company,
        "role": role,
        "stage": stage,
        "url": url,
        "jd_signals": jd_signals or [],
        "added_date": now_iso(),
        "updated_date": now_iso(),
        "notes": [],
    }
    opps.append(opp)
    save_pipeline(opps)
    return opp


def update_opportunity(opp_id: str, **updates) -> dict | None:
    opps = load_pipeline()
    for opp in opps:
        if opp.get("id") == opp_id or opp.get("id", "").startswith(opp_id):
            for key, value in updates.items():
                if value is not None:
                    opp[key] = value
            opp["updated_date"] = now_iso()
            save_pipeline(opps)
            return opp
    return None


def close_opportunity(opp_id: str, outcome: str) -> dict | None:
    return update_opportunity(opp_id, stage=outcome, closed_date=now_iso())


def get_opportunity(opp_id: str) -> dict | None:
    opps = load_pipeline()
    for opp in opps:
        if opp.get("id") == opp_id or opp.get("id", "").startswith(opp_id):
            return opp
    return None


def list_opportunities(stage_filter: str = None) -> list:
    opps = load_pipeline()
    if stage_filter:
        opps = [o for o in opps if o.get("stage") == stage_filter]
    return opps


def pipeline_stats() -> dict:
    opps = load_pipeline()
    stage_counts = {}
    for opp in opps:
        stage = opp.get("stage", "unknown")
        stage_counts[stage] = stage_counts.get(stage, 0) + 1

    active_stages = {"applied", "phone_screen", "interview_r1", "interview_r2", "interview_final"}
    active = sum(v for k, v in stage_counts.items() if k in active_stages)

    return {
        "total": len(opps),
        "active": active,
        "by_stage": stage_counts,
        "in_interview": sum(
            stage_counts.get(s, 0)
            for s in ["interview_r1", "interview_r2", "interview_final"]
        ),
    }


def main():
    global PIPELINE_PATH
    parser = argparse.ArgumentParser()
    parser.add_argument("--pipeline", default=str(PIPELINE_PATH))
    subparsers = parser.add_subparsers(dest="cmd")

    # --list
    list_p = subparsers.add_parser("list", help="List opportunities")
    list_p.add_argument("--stage", help="Filter by stage")
    list_p.add_argument("--format", choices=["json", "human"], default="human")

    # --add
    add_p = subparsers.add_parser("add", help="Add opportunity")
    add_p.add_argument("--company", required=True)
    add_p.add_argument("--role", required=True)
    add_p.add_argument("--stage", default="applied", choices=VALID_STAGES)
    add_p.add_argument("--url", default="")
    add_p.add_argument("--jd-signals", default="[]")

    # --update
    upd_p = subparsers.add_parser("update", help="Update opportunity")
    upd_p.add_argument("--id", required=True)
    upd_p.add_argument("--stage", choices=VALID_STAGES)
    upd_p.add_argument("--note", help="Add a note")
    upd_p.add_argument("--fit-score", type=int)

    # --close
    close_p = subparsers.add_parser("close", help="Close opportunity")
    close_p.add_argument("--id", required=True)
    close_p.add_argument("--outcome", required=True,
                         choices=["rejected", "ghosted", "withdrawn", "offer_received"])

    # --get
    get_p = subparsers.add_parser("get", help="Get one opportunity")
    get_p.add_argument("--id", required=True)

    # --stats
    subparsers.add_parser("stats", help="Pipeline statistics")

    args = parser.parse_args()

    # Override pipeline path if provided
    if args.pipeline != str(PIPELINE_PATH):
        PIPELINE_PATH = Path(args.pipeline).expanduser()

    if args.cmd == "list" or args.cmd is None:
        fmt = getattr(args, "format", "human")
        stage = getattr(args, "stage", None)
        opps = list_opportunities(stage)
        if fmt == "json":
            print(json.dumps(opps, indent=2))
        else:
            if not opps:
                print("Pipeline empty.")
            for o in opps:
                print(f"[{o.get('id','?')}] {o.get('stage','?'):20} {o.get('company','?')} — {o.get('role','?')}")

    elif args.cmd == "add":
        try:
            jd_signals = json.loads(args.jd_signals)
        except json.JSONDecodeError:
            jd_signals = []
        opp = add_opportunity(args.company, args.role, args.stage, args.url, jd_signals)
        print(json.dumps(opp, indent=2))

    elif args.cmd == "update":
        updates = {}
        if args.stage:
            updates["stage"] = args.stage
        if args.fit_score is not None:
            updates["fit_score"] = args.fit_score
        if args.note:
            opp = get_opportunity(args.id)
            if opp:
                notes = opp.get("notes", [])
                notes.append({"date": now_iso(), "note": args.note})
                updates["notes"] = notes
        result = update_opportunity(args.id, **updates)
        if result:
            print(json.dumps(result, indent=2))
        else:
            print(json.dumps({"error": f"opportunity {args.id} not found"}))
            sys.exit(1)

    elif args.cmd == "close":
        result = close_opportunity(args.id, args.outcome)
        if result:
            print(json.dumps(result, indent=2))
        else:
            print(json.dumps({"error": f"opportunity {args.id} not found"}))
            sys.exit(1)

    elif args.cmd == "get":
        result = get_opportunity(args.id)
        if result:
            print(json.dumps(result, indent=2))
        else:
            print(json.dumps({"error": f"opportunity {args.id} not found"}))
            sys.exit(1)

    elif args.cmd == "stats":
        stats = pipeline_stats()
        print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
