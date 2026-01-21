# agentsMind v2.0 — Agent Instructions for planMindv2.0

Date: 2026-01-21  
Timezone: America/Detroit

This zip contains the **agent task pack** that executes `planMindv2.0.zip`.

It is written for a “doer” agent that can:
- create/edit files
- run commands
- run tests
- capture logs
- produce the required artifacts per phase

---

## Inputs assumed available

- `planMindv2.0.zip` mounted locally (the plan this pack implements)

---

## Outputs expected from the agent

A working PoC repo with:
- `backend/` FastAPI service implementing `/health`, `/profiles`, `/generate`, `/resolve-conflict`
- `frontend/` LiteGraph + Tone.js UI implementing:
  - MusicalThoughtNode with debounced text DSL input
  - quantized swap audio scheduling
  - TheoryGate node fan-in calling `/resolve-conflict`
- test suites and acceptance evidence logs

---

## Canonical repo layout (create this)

```
mind_poc/
  backend/
    app/
      main.py
      api.py
      models.py
      profiles.py
      dsl_parser.py
      generator.py
      conflict_resolver.py
      validators.py
    tests/
      test_profiles.py
      test_dsl_parser.py
      test_generator_invariants.py
      test_conflict_resolver.py
    pyproject.toml   (or requirements.txt)
    README.md
  frontend/
    index.html
    package.json
    vite.config.js   (or equivalent)
    src/
      main.js
      api/
        client.js
      graph/
        litegraphNodes.js
      audio/
        toneScheduler.js
      state/
        runtimeStore.js
      validate/
        thoughtSchema.js
    assets/
    README.md
  contracts/
    thought.v0.schema.json
    resolve.v0.schema.json
  docs/
    evidence/
      phase1_backend.md
      phase2_contracts.md
      phase3_frontend.md
      phase4_fanin.md
      phase5_tests.md
```

---

## Non-negotiable immutables (must hold)

1. **Quantized Swap**: Thought updates swap only at next bar boundary.
2. **Canonical time string**: `"bar:beat:sixteenth"` everywhere.
3. **thought.v0 packet** includes required fields and passes schema.
4. **Backend is source of theory truth** (frontend does not “fix” clashes).
5. **No artist cloning** (profiles are descriptive only).

These immutables are defined in the plan at:
- `00_Overview/03_Contracts_Immutables.md`

---

## How to run phases

Execute phases in order:

1. `01_Phase_Backend_TheoryEngine/`
2. `02_Phase_Thought_Contract/`
3. `03_Phase_Frontend_NodeCanvas/`
4. `04_Phase_FanIn_TheoryGate/`
5. `05_Phase_Testing_Validation/`

Each phase has:
- a phase task file: `phases/PhaseX_*.md`
- a completion evidence template in `docs/evidence/`

At the end of each phase:
- run the defined checks/tests
- append logs + screenshots (if possible) into the matching evidence doc

