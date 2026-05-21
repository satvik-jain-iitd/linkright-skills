"""
validate_html.py — Pre-push HTML validation for resume files.

Usage:
  python3 validate_html.py resume.html
  python3 validate_html.py resume.html --format json
"""

import argparse
import json
import re
import sys
from pathlib import Path


ATS_HOSTILE = [
    (r"<table", "Tables break ATS parsing — use div layout"),
    (r"<frameset|<frame|<iframe", "Frames/iframes not parseable by ATS"),
    (r"position:\s*absolute", "Absolute positioning can break ATS text extraction"),
    (r"column-count\s*:\s*[2-9]", "CSS columns break ATS single-column expectation"),
    (r"text-indent\s*:\s*-\d{3,}", "Large negative text-indent hides text — ATS flag"),
    (r"color\s*:\s*white.*background.*white|color\s*:\s*#fff.*background.*#fff", "White-on-white hidden text — ATS red flag"),
]

REQUIRED_SECTIONS = ["experience", "education"]


def validate(path: Path) -> list[dict]:
    flags = []
    text = path.read_text(encoding="utf-8", errors="replace")
    text_lower = text.lower()

    # ATS hostile patterns
    for pattern, msg in ATS_HOSTILE:
        if re.search(pattern, text_lower):
            flags.append({"check": "ats", "severity": "WARN", "detail": msg})

    # Must have <html>, <head>, <body>
    for tag in ["<html", "<head", "<body"]:
        if tag not in text_lower:
            flags.append({"check": "structure", "severity": "BLOCK", "detail": f"Missing {tag} tag"})

    # Must have <title>
    if "<title>" not in text_lower:
        flags.append({"check": "structure", "severity": "WARN", "detail": "Missing <title> tag"})

    # Check unclosed tags (simple heuristic)
    opens = len(re.findall(r"<div[\s>]", text_lower))
    closes = len(re.findall(r"</div>", text_lower))
    if abs(opens - closes) > 3:
        flags.append({"check": "structure", "severity": "WARN",
                      "detail": f"Unbalanced divs: {opens} opens vs {closes} closes"})

    # Must have content (not empty skeleton)
    text_content = re.sub(r"<[^>]+>", " ", text).strip()
    if len(text_content) < 200:
        flags.append({"check": "content", "severity": "BLOCK", "detail": "File has less than 200 chars of text content"})

    # Inline base64 images (bloat ATS)
    b64_count = len(re.findall(r'src=["\']data:image', text))
    if b64_count > 0:
        flags.append({"check": "ats", "severity": "WARN",
                      "detail": f"{b64_count} base64 inline image(s) — large file size, possible ATS parsing issue"})

    # File size check
    size_kb = path.stat().st_size / 1024
    if size_kb > 500:
        flags.append({"check": "size", "severity": "WARN",
                      "detail": f"File size {size_kb:.0f}KB — resume HTML should be <500KB"})

    return flags


def main():
    p = argparse.ArgumentParser()
    p.add_argument("html_path")
    p.add_argument("--format", default="text", choices=["text", "json"])
    args = p.parse_args()

    path = Path(args.html_path).expanduser()
    if not path.exists():
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)

    flags = validate(path)
    blocks = [f for f in flags if f["severity"] == "BLOCK"]
    warns  = [f for f in flags if f["severity"] == "WARN"]
    status = "BLOCKED" if blocks else ("WARN" if warns else "CLEAN")

    if args.format == "json":
        print(json.dumps({"status": status, "path": str(path), "blocks": blocks, "warnings": warns}))
        sys.exit(1 if blocks else 0)

    print(f"\nHTML VALIDATION — {status}  ({path.name})")
    if status == "CLEAN":
        print("  All checks passed.")
        return

    if blocks:
        print(f"\nBLOCKERS ({len(blocks)}):")
        for f in blocks:
            print(f"  [{f['check']}] {f['detail']}")
    if warns:
        print(f"\nWARNINGS ({len(warns)}):")
        for f in warns:
            print(f"  [{f['check']}] {f['detail']}")

    if blocks:
        sys.exit(1)


if __name__ == "__main__":
    main()
