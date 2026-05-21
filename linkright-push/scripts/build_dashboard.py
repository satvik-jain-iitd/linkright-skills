"""
build_dashboard.py — Generate Kanban dashboard HTML from pipeline.json.
Pure client-side output — no server required.

Usage:
  python3 build_dashboard.py --pipeline ~/path/to/pipeline.json --output dashboard/index.html
"""

import argparse
import json
import re
from datetime import date, datetime
from pathlib import Path

STAGES = ["SAVED", "APPLIED", "SCREENING", "INTERVIEW", "OFFER", "REJECTED"]
STAGE_DISPLAY = {
    "saved": "SAVED", "applied": "APPLIED", "screening": "SCREENING",
    "interview": "INTERVIEW", "offer": "OFFER", "rejected": "REJECTED",
}


def days_in_stage(opp: dict) -> int:
    history = opp.get("stage_history", [])
    if not history:
        return 0
    try:
        latest = sorted(history, key=lambda x: x.get("date", ""))[-1]
        d = datetime.fromisoformat(str(latest.get("date", date.today()))).date()
        return (date.today() - d).days
    except Exception:
        return 0


def age_class(days: int) -> str:
    if days <= 7:
        return "green"
    if days <= 14:
        return "yellow"
    return "red"


def stage_color(stage: str) -> str:
    return {
        "SAVED": "#6b7280", "APPLIED": "#2563eb", "SCREENING": "#d97706",
        "INTERVIEW": "#7c3aed", "OFFER": "#16a34a", "REJECTED": "#dc2626",
    }.get(stage, "#6b7280")


