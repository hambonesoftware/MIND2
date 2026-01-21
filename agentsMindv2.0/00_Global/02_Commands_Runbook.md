# Command Runbook (agent cheat sheet)

## Backend
From `mind_poc/backend`:

### Install (venv recommended)
- `python -m venv .venv`
- Windows:
  - `.venv\Scripts\activate`
- Mac/Linux:
  - `source .venv/bin/activate`
- `pip install -r requirements.txt`

### Run
- `uvicorn app.main:app --reload --port 8000`

### Smoke tests
- `curl http://localhost:8000/health`
- `curl http://localhost:8000/profiles`

### Pytest
- `pytest -q`

## Frontend
From `mind_poc/frontend`:

### Install
- `npm install`

### Run
- `npm run dev`

### Verify
- open local URL
- create a Thought node
- type DSL: `[0 7 12] | vel:0.8 | seed:123`
- confirm audio plays and swaps next bar when edited

