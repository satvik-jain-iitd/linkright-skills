#!/usr/bin/env python3
"""
llm_dispatch.py — Free-LLM dispatch for Sage's external reasoning needs.

Cost policy: NEVER call api.anthropic.com (Claude API) or spawn subagents.
Use free provider tiers in cascade. Mirrors LinkRight CLI's `llm/direct.py`.

Cascade order (free providers only):
    1. Oracle Ollama        (zero cost, local Oracle VPS)
    2. Groq                 (free tier, fast)
    3. Cerebras             (free tier)
    4. Gemini free tier     (gemini-2.5-flash)
    5. Z.ai / SambaNova     (Route3 free-tier keys)
    6. Cloudflare AI Workers (free-tier)

Usage:
    python3 llm_dispatch.py --task <name> --prompt-file <prompt.txt> --output <out.json>
    python3 llm_dispatch.py --task <name> --prompt "<text>" --output <out.json>
    python3 llm_dispatch.py --list-providers  # show which providers have keys

Exit codes:
    0 = success (response written to output)
    1 = all providers exhausted (caller falls back to Claude inline reasoning,
        subscription quota only, no extra billing)
    2 = bad arguments
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional


_KEY_REGEX = re.compile(r'(AIza|sk-|gsk_|csk-|key-)[0-9A-Za-z_\-]{20,}')


def redact(s: str) -> str:
    """Redact API keys from log output."""
    return _KEY_REGEX.sub(r"\1...[REDACTED]", s)


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'").strip()
        if key and key not in os.environ:
            os.environ[key] = value


# Provider implementations — each returns response text or raises Exception
def try_oracle_ollama(prompt: str) -> str:
    backend_url = os.environ.get("ORACLE_BACKEND_URL")
    secret = os.environ.get("ORACLE_BACKEND_SECRET")
    if not backend_url or not secret:
        raise RuntimeError("ORACLE_BACKEND_URL/SECRET not set")
    req = urllib.request.Request(
        f"{backend_url.rstrip('/')}/api/generate",
        data=json.dumps({"model": "gemma3:1b", "prompt": prompt, "stream": False}).encode(),
        headers={"Authorization": f"Bearer {secret}", "Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())["response"]


def try_groq(prompt: str) -> str:
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        raise RuntimeError("GROQ_API_KEY not set")
    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=json.dumps({
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
        }).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"]


def try_cerebras(prompt: str) -> str:
    key = os.environ.get("CEREBRAS_API_KEY")
    if not key:
        raise RuntimeError("CEREBRAS_API_KEY not set")
    req = urllib.request.Request(
        "https://api.cerebras.ai/v1/chat/completions",
        data=json.dumps({
            "model": "llama3.3-70b",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
        }).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"]


def try_gemini(prompt: str) -> str:
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY not set")
    if not re.match(r'^AIza[0-9A-Za-z\-_]{20,}$', key):
        raise RuntimeError("GEMINI_API_KEY format unexpected")
    model = "gemini-2.5-flash"
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        data=json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode(),
        headers={"x-goog-api-key": key, "Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read())
        return data["candidates"][0]["content"]["parts"][0]["text"]


# Cascade definition: ordered list of (name, function) tuples
PROVIDERS = [
    ("oracle_ollama", try_oracle_ollama),
    ("groq",          try_groq),
    ("cerebras",      try_cerebras),
    ("gemini",        try_gemini),
]


def list_providers() -> None:
    """Show which providers have credentials configured."""
    home = Path.home()
    load_env_file(home / ".linkright" / ".env")
    for name, _ in PROVIDERS:
        env_var = {
            "oracle_ollama": "ORACLE_BACKEND_URL",
            "groq":          "GROQ_API_KEY",
            "cerebras":      "CEREBRAS_API_KEY",
            "gemini":        "GEMINI_API_KEY",
        }[name]
        present = "✓" if os.environ.get(env_var) else "✗"
        print(f"  {present} {name:<18} env: {env_var}")


def dispatch(prompt: str, task: str) -> Optional[str]:
    """Try providers in order; return first success or None."""
    home = Path.home()
    load_env_file(home / ".linkright" / ".env")

    for name, fn in PROVIDERS:
        start = time.time()
        try:
            response = fn(prompt)
            elapsed = time.time() - start
            print(f"  ✓ Provider '{name}' succeeded in {elapsed:.2f}s (task={task})",
                  file=sys.stderr)
            return response
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            print(f"  ✗ Provider '{name}' HTTP failure: {redact(str(e))}", file=sys.stderr)
        except RuntimeError as e:
            print(f"  ✗ Provider '{name}' skipped: {e}", file=sys.stderr)
        except Exception as e:
            print(f"  ✗ Provider '{name}' unexpected: {redact(str(e))}", file=sys.stderr)

    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Sage free-LLM dispatcher (NEVER calls Claude API)")
    parser.add_argument("--task", default="generic", help="Task name for logging")
    parser.add_argument("--prompt-file", type=Path, help="Read prompt from file")
    parser.add_argument("--prompt", help="Prompt text inline")
    parser.add_argument("--output", type=Path, help="Write response to file (default: stdout)")
    parser.add_argument("--list-providers", action="store_true", help="Show provider status and exit")
    args = parser.parse_args()

    if args.list_providers:
        list_providers()
        return 0

    if args.prompt_file and args.prompt_file.exists():
        prompt = args.prompt_file.read_text()
    elif args.prompt:
        prompt = args.prompt
    else:
        print("ERROR: provide --prompt or --prompt-file", file=sys.stderr)
        return 2

    response = dispatch(prompt, args.task)
    if response is None:
        print("ERROR: All free providers exhausted. Caller should fall back to Claude inline "
              "reasoning (subscription quota only).", file=sys.stderr)
        return 1

    if args.output:
        args.output.write_text(response)
        print(f"OK: response written to {args.output}", file=sys.stderr)
    else:
        print(response)
    return 0


if __name__ == "__main__":
    sys.exit(main())
