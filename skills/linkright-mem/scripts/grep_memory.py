"""
grep_memory.py — Multi-query grep across facts.md + signals.md.
Returns ranked results for skills querying profile memory.

Usage:
  python3 grep_memory.py --query "stakeholder alignment" --memory ~/.linkright/memory --top 10
  python3 grep_memory.py --signal "systems_thinking" --memory ~/.linkright/memory --format json
  python3 grep_memory.py --archetype "growth" --memory ~/.linkright/memory --format json
  python3 grep_memory.py --query "strength:high" --memory ~/.linkright/memory
"""

import argparse
import json
import re
from pathlib import Path


# Names aligned with ref_02_signal_taxonomy.md, ref_03_archetype_requirements.md
ARCHETYPE_SIGNALS = {
    "growth":      ["growth_experimentation", "data_fluency", "metric_definition",
                    "product_vision", "user_empathy", "systems_thinking"],
    "0to1":        ["early_stage_experience", "product_vision", "discovery_rigor",
                    "ambiguity_tolerance", "systems_thinking", "stakeholder_management"],
    "platform":    ["platform_experience", "technical_depth", "systems_thinking",
                    "stakeholder_management", "data_fluency", "outcome_ownership"],
    "enterprise":  ["enterprise_experience", "stakeholder_management", "go_to_market",
                    "outcome_ownership", "data_fluency", "systems_thinking"],
    "consumer":    ["user_empathy", "growth_experimentation", "discovery_rigor",
                    "data_fluency", "product_vision", "design_collaboration"],
    "data_ai":     ["data_fluency", "technical_depth", "systems_thinking",
                    "metric_definition", "product_vision", "outcome_ownership"],
    "design_led":  ["design_collaboration", "discovery_rigor", "product_vision",
                    "user_empathy", "systems_thinking", "outcome_ownership"],
    "marketplace": ["marketplace_experience", "growth_experimentation", "data_fluency",
                    "systems_thinking", "outcome_ownership", "metric_definition"],
}


def parse_facts_md(path: Path) -> list[dict]:
    if not path.exists():
        return []
    text = path.read_text()
    blocks = re.findall(r"---\n(.*?)\n---", text, re.DOTALL)
    facts = []
    for block in blocks:
        fact = {}
        for line in block.strip().split("\n"):
            if ":" in line and not line.startswith("  "):
                k, _, v = line.partition(":")
                fact[k.strip()] = v.strip().strip('"')
        if "id" in fact and "text" in fact:
            facts.append(fact)
    return facts


def parse_signals_md(path: Path) -> list[dict]:
    if not path.exists():
        return []
    text = path.read_text()
    blocks = re.findall(r"---\n(.*?)\n---", text, re.DOTALL)
    sigs = []
    for block in blocks:
        sig = {}
        lines = block.strip().split("\n")
        i = 0
        while i < len(lines):
            line = lines[i]
            if ":" in line and not line.startswith("  "):
                k, _, v = line.partition(":")
                k, v = k.strip(), v.strip().strip('"')
                if i + 1 < len(lines) and lines[i + 1].startswith("  - "):
                    items = []
                    i += 1
                    while i < len(lines) and lines[i].startswith("  - "):
                        items.append(lines[i][4:].strip())
                        i += 1
                    sig[k] = items
                    continue
                sig[k] = v
            i += 1
        if "name" in sig:
            sigs.append(sig)
    return sigs


# ---------------------------------------------------------------------------
# Optional semantic layer. Uses fastembed, the same library as the CLI. If it
# is not installed, retrieval silently falls back to keyword only. No cloud,
# no API cost, runs locally on CPU.
# ---------------------------------------------------------------------------
_EMBEDDER = None
_EMBED_TRIED = False


def get_embedder():
    global _EMBEDDER, _EMBED_TRIED
    if _EMBED_TRIED:
        return _EMBEDDER
    _EMBED_TRIED = True
    try:
        from fastembed import TextEmbedding
        _EMBEDDER = TextEmbedding()  # default small local model
    except Exception:
        _EMBEDDER = None
    return _EMBEDDER


def _cosine(a, b) -> float:
    try:
        import numpy as np
        a = np.asarray(a, dtype="float32")
        b = np.asarray(b, dtype="float32")
        na, nb = float(np.linalg.norm(a)), float(np.linalg.norm(b))
        return float(np.dot(a, b) / (na * nb)) if na and nb else 0.0
    except Exception:
        dot = sum(x * y for x, y in zip(a, b))
        na = sum(x * x for x in a) ** 0.5
        nb = sum(y * y for y in b) ** 0.5
        return dot / (na * nb) if na and nb else 0.0


def score_relevance(text: str, query_terms: list[str]) -> int:
    text_lower = text.lower()
    return sum(1 for t in query_terms if t.lower() in text_lower)


def _embed_texts(texts: list[str]):
    """Return a list of embedding vectors, or None if embedding is unavailable."""
    emb = get_embedder()
    if emb is None or not texts:
        return None
    try:
        return list(emb.embed(texts))
    except Exception:
        return None


