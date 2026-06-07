---
name: linkright-interview-coach
description: |
  Sage, LinkRight's FAANG-grade PM mock interview coach. Runs a personalized,
  signal-aware, multi-modal mock interview (HR, Behavioral, Culture, Product
  Sense, Analytical, System Design, Bar Raiser) and produces an actionable
  improvement playbook. Autonomous timer, 3-layer signal scoring (psychological,
  PM craft, executive presence), optional voice mode and A/V coaching. Reads the
  shared career memory, writes interview history, opt-in story bank.

  Use when the user says: /linkright-interview-coach, "mock interview", "Sage",
  "coach me", "practice a PM round", "product sense interview", "bar raiser",
  "grill me", or any request for a full mock interview with scoring.
---

# LinkRight Interview Coach (Sage)

This skill is a multi-file subsystem. The full operating manual is in
[`README.md`](./README.md); the runtime lives in `lib/`, `prompts/`, `scripts/`,
and `state/`.

To run it, follow `README.md` from the top. It reads the user's career memory at
`~/.linkright` (shared with the rest of LinkRight), conducts the chosen round,
scores across the three signal layers, and writes the session plus playbook back
to history. It never invents the user's experience, it grounds every probe in the
real profile.

Start: ask the user which round they want, then drive the session per
`README.md`.
