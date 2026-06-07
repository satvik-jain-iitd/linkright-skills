"""
init_memory.py — Initialize ~/.linkright/memory/ structure on first onboard.
Usage: python3 init_memory.py ~/.linkright/memory
"""
import sys
from pathlib import Path
from datetime import datetime

def main():
    memory_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / ".linkright" / "memory"

    for d in ["evidence", "interpretations", "expressions/bullets", "expressions/stories", "vectors"]:
        (memory_dir / d).mkdir(parents=True, exist_ok=True)

    facts_path = memory_dir / "facts.md"
    if not facts_path.exists():
        facts_path.write_text(f"""# LinkRight Memory — Facts
# Schema: each fact is a YAML block between --- markers
# DO NOT edit manually without /linkright-mem edit
# Created: {datetime.now().isoformat()}

""")

    signals_path = memory_dir / "signals.md"
    if not signals_path.exists():
        signals_path.write_text(f"""# LinkRight Memory — Signals
# Schema: each signal is a YAML block between --- markers
# DO NOT edit manually without /linkright-mem edit
# Created: {datetime.now().isoformat()}

""")

    outcomes_path = memory_dir / "outcomes.json"
    if not outcomes_path.exists():
        import json
        outcomes_path.write_text(json.dumps({
            "outcomes": [],
            "model_version": "1.0",
            "last_updated": datetime.now().isoformat(),
            "total_outcomes_recorded": 0,
            "model_confidence": "none"
        }, indent=2))

    print(f"Memory initialized at {memory_dir}")
    print(f"  facts.md     : {facts_path}")
    print(f"  signals.md   : {signals_path}")
    print(f"  outcomes.json: {outcomes_path}")

if __name__ == "__main__":
    main()
