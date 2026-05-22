#!/usr/bin/env python3
"""
Check HTML resume for ATS-hostile formatting.
Usage: python3 ats_scanner.py '<html>' | python3 ats_scanner.py --file resume.html
Output: JSON {"issues": [...], "clean": bool, "count": N}
"""

import argparse
import json
import re
import sys
from pathlib import Path


def scan_html(html: str) -> list:
    issues = []

    # Tables used for layout
    if re.search(r'<table\b', html, re.IGNORECASE):
        issues.append({
            "severity": "HIGH",
            "issue": "HTML table detected",
            "fix": "Use div/flexbox layout instead of tables — ATS parsers often skip table content"
        })

    # Text boxes / absolute positioning
    if re.search(r'position\s*:\s*(absolute|fixed)', html, re.IGNORECASE):
        issues.append({
            "severity": "HIGH",
            "issue": "Absolute/fixed positioned element",
            "fix": "Remove absolute positioning — ATS reads DOM order, positioned elements lose context"
        })

    # CSS columns (multi-column layouts)
    if re.search(r'column-count|column-gap|css-columns|grid-template-columns', html, re.IGNORECASE):
        issues.append({
            "severity": "HIGH",
            "issue": "Multi-column CSS layout detected",
            "fix": "Use single-column layout — ATS reads left-to-right, columns merge incorrectly"
        })

    # Overflow hidden on bullet containers
    if re.search(r'overflow\s*:\s*hidden', html, re.IGNORECASE):
        issues.append({
            "severity": "HIGH",
            "issue": "overflow:hidden on element — may truncate content",
            "fix": "Remove overflow:hidden from any text containers"
        })

    # Text in images (SVG/canvas/img with text as image)
    if re.search(r'<(?:svg|canvas)\b', html, re.IGNORECASE):
        issues.append({
            "severity": "MEDIUM",
            "issue": "SVG or canvas element — text inside is invisible to ATS",
            "fix": "Replace with plain HTML text or remove decorative elements"
        })

    # Headers/footers with critical info
    if re.search(r'@page|@media\s+print.*header|@media\s+print.*footer', html, re.IGNORECASE):
        issues.append({
            "severity": "MEDIUM",
            "issue": "Print header/footer styles detected",
            "fix": "Don't put name/contact in CSS-generated headers/footers — ATS won't read them"
        })

    # Unicode bullets/icons used as text
    fancy_bullets = re.findall(r'[■▪▸▶◆●►◉]', html)
    if fancy_bullets:
        issues.append({
            "severity": "LOW",
            "issue": f"Fancy Unicode bullet characters found: {set(fancy_bullets)}",
            "fix": "Use standard HTML <li> bullets or plain '-' — Unicode icons parse inconsistently"
        })

    # Text in background-image
    if re.search(r'background-image\s*:', html, re.IGNORECASE):
        issues.append({
            "severity": "LOW",
            "issue": "background-image CSS property — any text in images is invisible to ATS",
            "fix": "Use plain HTML text, not images for any content"
        })

    # font-size below 8px (too small, may be hidden text trick)
    small_fonts = re.findall(r'font-size\s*:\s*([0-9.]+)(?:px|pt)', html, re.IGNORECASE)
    for size_str in small_fonts:
        size = float(size_str)
        if size < 8:
            issues.append({
                "severity": "MEDIUM",
                "issue": f"Very small font size: {size}px — ATS may flag as keyword stuffing",
                "fix": "Remove any hidden text / font-size < 8px"
            })
            break

    return issues


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("html", nargs="?", help="HTML content")
    parser.add_argument("--file", help="HTML file path")
    parser.add_argument("--format", choices=["json", "human"], default="json")
    args = parser.parse_args()

    if args.file:
        html = Path(args.file).expanduser().read_text()
    elif args.html:
        html = args.html
    else:
        html = sys.stdin.read()

    if not html.strip():
        print(json.dumps({"error": "no HTML provided"}))
        sys.exit(1)

    issues = scan_html(html)
    result = {"issues": issues, "clean": len(issues) == 0, "count": len(issues)}
    high_count = sum(1 for i in issues if i["severity"] == "HIGH")

    if args.format == "json":
        print(json.dumps(result))
    else:
        if result["clean"]:
            print("✓ ATS CLEAN — no hostile formatting detected")
        else:
            print(f"✗ {result['count']} ATS issue(s) found ({high_count} HIGH severity):")
            for issue in issues:
                print(f"\n  [{issue['severity']}] {issue['issue']}")
                print(f"  → {issue['fix']}")

    sys.exit(0 if result["clean"] else 1)


if __name__ == "__main__":
    main()
