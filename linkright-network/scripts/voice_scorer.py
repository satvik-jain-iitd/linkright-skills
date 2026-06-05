"""
voice_scorer.py — Score a LinkedIn post on the LinkRight voice rubric (0-10).

Usage:
  python3 voice_scorer.py '<post_text>'
  echo '<post_text>' | python3 voice_scorer.py --stdin
  python3 voice_scorer.py '<post_text>' --format json
"""

import argparse
import json
import os
import re
import sys

FORBIDDEN_OPENINGS = [
    "excited to share", "humbled to announce", "i am proud to", "i'm proud to",
    "proud to announce", "proud to share", "thrilled to", "delighted to",
    "hot take:", "unpopular opinion:", "lessons from", "what i learned from",
    "x things", "n things", "y things", "things i've learned",
    "ai is changing everything", "the future of", "as a pm,", "as a product manager,",
]

FORBIDDEN_CLOSINGS = [
    "agree?", "what do you think?", "drop your thoughts", "let me know your thoughts",
    "share your experience", "share below", "comment below", "thoughts?",
    "curious to hear", "love to hear your", "what's your take?",
]

HEDGE_PATTERNS = [
    r"\bmight\s+(?:be|want|consider)\b",
    r"\bperhaps\b",
    r"\bsome\s+(?:might|would|could)\b",
    r"\bit\s+(?:seems?|appears?)\b",
    r"\bi\s+(?:think|feel|believe|wonder)\b.*\?",
    r"\bkind\s+of\b",
    r"\bsort\s+of\b",
    r"\bmaybe\b.*\bmaybe\b",
]

SPECIFIC_ANCHORS = [
    r"\b[A-Z][a-z]+(?:'s)?\s+(?:onboarding|dashboard|feature|product|API|app|platform|model|pricing|UX|UI|flow|experience)\b",
    r"\b(?:Google|Apple|Meta|Microsoft|Anthropic|OpenAI|Notion|Figma|Slack|Linear|Stripe|Shopify|Airbnb|Uber|Netflix|Spotify|Duolingo|Superhuman|Vercel|Cloudflare|Cursor|GitHub|Atlassian|Salesforce|HubSpot|Intercom)\b",
    r"\bspecifically\b|\bin particular\b",
    r"\b(?:v\d|version\s+\d|\d{4}\s+(?:launch|update|release))\b",
    r"\$\d+|\d+\s*(?:million|billion|percent|%|users|customers|ARR|MRR)\b",
]


def score_criterion_1(text: str) -> tuple[int, str]:
    """Opens with opinion (not question, fact, announcement)."""
    first_sentence = re.split(r"[.!?]", text.strip())[0].lower().strip()

    # Question opener = 0
    if first_sentence.endswith("?") or first_sentence.startswith(("what ", "why ", "how ", "when ", "have you", "do you")):
        return 0, "Opens with question — state the opinion first"

    # Forbidden opening = 0
    for phrase in FORBIDDEN_OPENINGS:
        if first_sentence.startswith(phrase) or phrase in first_sentence[:60]:
            return 0, f"Forbidden opening: '{phrase}'"

    # Weak opinion markers (hedged first sentence)
    for pat in HEDGE_PATTERNS[:3]:
        if re.search(pat, first_sentence):
            return 1, "First sentence hedged — stronger stance possible"

    # Strong: starts with declarative claim
    if len(first_sentence) > 20 and not first_sentence.endswith("?"):
        return 2, "Strong opinion-first opener"

    return 1, "Opener OK but could be stronger"


def score_criterion_2(text: str) -> tuple[int, str]:
    """References something specific (real company/product/decision)."""
    for pat in SPECIFIC_ANCHORS:
        if re.search(pat, text):
            return 2, "Specific real-world anchor found"

    # Check for generic signals
    generic = [r"\bmany companies\b", r"\bmost products\b", r"\bsome teams\b",
               r"\bSaaS companies\b", r"\btech companies\b", r"\benterprises?\b"]
    for pat in generic:
        if re.search(pat, text, re.IGNORECASE):
            return 1, "Generic industry reference — name the specific company"

    return 0, "No specific company, product, or decision named"


