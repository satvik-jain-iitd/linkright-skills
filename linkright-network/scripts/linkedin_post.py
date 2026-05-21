"""
linkedin_post.py — Post to LinkedIn via UGC Posts API.
Always runs dry-run first; requires explicit --confirm to POST.

Usage:
  python3 linkedin_post.py --text 'post text' --token-file ~/.linkright/.env --dry-run
  python3 linkedin_post.py --text 'post text' --token-file ~/.linkright/.env --confirm
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False

API_URL = "https://api.linkedin.com/v2/ugcPosts"
PROFILE_URL = "https://api.linkedin.com/v2/userinfo"


def load_token(token_file: str) -> str:
    path = Path(token_file).expanduser()
    if not path.exists():
        raise FileNotFoundError(f"Token file not found: {path}")
    text = path.read_text()
    # Support both KEY=value and bare token
    match = re.search(r"LINKEDIN_ACCESS_TOKEN\s*=\s*['\"]?([^\s'\"]+)", text)
    if match:
        return match.group(1)
    lines = [l.strip() for l in text.splitlines() if l.strip() and not l.startswith("#")]
    if lines:
        return lines[0]
    raise ValueError("No LinkedIn access token found in token file")


def get_author_urn(token: str) -> str:
    if not HAS_HTTPX:
        raise ImportError("pip install httpx")
    r = httpx.get(PROFILE_URL, headers={"Authorization": f"Bearer {token}"}, timeout=10)
    r.raise_for_status()
    sub = r.json().get("sub")
    if not sub:
        raise ValueError(f"Could not get user sub from userinfo: {r.text}")
    return f"urn:li:person:{sub}"


def build_payload(author_urn: str, text: str) -> dict:
    return {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": text},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--text", required=True)
    p.add_argument("--token-file", default="~/.linkright/.env")
    p.add_argument("--dry-run", action="store_true", default=True)
    p.add_argument("--confirm", action="store_true")
    args = p.parse_args()

    text = args.text.strip()
    if not text:
        p.error("Post text is empty")

    print(f"\nPOST PREVIEW ({len(text)} chars):")
    print("─" * 60)
    print(text)
    print("─" * 60)

    if args.dry_run and not args.confirm:
        print("\nDRY RUN — not posted. Add --confirm to actually post.")
        print(f"\nAPI call that would execute:")
        print(f"  POST {API_URL}")
        print(f"  Auth: Bearer <token>")
        print(f"  Body: {{'text': '{text[:60]}...'}}")
        return

    if not HAS_HTTPX:
        print("Error: pip install httpx", file=sys.stderr)
        sys.exit(1)

    token = load_token(args.token_file)
    author = get_author_urn(token)
    payload = build_payload(author, text)

    print(f"\nPosting as: {author}")
    r = httpx.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        },
        json=payload,
        timeout=15,
    )

    if r.status_code in (200, 201):
        post_id = r.headers.get("X-RestLi-Id") or r.json().get("id", "unknown")
        print(f"✓ Posted. ID: {post_id}")
    else:
        print(f"Error: HTTP {r.status_code}", file=sys.stderr)
        print(r.text, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
