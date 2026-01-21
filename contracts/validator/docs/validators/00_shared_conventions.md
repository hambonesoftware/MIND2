# 00 — Shared Conventions

## A) Inputs
Validators accept:

```yaml
inputs:
  resolvedGrammar: ResolvedGrammar
  resolvedControls: ResolvedControls
  thoughtMeta:
    thoughtId: string
    seed: int
    bars: int
    meter: string
    bpm: float
    grid: "1/4"|"1/8"|"1/16"|"1/32"
  generatedPart: GeneratedPart
  runtime:
    validatorVersion: string
    strict: boolean
```

## B) Determinism
Validators must be deterministic:
- They may compute metrics, but must not depend on timing, OS randomness, or iteration order.

## C) Severity and outcomes
- ERROR: illegal output or invariants broken → must fail in strict mode.
- WARN: output is legal but deviates from intent targets (style/profile/role).
- INFO: diagnostic.

## D) Repair suggestions
Validators may provide repair suggestions, but must NOT mutate events.
Mutation belongs to generator repair/backtrack.

## E) Metrics source of truth
If `GeneratedPart.metrics` exists, validators may:
- trust it in non-strict mode if a checksum matches,
- or recompute in strict mode to avoid stale metrics.