def score_criterion_3(text: str) -> tuple[int, str]:
    """Avoids all forbidden phrases."""
    text_lower = text.lower()

    # Check forbidden openings
    first_50 = text_lower[:50]
    for phrase in FORBIDDEN_OPENINGS:
        if phrase in first_50:
            return 0, f"Forbidden opening phrase: '{phrase}'"

    # Check forbidden closings
    last_100 = text_lower[-100:]
    for phrase in FORBIDDEN_CLOSINGS:
        if phrase in last_100:
            return 0, f"Forbidden closing phrase: '{phrase}'"

    # Check generic trends
    trend_phrases = ["ai is changing", "the future of", "game changer", "paradigm shift",
                     "thought leadership", "move the needle", "synergy", "impactful"]
    found = [p for p in trend_phrases if p in text_lower]
    if found:
        return 1, f"Near-forbidden generic phrase: {found[0]!r}"

    return 2, "Clean — no forbidden phrases"


def score_criterion_4(text: str) -> tuple[int, str]:
    """Clear position — doesn't hedge everything."""
    text_lower = text.lower()
    hedge_count = sum(1 for pat in HEDGE_PATTERNS if re.search(pat, text_lower))

    if hedge_count >= 3:
        return 0, f"{hedge_count} hedge phrases — take a clearer stance"
    if hedge_count == 1:
        return 1, "One hedge phrase — mostly clear"
    if hedge_count == 0:
        return 2, "Clear, unhedged position"
    return 1, f"{hedge_count} hedge phrases — slightly unclear"


def score_criterion_5(text: str) -> tuple[int, str]:
    """Unique voice — couldn't be swapped into anyone else's feed."""
    text_lower = text.lower()

    # Generic listicle patterns = 0
    listicle = [r"^\d+\s+(?:ways|things|tips|lessons|reasons)", r"here\s+(?:are|is)\s+\d+"]
    for pat in listicle:
        if re.search(pat, text_lower):
            return 0, "Listicle format — generic, interchangeable"

    # Generic insight patterns = 1
    generic_insights = ["the best pms", "great pms", "good product managers", "as a pm you"]
    for phrase in generic_insights:
        if phrase in text_lower:
            return 1, f"Generic PM-advice pattern: '{phrase}' — make it your specific experience"

    # Specificity signals = 2
    personal_markers = [r"\bi\b.{5,50}\b(?:noticed|realized|learned|saw|built|shipped|decided)\b",
                        r"\bin my\s+(?:experience|last|current|previous)\b",
                        r"\bwe\s+(?:shipped|built|launched|decided|realized)\b"]
    for pat in personal_markers:
        if re.search(pat, text_lower):
            return 2, "Personal, specific voice — distinctive"

    return 1, "Readable but not distinctly personal — ground it in your specific experience"


# ---------------------------------------------------------------------------
# Grounded voice signals. Measured, hard-to-fake checks. Optional config from
# the user's voice profile makes the banned-word and signature checks personal.
# Backward compatible: with no config, those two checks are skipped.
# ---------------------------------------------------------------------------

_SENT_SPLIT = re.compile(r"[.!?‼]+")

_CONTRAST_PATTERNS = [
    r"\bnot\b[^.?!]{1,40}\bbut\b",
    r"\brather than\b",
    r"\binstead of\b",
    r"\b\w+\s+not\s+\w+\b",
]


