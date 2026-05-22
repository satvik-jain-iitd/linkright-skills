# LinkRight Integration — Read/Write Contracts

V1 integration scope: Read profile, write interview history, optionally append story bank. V1.1+ adds closed-loop signal_weights update.

---

## File Path Conventions

| Purpose | Path | Read/Write |
|---|---|---|
| Profile metadata | `~/.linkright/profile/metadata.yaml` | Read |
| Profile nuggets | `~/.linkright/profile/nuggets.jsonl` | Read |
| Profile highlights | `~/.linkright/profile/highlights.jsonl` | Read |
| Profile embeddings | `~/.linkright/profile/embeddings.npz` | Optional read |
| Signal weights matrix | `~/.linkright/profile/signal_weights.yaml` OR `context/cli/linkright/src/linkright/resume/data/signal_weights.yaml` | Read |
| Interview history | `~/.linkright/interview-history/<ts>.json` | Write (append-only) |
| Latest history pointer | `~/.linkright/interview-history/latest.json` | Write (symlink) |
| Story bank entry | `~/.linkright/story-bank/<theme>-<ts>.md` | Write (opt-in only) |
| Sage voice config | `~/.linkright/sage-voice.yaml` | Read |

If `~/.linkright/` doesn't exist, fallback to `~/.claude/interview-history/` and `~/.claude/story-bank/`.

---

## Profile Read Contract

### metadata.yaml (expected fields)
```yaml
career_level: mid           # one of: fresher, early_career, mid, senior, executive
career_years: 5             # integer
last_role: "Senior PM"
last_company: "Razorpay"
target_role: "Senior PM"
target_companies: ["Meta", "Google", "Stripe"]
domain_arc: "data-analyst→PM"   # optional; for bridge-narrative inference
embedder_tier: "fastembed"  # which embedder was used
profile_created: "2026-03-15"
```

### nuggets.jsonl (one per line)
```json
{"id": "n_001", "text": "Led migration from monolith to microservices", "signals": ["leadership", "build-execution"], "magnitude": 4, "context": "Razorpay 2024"}
{"id": "n_002", "text": "Reduced p99 latency from 800ms to 120ms", "signals": ["data-driven", "build-execution"], "magnitude": 5, "context": "Razorpay 2024 Q3"}
```

### highlights.jsonl (one per line)
```json
{"id": "h_001", "bullet": "Led X by Y, achieving Z", "metric": "30% reduction", "scale": "team of 8", "year": "2024"}
```

### Output: candidate-summary.json (Sage's internal use)
```json
{
  "schema_version": "1.0",
  "career_level": "mid",
  "career_years": 5,
  "transition_phase": null,    // inferred if domain_arc present
  "domain_arc": "data-analyst→PM",
  "top_3_signals": ["data-driven", "user-empathy", "build-execution"],
  "absent_signals": ["revenue-impact-scale", "executive-influence"],
  "story_inventory": [
    {"theme": "leadership", "summary": "...", "source_nugget_id": "n_001"}
  ],
  "personalized_ceilings": {
    "product_sense": 4.2, "execution": 4.5, "strategy": 3.8,
    "analytical": 4.5, "leadership": 4.0, "ai_judgment": 3.0
  }
}
```

---

## Profile Fallback (when ~/.linkright/profile/ missing)

### Path A: Resume PDF upload
1. Sage asks user for PDF path
2. Use `markitdown` (preferred) or `pypdf` to extract text
3. Run lightweight signal extraction:
   - Detect career level via year-span + title progression
   - Detect domain arc via title transitions
   - Identify top signals via keyword frequency + magnitude markers
4. Build temporary `candidate-summary.json` (in `/tmp/`, not persisted to `~/.linkright/`)
5. Note: "Profile not persisted — to save, run `linkright profile create -r <pdf>`"

### Path B: 5-Q conversational capture
Sage asks (Romanized Hindi mix):
1. "Total PM career years kitne hain?"
2. "Last 2 companies aur roles kya rahe?"
3. "Strongest domain / area expertise — kya bolega resume highlight reel?"
4. "Sabse weak area — kahan grow karna hai?"
5. "Target role aur companies kya hain is interview ke liye?"

Build temporary `candidate-summary.json` from answers. Note as session-scoped, not persisted.

---

## Interview History Write Contract

### File: `~/.linkright/interview-history/<ts>.json`

