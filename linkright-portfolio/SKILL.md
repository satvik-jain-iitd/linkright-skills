---
name: linkright-portfolio
description: |
  Build externally-shareable PM proof-of-work. Converts raw experience into structured
  case studies, Proof-of-Thinking (POT) write-ups, company research briefs, and a
  GitHub Pages portfolio site.

  Philosophy: Show your thinking, not just your history. Any PM can list what they did.
  A strong portfolio demonstrates HOW you think — problems seen, trade-offs navigated,
  what you'd do differently.

  Use when user says: /linkright-portfolio, "write a case study", "portfolio site",
  "proof of thinking for [company]", "company research", "extract my metrics",
  or "build my portfolio".
---

# LinkRight Portfolio

SKILL_DIR   = `~/.claude/skills/linkright-portfolio`
SETUP       = `~/.linkright/user_setup.md`
MEM_DIR     = `~/.linkright/memory`
CASES_DIR   = `~/.linkright/portfolio/cases`
PORTFOLIO   = `~/.linkright/portfolio`

---

## Absolute Rules

- ALWAYS include Section 7 (What I Learned) in every case study — non-negotiable
- ALWAYS label estimated metrics — never present estimates as hard numbers
- NEVER write a generic POT — must reference a specific, real product decision
- ALWAYS run constraint validation before any case study is published
- NEVER publish work that violates user_setup.md hard_constraints
- NEVER claim team outcomes as personal outcomes without clear scope framing
- ALWAYS source case study facts from linkright-mem, not from invention

---

## Gate 0 — Load State

```bash
# Check existing portfolio artifacts
ls ~/.linkright/portfolio/cases/ 2>/dev/null || echo "no case studies yet"
ls ~/.linkright/portfolio/ 2>/dev/null || echo "portfolio not initialized"

# Load memory for metrics extraction
python3 ~/.claude/skills/linkright-mem/scripts/grep_memory.py \
  --memory ~/.linkright/memory 2>/dev/null | head -30
```

---

## Gate 1 — Mode Selection

```
AskUserQuestion:
  question: "What do you want to create?"
  options:
    A) Case study — for a specific project
    B) Proof-of-thinking (POT) — for a target company
    C) Full portfolio site — index + all case study pages
    D) Extract and organize metrics from memory
    E) Company research brief
```

---

## Gate 2 — Content Gathering

### Mode A — Case Study

Load relevant facts from memory:
```bash
# Find facts related to the project
python3 ~/.claude/skills/linkright-mem/scripts/grep_memory.py \
  --memory ~/.linkright/memory \
  --query '<project name or company>'
```

Ask user to fill any gaps:
- Context: team size, company stage, timeframe
- Problem: what evidence showed the problem
- Constraints: what couldn't change
- Key decisions made
- Outcome metrics (exact numbers or honest estimates)
- What they learned

### Mode B — POT

Ask user:
1. Which company?
2. Have you used the product in the last 2 weeks? (required)
3. What specific thing did you notice — a feature, UX decision, missing capability, pricing choice?

Do NOT proceed with a generic topic. The observation must be specific.

### Mode C — Portfolio Site

Load all case studies from `~/.linkright/portfolio/cases/`.
Select top 3 for homepage: strongest outcomes + best archetype match + most differentiated.

### Mode D — Metrics Extraction

```bash
# Extract all quantified facts from memory
python3 ~/.claude/skills/linkright-mem/scripts/grep_memory.py \
  --memory ~/.linkright/memory \
  --query 'percent OR reduced OR increased OR improved OR from OR to'
```

Build `metrics_inventory.md` with: metric, context, confidence, fact_id.

### Mode E — Research Brief

Ask user: target company name.
Research using available tools. Structure per ref_04_research_prompts.md.

---

## Gate 3 — Draft Generation

Write full draft per mode:

**Case study:** Follow 7-section structure from ref_01_case_study_template.md exactly.
Section 7 (What I Learned) is required — push back if user says "skip it".

**POT:** Follow 5-section structure. OBSERVATION must be specific + verifiable.

**Portfolio HTML:** Use template from ref_03_portfolio_html_template.md.
Generate: index.html + case study page(s).

**Research brief:** Use structure from ref_04_research_prompts.md.

---

## Gate 4 — Constraint Validation

Before showing final draft, run constraint check:

```bash
python3 ~/.claude/skills/linkright-mem/scripts/constraint_checker.py \
  --text '<full draft text>' \
  --constraints ~/.linkright/user_setup.md
```

If violations found: surface them. Do NOT deliver the draft until resolved.

Block types:
- `do_not_mention` hit — remove the reference
- `hard_constraints` violation — stop and ask user how to proceed
- Claimed metric beyond what memory supports — flag for review

---

## Gate 5 — Review + Finalize

Show draft. Review section by section.

For case studies: specifically highlight Section 7 — ask user: "Is this honest, or is it polished?"
The goal is one specific, real learning — not a PR statement.

For POTs: ask user: "Does the observation reflect something you actually noticed in the product?"

Iterate until user approves.

---

## Gate 6 — Publish

Write final files to `~/.linkright/portfolio/`:

```bash
mkdir -p ~/.linkright/portfolio/cases

# Write case study
cat > ~/.linkright/portfolio/cases/<slug>.html << 'EOF'
[final HTML]
EOF

# Write index if full site
cat > ~/.linkright/portfolio/index.html << 'EOF'
[final HTML]
EOF

echo "Saved. To deploy: /linkright-push → deploy portfolio"
```

If user wants live site: route to linkright-push for GitHub Pages deployment.

---

## References

| File | Purpose |
|---|---|
| `references/ref_01_case_study_template.md` | 7-section template + strong vs weak examples per section |
| `references/ref_02_pot_examples.md` | Annotated POT examples: strong / mediocre / weak |
| `references/ref_03_portfolio_html_template.md` | HTML/CSS template for index + case study pages |
| `references/ref_04_research_prompts.md` | Company research checklist + research brief structure |

---

## Phase Status

| Feature | Status |
|---|---|
| SKILL.md (orchestrator) | ✅ |
| ref_01_case_study_template.md | ✅ |
| ref_02_pot_examples.md | ✅ |
| ref_03_portfolio_html_template.md | ✅ |
| ref_04_research_prompts.md | ✅ |
| Portfolio HTML template | ✅ |
| GitHub Pages integration | ⏳ via linkright-push |
