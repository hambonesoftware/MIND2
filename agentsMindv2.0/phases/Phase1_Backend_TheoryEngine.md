# Phase 1 — Backend Theory Engine (FastAPI)

## Goal
Implement:
- `/health`
- `/profiles`
- `/generate`

Backend responsibilities:
- parse DSL v0 into Intent
- apply Style Profile + overrides
- generate thought.v0 sequence
- validate output against thought.v0 schema (once Phase 2 exists; for now, validate with pydantic + invariants)

---

## Step-by-step tasks

### 1) Create backend skeleton
Create:
- `mind_poc/backend/app/main.py`
- `mind_poc/backend/app/api.py`
- `mind_poc/backend/app/models.py`
- `mind_poc/backend/app/profiles.py`
- `mind_poc/backend/app/dsl_parser.py`
- `mind_poc/backend/app/generator.py`
- `mind_poc/backend/app/validators.py`

Add:
- `mind_poc/backend/requirements.txt` (or pyproject)
- `mind_poc/backend/README.md`

### 2) Implement Style Profiles v0
Minimum profiles:
- `wide_acoustic`
- `percussive_fingerstyle`
- `dark_pulse_synth`

Include:
- validation (ranges, required fields)
- label metadata for frontend dropdown

### 3) Implement DSL parser v0
Parse:
- pattern bracket list `[0 7 12]`
- modifiers via `| key:value`

Must produce:
- `Intent(pattern: list[int], modifiers: dict)`
- span info in errors when possible

### 4) Implement heuristic generator v0
Follow plan:
- time signature fixed 4/4
- division fixed default 16
- loop_bars default 1
- deterministic RNG with seed

Output:
- `Thought(schema_version="thought.v0", ...)`

### 5) Implement error model
Canonical error payload:
- error_code
- message
- hint
- span [start, end] optional

### 6) Add unit tests (minimum)
- `tests/test_profiles.py`
- `tests/test_dsl_parser.py`
- `tests/test_generator_invariants.py`

Invariants:
- times are valid strings
- midi in 0..127
- velocity scale consistent (recommend 0..1)
- sorted by time

---

## Acceptance checklist (Phase 1 gate)

- [ ] `GET /health` returns `{ "status": "ok" }`
- [ ] `GET /profiles` returns >= 3 profiles
- [ ] `POST /generate` returns valid Thought for `[0 7 12] | seed:123`
- [ ] invalid DSL returns structured error
- [ ] `pytest` passes

---

## Evidence to write
Append to: `mind_poc/docs/evidence/phase1_backend.md`
Include:
- command logs for run + tests
- sample request/response payloads
- any known limitations

