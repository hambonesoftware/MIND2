# Global Agent Rules (do not violate)

## 1) Safety / scope
- Implement ONLY what is needed for the PoC plan.
- Do not add large frameworks or unrelated features.

## 2) Determinism
- The backend generator must support a `seed` override.
- Use local RNG instances (do not rely on global random state).

## 3) Schema-first discipline
- Implement JSON Schemas in `contracts/` first (Phase 2),
  then validate on both backend + frontend.

## 4) Logging discipline
- Add clear logs for:
  - request received
  - parse result
  - generation timing
  - conflict resolution actions
- Frontend logs state transitions for each node.

## 5) Error handling
- Backend errors must be structured:
  - error_code, message, hint, span
- Frontend must show errors without stopping last-good audio.

## 6) “No ellipses” in delivered code
- Do not use `...` placeholders. Write full, complete files.

## 7) Minimal dependencies
Backend:
- fastapi, uvicorn, pydantic, pytest (plus jsonschema validator if desired)
Frontend:
- litegraph.js, tone
- vite (recommended) or a simple dev server

