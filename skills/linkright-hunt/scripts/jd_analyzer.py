#!/usr/bin/env python3
"""
Extract structured signals from a job description.
Usage: python3 jd_analyzer.py --jd 'JD text here'
       python3 jd_analyzer.py --file jd.txt
Output: JSON {
  "archetype": str,
  "signals": [{"signal": str, "weight": float, "evidence": str}],
  "required_tools": [str],
  "experience_years_min": int|null,
  "stage": str,
  "remote": bool,
  "location": str
}
"""

import argparse
import json
import re
import sys
from pathlib import Path


SIGNAL_PATTERNS = [
    ("growth_experimentation", [
        r"a/b test", r"experiment", r"growth (team|hacking|loop)", r"activation", r"retention",
        r"funnel", r"conversion", r"acquisition channel", r"cac", r"ltv", r"viral",
    ]),
    ("data_fluency", [
        r"\bsql\b", r"data.driven", r"analytics", r"metrics", r"quantitative",
        r"instrumentation", r"dashboard", r"amplitude", r"mixpanel", r"looker", r"tableau",
    ]),
    ("product_vision", [
        r"product vision", r"roadmap (ownership|strategy)", r"product strategy",
        r"north star", r"long.term", r"define (the )?direction",
    ]),
    ("systems_thinking", [
        r"platform", r"ecosystem", r"systems? thinking", r"architecture",
        r"scalab", r"infrastructure", r"technical debt",
    ]),
    ("stakeholder_management", [
        r"stakeholder", r"executive", r"cross.functional", r"c.suite", r"vp.level",
        r"alignment", r"influence without authority",
    ]),
    ("discovery_rigor", [
        r"user research", r"customer (discovery|interview)", r"qualitative",
        r"ux research", r"jobs.to.be.done", r"user (needs|pain)",
    ]),
    ("go_to_market", [
        r"go.to.market", r"gtm", r"launch", r"pricing", r"positioning",
        r"channel", r"market entry",
    ]),
    ("technical_depth", [
        r"technical (background|pm|product manager)", r"api", r"engineer.?s? (background|degree)",
        r"work(ing)? with engineer", r"system design", r"infra",
    ]),
    ("design_collaboration", [
        r"design (collaboration|partner|process)", r"figma", r"ux", r"wireframe",
        r"prototype", r"design system",
    ]),
    ("metric_definition", [
        r"define (metrics|kpi|success)", r"north star metric", r"okr",
        r"success criteria", r"(set|own) the metric",
    ]),
    ("outcome_ownership", [
        r"own(ing)? the (outcome|result|metric|product)", r"p&l", r"accountability",
        r"end.to.end ownership",
    ]),
    ("early_stage_experience", [
        r"(seed|series [ab]|startup|early.stage|0.to.1|zero.to.one)",
        r"founding (pm|product manager)", r"greenfield", r"0→1",
    ]),
    ("enterprise_experience", [
        r"enterprise (customer|sales|contract|deal)", r"b2b (enterprise|software)",
        r"saas (enterprise|platform)", r"procurement", r"compliance",
    ]),
    ("marketplace_experience", [
        r"two.sided", r"marketplace", r"supply( side)?", r"demand( side)?",
        r"gmv", r"take rate", r"liquidity",
    ]),
    ("platform_experience", [
        r"platform (team|pm|product)", r"developer (experience|platform)",
        r"internal (platform|tooling)", r"api (product|platform)",
    ]),
]

ARCHETYPE_SIGNAL_WEIGHTS = {
    "growth": ["growth_experimentation", "data_fluency", "metric_definition"],
    "0to1": ["early_stage_experience", "product_vision", "discovery_rigor"],
    "enterprise": ["enterprise_experience", "stakeholder_management", "go_to_market"],
    "platform": ["platform_experience", "technical_depth", "systems_thinking"],
    "marketplace": ["marketplace_experience", "growth_experimentation", "data_fluency"],
    "design_led": ["design_collaboration", "discovery_rigor", "product_vision"],
}

