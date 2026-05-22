---
name: linkright-network
description: |
  LinkedIn content engine + cold email outreach, combined. LinkedIn mode: creates
  Proof-of-Thinking (POT) posts, PM insight posts, content calendars — voice-scored
  (0-10 rubric, must pass ≥7 before delivery), constraint-checked against user_setup.md,
  optional LinkedIn API scheduling. Outreach mode: cold emails to hiring managers and PMs
  at target companies — research-backed opening, specific ask, no generic phrases.
  Reads signals from linkright-mem to pick the right competencies to demonstrate.
  Never posts or sends anything without explicit user approval.

  Use when user says: /linkright-network, "LinkedIn post", "write a post", "content calendar",
  "cold email", "reach out to hiring manager", "outreach email", "POT post", "networking email",
  "brand audit my posts", "voice check", "schedule LinkedIn post", or any content/networking ask.
---

# LinkRight Network

SKILL_DIR   = `~/.claude/skills/linkright-network`
SETUP       = `~/.linkright/user_setup.md`
MEM_DIR     = `~/.linkright/memory`
VOICE_REF   = `~/.claude/skills/linkright-network/references/ref_01_voice_profile.md`
POST_REF    = `~/.claude/skills/linkright-network/references/ref_02_post_templates.md`
EMAIL_REF   = `~/.claude/skills/linkright-network/references/ref_05_cold_email_templates.md`

---

## Absolute Rules

- NEVER post or send anything without explicit user "yes, post it" approval
- NEVER use LinkedIn API for reading, scraping, or connection automation — posting only
- NEVER open a post with a forbidden phrase (see Voice Profile)
- NEVER end a post with "Agree?" / "What do you think?" / "Drop thoughts below"
- NEVER write generic trend commentary without specific real-product anchor
- ALWAYS run voice score before showing user any draft
- ALWAYS run constraint check (user_setup.md) before delivery
- ALWAYS load profile signals from linkright-mem before generating content
- NEVER fabricate quotes, stats, or claims about specific companies
- ALWAYS use agent-browser for product research, not training memory

---

## Gate 0 — Load Profile Signals

Before any content generation, pull signals to know what competencies to demonstrate:

```bash
python3 ~/.claude/skills/linkright-mem/scripts/grep_memory.py \
  --query "strength:high" \
  --memory ~/.linkright/memory \
  --format json
```

If mem empty → proceed with user-provided context.

---

## Gate 1 — Mode Selection

```
AskUserQuestion:
  question: "What do you need?"
  options:
    A) LinkedIn post — write one specific post
    B) Content calendar — 4-week plan with drafts
    C) Cold outreach email — to a hiring manager or PM
    D) Voice check — score a draft I've written
    E) Brand audit — review recent posting patterns
    F) Schedule post — LinkedIn API (requires setup)
```

---

## LINKEDIN POST PATH (modes A, B)

---

## Post Gate 1 — Post Type + Topic

For single post (A):
```
AskUserQuestion:
  question: "What type of post?"
  options:
    POT (Proof-of-Thinking) — analyze a real company's product decision
    PM Insight — share a specific framework, pattern, or lesson
    Process Transparency — show how you think about a PM problem type
    Short Take — 1-3 sentence opinion on a real industry event/decision
    Career Milestone — genuine achievement (max 1×/quarter)
```

Ask: "What topic, company, or signal should this post feature?"

For calendar (B): Ask for goals + target companies + signals to emphasize this month.

---

## Post Gate 2 — Research (POT posts only)

**Mandatory: research the product before writing.**

Use agent-browser to:
1. Navigate to the target company's product or specific feature
2. Observe actual UX, flows, copy, onboarding steps
3. Note specific details: exact copy, design choices, what's missing

Never write a POT post from memory or hearsay. Every observation must be verifiable.

---

## Post Gate 3 — Draft

Write draft per post type template (see `references/ref_02_post_templates.md`).

**Voice Rules (apply to every draft):**

1. **Opinion first** — state view in sentence 1. Never open with a question or fact.
2. **Specific over generic** — name the company, product, or decision
3. **Surface the tension** — two things pulling against each other
4. **No performance** — no "humbled", "inspired", "excited to share" unless literal
5. **Could only be written by one person** — not interchangeable with any other PM

**Forbidden openings:**
- "Excited to share" / "Humbled to announce" / "I am proud to"
- "Hot take:" / "Unpopular opinion:"
- "Lessons from X years in Y"
- "AI is changing everything"
- "The future of [X] is..."

**Forbidden closings:**
- "Agree?" / "What do you think?" / "Drop your thoughts below"
- "Let me know your thoughts" / "Share your experience below"

---

## Post Gate 4 — Voice Score

```bash
python3 ~/.claude/skills/linkright-network/scripts/voice_scorer.py '<post_text>'
```

**Rubric (0-2 per criterion = 10 max):**

| # | Criterion | 0 | 1 | 2 |
|---|---|---|---|---|
| 1 | Opens with opinion (not question/fact/announcement) | question or generic opener | weak opinion | strong opinion, specific |
| 2 | References something specific (real company/product/decision) | nothing specific | vague reference | named real product/decision |
| 3 | Avoids all forbidden phrases | has forbidden phrase | 1 borderline | clean |
| 4 | Clear position — doesn't hedge everything | all hedged | partial | clear, defensible stance |
| 5 | Unique voice — couldn't be swapped into anyone else's feed | fully generic | distinctive | unmistakably specific voice |

