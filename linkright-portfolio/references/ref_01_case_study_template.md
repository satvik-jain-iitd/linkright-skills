# ref_01 — Case Study Template

## 7-Section Structure (all sections required)

```
# [Project Title]
[Company] | [Role] | [Timeframe]

---

## 1. CONTEXT
[Company stage, team composition, your specific role, timeframe.
What was the environment you were operating in?]

## 2. PROBLEM
[What was broken, missing, or unclear? What evidence showed this?
Not "we wanted to improve X" — what was actually wrong?]

## 3. CONSTRAINTS
[What you could NOT change: tech debt, org constraints, time, resources, politics.
This section shows PM maturity more than any other.]

## 4. APPROACH
[How you thought about it — frameworks used, hypotheses formed,
what alternatives you considered and why you chose this path.
Show your reasoning, not just your actions.]

## 5. EXECUTION
[What you actually did — who you worked with, what decisions you made,
how you kept things moving, what got hard and how you navigated it.
Specific > generic.]

## 6. OUTCOME
[Quantified results wherever possible.
If estimating: label it ("user-reported", "internal estimate").
Be clear about your direct contribution vs team contribution.]

## 7. WHAT I LEARNED
[One honest, specific learning. Not a PR statement.
"I learned that I underweighted engineering complexity when making timeline promises."]
```

---

## Section-by-Section Guidance

### Section 1 — Context

**What to include:**
- Company stage: seed, Series A-B, growth, public, enterprise
- Team: how many engineers, designers, data? Who reported to whom?
- Your role: individual contributor, tech lead PM, founding PM?
- Timeframe: when did this happen, how long did it take?

**Weak:**
> I worked at a startup on a mobile app.

**Strong:**
> Series B fintech app (120 employees, 8-person product team). I was the sole PM for the consumer onboarding flow, reporting to VP Product. Project ran Aug–Nov 2023.

---

### Section 2 — Problem

**What to include:**
- What evidence showed there was a problem? (data, user research, tickets, complaints)
- Who felt the pain and how?
- What had already been tried?

**Weak:**
> We wanted to improve our onboarding experience.

**Strong:**
> 60-day retention was 28% against a 45% category benchmark. Exit surveys showed 40% of churned users cited "didn't understand what to do first." Support tickets about first-login confusion were the #1 category at 34% of all tickets.

---

### Section 3 — Constraints

**What to include:**
- Technical: legacy systems, no auth changes, mobile-only, etc.
- Organizational: team frozen until Q3, no design budget, approval from legal
- Time: hard launch deadline
- What you were NOT allowed to do (this shows you navigated real constraints, not a greenfield sandbox)

**Weak:**
> We had limited resources.

**Strong:**
> Engineering was committed to a compliance sprint until mid-September — no backend changes before then. We couldn't change the core auth flow (security freeze). The product design team had one designer split across 3 squads.

---

### Section 4 — Approach

**What to include:**
- How did you diagnose the problem? (sessions, funnel analysis, interviews)
- What alternatives did you consider?
- What framework or reasoning guided your choice?

**Weak:**
> I analyzed the data and decided to redesign the onboarding.

**Strong:**
> I ran 8 user sessions with 30-day-churn cohort. 6 of 8 couldn't articulate what action they were supposed to take on day 1. The existing onboarding had 11 steps — I hypothesized we could cut to 4 without losing activation intent. I considered: (a) skip all onboarding, (b) contextual tooltips, (c) progressive disclosure. Rejected (a) because discovery data showed intent questions had high completion; rejected (b) because they added complexity without direction. Chose (c).

---

### Section 5 — Execution

**What to include:**
- Who was involved (specific roles, not just "the team")
- Key decisions made mid-execution and why
- What got hard and how you handled it
- Timeline / milestones hit or missed

**Weak:**
> I worked with engineering and design to build the new flow.

**Strong:**
> Paired with one designer for 3 weeks of prototyping. Engineering had 2 weeks post-sprint. We hit scope conflict: eng wanted to reuse the existing form components (would have kept 6 of 11 steps). I escalated to VP Engineering — not for override, but to get 2 extra days for a new component. They agreed when I showed the session data. Shipped to 10% of new users on Oct 14.

---

### Section 6 — Outcome

**What to include:**
- Primary metric change (what you were trying to move)
- Secondary effects (good or bad)
- Scope clarity: "in the cohort we measured" vs "across all users"
- Confidence level on estimates

**Weak:**
> Retention improved significantly and stakeholders were happy.

**Strong:**
> 60-day retention improved from 28% to 41% in the test cohort (4-week measurement, n=1,800). Support tickets about first-login dropped 52% month-over-month. Engineering time to onboard new features in this flow: reduced from 3 days to 0.5 days (simpler component structure). Full rollout to 100% in November.

---

### Section 7 — What I Learned

This is the most important section. It must be honest and specific.

**Weak (PR statement):**
> This project taught me the importance of user research and data-driven decision making.

**Still weak (vague):**
> I learned to communicate better with stakeholders.

**Strong (honest, specific):**
> I underestimated how much the existing 11-step flow was being used by CS as a filter for low-intent users — something I didn't discover until we saw support ticket volume shift to different question types post-launch. I would have run a pre-launch audit with the CS team if I were doing this again.

**Strong alternative:**
> I made the scope decision to cut to 4 steps based on session data from churned users. I didn't validate the new flow with retained users — I assumed it would work for them too. It did, but I got lucky. I now always test with both cohorts when redesigning core flows.

---

## Quality Checklist (run before Gate 4)

- [ ] All 7 sections present
- [ ] Context includes: company stage, team size, your role, timeframe
- [ ] Problem has specific evidence (not just "we wanted to improve")
- [ ] Constraints section is substantive (≥2 real constraints)
- [ ] Approach shows alternatives considered and rejected
- [ ] Execution names specific people/roles involved
- [ ] Outcome has at least one quantified metric or honest "we didn't measure"
- [ ] Section 7 is honest, not performative
- [ ] No phrases: "leveraged", "seamlessly", "drove significant impact", "key stakeholders"
- [ ] No claimed outcomes that can't be defended in an interview
