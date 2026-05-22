# ref_02 — POT Examples (Proof-of-Thinking)

## What Makes a POT Work

A POT is 400-600 words analyzing ONE specific product decision at a real company.
It must be specific enough that the hiring PM at that company recognizes exactly what you're talking about.

The 5 sections:
1. **OBSERVATION** — what you noticed (specific, real, verifiable)
2. **HYPOTHESIS** — why you think they made this decision
3. **TRADE-OFF** — what they optimized for vs what they gave up
4. **YOUR TAKE** — what you'd explore if you were the PM
5. **SIGNAL** (optional) — what this reveals about your thinking

---

## Example 1 — Strong POT

**Company:** Linear
**Topic:** No emoji reactions on issues

---

**OBSERVATION**

Linear doesn't have emoji reactions on issue comments. You can comment, but you can't 👍 or ❤️ a comment. This is a deliberate omission — it's been requested multiple times in their community forum, and they've consistently declined.

**HYPOTHESIS**

I think Linear made this decision to protect signal quality. In tools like Jira or GitHub Issues, emoji reactions often become a proxy for priority or stakeholder sentiment — a 👍 flood becomes a way for non-PMs to "vote" on issues. This creates noise in the triage process and can overweight vocal users. Linear's core bet is that issue management should be PM-driven, not democratized via reactions.

**TRADE-OFF**

They optimized for: clean triage signal, PM authority over prioritization.
They gave up: quick lightweight acknowledgment of comments, community engagement for their public roadmap issues, and a "feel good" interaction pattern that many users expect.

The cost is visible: the community forum has repeated requests for reactions, and some users explicitly say the tool "feels cold."

**YOUR TAKE**

I would explore whether the problem is reactions themselves or reactions-as-priority-signal. A possible middle path: allow reactions only on internal team issues (not public roadmap items), or allow reactions but explicitly exclude them from any sorting, weighting, or filtering logic. The concern about noisy prioritization might be solvable with a design constraint rather than a feature absence.

I'd want to understand: what % of the "coldness" feedback correlates with team size? My hypothesis is that smaller teams (1-5) don't mind the absence; larger teams (15+) miss it for async acknowledgment. That segmentation would change the answer.

**SIGNAL**

I notice deliberate product absences more than feature additions — the things a mature product team chose NOT to build are often more telling than what they built.

---

## Example 2 — Mediocre POT

**Company:** Notion
**Topic:** Notion AI placement

---

**OBSERVATION**

Notion AI is deeply integrated into the editor — you can access it anywhere with a slash command.

**HYPOTHESIS**

They probably wanted to make AI feel native to the tool, not like a separate product.

**TRADE-OFF**

More native experience vs potentially overwhelming users with too many options.

**YOUR TAKE**

I think they could improve the onboarding for AI to make it clearer what it's useful for. Maybe show examples inline.

---

**What's wrong with Example 2:**

- Observation is generic (everyone who uses Notion notices AI is in the editor)
- Hypothesis is obvious ("wanted it to feel native")
- Trade-off is vague ("too many options")
- Your Take is a cliché ("improve onboarding", "show examples")
- Nothing here demonstrates PM thinking — it's a product summary, not an analysis
- A recruiter reading this learns nothing about how you think

---

## Example 3 — Weak POT (shows what NOT to submit)

**Company:** Figma
**Topic:** Figma is a great product

---

**OBSERVATION**

Figma has become the design tool of choice for most product teams. Their auto-layout feature is incredibly powerful and their collaboration features are best in class.

**HYPOTHESIS**

They clearly have a strong product team and understand designer needs deeply.

**TRADE-OFF**

It's hard to think of major trade-offs — they seem to have done most things right.

**YOUR TAKE**

I'd love to work on a product like this. I believe I could contribute to making the collaboration even better.

---

**What's wrong with Example 3:**

- Observation is praise, not analysis
- No specific product decision examined
- "Hard to think of trade-offs" — this means you didn't look hard enough
- "YOUR TAKE" is a cover letter statement, not PM thinking
- "Best in class", "incredibly powerful" — generic superlatives, zero insight
- This POT would immediately disqualify a candidate at a company like Figma

---

## Strong vs Weak Side-by-Side

| Dimension | Strong | Weak |
|---|---|---|
| Observation | "No emoji reactions — verified absent after community request" | "AI is deeply integrated into the editor" |
| Hypothesis | Explains WHY they made this specific call | Restates the obvious |
| Trade-off | Names what was sacrificed concretely | "Might overwhelm users" |
| Your Take | Proposes a testable hypothesis | "Improve the onboarding" |
| Tone | Curious, analytical | Complimentary or vague |
| Specificity | Can't apply to any other product | Could describe any product |

---

## POT Hard Rules (repeated from SKILL.md)

- ALWAYS specific to ONE thing — not "thoughts on Company X's strategy"
- NEVER generic praise of the company
- ALWAYS shows a concrete trade-off or decision point
- NEVER just criticism — curious and constructive, not snarky
- MUST reference something real and verifiable
- REQUIRES actual product usage before writing (15 minutes minimum)
- 400-600 words — not a tweet, not an essay
