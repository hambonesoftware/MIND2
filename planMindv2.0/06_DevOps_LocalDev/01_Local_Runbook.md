# Local Runbook (PoC)

## Backend

### Setup
- Python 3.12 recommended
- Create venv
- Install requirements:
  - fastapi
  - uvicorn
  - pydantic
  - pytest

### Run
- `uvicorn app.main:app --reload --port 8000`

### Verify
- `GET http://localhost:8000/health`
- `GET http://localhost:8000/profiles`

## Frontend

### Setup
- Node 20 recommended
- Simple dev server (Vite or equivalent)

### Run
- `npm install`
- `npm run dev`

### Verify
- Page loads LiteGraph canvas
- Creating a Thought node and typing DSL triggers backend call
- Audio plays (ensure browser audio permission)

## CORS
- Backend should allow localhost dev origins (configurable)

