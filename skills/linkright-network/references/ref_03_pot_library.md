# ref_03 — POT Library (Points of View)

## What Is This File

This file stores your standing Points of View — opinions on product, craft, industry, and work.
These are the raw material for LinkedIn posts, cold email hooks, and interview "what do you think about X?" moments.

POTs are personal. They must be YOUR actual views — not AI-generated takes.
Add a new entry whenever you notice yourself thinking something distinctive about a product, trend, or problem.

---

## POT Entry Format

```
---
id: pot_NNN
date: YYYY-MM-DD
domain: [product / growth / leadership / industry / craft / ai / ux / data]
headline: [1-sentence strong opinion — this should be arguable]
evidence: |
  [Why you believe this. Can be personal experience, data you've seen, pattern noticed.]
post_uses: [list of post IDs where this POT was used — populated over time]
---
```

---

## Sample Structure (Empty — User Populates)

```
---
id: pot_001
date: 
domain: 
headline: 
evidence: |
  
post_uses: []
---
```

```
---
id: pot_002
date: 
domain: 
headline: 
evidence: |
  
post_uses: []
---
```

---

## POT Quality Rules

1. **Arguable** — "Good products need good design" is not a POT. "Most PMs waste their design team by involving them too late" is a POT.
2. **Specific** — "AI is changing everything" is not a POT. "Most B2B AI products are failing because they automate tasks users didn't want to do in the first place" is a POT.
3. **Grounded** — Must have personal evidence or a concrete example behind it.
4. **Not a trend report** — You have a view on the trend, not just the trend itself.

---

## Domain Tags

| Tag | Examples |
|---|---|
| `product` | Product decisions, tradeoffs, roadmap philosophy |
| `growth` | Acquisition, retention, activation tactics and failures |
| `leadership` | How teams work, how PMs lead, hiring, culture |
| `industry` | Specific vertical insights (fintech, health, SaaS, etc.) |
| `craft` | How to write specs, run discovery, structure roadmaps |
| `ai` | AI products, LLMs, automation, AI PM challenges |
| `ux` | Design decisions, UX patterns, accessibility |
| `data` | Analytics, metrics, data culture |

---

## Using POTs in Posts

When writing a post (via linkright-network):
1. Pick a POT from this library
2. Run it through ref_02_post_templates.md — choose hook format
3. Use voice_scorer.py to check authenticity before posting
4. After posting, update `post_uses` field with the post ID

This prevents recycling the same POT too often and builds a body of work over time.
