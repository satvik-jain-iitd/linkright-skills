# ref_03 — Archetype Signal Requirements

## How to Use This File

Each archetype has:
- **Required signals** (weight 1.0) — must have at STRONG or MEDIUM to pass signal bar
- **Differentiating signals** (weight 0.7) — separate top-quartile candidates; aim for STRONG
- **Disqualifying gaps** — signals at LOW or UNKNOWN that will lose you the role

Signal strength mapping: STRONG = 1.0, MEDIUM = 0.6, LOW = 0.2, UNKNOWN = 0.0

---

## Archetype 1 — Growth PM

Target companies: Series A-C consumer/B2B SaaS, marketplace, fintech

**Required signals (weight 1.0):**
- `growth_experimentation`
- `data_fluency`
- `metric_definition`
- `outcome_ownership`

**Differentiating signals (weight 0.7):**
- `go_to_market`
- `discovery_rigor`
- `b2c_experience` or `marketplace_experience`

**Disqualifying gaps:**
- `growth_experimentation` at LOW → cannot claim Growth PM archetype
- `data_fluency` at LOW → will fail technical screen

---

## Archetype 2 — 0→1 / Founding PM

Target companies: pre-seed to Series A, new product lines at larger companies

**Required signals (weight 1.0):**
- `product_vision`
- `ambiguity_tolerance`
- `early_stage_experience`
- `discovery_rigor`

**Differentiating signals (weight 0.7):**
- `systems_thinking`
- `technical_depth`
- `go_to_market`

**Disqualifying gaps:**
- No story demonstrating `shipped_0_to_1` → cannot credibly claim this archetype
- `ambiguity_tolerance` at UNKNOWN → will fail "how do you handle uncertainty" questions

---

## Archetype 3 — Platform / Infrastructure PM

Target companies: developer tools, cloud infra, API-first products, internal platforms

**Required signals (weight 1.0):**
- `technical_depth`
- `platform_experience`
- `stakeholder_management`
- `systems_thinking`

**Differentiating signals (weight 0.7):**
- `metric_definition` (SLA, reliability metrics)
- `data_fluency`
- `go_to_market` (developer GTM)

**Disqualifying gaps:**
- `technical_depth` at LOW → blocked at hiring manager screen
- `platform_experience` at UNKNOWN → need at least one supporting fact

---

## Archetype 4 — Enterprise B2B PM

Target companies: Series B+, mid-market/enterprise SaaS, regulated industries

**Required signals (weight 1.0):**
- `enterprise_experience`
- `stakeholder_management`
- `roadmap_ownership`
- `outcome_ownership`

**Differentiating signals (weight 0.7):**
- `go_to_market` (enterprise GTM, pricing, packaging)
- `regulated_industry`
- `discovery_rigor` (working with enterprise customers)

**Disqualifying gaps:**
- `enterprise_experience` at UNKNOWN with no supporting fact → hard to pass interview
- No story about `managed_exec_stakeholder` → will fail behavioral round

---

## Archetype 5 — Consumer / B2C PM

Target companies: consumer apps, social, fintech consumer, health consumer

**Required signals (weight 1.0):**
- `b2c_experience`
- `user_empathy`
- `growth_experimentation`
- `metric_definition`

**Differentiating signals (weight 0.7):**
- `discovery_rigor`
- `design_collaboration`
- `data_fluency`

**Disqualifying gaps:**
- No concrete `metric_moved` example in consumer context → fails specificity test
- `user_empathy` at LOW → interviewer won't trust product judgment

---

## Archetype 6 — Data / AI PM

Target companies: ML-heavy products, AI applications, analytics tools, data infrastructure

**Required signals (weight 1.0):**
- `data_fluency`
- `technical_depth`
- `metric_definition`
- `systems_thinking`

**Differentiating signals (weight 0.7):**
- `discovery_rigor` (research-grounded AI features)
- `outcome_ownership` (model performance ownership)
- `product_vision` (AI product vision)

**Disqualifying gaps:**
- `technical_depth` at LOW → cannot collaborate meaningfully with ML engineers
- No AI/ML product example → interview will expose immediately

---

## Archetype 7 — Design-Led PM

Target companies: design-maturity companies (Figma, Notion, Linear), consumer apps

**Required signals (weight 1.0):**
- `user_empathy`
- `design_collaboration`
- `discovery_rigor`
- `product_vision`

**Differentiating signals (weight 0.7):**
- `systems_thinking` (design systems, consistency)
- `outcome_ownership`
- `influence_without_authority` (working with strong design culture)

**Disqualifying gaps:**
- `design_collaboration` at LOW → will lose to candidates with design background
- No qualitative research story → fails discovery screen

---

## Archetype 8 — Marketplace PM

Target companies: two-sided marketplaces, gig economy, logistics, commerce

**Required signals (weight 1.0):**
- `marketplace_experience`
- `systems_thinking`
- `growth_experimentation`
- `data_fluency`

**Differentiating signals (weight 0.7):**
- `metric_definition` (liquidity, GMV, take rate)
- `stakeholder_management` (supply + demand side)
- `outcome_ownership`

**Disqualifying gaps:**
- `marketplace_experience` at UNKNOWN with no story → will fail "tell me about a two-sided problem you've solved"
- `systems_thinking` at LOW → cannot reason about supply/demand mechanics

---

## Gap Analysis Protocol

When running gap analysis against a target archetype:

1. Load user signal strengths from memory/signals.md
2. Map against required signals for target archetype
3. For each required signal at LOW or UNKNOWN:
   - Surface exact gap: "growth_experimentation is LOW — no fact supports this"
   - Propose memory update: "Can you tell me about an experiment you ran?"
4. For each disqualifying gap: flag explicitly before running application flow

Gap analysis runs automatically in linkright-mem Gate 4 and linkright-hunt Gate 1.
