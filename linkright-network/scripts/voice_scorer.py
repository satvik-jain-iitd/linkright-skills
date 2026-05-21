"""
voice_scorer.py — Score a LinkedIn post on the LinkRight voice rubric (0-10).

Usage:
  python3 voice_scorer.py '<post_text>'
  echo '<post_text>' | python3 voice_scorer.py --stdin
  python3 voice_scorer.py '<post_text>' --format json
"""

import argparse
import json
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
    args = p.parse_args()

    if args.stdin or (args.text is None):
        text = sys.stdin.read().strip()
    else:
        text = args.text.strip()

    if not text:
        p.error("No post text provided")

    result = score(text)

    if args.format == "json":
        print(json.dumps(result, indent=2))
        return

    status = "PASS ✓" if result["passes"] else "FAIL ✗ — rewrite needed"
    print(f"\nVOICE SCORE: {result['total']}/10  [{status}]")
    print(f"Threshold: {result['threshold']}/10\n")
    for b in result["breakdown"]:
        bar = "●" * b["score"] + "○" * (b["max"] - b["score"])
        print(f"  {bar}  {b['criterion']:<30} {b['score']}/{b['max']}  — {b['reason']}")
    print()

    if not result["passes"]:
        weak = sorted(result["breakdown"], key=lambda x: x["score"])[:2]
        print("Fix these first:")
        for w in weak:
            print(f"  [{w['criterion']}] {w['reason']}")


if __name__ == "__main__":
    main()