**Threshold: 7/10.** Below 7 → rewrite internally, show user improved version with what changed.

---

## Post Gate 5 — Constraint Check

Read SETUP: `topics_to_avoid_in_posts`, `companies_not_to_comment_on`, `do_not_mention`.

Flag any violation. Block delivery until resolved.

---

## Post Gate 6 — Deliver / Schedule

**Manual post:** output as clean copy-ready text. No markdown. No asterisks. Exactly what goes into LinkedIn.

**Schedule (if mode F):**
```bash
# LinkedIn UGC Posts API
# POST https://api.linkedin.com/v2/ugcPosts
# Auth: Bearer <access_token from ~/.linkright/.env>
# Body: see references/ref_04_linkedin_api.md

python3 ~/.claude/skills/linkright-network/scripts/linkedin_post.py \
  --text '<post_text>' \
  --token-file ~/.linkright/.env \
  --dry-run  # show curl first, then confirm before POST
```

NEVER execute the POST without showing the exact API call to user first.

---

## Content Calendar Format (mode B)

Generate 4-week calendar:

```
CONTENT CALENDAR — [Month] [Year]
Goal: [user's stated goal — e.g., "Signal AI PM archetype before Anthropic interview"]
Signals to feature: [from mem or user input]

WEEK 1
  Post 1 (POT): [company] — [specific observation to research]
  Post 2 (PM Insight): [signal] — [specific angle]

WEEK 2
  Post 3 (Short Take): [industry event/announcement — research this]
  Post 4 (Process Transparency): [how you approach X problem]

WEEK 3
  Post 5 (POT): [company 2] — [different signal emphasis]
  Post 6 (PM Insight): [framework/mental model you actually use]

WEEK 4
  Post 7 (Short Take or Milestone): [if milestone exists; else short take]
  Post 8 (PM Insight): [pattern recognition — something you keep seeing]

Frequency: 2 posts/week during active search. 3/week max.
Quality > quantity. One strong POT > five generic insights.
```

Draft posts 1-2 immediately. Offer to draft rest on request.

---

## COLD EMAIL PATH (mode C)

---

## Email Gate 1 — Target Inputs

Ask:
- Name of person
- Company + role (e.g., "Head of Product at Anthropic")
- Why reaching out: HM outreach / referral request / info interview
- What you've observed about their work (or research it)

---

## Email Gate 2 — Research

Use agent-browser to:
1. Find recent posts/articles by this person on LinkedIn
2. Note one specific thing they've written, built, or said
3. Never use generic "I admire your company's mission" — always cite something real

---

## Email Gate 3 — Write Email

Structure (hard rules):
```
SUBJECT: [specific topic] — quick question from a [brief signal]
  e.g. "AI onboarding flows — question from a PM building in this space"
  NOT: "Would love to connect" / "Quick intro"

BODY:

Para 1 (3 sentences max):
  Specific observation about their work/company/product.
  Not praise — observation. Shows you did homework.
  e.g. "I noticed [company]'s [specific feature] takes a different approach than 
  [competitor] — [what you observed about the tradeoff]."

Para 2 (2 sentences):
  Who you are in one sentence + why their specific work is relevant to you.
  e.g. "I'm a PM with [X years] in [domain], currently focused on [specific angle]."

Para 3 (1-2 sentences):
  Specific ask — make it easy to say yes or respond briefly.
  e.g. "Would you have 20 minutes for a call? Or happy to send one question by email
  if that's easier."

NO sign-off filler. Direct.
```

**Forbidden:**
- "I'd love to pick your brain"
- "I'm a big fan of your company / mission / products"
- "I know you're busy, but..." (opens with apology)
- "I'm reaching out because..." (obvious, wastes their time)

---

## Email Gate 4 — Constraint Check + Deliver

Check `do_not_mention` in SETUP. Flag any violation.

Output: clean email text. Subject line separate. No formatting characters.

---

## Voice Check (mode D)

Paste draft. Run voice_scorer.py. Show:
- Score per criterion with reasoning
- Total score
- If <7: specific rewrites for lowest-scoring criteria
- If ≥7: confirm clean, note any optional improvements

---

## Brand Audit (mode E)

Ask user to paste their 5 most recent LinkedIn posts. Analyze:
- Average voice score across posts
- Opener patterns (is first sentence strong?)
- Forbidden phrase frequency
- Signals featured — do they match target archetype?
- Repetitive themes or structures
- Strongest post (why) + weakest post (why)

Output: table + 3 specific recommendations.

---

## Scripts Reference

| Script | Purpose |
|---|---|
| `scripts/voice_scorer.py` | Score post 0-10 on voice rubric |
| `scripts/linkedin_post.py` | LinkedIn UGC API post (dry-run first) |
| `scripts/constraint_check_post.py` | Check post against user_setup.md |

---

## Phase Status

| Feature | Status |
|---|---|
| SKILL.md (orchestrator) | ✅ |
| voice_scorer.py | ✅ |
| Post templates (ref_02) | ✅ |
| Voice profile (ref_01) | ✅ |
| Cold email templates (ref_05) | ✅ |
| linkedin_post.py (API) | ✅ |
| constraint_check_post.py | ✅ |
| LinkedIn OAuth setup (ref_04) | ✅ |
| POT library (ref_03) | ✅ (empty template — user populates) |
