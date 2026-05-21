# LinkRight — AI Career OS

A modular skill bundle that turns Claude Code (or any [Agent Skills](https://agentskills.io)-compatible harness) into an intelligent job search copilot.

## Skills

| Skill | What it does |
|---|---|
| `linkright-mem` | Memory engine — ingests resume/experience into structured facts + signals |
| `linkright-hunt` | Job discovery — scrapes, scores, and surfaces PM-adjacent opportunities |
| `linkright-sync` | Resume & cover letter — pixel-perfect, ATS-safe, tailored to each JD |
| `linkright-interview` | Interview prep — STAR story bank, question bank, TTS mock interviews |
| `linkright-push` | GitHub backbone — versioned resume hosting, Kanban dashboard, memory vault |

## Install

```bash
# Clone to Claude Code skills directory
git clone https://github.com/satvik-jain-iitd/linkright-skills ~/.claude/skills/linkright-skills-bundle

# Or copy individual skills
git clone https://github.com/satvik-jain-iitd/linkright-skills /tmp/linkright-skills
cp -r /tmp/linkright-skills/linkright-mem ~/.claude/skills/
cp -r /tmp/linkright-skills/linkright-hunt ~/.claude/skills/
cp -r /tmp/linkright-skills/linkright-sync ~/.claude/skills/
cp -r /tmp/linkright-skills/linkright-interview ~/.claude/skills/
cp -r /tmp/linkright-skills/linkright-push ~/.claude/skills/
```

Or install to the [Agent Skills](https://agentskills.io) universal directory:
```bash
cp -r /tmp/linkright-skills/linkright-* ~/.agents/skills/
```

## Recommended start order

1. `/linkright-push` → first-time setup (creates GitHub repos)
2. `/linkright-mem` → onboard (ingest your resume → facts + signals)
3. `/linkright-hunt` → discover opportunities
4. `/linkright-sync` → tailor resume/cover letter for a specific JD
5. `/linkright-interview` → prep stories + run mock interviews

## Requirements

- Claude Code (or any Agent Skills-compatible harness)
- Python 3.10+
- `sentence-transformers` (for semantic job scoring): `pip install sentence-transformers`
- `gh` CLI (for linkright-push): `brew install gh`

## Architecture

Each skill is a standalone SKILL.md + scripts/ folder. Skills integrate bidirectionally via:
- `~/.linkright/memory/` — shared facts/signals store
- `~/Downloads/Mission Job Switch/job scraping/db/jobs.db` — job database
- `~/Downloads/Mission Job Switch/job scraping/memory/pipeline.json` — opportunity pipeline

---

Built with [Agent Skills](https://agentskills.io) standard — works on Claude Code, Pi, Gemini CLI, Cursor, and 25+ other tools.