def load_voice_config(path=None) -> dict:
    """Optional grounded-voice config. Returns {} if none found.

    Shape: {"signature": "‼️", "banned_words": {"leverage": "edge", "ensure": "made sure"}}
    """
    candidates = [path, os.path.expanduser("~/.linkright/voice_profile.json")]
    for p in candidates:
        if p and os.path.exists(p):
            try:
                with open(p, encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
    return {}


def _sentence_lengths(text: str):
    sents = [s.strip() for s in _SENT_SPLIT.split(text) if s.strip()]
    return [len(s.split()) for s in sents]


def check_burstiness(text: str):
    lens = _sentence_lengths(text)
    if len(lens) < 3:
        return 1, "Too few sentences to judge rhythm"
    mean = sum(lens) / len(lens)
    std = (sum((l - mean) ** 2 for l in lens) / len(lens)) ** 0.5
    cv = std / mean if mean else 0
    spread = max(lens) - min(lens)
    if cv >= 0.5 and spread >= 8:
        return 2, f"Bursty rhythm, reads human (cv {cv:.2f}, spread {spread} words)"
    if cv >= 0.3:
        return 1, f"Some variation (cv {cv:.2f}) — push shorter and longer lines"
    return 0, f"Flat, uniform sentences read machine made (cv {cv:.2f})"


def check_contrast(text: str):
    for pat in _CONTRAST_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            return 2, "Has a contrast pair, X not Y"
    return 0, "No contrast pair — add one, X not Y"


def check_banned_words(text: str, config: dict):
    banned = config.get("banned_words", {}) if config else {}
    if not banned:
        return None, "No banned-word list configured — skipped"
    tl = text.lower()
    hits = [w for w in banned if re.search(r"\b" + re.escape(w.lower()) + r"\b", tl)]
    if hits:
        swaps = ", ".join(f"{w} to {banned[w]}" for w in hits)
        return 0, f"Banned word(s): {', '.join(hits)} — swap {swaps}"
    return 2, "No banned words"


def check_signature(text: str, config: dict):
    sig = config.get("signature") if config else None
    if not sig:
        return None, "No hook signature configured — skipped"
    lines = [l for l in text.splitlines() if l.strip()]
    hook = "\n".join(lines[:2])
    if sig in hook:
        return 2, f"Hook carries the signature {sig}"
    return 0, f"Hook is missing the signature {sig}"


def grounded_signals(text: str, config: dict) -> dict:
    b_s, b_r = check_burstiness(text)
    c_s, c_r = check_contrast(text)
    bw_s, bw_r = check_banned_words(text, config)
    sg_s, sg_r = check_signature(text, config)
    checks = [
        {"signal": "Bursty rhythm, anti machine", "score": b_s, "reason": b_r},
        {"signal": "Contrast pair, X not Y", "score": c_s, "reason": c_r},
        {"signal": "Banned words", "score": bw_s, "reason": bw_r},
        {"signal": "Hook signature", "score": sg_s, "reason": sg_r},
    ]
    hard_fail = (bw_s == 0) or (sg_s == 0)
    return {"checks": checks, "hard_fail": hard_fail}


def score(text: str) -> dict:
    c1, r1 = score_criterion_1(text)
    c2, r2 = score_criterion_2(text)
    c3, r3 = score_criterion_3(text)
    c4, r4 = score_criterion_4(text)
    c5, r5 = score_criterion_5(text)
    total = c1 + c2 + c3 + c4 + c5
    return {
        "total": total,
        "threshold": 7,
        "passes": total >= 7,
        "breakdown": [
            {"criterion": "Opens with opinion",    "score": c1, "max": 2, "reason": r1},
            {"criterion": "Specific anchor",        "score": c2, "max": 2, "reason": r2},
            {"criterion": "No forbidden phrases",   "score": c3, "max": 2, "reason": r3},
            {"criterion": "Clear position",         "score": c4, "max": 2, "reason": r4},
            {"criterion": "Unique voice",           "score": c5, "max": 2, "reason": r5},
        ],
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("text", nargs="?", default=None)
    p.add_argument("--stdin", action="store_true")
    p.add_argument("--format", default="text", choices=["text", "json"])
    p.add_argument("--voice-config", default=None,
                   help="path to the user's voice_profile.json (signature, banned_words)")
    args = p.parse_args()

    if args.stdin or (args.text is None):
        text = sys.stdin.read().strip()
    else:
        text = args.text.strip()

    if not text:
        p.error("No post text provided")

    result = score(text)
    config = load_voice_config(args.voice_config)
    result["grounded"] = grounded_signals(text, config)
    result["passes_all"] = result["passes"] and not result["grounded"]["hard_fail"]

    if args.format == "json":
        print(json.dumps(result, indent=2))
        return

    status = "PASS ✓" if result["passes"] else "FAIL ✗ — rewrite needed"
    print(f"\nVOICE SCORE: {result['total']}/10  [{status}]")
    print(f"Threshold: {result['threshold']}/10\n")
    for b in result["breakdown"]:
        bar = "●" * b["score"] + "○" * (b["max"] - b["score"])
        print(f"  {bar}  {b['criterion']:<30} {b['score']}/{b['max']}  — {b['reason']}")

    print("\nGROUNDED VOICE SIGNALS:")
    for g in result["grounded"]["checks"]:
        sc = g["score"]
        mark = "—" if sc is None else ("●●" if sc == 2 else ("●○" if sc == 1 else "○○"))
        print(f"  {mark}  {g['signal']:<28} {g['reason']}")
    print()

    if result["passes_all"]:
        print("VERDICT: ships ✓  (voice quality and grounded signals both clear)")
    elif result["grounded"]["hard_fail"]:
        print("VERDICT: blocked ✗  (a grounded hard check failed, banned word or missing signature)")
    else:
        print("VERDICT: rewrite ✗  (voice score below threshold)")

    if not result["passes"]:
        weak = sorted(result["breakdown"], key=lambda x: x["score"])[:2]
        print("\nFix these first:")
        for w in weak:
            print(f"  [{w['criterion']}] {w['reason']}")


if __name__ == "__main__":
    main()
