# Example — Minimal ValidationReport (YAML)

```yaml
thoughtId: "T-001"
validatorVersion: "v9.14.0"
passed: false
summary:
  errorCount: 1
  warnCount: 2
  infoCount: 0
violations:
  - id: "L3_ILLEGAL_PC"
    severity: "ERROR"
    category: "LEGality"
    message: "Found pitch class 1 not allowed and not permitted by chromatic policy."
    paths:
      - kind: "control"
        path: "ResolvedControls.pitch.allowedPitchClasses"
      - kind: "event"
        path: "NoteEvent(part=melody,startTick=24,midi=61)"
    evidence:
      illegalPc: 1
computedMetrics:
  pitch_class_histogram: {0: 0.22, 2: 0.18, 4: 0.12, 5: 0.10, 7: 0.18, 9: 0.20}
mustMoveResults: []
determinism:
  checked: true
  identical: true
  hashA: "a1b2..."
  hashB: "a1b2..."
suggestedRepairs:
  - id: "R_DROP_OR_REPLACE"
    target: "generator"
    description: "Replace illegal pitch class with nearest legal pitch class within range."
    recommendedChange:
      action: "replace_pitch_class"
      fromPc: 1
      toPcCandidates: [0,2]
    rationale: "Preserves contour while restoring legality."
```
