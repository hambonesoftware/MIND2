# `/resolve-conflict` Endpoint (PoC)

## Request
```json
{
  "schema_version": "resolve.v0",
  "style_profile": "wide_acoustic",
  "inputs": [
    { "node_id": "bass_01", "role": "bass", "thought": { "...thought.v0..." } },
    { "node_id": "lead_01", "role": "lead", "thought": { "...thought.v0..." } }
  ]
}
```

## Response (Option A recommended)
```json
{
  "schema_version": "resolve.v0",
  "style_profile": "wide_acoustic",
  "resolved": [
    { "node_id": "bass_01", "thought": { "...corrected..." } },
    { "node_id": "lead_01", "thought": { "...corrected..." } }
  ],
  "meta": {
    "clashes_detected": 1,
    "actions": [
      { "time": "0:1:0", "node_id": "lead_01", "action": "shift", "semitones": 2 }
    ]
  }
}
```

## Error response
Same canonical error structure as `/generate`.

