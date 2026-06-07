# ref_03 — Rejection & Ghosting Analysis Framework

## Rejection Types

| Type | Definition | Likely stage |
|---|---|---|
| `ghosted_applied` | Applied, no response in 21d+ | Pre-screen |
| `ghosted_screening` | Scheduled screen, never followed up | Pre-screen |
| `early_reject` | Rejection within 0-7d of application | Pre-screen / ATS |
| `post_screen_reject` | Phone screen completed, then rejected | Recruiter |
| `post_interview_reject` | Interview(s) completed, then rejected | Hiring team |
| `offer_rescinded` | Offer made, then withdrawn | Post-offer |

---

## Analysis Protocol

### Step 1 — Map signals

Pull user archetype signals from user_setup.md.
Pull JD signals that were flagged at application time (from pipeline.json `jd_signals` field if present).

Compare: which JD signals are at LOW or UNKNOWN strength in user profile?

### Step 2 — Assign probable cause

| Scenario | Probable cause label |
|---|---|
| JD primary signal at LOW strength | `fit_gap_signal:[signal_name]` |
| ATS-hostile resume formatting | `ats_parse_failure` |
| Applied in first 48h vs ghosted | `high_competition_early_apply` |
| No tailoring, generic resume sent | `undifferentiated_application` |
| Role closed before reviewed | `timing_unlucky` |
| Interview round, then reject | `performance_interview` or `fit_gap_culture` |
| All signals strong, still rejected | `confounder_likely` |

### Step 3 — List confounders (ALWAYS include)

Never omit confounders. These are causes beyond control:

- Internal candidate was already preferred before posting went live
- Hiring freeze or headcount reallocation
- Another candidate had a warmer referral
- ATS keyword filter mismatch (even with strong profile)
- Role requirements changed after posting
- Interviewer personal bias (not detectable, not actionable)
- Team size / composition fit (not stated in JD)
- Timeline: candidate was available later than hiring team needed

Rule: if the analysis has no confounders, add the full list — rejection is never fully explained by fit alone.

---

## PM-Specific Rejection Patterns

| Rejection pattern (seen 3+ times) | Likely root cause | Action |
|---|---|---|
| Pass at application, fail at recruiter screen | Resume signals don't match phone answers | Align resume bullets to what you'd actually say |
| Pass recruiter, fail at hiring manager | Can't articulate product vision or user research rigor | Practice PM-level structured answers |
| Pass interviews, fail at take-home | Cases feel generic or lack data | Add company-specific framing, use real numbers |
| Multiple ghostings, strong profile | Resume not passing ATS | Run ats_scanner.py on resume |
| Interviews at X-level roles, offers only at X-1 | Seniority signals not clear in materials | Strengthen leadership + ambiguity signals |

---

## Pattern Check Rules

Track rejection count by stage. Surface pattern when N ≥ 3 at same stage.

```
Pattern check: [N] rejections at [stage] in last [period].
[If N≥3]: Pattern detected. [Probable systemic cause].
Recommendation: [1 specific action — never a list]
```

---

## Output Format

```
OUTCOME ANALYSIS — [Company] — [Role]
Date: [YYYY-MM-DD]
Type: [rejection type from table above]
Stage: [where it ended]

PROBABLE CAUSE:
  [Primary cause label + explanation]
  [Secondary cause if applicable]

CONFOUNDERS (factors outside your control):
  - [confounder 1]
  - [confounder 2]
  - [confounder 3]
  [always at least 3]

PATTERN CHECK:
  [N] outcomes recorded at similar stage.
  [Pattern note if N≥3, else "No pattern yet."]

MEMORY UPDATE:
  Record this outcome to update shortlist model? (y/n)
  → Routes to linkright-hunt pipeline tracking.

ACTION ITEM:
  [0 or 1 specific action — never a list. "None required" is valid.]
```

---

## Tone Rules

- Analytical only. Never say "unfortunately" or "I'm sorry to hear".
- Never frame rejection as a verdict on worth or ability.
- Never speculate about interviewer intent beyond what evidence supports.
- Always keep confounders visible — they legitimize uncertainty.
