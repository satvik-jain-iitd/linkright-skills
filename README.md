# LinkRight — Your AI Job Search Copilot

LinkRight turns Claude AI into a personal career assistant that remembers your entire work history, finds jobs that match your profile, writes tailored resumes on demand, and coaches you through interviews — all running locally on your computer.

**No subscription. No SaaS. No data sent to third parties. Runs on Claude Code.**

---

## What it does

Think of LinkRight as 9 specialists working together:

| Skill | Plain English |
|---|---|
| `/linkright-setup` | First-time setup wizard. Run this once to get everything working. |
| `/linkright-mem` | Your career memory. Feed it your resume once — it remembers everything forever. |
| `/linkright-hunt` | Job finder. Searches 500+ companies' job boards and scores each job against your profile. |
| `/linkright-sync` | Resume writer. Takes any job description and outputs a tailored, ATS-safe resume in minutes. LaTeX/Overleaf by default, HTML optional. |
| `/linkright-push` | Publisher. Puts your resume on GitHub Pages with a shareable link. For LaTeX, a GitHub Action auto-compiles your `.tex` to PDF on push. Version-controlled. |
| `/linkright-interview` | Interview coach. Builds your story bank, runs mock interviews with voice, scores you like FAANG. |
| `/linkright-companion` | Daily briefing. Every morning, what to do today, where your applications stand, what to follow up on. |
| `/linkright-network` | Content and outreach. Writes LinkedIn posts and cold emails in your own voice, grounded in your real career facts and voice-scored before you ever see a draft. Never posts without your approval. |
| `/linkright-portfolio` | Proof-of-work builder. Turns your experience into case studies, Proof-of-Thinking write-ups, company research briefs, and a shareable GitHub Pages portfolio site. |

---

## How it works (non-technical)

LinkRight is built using "Agent Skills" — instruction files that tell Claude AI exactly how to behave for a specific task. When you type `/linkright-hunt` in Claude Code, it loads the hunt skill and Claude knows exactly how to search for jobs, score them, and save the results.

Your data stays on your computer in `~/.linkright/`. Nothing is uploaded anywhere unless you explicitly push to GitHub.

```
You type: /linkright-mem
Claude reads: your resume
Claude stores: structured facts + skills in ~/.linkright/memory/
You own everything.
```

---

## Quick Start

### Step 1 — Install Claude Code

Download from [claude.ai/code](https://claude.ai/code). Free with a Claude subscription.

### Step 2 — Install LinkRight

```bash
# Clone this repo into Claude's skills folder
git clone https://github.com/satvik-jain-iitd/linkright-skills ~/.claude/skills/linkright-bundle

# Copy each skill into place
cp -r ~/.claude/skills/linkright-bundle/linkright-* ~/.claude/skills/
cp -r ~/.claude/skills/linkright-bundle/linkright-interview-coach ~/.claude/skills/
```

### Step 3 — Run Setup

Open Claude Code and type:
```
/linkright-setup
```

This runs a guided wizard that:
- Asks you 13 questions (name, title, target roles, salary expectations, etc.)
- Creates your config file at `~/.linkright/user_setup.md`
- Installs Python packages needed for job scraping
- Checks your system tools
- Sets up the job database
- Verifies everything is connected

### Step 4 — Feed it your resume

```
/linkright-mem
```

Paste your resume text when asked. LinkRight extracts facts and skills from it. This is the foundation everything else builds on.

### Step 5 — Find jobs

```
/linkright-hunt
```

Describe what you're looking for in plain language:
> "Find AI startup PM roles in India, last 3 days, remote ok"

It searches, scores, and shows you a ranked list.

---

## Recommended order

```
/linkright-setup     ← do this first, once
/linkright-mem       ← ingest your resume
/linkright-hunt      ← find jobs
/linkright-sync      ← tailor resume for a specific job
/linkright-push      ← publish resume to GitHub Pages
/linkright-interview ← practice for your interview
/linkright-companion ← daily check-in
/linkright-network   ← LinkedIn posts + cold outreach
/linkright-portfolio ← build shareable proof-of-work
```

---

## What you need

| Requirement | How to get it |
|---|---|
| Claude Code | [claude.ai/code](https://claude.ai/code) — Mac, Windows, or web |
| Python 3.10+ | Usually already installed. Check: `python3 --version` |
| Git | `brew install git` (Mac) or [git-scm.com](https://git-scm.com) |
| GitHub CLI (`gh`) | `brew install gh` — needed only for resume publishing |

Optional (for better interview coaching):
- `GEMINI_API_KEY` — enables A/V coaching (video + audio analysis of your mock interview)
- `GROQ_API_KEY` — free LLM fallback for generating improvement playbooks

---

## Works for any role

LinkRight was built to be generic. It supports:

- Product Managers (AI PM, Growth PM, Enterprise PM, Founding PM)
- Software Engineers (Staff, Principal, EM)
- Data Scientists & ML Engineers
- Analytics Leads
- Chief of Staff / Strategic Operators
- Any knowledge worker doing a structured job search

The system adapts to your role via `~/.linkright/user_setup.md` — no hardcoding.

---

## Your data

```
~/.linkright/
├── user_setup.md          ← your config (role, targets, constraints)
├── .env                   ← API keys + salary (private, never committed)
├── memory/
│   ├── facts.md           ← every career fact extracted from your resume
│   ├── signals.md         ← professional strengths derived from facts
│   └── expressions/
│       └── stories/       ← STAR interview stories, ready to use
├── profile/               ← interview coach profile
├── jobs/
│   ├── db/jobs.db         ← job search database
│   └── memory/
│       └── pipeline.json  ← your opportunity tracker
└── interview-history/     ← mock interview transcripts + scorecards
```

Everything in `~/.linkright/` is yours. No sync, no cloud, no account.

---

## Skill architecture

Each skill is a `SKILL.md` file — a plain text instruction document that tells Claude how to behave. No black-box binaries. You can read, edit, and understand every instruction.

```
linkright-mem/
├── SKILL.md           ← instructions Claude follows
└── scripts/
    ├── fact_extractor.py
    ├── signal_deriver.py
    ├── grep_memory.py
    └── ...
```

Skills communicate via shared files in `~/.linkright/`. Each skill reads what the previous one wrote.

```
linkright-mem writes → facts.md + signals.md
linkright-hunt reads → user_setup.md, writes → jobs.db + pipeline.json
linkright-sync reads → facts.md + pipeline.json, writes → resume .tex/PDF (HTML optional)
linkright-push reads → resume files, writes → GitHub Pages URL (Action compiles .tex → PDF)
linkright-interview reads → facts.md + pipeline.json
```

---

## Built on Agent Skills standard

This repo follows the [Agent Skills](https://agentskills.io) open standard — skill bundles that work across Claude Code, Gemini CLI, Cursor, and 25+ other AI coding tools.

---

## License

MIT. Fork it, adapt it, build on it.
