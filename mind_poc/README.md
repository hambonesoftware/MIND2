# MIND PoC

## Run everything
From the repository root:
```bash
python run.py
```

## Backend

### Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

### Run
```bash
uvicorn app.main:app --reload --port 8000
```

### Verify
```bash
curl http://localhost:8000/health
curl http://localhost:8000/profiles
```

### CORS
The backend allows the Vite dev origin `http://localhost:5173` by default.

### Debug logging
Set `MIND_DEBUG=1` to increase logging verbosity.

## Frontend

### Setup
```bash
cd frontend
npm install
```

### Run
```bash
npm run dev
```

### Verify
- Open the Vite URL printed in the terminal.
- Create a `MusicalThought` node and type a DSL pattern.
- Confirm audio swaps at the next bar.

## Logging expectations

Backend logs:
- request received
- profile selection
- schema validation failures
- conflict resolution actions

Frontend logs:
- node state transitions
- swap scheduling time
- schema validation failures
