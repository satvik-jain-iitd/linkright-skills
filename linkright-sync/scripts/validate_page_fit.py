#!/usr/bin/env python3
"""
Check if HTML resume content fits within A4 page (271.6mm usable height).
Usage: python3 validate_page_fit.py '<html_content>'
       python3 validate_page_fit.py --file resume.html
Output: JSON {"fits": bool, "estimated_height_mm": X, "budget_mm": 271.6, "overflow_mm": Y}
"""

import argparse
import json
import re
import sys

A4_HEIGHT_MM = 271.6  # A4 usable height at standard margins

# Line height estimates in mm (Roboto 10px)
LINE_HEIGHT_MM = 4.23      # single line of text (~16px line-height)
SECTION_GAP_MM = 3.70      # gap between sections
ROLE_HEADER_MM = 6.35      # company/role header line
SECTION_HEADER_MM = 5.29   # section heading (e.g., EXPERIENCE)
CONTACT_BAR_MM = 7.40      # name + contact bar
SKILLS_ROW_MM = 4.23       # one row of skills
SPACER_MM = 1.50           # bullet-group-spacer


def strip_tags(text: str) -> str:
    return re.sub(r'<[^>]+>', ' ', text)


def estimate_height(html: str) -> float:
    """Rough height estimation from HTML structure."""
    height = 0.0

    # Contact / name header
    if re.search(r'<h1|class=["\']name["\']', html):
        height += CONTACT_BAR_MM

    # Count section headers
    headers = re.findall(r'<(h2|h3)[^>]*>|class=["\'][^"\']*section[^"\']*["\']', html)
    height += len(headers) * SECTION_HEADER_MM

    # Count role/company blocks
    roles = re.findall(r'class=["\'][^"\']*role[^"\']*["\']|class=["\'][^"\']*job[^"\']*["\']|\\\\bf ', html)
    height += len(roles) * ROLE_HEADER_MM

    # Count bullet items
    bullets = re.findall(r'<li\b(?![^>]*aria-hidden)', html)
    height += len(bullets) * LINE_HEIGHT_MM

    # Count bullet group spacers
    spacers = re.findall(r'aria-hidden=["\']true["\']', html)
    height += len(spacers) * SPACER_MM

    # Section gaps (approximate)
    height += max(0, len(headers) - 1) * SECTION_GAP_MM

    return height


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("html", nargs="?", help="HTML content string")
    parser.add_argument("--file", help="HTML file path")
    parser.add_argument("--budget", type=float, default=A4_HEIGHT_MM)
    parser.add_argument("--format", choices=["json", "human"], default="json")
    args = parser.parse_args()

    if args.file:
        from pathlib import Path
        html = Path(args.file).expanduser().read_text()
    elif args.html:
        html = args.html
    else:
        html = sys.stdin.read()

    if not html.strip():
        print(json.dumps({"error": "no content provided"}))
        sys.exit(1)

    estimated = estimate_height(html)
    fits = estimated <= args.budget
    overflow = max(0.0, estimated - args.budget)

    result = {
        "fits": fits,
        "estimated_height_mm": round(estimated, 1),
        "budget_mm": args.budget,
        "overflow_mm": round(overflow, 1),
    }

    if args.format == "json":
        print(json.dumps(result))
    else:
        status = "✓ FITS" if fits else f"✗ OVERFLOW by {overflow:.1f}mm"
        print(f"{status} — estimated {estimated:.1f}mm / {args.budget}mm budget")
        if not fits:
            bullets_to_cut = int(overflow / LINE_HEIGHT_MM) + 1
            print(f"  → Remove ~{bullets_to_cut} bullet(s) or tighten spacing")

    sys.exit(0 if fits else 1)


if __name__ == "__main__":
    main()