def search(query: str, facts: list[dict], signals: list[dict], top: int = 10) -> dict:
    # Contract: never surface a fact the user told us not to use.
    facts = [f for f in facts if f.get("credibility", "").strip().lower() != "do_not_use"]

    # Handle special queries (pure filter, no ranking needed)
    if query.startswith("strength:"):
        strength_filter = query.split(":")[1].strip()
        matched_signals = [s for s in signals if s.get("strength") == strength_filter]
        return {"facts": [], "signals": matched_signals[:top], "mode": "filter"}

    terms = query.lower().split()

    fact_texts = [f.get("text", "") + " " + f.get("role", "") for f in facts]
    sig_texts = [s.get("name", "") + " " + s.get("description", "") + " " + s.get("label", "")
                 for s in signals]

    # Keyword score, normalized 0..1 by the number of query terms so it blends
    # cleanly with cosine similarity.
    n_terms = max(len(terms), 1)
    kw_facts = [score_relevance(t, terms) / n_terms for t in fact_texts]
    kw_sigs = [score_relevance(t, terms) / n_terms for t in sig_texts]

    # Optional semantic layer. Same fastembed model as the CLI, local CPU, no cost.
    mode = "keyword"
    sem_facts = [0.0] * len(facts)
    sem_sigs = [0.0] * len(signals)
    q_emb = _embed_texts([query])
    if q_emb is not None:
        qv = q_emb[0]
        f_embs = _embed_texts(fact_texts) if fact_texts else []
        s_embs = _embed_texts(sig_texts) if sig_texts else []
        if f_embs is not None and s_embs is not None:
            sem_facts = [_cosine(qv, e) for e in f_embs]
            sem_sigs = [_cosine(qv, e) for e in s_embs]
            mode = "hybrid"

    # Blend. In hybrid mode weight keyword and semantic evenly; in keyword mode
    # the semantic term is zero so this reduces to pure keyword ranking.
    w_sem = 0.5 if mode == "hybrid" else 0.0
    w_kw = 1.0 - w_sem if mode == "hybrid" else 1.0

    scored_facts = []
    for i, f in enumerate(facts):
        blended = w_kw * kw_facts[i] + w_sem * sem_facts[i]
        if blended > 0:
            scored_facts.append((blended, f))
    scored_facts.sort(key=lambda x: -x[0])

    scored_signals = []
    for i, s in enumerate(signals):
        blended = w_kw * kw_sigs[i] + w_sem * sem_sigs[i]
        if blended > 0:
            scored_signals.append((blended, s))
    scored_signals.sort(key=lambda x: -x[0])

    return {
        "facts":   [f for _, f in scored_facts[:top]],
        "signals": [s for _, s in scored_signals[:top]],
        "mode":    mode,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--query", default=None)
    p.add_argument("--signal", default=None, help="Get facts for a specific signal")
    p.add_argument("--archetype", default=None, help="Get all signals for an archetype")
    p.add_argument("--memory", required=True)
    p.add_argument("--top", type=int, default=10)
    p.add_argument("--format", default="text", choices=["text", "json"])
    args = p.parse_args()

    memory = Path(args.memory)
    facts   = parse_facts_md(memory / "facts.md")
    signals = parse_signals_md(memory / "signals.md")
    signal_map = {s["name"]: s for s in signals}

    if args.archetype:
        required = ARCHETYPE_SIGNALS.get(args.archetype, [])
        result_signals = [signal_map[s] for s in required if s in signal_map]
        missing = [s for s in required if s not in signal_map]
        result = {"archetype": args.archetype, "signals": result_signals, "missing": missing}
        if args.format == "json":
            print(json.dumps(result, indent=2))
        else:
            print(f"\nSignals for archetype: {args.archetype}")
            for s in result_signals:
                print(f"  {s.get('strength','?'):6}  {s['name']}")
            if missing:
                print(f"\nMissing: {', '.join(missing)}")
        return

    if args.signal:
        sig = signal_map.get(args.signal)
        if not sig:
            print(json.dumps({"error": f"Signal '{args.signal}' not found"}))
            return
        fact_ids = sig.get("supporting_facts", [])
        supporting = [f for f in facts if f.get("id") in fact_ids]
        result = {"signal": sig, "supporting_facts": supporting}
        if args.format == "json":
            print(json.dumps(result, indent=2))
        else:
            print(f"\nSignal: {args.signal}  strength={sig.get('strength','?')}")
            for f in supporting:
                print(f"  {f['id']}: {f['text']}")
        return

    if args.query:
        result = search(args.query, facts, signals, args.top)
        if args.format == "json":
            print(json.dumps(result, indent=2))
        else:
            print(f"\nFACTS matching '{args.query}'  (retrieval: {result.get('mode','keyword')}):")
            for f in result["facts"]:
                print(f"  {f['id']}: {f['text']}  ({f.get('role','')})")
            print(f"\nSIGNALS matching '{args.query}':")
            for s in result["signals"]:
                print(f"  {s['name']}  strength={s.get('strength','?')}")
        return

    # Default: show summary
    print(f"\nMEMORY SUMMARY")
    print(f"  Facts  : {len(facts)}")
    print(f"  Signals: {len(signals)}")
    by_strength = {}
    for s in signals:
        k = s.get("strength", "unknown")
        by_strength[k] = by_strength.get(k, 0) + 1
    for k, v in sorted(by_strength.items()):
        print(f"    {k}: {v}")


if __name__ == "__main__":
    main()
