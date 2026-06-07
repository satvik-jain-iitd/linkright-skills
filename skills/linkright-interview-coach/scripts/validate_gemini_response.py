#!/usr/bin/env python3
"""
validate_gemini_response.py — Validate Gemini stage JSON against schema.

Replaces the broken jq-based validator (adversarial review #3). Separate
Python file (not heredoc inside bash) so stdin isn't consumed by source loading.

Usage:
    python3 validate_gemini_response.py <stage> <schema_path> <json_path_or_->
      stage:       stage1 | stage2 | stage3
      schema_path: path to gemini-response-schemas.json
      json_path:   path to JSON file, or "-" for stdin

Exit codes:
    0 = valid (echoes parsed JSON to stdout)
    1 = invalid (error on stderr)
    2 = bad arguments
"""

import json
import re
import sys
from pathlib import Path


def extract_json_block(text: str) -> str:
    """Strip code fences (```json...``` etc) and extract outer { ... } block."""
    # Remove fenced markers at any line
    text = re.sub(r'(?m)^[`~]{3,}[a-zA-Z]*\s*$', '', text)
    text = re.sub(r'(?m)^[`~]{3,}\s*$', '', text)
    # Find outer braces
    start = text.find('{')
    end = text.rfind('}')
    if start >= 0 and end > start:
        return text[start:end + 1]
    return text


def main() -> int:
    if len(sys.argv) != 4:
        print(
            "Usage: python3 validate_gemini_response.py <stage> <schema_path> <json_path_or_->",
            file=sys.stderr,
        )
        return 2

    stage_arg = sys.argv[1]
    schema_path = Path(sys.argv[2])
    json_arg = sys.argv[3]

    if stage_arg not in ("stage1", "stage2", "stage3"):
        print(f"ERROR: Invalid stage '{stage_arg}'. Must be stage1, stage2, or stage3.",
              file=sys.stderr)
        return 2

    # Read raw input
    if json_arg in ("-", "/dev/stdin"):
        raw = sys.stdin.read()
    else:
        p = Path(json_arg)
        if not p.exists():
            print(f"ERROR: JSON file not found: {json_arg}", file=sys.stderr)
            return 1
        raw = p.read_text()

    clean = extract_json_block(raw).strip()

    if not clean:
        print("ERROR: Empty input after fence stripping.", file=sys.stderr)
        return 1

    try:
        data = json.loads(clean)
    except json.JSONDecodeError as e:
        print(
            f"ERROR: Invalid JSON ({e}). Cause: extra prose, unbalanced braces, or trailing commas.",
            file=sys.stderr,
        )
        return 1

    if not schema_path.exists():
        print(f"ERROR: schema file missing at {schema_path}", file=sys.stderr)
        return 1

    try:
        full_schema = json.loads(schema_path.read_text())
    except Exception as e:
        print(f"ERROR: Could not load schema: {e}", file=sys.stderr)
        return 1

    stage_to_def = {
        "stage1": "stage1_video",
        "stage2": "stage2_audio",
        "stage3": "stage3_transcript",
    }
    stage_def_name = stage_to_def[stage_arg]
    defs = full_schema.get("definitions", {})
    if stage_def_name not in defs:
        print(f"ERROR: schema missing definitions.{stage_def_name}", file=sys.stderr)
        return 1
    stage_schema = defs[stage_def_name]

    # Prefer real jsonschema library if available
    try:
        import jsonschema
        from jsonschema import RefResolver, ValidationError

        resolver = RefResolver.from_schema(full_schema)
        try:
            jsonschema.validate(instance=data, schema=stage_schema, resolver=resolver)
        except ValidationError as e:
            path_str = " > ".join(str(p) for p in e.absolute_path) or "<root>"
            print(f"ERROR: Schema validation failed at {path_str}: {e.message}",
                  file=sys.stderr)
            return 1
    except ImportError:
        # Manual fallback
        required_top = stage_schema.get("required", [])
        missing_top = [f for f in required_top if f not in data]
        if missing_top:
            print(f"ERROR: Missing required top-level fields: {', '.join(missing_top)}",
                  file=sys.stderr)
            return 1

        expected_stage = stage_schema["properties"]["stage"]["const"]
        actual_stage = data.get("stage")
        if actual_stage != expected_stage:
            print(f"ERROR: Wrong 'stage' value. Expected '{expected_stage}', got '{actual_stage}'",
                  file=sys.stderr)
            return 1

        scoring = data.get("scoring", {})
        scoring_required = stage_schema["properties"]["scoring"].get("required", [])
        missing_scoring = [f for f in scoring_required if f not in scoring]
        if missing_scoring:
            print(f"ERROR: Missing scoring sub-fields: {', '.join(missing_scoring)}",
                  file=sys.stderr)
            return 1

    # Valid — echo parsed JSON for downstream piping
    print(json.dumps(data, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
