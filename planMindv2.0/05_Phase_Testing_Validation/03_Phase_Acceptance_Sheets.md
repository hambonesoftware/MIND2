# Phase Acceptance Sheets (copy/paste)

Use these as “gates” after each phase.

---

## Gate: Phase 1 — Backend Theory Engine

- [ ] `GET /health` → ok
- [ ] `GET /profiles` returns >= 3 profiles
- [ ] `POST /generate` returns valid `thought.v0` for:
  - `[0 7 12]`
  - `[0 2 4] | dens:0.2`
- [ ] invalid DSL returns structured error
- [ ] unit tests for parser + generator pass

Evidence / Notes:
- build log:
- test log:
- example payloads:

---

## Gate: Phase 2 — Thought Contract

- [ ] JSON Schema file exists for `thought.v0`
- [ ] backend validates responses against schema
- [ ] frontend validates incoming thoughts before scheduling
- [ ] incompatible schema versions produce a visible error

Evidence / Notes:

---

## Gate: Phase 3 — Frontend Node Canvas

- [ ] Thought node plays
- [ ] Text edits swap only at next bar
- [ ] Errors do not kill audio
- [ ] UI displays “pending” while waiting for backend

Evidence / Notes:

---

## Gate: Phase 4 — Fan-In Theory Gate

- [ ] Two nodes routed through gate produce sound
- [ ] At least one clash test demonstrates correction
- [ ] resolution metadata is visible (log or UI)

Evidence / Notes:

---

## Gate: Phase 5 — Testing & Validation

- [ ] backend unit tests green
- [ ] rapid typing test stable
- [ ] manual style test A/B matches expectations

Evidence / Notes:

