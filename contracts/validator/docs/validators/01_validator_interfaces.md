# 01 — Validator Interfaces

## ValidationReport (canonical)
```yaml
ValidationReport:
  thoughtId: string
  validatorVersion: string
  passed: boolean
  summary:
    errorCount: int
    warnCount: int
    infoCount: int
  violations: [Violation]
  computedMetrics: object
  mustMoveResults: [MustMoveResult]
  determinism:
    checked: boolean
    identical: boolean|null
    hashA: string|null
    hashB: string|null
  suggestedRepairs: [RepairSuggestion]
```

## Violation
```yaml
Violation:
  id: string
  severity: "ERROR"|"WARN"|"INFO"
  category: "LEGality"|"STYLE"|"MUST_MOVE"|"DETERMINISM"|"ARRANGEMENT"|"RENDER"
  message: string
  paths:
    - kind: "control"|"grammar"|"event"
      path: string            # dotted path or event pointer
  evidence: object|null
```

## MustMoveResult
```yaml
MustMoveResult:
  id: string
  controlPath: string
  change: object             # what changed (delta)
  metricName: string
  metricDelta: object        # e.g., numeric delta, KL divergence
  threshold: object
  passed: boolean
  notes: string|null
```

## RepairSuggestion
```yaml
RepairSuggestion:
  id: string
  target: "generator"|"resolver"|"ui"
  description: string
  recommendedChange: object
  rationale: string
```

## Contract files
See JSON schemas in `contracts/`.
