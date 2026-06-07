"""
generate_pdf.py — HTML to PDF via headless Chrome.
Falls back to weasyprint if Chrome not found.

Usage:
  python3 generate_pdf.py resume.html
  python3 generate_pdf.py resume.html --output resume.pdf
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "chromium-browser",
    "chromium",
    "google-chrome",
    "google-chrome-stable",
]


def find_chrome() -> str | None:
    for c in CHROME_CANDIDATES:
        if Path(c).exists():
            return c
        if shutil.which(c):
            return c
    return None


def pdf_via_chrome(html_path: Path, pdf_path: Path) -> bool:
    chrome = find_chrome()
    if not chrome:
        return False
    abs_html = html_path.resolve()
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--run-all-compositor-stages-before-draw",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={pdf_path.resolve()}",
        f"file://{abs_html}",
    ]
    result = subprocess.run(cmd, capture_output=True, timeout=60)
    return result.returncode == 0 and pdf_path.exists()


def pdf_via_weasyprint(html_path: Path, pdf_path: Path) -> bool:
    try:
        import weasyprint  # type: ignore
        weasyprint.HTML(filename=str(html_path.resolve())).write_pdf(str(pdf_path))
        return pdf_path.exists()
    except ImportError:
        return False


def main():
    p = argparse.ArgumentParser()
    p.add_argument("html_path")
    p.add_argument("--output", default=None)
    args = p.parse_args()

    html_path = Path(args.html_path).expanduser()
    if not html_path.exists():
        print(f"Error: HTML not found: {html_path}", file=sys.stderr)
        sys.exit(1)

    pdf_path = Path(args.output).expanduser() if args.output else html_path.with_suffix(".pdf")

    print(f"Generating PDF: {pdf_path.name}")

    if pdf_via_chrome(html_path, pdf_path):
        print(f"✓ PDF: {pdf_path}  (via headless Chrome)")
        return

    if pdf_via_weasyprint(html_path, pdf_path):
        print(f"✓ PDF: {pdf_path}  (via WeasyPrint)")
        return

    print("Error: PDF generation failed.", file=sys.stderr)
    print("Install Chrome or: pip install weasyprint", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
