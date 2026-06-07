# Voice Profile — LinkRight Network

## Core Attributes

```
TONE:        direct, considered, occasionally contrarian
STYLE:       opinion-first, not question-first
SPECIFICITY: always names a real product, decision, or tension
LENGTH:      150-300 words standalone; 50-100 for short take
STRUCTURE:   Hook → Tension/Insight → Take → (optional) So what?
```

## Five Voice Rules

**1. Opinion first.** State your view sentence 1. Argument follows.
- Bad: "Here's an interesting question about product prioritization…"
- Good: "Most product roadmaps fail at the same step — not planning, but saying no."

**2. Specific over generic.** Name the company, product, or decision.
- Bad: "Many SaaS companies struggle with onboarding."
- Good: "Notion's onboarding asks too much before showing what's possible."

**3. Surface the tension.** Two things pulling against each other.
- Speed vs quality / user demand vs business model / simplicity vs flexibility

**4. No performance.** Don't perform emotions.
- If you weren't humbled, don't write "humbled." Readers detect performed emotions.

**5. Consistent.** If an opener could swap into any other post without feeling off → both are too generic.

---

## Grounded Voice, read the user's profile first

Before drafting or scoring, load the user's grounded voice profile, the one built from their interview plus a stylometry pass, from their instance, for example `~/.linkright/memory` or the user's voice profile file. That profile supplies the specifics, the signature phrases, the sentence rhythm range, the hook signature, and the user's own banned words with their swaps. The rules here are the generic structure, the user's profile makes it personal. If no grounded profile exists yet, use the generic rules and offer to build one.

## Structural Voice Signals, apply on top of the Five Rules

These are the measured, hard to fake signals. They are generic mechanics, the user's profile fills in the specifics.

**6. Open on a hard fact or an uncomfortable truth.** No wind up, lead with the thing that stops the scroll.

**7. Use at least one contrast pair, X not Y.** For example, experience not tenure, fear not confidence. This is the most reliable voice move.

**8. Build long, then close on a short principle.** A longer build, then a clipped one line principle to end, not a sell.

**9. Keep the rhythm bursty.** A short line next to a long one, never uniform length. This sentence length variation is the human, anti machine, signal.

**10. Carry the user's hook signature.** If the profile defines one, the last line of the hook ends on it exactly.

**11. Map the user's banned words to their swaps.** From the profile, for example leverage to edge, ensure to made sure. The user's raw speech may use these, the written post does not.

**12. No hedging.** No maybe, arguably, or might. Own the call.

---

## Forbidden Openings (auto-fail voice score)

- "Excited to share" / "Humbled to announce" / "I am proud to" / "Thrilled to"
- "Hot take:" / "Unpopular opinion:"
- "Lessons from X years in Y" / "X things I learned from Y"
- "AI is changing everything" / "The future of [X] is..."
- "As a PM," / "As a product manager,"

## Forbidden Closings (auto-fail voice score)

- "Agree?" / "What do you think?" / "Drop your thoughts below"
- "Let me know your thoughts" / "Share your experience below"
- "Curious to hear what you think" / "Thoughts?"

---

## Voice Score Rubric (0-2 per criterion = 10 max, need ≥7 to pass)

| # | Criterion | 0 | 1 | 2 |
|---|---|---|---|---|
| 1 | Opens with opinion | Question or forbidden opener | Weak/hedged opinion | Strong, specific opinion |
| 2 | Specific anchor | No real product/company | Vague reference | Named real product/decision |
| 3 | No forbidden phrases | Has forbidden phrase | 1 borderline | Completely clean |
| 4 | Clear position | Everything hedged | Partially clear | Clear, defensible stance |
| 5 | Unique voice | Fully generic/interchangeable | Distinctive but generic | Unmistakably personal |

---

## Weak vs Strong Examples

**POT post — WEAK:**
> Many companies are struggling with AI product design decisions. The user experience of AI tools is often confusing and users don't always trust the outputs. This is something product teams should think about carefully. What's your experience with AI trust issues?

Problems: no specific company, opens with generic observation, ends with question, not a single opinion.

**POT post — STRONG:**
> Anthropic made an unusual choice with Claude's onboarding — it doesn't start with a demo. Most AI products lead with the flashiest capability. Claude leads with what you can't do.
>
> The bet: if users first understand constraints, they build more realistic mental models and have better conversations. The tradeoff: you lose the "wow" moment that drives early word-of-mouth.
>
> I'd explore a middle path — show one clear capability, then immediately show where it breaks. Sets expectations and demonstrates honesty in the same move. For a safety-focused company, that's the right brand signal.

Passes: opinion-first, specific company, surfaces tension, clear take, distinctive voice.

---

**PM Insight — WEAK:**
> Great product managers know how to communicate with stakeholders. It's important to be clear, concise, and empathetic. Building relationships takes time but pays off in the long run. Lessons learned from 3 years of PM work.

Problems: generic advice, forbidden opener pattern, no specific anchor, nothing defensible.

**PM Insight — STRONG:**
> Most alignment failures aren't about disagreement. They're about different definitions of done.
>
> Engineering thinks "done" means shipped. Design thinks "done" means polished. Ops thinks "done" means documented. Leadership thinks "done" means adopted.
>
> I've stopped starting sprint planning without first writing one sentence: "This is done when [specific observable outcome]." Takes 2 minutes. Saves 2 weeks of re-alignment.

Passes: strong opener, surfaces tension, specific and actionable, could only be written by someone who's experienced this.