def build_html(pipeline_data: list, pipeline_path: str) -> str:
    by_stage: dict = {s: [] for s in STAGES}
    for opp in pipeline_data:
        raw_stage = str(opp.get("stage", "saved")).lower()
        stage = STAGE_DISPLAY.get(raw_stage, "SAVED")
        if stage in by_stage:
            by_stage[stage].append(opp)

    # Metrics
    total = len(pipeline_data)
    applied = sum(1 for o in pipeline_data if o.get("stage", "").lower() in ("applied", "screening", "interview", "offer"))
    responses = sum(1 for o in pipeline_data if o.get("stage", "").lower() in ("screening", "interview", "offer"))
    interviews = sum(1 for o in pipeline_data if o.get("stage", "").lower() in ("interview", "offer"))
    response_rate = round(responses / applied * 100) if applied > 0 else 0
    interview_rate = round(interviews / responses * 100) if responses > 0 else 0
    avg_fit = 0
    fit_scores = [o.get("fit_score") or o.get("relevance_score") for o in pipeline_data if o.get("fit_score") or o.get("relevance_score")]
    if fit_scores:
        avg_fit = round(sum(float(s) for s in fit_scores) / len(fit_scores) * 100)

    # Kanban columns HTML
    columns_html = ""
    for stage in STAGES:
        cards = by_stage[stage]
        color = stage_color(stage)
        cards_html = ""
        for opp in sorted(cards, key=lambda x: days_in_stage(x), reverse=True):
            d = days_in_stage(opp)
            cls = age_class(d)
            fit = opp.get("fit_score") or opp.get("relevance_score") or 0
            fit_pct = f"{round(float(fit)*100)}%" if fit else "—"
            title = opp.get("title", "Unknown Role")
            company = opp.get("company", "Unknown")
            url = opp.get("job_url") or opp.get("url") or "#"
            cards_html += f"""
            <div class="card age-{cls}">
              <div class="card-company">{company}</div>
              <div class="card-title"><a href="{url}" target="_blank">{title}</a></div>
              <div class="card-meta">
                <span class="age-dot age-{cls}"></span>{d}d &nbsp;·&nbsp; fit: {fit_pct}
              </div>
            </div>"""
        count = len(cards)
        columns_html += f"""
        <div class="col">
          <div class="col-header" style="border-top:3px solid {color}">
            <span class="col-label">{stage}</span>
            <span class="col-count">{count}</span>
          </div>
          <div class="col-cards">{cards_html if cards_html else '<p class="empty-col">—</p>'}</div>
        </div>"""

    today = date.today().isoformat()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Career Dashboard</title>
  <style>
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
         background:#f1f5f9;color:#1e293b;min-height:100vh}}
    .header{{background:#1e293b;color:#fff;padding:16px 32px;display:flex;
             align-items:center;justify-content:space-between}}
    .header h1{{font-size:1.1rem;font-weight:600;letter-spacing:.02em}}
    .header .updated{{font-size:.75rem;color:#94a3b8}}
    .metrics{{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));
              gap:12px;padding:24px 32px;background:#fff;border-bottom:1px solid #e2e8f0}}
    .metric{{background:#f8fafc;border-radius:8px;padding:14px 16px;
             border:1px solid #e2e8f0}}
    .metric .val{{font-size:1.6rem;font-weight:700;color:#1e293b}}
    .metric .lbl{{font-size:.7rem;color:#64748b;margin-top:2px;text-transform:uppercase;
                  letter-spacing:.05em}}
    .board{{display:flex;gap:12px;padding:20px 24px;overflow-x:auto;min-height:60vh}}
    .col{{min-width:200px;flex:1;background:transparent}}
    .col-header{{background:#fff;border-radius:6px 6px 0 0;padding:10px 12px;
                 display:flex;justify-content:space-between;align-items:center;
                 border:1px solid #e2e8f0;border-bottom:none}}
    .col-label{{font-size:.7rem;font-weight:700;letter-spacing:.08em;color:#475569}}
    .col-count{{font-size:.75rem;background:#f1f5f9;border-radius:10px;
                padding:2px 8px;color:#64748b}}
    .col-cards{{background:#f8fafc;border:1px solid #e2e8f0;border-radius:0 0 6px 6px;
                padding:8px;min-height:200px;display:flex;flex-direction:column;gap:8px}}
    .card{{background:#fff;border-radius:6px;padding:10px 12px;
           border:1px solid #e2e8f0;cursor:default}}
    .card.age-yellow{{border-left:3px solid #f59e0b}}
    .card.age-red{{border-left:3px solid #ef4444}}
    .card-company{{font-size:.65rem;color:#94a3b8;text-transform:uppercase;
                   letter-spacing:.05em;margin-bottom:2px}}
    .card-title a{{font-size:.8rem;font-weight:600;color:#1e293b;text-decoration:none;
                   line-height:1.3}}
    .card-title a:hover{{color:#2563eb}}
    .card-meta{{font-size:.68rem;color:#94a3b8;margin-top:6px;display:flex;
                align-items:center;gap:4px}}
    .age-dot{{width:7px;height:7px;border-radius:50%;display:inline-block}}
    .age-dot.age-green{{background:#22c55e}}
    .age-dot.age-yellow{{background:#f59e0b}}
    .age-dot.age-red{{background:#ef4444}}
    .empty-col{{color:#cbd5e1;font-size:.75rem;text-align:center;padding:16px 0}}
    .footer{{text-align:center;color:#94a3b8;font-size:.7rem;padding:16px;
             border-top:1px solid #e2e8f0;margin-top:8px}}
  </style>
</head>
<body>
  <div class="header">
    <h1>Career Dashboard</h1>
    <span class="updated">Updated: {today} · {total} opportunities</span>
  </div>

  <div class="metrics">
    <div class="metric"><div class="val">{applied}</div><div class="lbl">Applied</div></div>
    <div class="metric"><div class="val">{response_rate}%</div><div class="lbl">Response rate</div></div>
    <div class="metric"><div class="val">{interview_rate}%</div><div class="lbl">→ Interview rate</div></div>
    <div class="metric"><div class="val">{by_stage["INTERVIEW"].__len__()}</div><div class="lbl">Active interviews</div></div>
    <div class="metric"><div class="val">{avg_fit}%</div><div class="lbl">Avg fit score</div></div>
    <div class="metric"><div class="val">{total}</div><div class="lbl">Total tracked</div></div>
  </div>

  <div class="board">{columns_html}</div>

  <div class="footer">
    Generated by linkright-push · pipeline: {pipeline_path}
    · Color: <span style="color:#22c55e">●</span> &lt;7d
    <span style="color:#f59e0b">●</span> 7–14d
    <span style="color:#ef4444">●</span> &gt;14d in stage
  </div>
</body>
</html>"""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--pipeline", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()

    pipeline_path = Path(args.pipeline).expanduser()
    if not pipeline_path.exists():
        print(f"Error: pipeline not found: {pipeline_path}")
        raise SystemExit(1)

    raw = json.loads(pipeline_path.read_text())
    opps = raw if isinstance(raw, list) else raw.get("opportunities", [])

    html = build_html(opps, str(pipeline_path))

    out = Path(args.output).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print(f"Dashboard written: {out}  ({len(opps)} opportunities)")


if __name__ == "__main__":
    main()
