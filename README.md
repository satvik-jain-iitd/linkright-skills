# LinkRight

One local-first career OS, installed as a single plugin. Every skill reads and
writes one shared career memory at `~/.linkright`, so your resume, interviews,
content, and outreach all stand on the same confirmed facts about your work.

## Install (marketplace)

```
/plugin marketplace add satvik-jain-iitd/linkright-skills
/plugin install linkright@linkright
```

First run: `/linkright-setup`, then `/linkright-mem` to onboard your resume.

## What's inside

Memory is the foundation: `linkright-mem` owns the shared Evidence, Facts, and
Signals store. Get the job: `linkright-sync` (ATS-safe resume), `linkright-hunt`
(role search), `linkright-push` (publish to GitHub Pages), `linkright-portfolio`
(proof of work). Prep: `linkright-interview` (story bank), `linkright-interview-coach`
(Sage, full mock with scoring). Be seen: the content engine in `engine/` driven by
`content-daily-post`, `content-topic-hunt`, `content-profile-search`,
`content-optimize`, and `content-voice-setup`. Reach out: `linkright-network`
(one-to-one outreach). Run it: `linkright-setup` (first-run wizard),
`linkright-companion` (daily briefing).

All skills point at `~/.linkright`. The `linkright` CLI on PyPI writes the
canonical store; the skills read the derived view and refresh it on use.
