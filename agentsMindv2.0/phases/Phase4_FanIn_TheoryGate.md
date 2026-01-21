# Phase 4 — Fan-In Logic (Theory Gate)

## Goal
- Add TheoryGate node to frontend
- Add `/resolve-conflict` to backend
- Demonstrate clash detection + correction

---

## Step-by-step tasks

### 1) Backend: conflict resolver module
Create:
- `backend/app/conflict_resolver.py`

Implement:
- parse input thoughts
- detect clashes at identical time slots
- apply profile `clash_policy` (PoC uses shift primarily)
- protect bass role

Return:
- corrected thoughts per input node_id
- meta.actions trace list

### 2) Backend: endpoint `/resolve-conflict`
Add to API:
- request schema_version `resolve.v0`
- validate inputs thoughts against thought.v0 schema
- produce response validate against resolve.v0 schema

### 3) Frontend: TheoryGate node
- 2-4 inputs
- gather latest upstream thoughts
- call `/resolve-conflict` when any input updates
- output corrected thoughts downstream (or directly schedule them if PoC chooses)

### 4) Demonstration patch
Create an example patch in UI:
- bass node outputs a stable root
- lead node outputs an intentionally clashing tone (configure avoid_intervals for test)
- gate resolves by shifting lead

---

## Acceptance checklist (Phase 4 gate)

- [ ] Two nodes routed through gate play
- [ ] At least one clash corrected (visible in logs/meta.actions)
- [ ] Correction swaps at next bar (still uses quantized swap)

---

## Evidence to write
Append to: `mind_poc/docs/evidence/phase4_fanin.md`
Include:
- sample resolve request/response
- logs showing action trace
- reproduction steps

