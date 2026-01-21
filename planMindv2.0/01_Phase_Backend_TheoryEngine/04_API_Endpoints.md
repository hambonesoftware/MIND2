# Backend API Endpoints (PoC)

## `GET /health`
Response:
```json
{ "status": "ok" }
```

## `GET /profiles`
Response:
```json
{
  "profiles": [
    { "id": "wide_acoustic", "label": "Wide-Interval Acoustic", "params": { "...": "..." } },
    { "id": "percussive_fingerstyle", "label": "Percussive Fingerstyle", "params": { "...": "..." } }
  ]
}
```

## `POST /generate`
Request:
```json
{
  "schema_version": "thought.v0",
  "node_id": "lead_01",
  "style_profile": "wide_acoustic",
  "intent_text": "[0 7 12] | slap:0.5 | vel:0.8 | seed:123",
  "context": {
    "tempo": 120,
    "time_signature": "4/4",
    "anchor_midi": 60,
    "role": "lead"
  }
}
```

Response:
```json
{
  "schema_version": "thought.v0",
  "node_id": "lead_01",
  "status": "active",
  "style_profile": "wide_acoustic",
  "meta": { "tempo": 120, "time_signature": "4/4", "loop_bars": 1, "division": 16 },
  "sequence": [
    { "midi": 62, "time": "0:0:0", "velocity": 0.75, "type": "note", "duration": "0:0:1" },
    { "midi": null, "time": "0:0:1", "velocity": 0.0, "type": "mute" }
  ]
}
```

## Error response (canonical)
```json
{
  "error": {
    "error_code": "DSL_VALUE_RANGE_ERROR",
    "message": "Modifier 'slap' must be between 0 and 1.",
    "hint": "Try slap:0.25",
    "span": [14, 22]
  }
}
```

