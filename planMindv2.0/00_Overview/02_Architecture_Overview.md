# Architecture Overview

## Components

### Backend (Python / FastAPI)
Responsibilities:
- Parse the DSL text into an **Intent** structure
- Apply a **Style Profile** to generate a note/event sequence
- Resolve clashes when multiple thoughts are combined (Theory Gate endpoint)

Key endpoints (PoC):
- `POST /generate` → generate a Thought sequence
- `POST /resolve-conflict` → resolve conflicts between multiple sequences
- `GET /profiles` → list available style profiles and parameters
- `GET /health` → sanity check

### Protocol (JSON Contract)
Responsibilities:
- Standard packet between backend and frontend
- Versioned schema so the UI can reject incompatible payloads safely

### Frontend (HTML/JS ESM)
Responsibilities:
- LiteGraph node canvas (visual composition)
- Nodes that send DSL text to backend with debounced updates
- Tone.js scheduling and transport control
- Quantized swap to keep loop seamless
- Visual feedback for errors / status

## Data flow

1. User types DSL text in node editor.
2. Frontend debounces (e.g., 500ms) and sends:
   - node_id
   - style_profile
   - intent_text
   - harmonic anchor context (optional in PoC)
3. Backend parses intent + profile and returns Thought JSON.
4. Frontend schedules returned events onto Tone.Transport.
5. On subsequent edits: frontend requests new Thought, but only swaps playback at next bar.

## “Fan-in” flow

1. User wires two Thought nodes into a TheoryGate node.
2. Gate collects both sequences and sends them to `/resolve-conflict`.
3. Backend returns corrected sequences (or a merged “resolved” stream).
4. Frontend schedules corrected outputs at next bar.

## Recommended repo layout (PoC)

- `backend/`
  - `app/main.py`
  - `app/api.py`
  - `app/models.py`
  - `app/profiles.py`
  - `app/dsl_parser.py`
  - `app/generator.py`
  - `app/conflict_resolver.py`
  - `tests/`
- `frontend/`
  - `index.html`
  - `src/main.js`
  - `src/audio/toneScheduler.js`
  - `src/graph/litegraphNodes.js`
  - `src/api/client.js`
  - `src/state/runtimeStore.js`
  - `assets/`

