# ref_03 — Bullet Quality Standards

## AI-Smell Phrases — Banned List

Do NOT use these in any resume bullet. Flag immediately if found.

### Generic Superlatives (no evidence)
- exceptional, excellent, outstanding, world-class, best-in-class

### AI Filler
- seamlessly, holistically, robust, scalable solution, impactful, pivotal
- a wide range of, vast array of, end-to-end

### Corporate Jargon
- leverage/leveraged, utilize/utilized, facilitate/facilitated
- synergy, synergize, paradigm shift, thought leader

### Vague Ownership
- responsible for, assisted with, helped to, worked with/on, contributed to
- played a key/pivotal/critical role, ensured, supported

### Unquantified Claims
- significantly improved, dramatically reduced, drove significant impact
- major improvements, notable results, substantial increase

### Clichés
- passionate about, results-driven, team player, self-starter, go-getter
- hard-working, detail-oriented, strong work ethic, proactive
- in a fast-paced environment, cross-functional teams (without specifics)

### Cover Letter Leakage (never in resume bullets)
- I am excited to, I believe I would be, in today's fast-paced world
- I am passionate about, my background in

---

## Strong Action Verbs — By Signal Type

### Product Strategy / Vision
- Defined, Designed, Architected, Established, Conceived, Pioneered, Reframed

### Execution / Delivery
- Shipped, Launched, Built, Delivered, Deployed, Released, Completed

### Leadership / Influence
- Led, Drove, Directed, Championed, Aligned, Rallied, Secured buy-in from

### Data / Analysis
- Analyzed, Diagnosed, Modeled, Measured, Audited, Benchmarked, Instrumented

### Growth / Improvement
- Grew, Increased, Reduced, Accelerated, Improved, Optimized, Cut

### Process / Systems
- Implemented, Streamlined, Automated, Standardized, Scaled, Restructured

### Stakeholder / Communication
- Presented, Negotiated, Influenced, Partnered, Coordinated

### Research / Discovery
- Researched, Interviewed, Synthesized, Mapped, Identified, Validated

---

## X-Y-Z Format — Strong vs Weak

The standard: **[Action verb] [what] [quantified impact]**

### Weak → Strong Examples

| Weak | Strong |
|---|---|
| Responsible for growth initiatives | Grew MAU 34% in 2 quarters by redesigning onboarding |
| Worked on roadmap planning | Defined Q2–Q3 roadmap for 5-engineer team, shipping 3 of 4 milestones on time |
| Helped improve user retention | Increased 30-day retention from 41% to 58% via cohort-specific activation emails |
| Leveraged data to drive decisions | Instrumented 12 funnel steps; identified checkout drop as top cause (67% of exits) |
| Facilitated cross-functional alignment | Aligned 4 teams (Eng, Design, Marketing, CS) on revised launch scope in 48-hour sprint |
| Assisted with stakeholder management | Presented monthly roadmap reviews to 3 C-suite stakeholders; secured budget for Q3 expansion |

### Rules

1. **Action verb first** — never start with "I" or "Was"
2. **No orphan words** — bullet must not end with a lone preposition or article on a new line
3. **Metric if possible** — %, $, count, time delta, scope size
4. **If no metric available** — use scope or specificity: "4-engineer team", "3 stakeholders", "across 2 product lines"
5. **One idea per bullet** — never compound with "and also"

---

## Orphan Word Prevention

An orphan = a single word or very short fragment on the last line of a wrapped bullet.

Mitigation options (in order of preference):
1. Rephrase to eliminate the word
2. Replace a long phrase with a shorter synonym (see suggest_synonyms.py)
3. Add 1-2 words to the previous clause to push text to same line
4. Shorten the clause containing the orphan

Never: add filler words just to fix an orphan — rewrite the bullet.

---

## Width Budget

Max line width: **158.07mm** (A4 single-column body, Roboto 10px)

- `ok`: 85%–100% of budget
- `short`: <85% — consider expanding if bullet is incomplete
- `long`: >100% — wrap occurs, check for orphan

Run measure_width.py on every bullet before finalizing.