TOOL_PATTERNS = {
    "sql": r"\bsql\b",
    "python": r"\bpython\b",
    "figma": r"\bfigma\b",
    "amplitude": r"\bamplitude\b",
    "mixpanel": r"\bmixpanel\b",
    "looker": r"\blooker\b",
    "tableau": r"\btableau\b",
    "jira": r"\bjira\b",
    "notion": r"\bnotion\b",
    "salesforce": r"\bsalesforce\b",
    "zendesk": r"\bzendesk\b",
    "segment": r"\bsegment\b",
    "dbt": r"\bdbt\b",
}

STAGE_PATTERNS = {
    "seed": r"\bseed\b",
    "series_a": r"series [a-b]\b",
    "series_b": r"series [b-c]\b",
    "growth": r"(series [c-e]|growth stage|scale.up)",
    "public": r"(public company|listed|nasdaq|nyse|ipo)",
    "enterprise": r"enterprise",
}


def extract_signals(text: str) -> list:
    text_lower = text.lower()
    results = []
    for signal, patterns in SIGNAL_PATTERNS:
        for pat in patterns:
            m = re.search(pat, text_lower)
            if m:
                # Extract surrounding context as evidence
                start = max(0, m.start() - 40)
                end = min(len(text), m.end() + 40)
                evidence = text[start:end].strip().replace('\n', ' ')
                results.append({
                    "signal": signal,
                    "weight": 1.0,
                    "evidence": f"...{evidence}...",
                })
                break
    return results


def detect_archetype(signals: list) -> str:
    signal_names = {s["signal"] for s in signals}
    best = ("unknown", 0)
    for archetype, required in ARCHETYPE_SIGNAL_WEIGHTS.items():
        score = sum(1 for r in required if r in signal_names)
        if score > best[1]:
            best = (archetype, score)
    return best[0]


def extract_tools(text: str) -> list:
    text_lower = text.lower()
    return [tool for tool, pat in TOOL_PATTERNS.items() if re.search(pat, text_lower)]


def extract_experience_years(text: str) -> int | None:
    text_lower = text.lower()
    m = re.search(r'(\d+)\+?\s*years? (of )?(product management|pm|product)', text_lower)
    if m:
        return int(m.group(1))
    m = re.search(r'(\d+)\s*[-–]\s*\d+\s*years?', text_lower)
    if m:
        return int(m.group(1))
    return None


def detect_stage(text: str) -> str:
    text_lower = text.lower()
    for stage, pat in STAGE_PATTERNS.items():
        if re.search(pat, text_lower):
            return stage
    return "unknown"


def detect_remote(text: str) -> bool:
    return bool(re.search(r'(remote|work from home|wfh|distributed team)', text.lower()))


def extract_location(text: str) -> str:
    m = re.search(r'((?:san francisco|new york|london|bangalore|remote)[^\n,]{0,30})', text, re.IGNORECASE)
    return m.group(1).strip() if m else "unknown"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jd", help="JD text")
    parser.add_argument("--file", help="File path to JD text")
    parser.add_argument("--format", choices=["json", "human"], default="json")
    args = parser.parse_args()

    if args.file:
        text = Path(args.file).expanduser().read_text()
    elif args.jd:
        text = args.jd
    else:
        text = sys.stdin.read()

    if not text.strip():
        print(json.dumps({"error": "no JD text provided"}))
        sys.exit(1)

    signals = extract_signals(text)
    archetype = detect_archetype(signals)
    tools = extract_tools(text)
    exp_years = extract_experience_years(text)
    stage = detect_stage(text)
    remote = detect_remote(text)
    location = extract_location(text)

    result = {
        "archetype": archetype,
        "signals": signals,
        "required_tools": tools,
        "experience_years_min": exp_years,
        "stage": stage,
        "remote": remote,
        "location": location,
    }

    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print(f"Archetype: {archetype}")
        print(f"Stage: {stage} | Remote: {remote} | Location: {location}")
        if exp_years:
            print(f"Experience: {exp_years}+ years")
        print(f"\nSignals detected ({len(signals)}):")
        for s in signals:
            print(f"  {s['signal']}")
        if tools:
            print(f"\nTools: {', '.join(tools)}")


if __name__ == "__main__":
    main()
