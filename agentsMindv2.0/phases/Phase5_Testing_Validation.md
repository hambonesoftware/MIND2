# Phase 5 — Testing & Validation

## Goal
Prove robustness:
- backend unit tests cover parser, generator, conflict resolution
- frontend logic tests cover scheduler state transitions
- manual musical tests A/B + rapid typing stability

---

## Step-by-step tasks

### 1) Backend tests
Ensure tests cover:
- profile validation
- DSL parsing error spans
- generator invariants (time sort, midi range, velocity range)
- conflict resolver action trace correctness

### 2) Frontend logic tests (lightweight)
At minimum:
- runtime store prevents double parts
- swap queue keeps only newest pending update
- schema version mismatch rejects scheduling

If no test harness:
- create a small pure-JS test runner script and document how to run it

### 3) Manual tests
Execute plan’s test cases:
- Acoustic Flow
- Percussive Groove
- Rapid typing stability
- Conflict resolution demo

### 4) Final polish
- ensure README run steps are accurate
- ensure logs are understandable
- ensure CORS configured for dev

---

## Acceptance checklist (Phase 5 gate)

- [ ] Backend tests pass (`pytest`)
- [ ] Manual tests A/B sound meaningfully different
- [ ] Rapid typing does not create overlap
- [ ] Conflict resolution demo is reproducible

---

## Evidence to write
Append to: `mind_poc/docs/evidence/phase5_tests.md`
Include:
- test logs
- manual test notes
- known limitations list

