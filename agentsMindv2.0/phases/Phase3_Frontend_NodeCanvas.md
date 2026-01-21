# Phase 3 — Frontend Node Canvas (LiteGraph + Tone.js)

## Goal
Implement a working UI where:
- user can create a Thought node
- type DSL
- hear playback
- edits swap only at next bar (quantized swap)

---

## Step-by-step tasks

### 1) Frontend scaffold
Create:
- `mind_poc/frontend/index.html`
- `mind_poc/frontend/src/main.js`
- `mind_poc/frontend/src/api/client.js`
- `mind_poc/frontend/src/audio/toneScheduler.js`
- `mind_poc/frontend/src/graph/litegraphNodes.js`
- `mind_poc/frontend/src/state/runtimeStore.js`
- `mind_poc/frontend/src/validate/thoughtSchema.js`
- `mind_poc/frontend/package.json`
- `mind_poc/frontend/vite.config.js` (recommended)

### 2) LiteGraph canvas
- Initialize LiteGraph canvas
- Add palette/menu to create nodes

### 3) MusicalThoughtNode
Must include:
- text entry (overlay textarea acceptable)
- profile selector (dropdown populated from backend `/profiles`)
- status indicator
- debounced API calls (500ms)
- abort previous in-flight request on new edit

### 4) Tone scheduler w/ Quantized Swap
For each node:
- keep active Part
- build next Part on successful generate
- schedule swap at next bar boundary
- guarantee no overlap / double-play

### 5) Error UX
- show backend errors in the node
- keep last good part playing

---

## Acceptance checklist (Phase 3 gate)

- [ ] Thought node plays audible sequence
- [ ] Edits do not glitch; swap at next bar
- [ ] Errors do not stop last-good audio
- [ ] Console logs show state transitions cleanly

---

## Evidence to write
Append to: `mind_poc/docs/evidence/phase3_frontend.md`
Include:
- npm install/run logs
- a short description of how to reproduce
- screenshots if possible

