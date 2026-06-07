#!/usr/bin/env python3
"""
Check WCAG AA color contrast ratio between foreground and background.
Usage: python3 validate_contrast.py '#0F766E' ['#FFFFFF']
Output: JSON {"ratio": X, "passes_aa": bool, "passes_aaa": bool, "hex": "#..."}
WCAG AA requires ratio >= 4.5:1 for normal text.
"""

import argparse
import json
import sys


def hex_to_rgb(hex_color: str) -> tuple:
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join(c * 2 for c in hex_color)
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return r, g, b


def relative_luminance(r: int, g: int, b: int) -> float:
    """WCAG 2.1 relative luminance formula."""
    def channel(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast_ratio(color1: str, color2: str = "#FFFFFF") -> float:
    r1, g1, b1 = hex_to_rgb(color1)
    r2, g2, b2 = hex_to_rgb(color2)
    l1 = relative_luminance(r1, g1, b1)
    l2 = relative_luminance(r2, g2, b2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("foreground", help="Foreground hex color (e.g. #0F766E)")
    parser.add_argument("background", nargs="?", default="#FFFFFF", help="Background hex color (default: #FFFFFF)")
    parser.add_argument("--format", choices=["json", "human"], default="json")
    args = parser.parse_args()

    try:
        ratio = contrast_ratio(args.foreground, args.background)
    except (ValueError, IndexError) as e:
        print(json.dumps({"error": f"Invalid hex color: {e}"}))
        sys.exit(1)

    passes_aa = ratio >= 4.5
    passes_aaa = ratio >= 7.0

    result = {
        "hex": args.foreground,
        "background": args.background,
        "ratio": round(ratio, 2),
        "passes_aa": passes_aa,
        "passes_aaa": passes_aaa,
    }

    if args.format == "json":
        print(json.dumps(result))
    else:
        status = "✓ PASS" if passes_aa else "✗ FAIL"
        print(f"{status} — {args.foreground} on {args.background}: {ratio:.2f}:1 (AA requires 4.5:1)")
        if not passes_aa:
            print("  → Choose a darker shade of this color for text use")

    sys.exit(0 if passes_aa else 1)


if __name__ == "__main__":
    main()
