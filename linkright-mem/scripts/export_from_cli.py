"""export_from_cli.py — derive the skills markdown memory from the CLI canonical store.

Single source of truth is the CLI v2 store at ~/.linkright/profile
(facts.jsonl, signals.jsonl, canonical_profile.json). The skills read markdown at
~/.linkright/memory (facts.md, signals.md). This script regenerates that markdown
from the jsonl, so the two surfaces never diverge. The jsonl is canonical, the
markdown is a derived, human-readable, git-vault-friendly view.

Run it after any CLI memory change (onboard, enrich, diary), or wire it into those
flows. It is deterministic and idempotent.

Usage:
  python3 export_from_cli.py
  python3 export_from_cli.py --profile ~/.linkright/profile --memory ~/.linkright/memory
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return out


def conf_float_to_enum(c) -> str:
    """CLI confidence is a float 0..1. Skills use the contract vocab."""
    try:
        c = float(c)
    except (TypeError, ValueError):
        return "directional"
    if c >= 0.9:
        return "exact"
    if c >= 0.7:
        return "strong"
    if c >= 0.45:
        return "directional"
    return "thin"


def build_role_map(profile_dir: Path) -> dict[str, dict]:
    """role_id -> {label, period} from canonical_profile.json."""
    p = profile_dir / "canonical_profile.json"
    roles: dict[str, dict] = {}
    if not p.exists():
        return roles
    try:
        prof = json.loads(p.read_text())
    except json.JSONDecodeError:
        return roles
    for r in prof.get("roles", []) or []:
        title = (r.get("title") or "").strip()
        company = (r.get("company") or "").strip()
        if title and company:
            label = f"{title} at {company}"
        else:
            label = title or company
        start = (r.get("start_date") or "").strip()
        end = (r.get("end_date") or "").strip() or ("present" if r.get("is_current") else "")
        period = f"{start} to {end}" if start else ""
        roles[r.get("id", "")] = {"label": label, "period": period}
    return roles


def strength_from_signal(sig: dict) -> str:
    """Map to high/medium/low, matching the skills signal_deriver convention."""
    n = len(sig.get("source_fact_ids") or [])
    if n >= 3:
        return "high"
    if n >= 2:
        return "medium"
    return "low"


def _esc(s) -> str:
    return str(s).replace('"', '\\"')


def export_facts(facts: list[dict], roles: dict[str, dict], out_path: Path) -> int:
    blocks = ["# LinkRight Memory, Facts (derived from CLI canonical store, do not edit by hand)\n"]
    n = 0
    for f in facts:
        if f.get("stale"):
            continue
        rid = f.get("role_id") or ""
        role = roles.get(rid, {}).get("label", "")
        period = roles.get(rid, {}).get("period", "")
        ev = f.get("evidence_atom_ids") or []
        ev_yaml = "\n".join(f'  - "{_esc(e)}"' for e in ev) or '  - "cli_canonical"'
        blocks.append(
            "---\n"
            f"id: {f.get('id', '')}\n"
            f'text: "{_esc(f.get("text", ""))}"\n'
            f'role: "{_esc(role)}"\n'
            f'period: "{_esc(period)}"\n'
            "evidence_refs:\n"
            f"{ev_yaml}\n"
            f"confidence: {conf_float_to_enum(f.get('confidence', 0))}\n"
            "signals_derived: []\n"
            "---"
        )
        n += 1
    out_path.write_text("\n\n".join(blocks) + "\n")
    return n


def export_signals(signals: list[dict], out_path: Path) -> int:
    blocks = ["# LinkRight Memory, Signals (derived from CLI canonical store, do not edit by hand)\n"]
    n = 0
    for s in signals:
        if s.get("stale"):
            continue
        name = s.get("canonical_name", "")
        label = name.replace("_", " ").title()
        sf = s.get("source_fact_ids") or []
        if sf:
            sf_block = "supporting_facts:\n" + "\n".join(f"  - {x}" for x in sf)
        else:
            sf_block = "supporting_facts: []"
        blocks.append(
            "---\n"
            f"id: {s.get('id', '')}\n"
            f'name: "{_esc(name)}"\n'
            f'label: "{_esc(label)}"\n'
            f'description: "{_esc(s.get("definition", ""))}"\n'
            f"{sf_block}\n"
            f"strength: {strength_from_signal(s)}\n"
            "confidence: confirmed\n"
            "---"
        )
        n += 1
    out_path.write_text("\n\n".join(blocks) + "\n")
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", default=str(Path.home() / ".linkright" / "profile"))
    ap.add_argument("--memory", default=str(Path.home() / ".linkright" / "memory"))
    args = ap.parse_args()

    profile_dir = Path(args.profile)
    memory_dir = Path(args.memory)
    memory_dir.mkdir(parents=True, exist_ok=True)

    # Safety: never clobber the derived markdown when there is no canonical
    # source. A skill-only setup (no CLI store) keeps its own markdown.
    if not (profile_dir / "facts.jsonl").exists() and not (profile_dir / "signals.jsonl").exists():
        print(f"No CLI canonical store at {profile_dir}, leaving {memory_dir} untouched.")
        return

    facts = load_jsonl(profile_dir / "facts.jsonl")
    signals = load_jsonl(profile_dir / "signals.jsonl")
    roles = build_role_map(profile_dir)

    nf = export_facts(facts, roles, memory_dir / "facts.md")
    ns = export_signals(signals, memory_dir / "signals.md")
    print(f"Exported {nf} facts, {ns} signals from {profile_dir} to {memory_dir}")


if __name__ == "__main__":
    main()
