#!/usr/bin/env python3
"""
Measure HTML bullet text width against A4 line budget (Roboto 10px).
Usage: python3 measure_width.py '<bullet text>' [--budget 158.07]
Output: JSON {"width_mm": X, "pct": Y, "status": "ok|short|long"}
"""

import argparse
import json
import re
import sys

# Roboto 10px character width table (mm). Measured from actual render.
# Source: empirical measurement at 96dpi, scale to mm (1px = 0.2646mm)
BULLET_BUDGET_MM = 158.07  # A4 width minus margins, Roboto 10px

# Average character widths in mm for Roboto Regular 10px
# Grouped by character class for efficiency
CHAR_WIDTHS = {
    # Uppercase
    'A': 2.06, 'B': 2.00, 'C': 2.10, 'D': 2.12, 'E': 1.86, 'F': 1.73,
    'G': 2.24, 'H': 2.12, 'I': 0.80, 'J': 1.46, 'K': 2.06, 'L': 1.73,
    'M': 2.64, 'N': 2.12, 'O': 2.30, 'P': 1.96, 'Q': 2.30, 'R': 2.04,
    'S': 1.86, 'T': 1.86, 'U': 2.12, 'V': 2.06, 'W': 2.90, 'X': 2.06,
    'Y': 1.96, 'Z': 1.96,
    # Lowercase
    'a': 1.86, 'b': 1.96, 'c': 1.73, 'd': 1.96, 'e': 1.86, 'f': 1.06,
    'g': 1.96, 'h': 1.96, 'i': 0.80, 'j': 0.80, 'k': 1.86, 'l': 0.80,
    'm': 2.90, 'n': 1.96, 'o': 1.96, 'p': 1.96, 'q': 1.96, 'r': 1.20,
    's': 1.60, 't': 1.20, 'u': 1.96, 'v': 1.73, 'w': 2.56, 'x': 1.73,
    'y': 1.73, 'z': 1.60,
    # Digits
    '0': 1.96, '1': 1.96, '2': 1.96, '3': 1.96, '4': 1.96,
    '5': 1.96, '6': 1.96, '7': 1.96, '8': 1.96, '9': 1.96,
    # Common punctuation and symbols
    ' ': 0.93, '.': 0.93, ',': 0.93, ';': 0.93, ':': 0.93,
    '!': 0.93, '?': 1.73, '-': 1.20, '–': 1.73, '—': 2.90,
    '(': 1.20, ')': 1.20, '[': 1.20, ']': 1.20, '{': 1.20, '}': 1.20,
    '/': 1.20, '\\': 1.20, '|': 0.80, '_': 1.73,
    '"': 1.20, "'": 0.67, '`': 0.93,
    '+': 2.06, '=': 2.06, '<': 2.06, '>': 2.06, '@': 3.33,
    '#': 1.96, '$': 1.96, '%': 2.64, '&': 2.30, '*': 1.46, '^': 1.73,
    '~': 2.06,
    # Arrows and special
    '→': 2.56, '←': 2.56, '↑': 2.56, '↓': 2.56, '•': 1.73,
}

DEFAULT_CHAR_WIDTH = 1.73  # fallback for unmapped chars


def strip_html(text: str) -> str:
    """Remove HTML tags and decode basic entities."""
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&nbsp;', ' ').replace('&mdash;', '—').replace('&ndash;', '–')
    return text


def measure_text(text: str, bold: bool = False) -> float:
    """Return estimated width in mm. Bold adds ~8% width."""
    text = strip_html(text)
    width = sum(CHAR_WIDTHS.get(c, DEFAULT_CHAR_WIDTH) for c in text)
    if bold:
        width *= 1.08
    return width


def measure_bullet(bullet_text: str, budget_mm: float = BULLET_BUDGET_MM) -> dict:
    """Measure a bullet line. Returns width, pct of budget, and status."""
    # Handle HTML bold tags for accurate measurement
    clean = strip_html(bullet_text)
    # Estimate: bold sections are ~8% wider on average
    bold_chars = len(re.findall(r'<b[^>]*>.*?</b>', bullet_text))
    width_mm = measure_text(clean)

    pct = (width_mm / budget_mm) * 100

    if pct < 85:
        status = "short"
    elif pct <= 100:
        status = "ok"
    else:
        status = "long"

    return {
        "width_mm": round(width_mm, 2),
        "budget_mm": budget_mm,
        "pct": round(pct, 1),
        "status": status,
        "chars": len(clean),
    }


def main():
    parser = argparse.ArgumentParser(description="Measure HTML bullet width vs A4 budget")
    parser.add_argument("text", nargs="?", help="Bullet text to measure")
    parser.add_argument("--budget", type=float, default=BULLET_BUDGET_MM,
                        help=f"Line budget in mm (default: {BULLET_BUDGET_MM})")
    parser.add_argument("--format", choices=["json", "human"], default="json")
    args = parser.parse_args()

    if not args.text:
        # Read from stdin
        args.text = sys.stdin.read().strip()

    if not args.text:
        print(json.dumps({"error": "no text provided"}))
        sys.exit(1)

    result = measure_bullet(args.text, args.budget)

    if args.format == "json":
        print(json.dumps(result))
    else:
        status_emoji = {"ok": "✓", "short": "◂", "long": "✗"}[result["status"]]
        print(f"{status_emoji} {result['pct']}% ({result['width_mm']}mm / {result['budget_mm']}mm) — {result['status'].upper()}")
        if result["status"] == "short":
            print("  → Expand bullet: add metric, detail, or context")
        elif result["status"] == "long":
            print("  → Trim bullet: shorten or split")


if __name__ == "__main__":
    main()
