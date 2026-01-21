# planMind v2.0 — Node-Driven Live-Coding Music PoC

Date: 2026-01-21  
Timezone: America/Detroit

This zip is the **project plan** for a Proof of Concept (PoC) that combines:

- **Tidal-style text entry** (compact DSL)
- **n8n-style node graph** (LiteGraph.js)
- **Python “Theory Engine”** (FastAPI) that generates musically-valid note streams
- **Style Profiles** (descriptive rule-sets, not artist emulation) that steer generation and conflict resolution
- **Tone.js** scheduling with a **quantized swap** so updates stay seamless

This plan is written **as if matching agent instructions already exist** (e.g., `agentsMindv2.0.zip`) and will reference “Agent Tasks” per phase.  
No agent files are included here.

---

## What “done” means for the PoC

By the end of the PoC you can:

1. Open a browser page with a **LiteGraph canvas**.
2. Drop a **MusicalThoughtNode** that has a **text DSL input** and a **style selector**.
3. Type a short pattern like:  
   `"[0 7 12] | slap:0.5 | vel:0.8 | oct:+1"`
4. Hear sound played by Tone.js.
5. Add a second node (e.g., bass) and route both into a **TheoryGate** node.
6. Hear both streams together, where the backend resolves clashes using profile-driven rules.
7. Changes to text are applied only on the **next bar** (quantized swap), so loops never “glitch”.

---

## Directory map

- `00_Overview/` — product definition, glossary, constraints, decisions
- `01_Phase_Backend_TheoryEngine/` — FastAPI, profiles, DSL parsing, generation
- `02_Phase_Thought_Contract/` — JSON schema, versioning rules
- `03_Phase_Frontend_NodeCanvas/` — LiteGraph custom nodes, Tone.js scheduling
- `04_Phase_FanIn_TheoryGate/` — multi-input resolution and /resolve-conflict
- `05_Phase_Testing_Validation/` — test plan, fixtures, acceptance sheets
- `06_DevOps_LocalDev/` — local setup, scripts, runbooks
- `07_Backlog/` — scoped backlog for v2.x

---

## Phase order (high level)

1. **Backend Theory Engine**
2. **Thought Contract**
3. **Frontend Node Canvas**
4. **Fan-In Theory Gate**
5. **Testing & Validation**

Each phase has:
- goals, scope, non-scope
- required artifacts
- Agent Tasks (assumed to exist)
- acceptance criteria (“phase gates”)

---

## Compatibility note (future MIND alignment)

This PoC is **not** the full MIND v9.x architecture.  
However, it is deliberately designed so that the “Thought” packet and the “Theory Gate” concept can later map to your more formal, multi-pane control grammar (e.g., *ResolvedControls* groupings) without rewriting everything.

