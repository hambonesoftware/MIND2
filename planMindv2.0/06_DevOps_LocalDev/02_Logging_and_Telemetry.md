# Logging & Telemetry (PoC)

## Backend logs
Must log:
- request id
- node_id
- style_profile
- parse success/failure
- generation timing
- conflict resolution actions

## Frontend logs
Must log (console ok):
- node id state transitions: idle → pending → scheduled → active
- quantized swap scheduling time
- schema validation failures with path

## Debug switches (recommended)
- `?debug=1` enables verbose UI logs
- backend env var `MIND_DEBUG=1` increases log verbosity

