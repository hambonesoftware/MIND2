# Phase 2 — Thought Contract (JSON Schema)

## Goal
Define:
- `contracts/thought.v0.schema.json`
- `contracts/resolve.v0.schema.json`

Then integrate schema validation:
- backend validates outgoing packets
- frontend validates incoming packets

---

## Step-by-step tasks

### 1) Create `thought.v0` JSON Schema
Implement fields from the plan:
- required top-level fields
- meta object with required keys
- sequence event union with conditional requirements
- time regex: `^\d+:\d+:\d+$`

### 2) Create `resolve.v0` JSON Schema
- wrapper object containing `style_profile`, `inputs[]`, and `resolved[]`
- include optional `meta.actions[]` for resolution trace

### 3) Backend validation
In backend:
- load schema files
- validate `Thought` before returning
- on validation failure: return structured error `SCHEMA_VALIDATION_ERROR`

### 4) Frontend validation
In frontend:
- implement a validator module that checks:
  - `schema_version` supported
  - required keys present
  - time strings valid
- (Optional) use a JSON Schema lib in JS, but keep it lightweight

---

## Acceptance checklist (Phase 2 gate)

- [ ] Schemas exist and validate example packets
- [ ] Backend rejects invalid output
- [ ] Frontend rejects invalid packets without scheduling

---

## Evidence to write
Append to: `mind_poc/docs/evidence/phase2_contracts.md`
Include:
- schema snippets (not entire file if huge)
- validation test logs
- a “known compatible packet” example

