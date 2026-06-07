# LinkRight

A local-first career operating system. One Claude Code plugin, fifteen skills, all standing on a single career memory that lives on your own machine.

I built it to run my own job search. It tailors resumes, runs mock interviews, finds and scores roles, writes content and outreach in my voice, and tracks the whole pipeline. Nothing leaves the computer unless I choose to push it.

## The problem I set out to solve

A job search runs across a dozen disconnected tools. Your resume sits in one place, your stories in another, your applications in a spreadsheet, your LinkedIn in a tab. The facts about your own career get retyped into each one and slowly drift apart.

Every AI writing tool adds a second failure on top: it invents your experience. Ask one for a resume bullet and it hands you a metric you never earned.

LinkRight closes both gaps. One memory holds the confirmed facts about your work. Every skill reads from it and writes back to it, so the resume, the interview answers, the content, and the outreach all stand on the same ground.

The model only proposes language. Deterministic code decides what ships, and by construction it cannot introduce a number that is not already in your record.

## Who it's for

Anyone running a serious, structured job search who wants to own their data.

I built it for product managers first, because that is my own move, but the system carries no role assumptions. Your role, targets, and constraints live in your config, not in the code. It works the same for engineers, data scientists, analysts, chiefs of staff, any knowledge worker doing the job search properly.

## How it's built

Three layers, and the order matters.

**Memory is the spine.** Career data is modeled as Evidence, then Facts, then Signals: raw memos and your resume become atomic facts, facts become the professional signals you actually pitch on. The `linkright` CLI on PyPI writes the canonical store; the plugin skills read a derived view of it and refresh that view on use. One brain shared across the terminal and Claude Code, so the two never contradict each other.

**Skills are the surface.** Fifteen of them, each a plain `SKILL.md` instruction file plus its scripts. No black-box binaries; you can read and edit every instruction. They talk to each other only through the shared files in `~/.linkright`, so each skill picks up exactly what the last one wrote.

**Generate-then-verify is the safety model.** Wherever a small model proposes text, a deterministic gate disposes of it. The resume width optimizer is the clearest example: exact math measures the line, rules rewrite first, a local model on my own VPS only steps in for the hard cases, and a metric guard rejects any candidate that adds a number the original did not have. The model widens the language; code owns correctness.

It is local-first on purpose. Your data sits in `~/.linkright`, the cheap inference runs on a small fleet of local models, and the running cost is zero with a single free LLM key. Privacy and cost both fall out of the same decision.

### The fifteen skills

| Skill | What it does |
|---|---|
| `linkright-mem` | The shared career memory. Ingests your resume and diary once, extracts facts and signals, and serves them to everything else. |
| `linkright-sync` | Tailors an ATS-safe resume to a job description. LaTeX by default, HTML optional. |
| `linkright-hunt` | Finds open roles and scores each one against your profile. |
| `linkright-push` | Publishes the resume to GitHub Pages with a shareable link; a GitHub Action compiles the LaTeX to PDF on push. |
| `linkright-portfolio` | Turns your work into case studies and a shareable portfolio site. |
| `linkright-interview` | Builds your story bank and screening seeds. |
| `linkright-interview-coach` | Sage, a full FAANG-grade mock interview with signal scoring and a playbook. Optional voice mode. |
| `content-daily-post` | Writes one on-voice, grounded, gated LinkedIn post with its media asset. |
| `content-topic-hunt` | Finds high-signal recent stories worth posting about. |
| `content-profile-search` | Finds the right people to reach out to. |
| `content-optimize` | Tunes the content system from real performance. |
| `content-voice-setup` | Builds your writing voice once, from a short interview. |
| `linkright-network` | One-to-one outreach: cold emails grounded in your real career facts. |
| `linkright-setup` | First-run wizard for your career config. |
| `linkright-companion` | Daily briefing: what to do today, where your applications stand. |

The `content-*` skills sit on a config-driven content engine that lives in `engine/`. It learns your real writing voice, then plans, drafts, designs, gates, and schedules posts in that voice. Everything specific to you stays in your config, not the engine.

## What this project demonstrates

I am putting it here plainly, since this repo doubles as a work sample.

Product judgment: I started from a real, painful workflow and cut it down to one decision, keep the career facts in one place and make every surface obey them.

Systems design: a shared-memory architecture with a clean split between the canonical store and the derived views skills read, so fifteen independent skills stay consistent without coordinating.

Pragmatic ML: a generate-then-verify pattern with deterministic gates and cost-tiered local inference, so a small, cheap model is safe to use because code, not the model, owns the truth.

Shipping: it is published on PyPI, distributed through a Claude Code marketplace, and I run it on my own search every day.

## Install

LinkRight installs as a single plugin through the marketplace.

```
/plugin marketplace add satvik-jain-iitd/linkright-skills
/plugin install linkright@linkright
```

That is the whole install. The plugin bundles all fifteen skills and the content engine.

<details>
<summary>Manual install without the marketplace</summary>

```bash
git clone https://github.com/satvik-jain-iitd/linkright-skills ~/.claude/skills/linkright-bundle
bash ~/.claude/skills/linkright-bundle/install.sh
```

This copies each skill into `~/.claude/skills/`. Use it if you want the skills on disk rather than managed by the plugin manager.
</details>

### What you need

Claude Code, from [claude.ai/code](https://claude.ai/code). Python 3.10 or newer for the skill scripts. Git, and the GitHub CLI (`gh`) only if you want resume publishing. Two optional keys make the interview coach richer: `GEMINI_API_KEY` for audio and video analysis of a mock, and `GROQ_API_KEY` as a free LLM fallback for the playbook.

## First run

```
/linkright-setup     run once; sets up your career config
/linkright-mem       ingest your resume into the shared memory
```

After that the rest follow your search: `/linkright-hunt` to find roles, `/linkright-sync` to tailor a resume for one, `/linkright-push` to publish it, `/linkright-interview-coach` to practice, `/linkright-companion` for the daily briefing.

Everything you create lives in `~/.linkright`. No account, no sync, no cloud.

## The wider system

LinkRight is one product split across a few repositories.

This repo is the plugin, the surface you install. The career brain underneath it is the CLI at [`linkright_production`](https://github.com/satvik-jain-iitd/linkright_production), published as `linkright` on PyPI. The web platform, a Next.js site with a Python resume pipeline and a Chrome extension, is [`sync-resume-engine`](https://github.com/satvik-jain-iitd/sync-resume-engine), live at [sync.linkright.in](https://sync.linkright.in). The published artifacts have their own homes: [`linkright-resume`](https://github.com/satvik-jain-iitd/linkright-resume) for the versioned resume, [`linkright-portfolio`](https://github.com/satvik-jain-iitd/linkright-portfolio) for the portfolio and pipeline dashboard. The career memory itself stays private.

## License

MIT. Fork it, adapt it, build on it.