Schema:
```json
{
  "schema_version": "1.0",
  "session_id": "<uuid>",
  "timestamp": "2026-05-13T14:32:18Z",
  "candidate_snapshot": {
    "career_level": "mid",
    "transition_phase": null,
    "domain_arc": "data-analyst→PM",
    "top_3_signals": ["data-driven", "user-empathy", "build-execution"]
  },
  "round": {
    "id": 4,
    "name": "Product Sense",
    "problem_type": {"id": "4.3", "name": "Design X for Y"},
    "question": "Design WhatsApp for senior citizens in tier-2 cities",
    "difficulty_bar": "Senior PM (E5/L5)"
  },
  "duration_seconds": 2734,
  "voice_mode": false,
  "scoring": {
    "layer_a_total": "3.4 / 5",
    "layer_b_total": "3.8 / 5",
    "layer_c_total": "3.2 / 5",
    "overall_personalized": "13.4 / 15",
    "verdict": "HIRE"
  },
  "av_coaching_attached": false,
  "gemini_stages_received": [],
  "behavior_log": {
    "yellow_nudges": 2,
    "orange_interrupts": 0,
    "hard_cutoffs": 0,
    "ramble_count": 1
  },
  "playbook_gaps": [
    {"gap": "Constraint Articulation Absent", "severity": "high"},
    {"gap": "Tradeoff Naming Weak", "severity": "medium"},
    {"gap": "Generic User Personas", "severity": "medium"}
  ],
  "drill_recommendations": [...],
  "stories_saved_count": 0
}
```

### File: `~/.linkright/interview-history/latest.json` (symlink)
Always points to most recent. For quick `cat latest.json` query.

### Append-only invariant
- Never overwrite existing history files
- If `<ts>.json` collides (same second), append `-1`, `-2`, etc.

---

## Story Bank Write Contract (opt-in only)

### File: `~/.linkright/story-bank/<theme>-<ts>.md`

Sage prompts at end of interview:
> "Phase 3 answer was strong — your data-analyst-to-PM bridge narrative. Save as story-bank entry? (Yes/No)"

User must explicitly consent per entry.

### Schema:
```markdown
---
theme: leadership-without-authority
created: 2026-05-13
source_session: <uuid>
career_level_at_capture: mid
metrics:
  impact_metric: "30% reduction in onboarding time"
  scale_metric: "team of 8"
linked_resume_bullet_id: "h_001"
linked_nugget_id: "n_001"
applicable_question_types:
  - Behavioral STAR — Leadership without authority
  - Culture Fit — Resume narrative
  - Product Sense — Improve X (when discussing buy-in)
---

## Situation
{{user's narrated situation}}

## Task
{{what they needed to accomplish}}

## Action
{{specific actions they took}}

## Result
{{outcome with metrics}}

## Reflection / Learning
{{what they learned, what they'd do differently}}

## Verbatim Quote (Sage-captured)
> {{exact phrase from interview transcript that earned saving}}

## Why Sage Flagged This for Saving
{{1-2 sentence rationale — e.g., "Specificity density + bridge narrative make this reusable across leadership / influence / cross-functional question types"}}
```

---

## Signal Weights Read Contract

Path resolution (in order):
1. `~/.linkright/profile/signal_weights.yaml` (user override)
2. `context/cli/linkright/src/linkright/resume/data/signal_weights.yaml` (canonical)
3. Sage's embedded fallback (basic mid-level weights)

Apply per `lib/scoring_rubric.md` formula:
```
weighted_score = raw_score × signal_weights[dim][career_level]
```

---

## V1.1+ Integrations (deferred)

### Closed-loop signal_weights update (doc_24)
- Aggregate last N interview sessions
- Compute per-dimension signal deltas
- Suggest `signal_weights.yaml` updates (require user approval per `OQ7`)

### Resume tailoring feedback hook (doc_12)
- Pass interview gaps to next `linkright resume tailor` invocation
- Surface: "You struggled to articulate metric X verbally — confirm exact figure for resume bullet Y?"

### LinkRight CLI exposure (doc_08)
- `linkright interview coach` command wraps the skill
- Same behavior as Claude-invoked skill, just from terminal

### Weekly "wins to document" (doc_26)
- Sage prompts after strong story: "Add to story bank?"
- Roll-up sent to weekly review

---

## Privacy Invariants

1. Sage NEVER auto-uploads any file to third parties
2. A/V files stay LOCAL on user's machine
3. Gemini handoff is user-initiated; Sage only provides paste-ready prompts
4. Story bank writes require EXPLICIT user consent PER entry
5. Profile data is READ-ONLY; Sage cannot modify profile
6. Interview history can be deleted by user at any time (it's plain JSON)
