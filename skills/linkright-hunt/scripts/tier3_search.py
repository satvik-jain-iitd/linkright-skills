#!/usr/bin/env python3
"""
Tier 3 job search — Remotive, RemoteOK, Wellfound (YC).
Usage: python3 tier3_search.py --query 'product manager' [--source remotive|remoteok|all]
Output: JSON list of {title, company, url, location, tags, source, posted_date}
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
import re
from datetime import datetime


def search_remotive(query: str) -> list:
    """Remotive public API — free, no auth required."""
    try:
        encoded = urllib.parse.quote(query)
        url = f"https://remotive.com/api/remote-jobs?search={encoded}&limit=20"
        req = urllib.request.urlopen(url, timeout=10)
        data = json.loads(req.read())
        jobs = data.get("jobs", [])
        return [
            {
                "title": j.get("title", ""),
                "company": j.get("company_name", ""),
                "url": j.get("url", ""),
                "location": j.get("candidate_required_location", "Remote"),
                "tags": j.get("tags", []),
                "source": "remotive",
                "posted_date": j.get("publication_date", "")[:10],
            }
            for j in jobs
        ]
    except Exception as e:
        return [{"error": f"remotive: {e}"}]


def search_remoteok(query: str) -> list:
    """RemoteOK public API — free, no auth required."""
    try:
        url = "https://remoteok.com/api"
        req = urllib.request.Request(url, headers={"User-Agent": "linkright-hunt/1.0"})
        response = urllib.request.urlopen(req, timeout=10)
        all_jobs = json.loads(response.read())
        # First item is metadata, skip it
        if all_jobs and "legal" in str(all_jobs[0]):
            all_jobs = all_jobs[1:]

        query_lower = query.lower()
        filtered = []
        for j in all_jobs:
            if not isinstance(j, dict):
                continue
            title = j.get("position", "")
            if not any(term in title.lower() for term in query_lower.split()):
                continue
            filtered.append({
                "title": title,
                "company": j.get("company", ""),
                "url": j.get("url", ""),
                "location": "Remote",
                "tags": j.get("tags", []) or [],
                "source": "remoteok",
                "posted_date": datetime.fromtimestamp(
                    int(j.get("epoch", 0))
                ).strftime("%Y-%m-%d") if j.get("epoch") else "",
            })
            if len(filtered) >= 20:
                break
        return filtered
    except Exception as e:
        return [{"error": f"remoteok: {e}"}]


def search_wellfound(query: str) -> list:
    """
    Wellfound (YC's AngelList) — no free public API.
    Returns a search URL for manual review instead.
    """
    encoded = urllib.parse.quote(query)
    search_url = f"https://wellfound.com/jobs?q={encoded}&role=product-manager"
    return [{
        "title": "Wellfound search (manual review required)",
        "company": "various",
        "url": search_url,
        "location": "varies",
        "tags": [],
        "source": "wellfound",
        "posted_date": "",
        "note": "Wellfound has no free public API. Open URL in browser to review results.",
    }]


def filter_pm_roles(jobs: list) -> list:
    """Keep only PM-relevant roles."""
    pm_terms = [
        "product manager", "pm ", "head of product", "vp of product",
        "director of product", "product lead", "product owner",
        "senior pm", "principal pm", "group pm", "associate pm",
    ]
    filtered = []
    for j in jobs:
        if "error" in j:
            filtered.append(j)
            continue
        title_lower = j.get("title", "").lower()
        if any(term in title_lower for term in pm_terms):
            filtered.append(j)
    return filtered


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", default="product manager")
    parser.add_argument("--source", choices=["remotive", "remoteok", "wellfound", "all"],
                        default="all")
    parser.add_argument("--pm-only", action="store_true", default=True,
                        help="Filter to PM roles only")
    parser.add_argument("--format", choices=["json", "human"], default="json")
    args = parser.parse_args()

    results = []

    if args.source in ("remotive", "all"):
        results.extend(search_remotive(args.query))

    if args.source in ("remoteok", "all"):
        results.extend(search_remoteok(args.query))

    if args.source in ("wellfound", "all"):
        results.extend(search_wellfound(args.query))

    if args.pm_only:
        results = filter_pm_roles(results)

    if args.format == "json":
        print(json.dumps(results, indent=2))
    else:
        errors = [r for r in results if "error" in r]
        jobs = [r for r in results if "error" not in r]
        print(f"Found {len(jobs)} jobs (query: '{args.query}')")
        for j in jobs:
            print(f"\n  [{j['source']}] {j['title']} @ {j['company']}")
            print(f"  {j['url']}")
            if j.get("tags"):
                print(f"  Tags: {', '.join(j['tags'][:5])}")
        if errors:
            print(f"\nErrors ({len(errors)}):")
            for e in errors:
                print(f"  {e}")


if __name__ == "__main__":
    main()
