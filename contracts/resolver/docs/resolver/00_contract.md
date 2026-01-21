# 00 — Resolver Contract (Theory-first)

## Purpose
Compile a Thought (14 panes + inheritance + catalogs) into deterministic, testable, generator-ready IR.

This revision introduces explicit layers:

- `ResolvedGrammar`: theory-native legality + vocab (hard constraints)
- `ResolvedControls`: generator-ready controls (weights/masks/plans) produced *within* grammar
- `ResolveTrace`: why the compiler chose each value

The resolver is not a generator. It compiles constraints and preferences.

---

## Outputs (v9.14 theory-first)

### Output A — ResolvedGrammar (NEW)
Hard legality and vocabulary. This is what a music theory postdoc cares about first.

### Output B — ResolvedControls (FROZEN)
Frozen control surface used by generators.
All values MUST be legal under ResolvedGrammar.

### Output C — Trace + warnings/errors
Mandatory diagnostics.

---

## Resolver signature

### Inputs
```yaml
inputs:
  thoughtSpec: ThoughtSpec                # 14 pane UI specification (authoring surface)
  catalogs:
    styleCatalog: StyleCatalog            # styleFamily/styleVariant definitions (includes grammar + default biases)
    profileCatalog: ProfileCatalog        # profile definitions (bias defaults)
  upstream:
    upstreamResolvedGrammar: ResolvedGrammar|null
    upstreamResolvedControls: ResolvedControls|null
    upstreamContextSelection: object|null
  global:
    globalSetup: object|null
  runtime:
    resolverVersion: string
    overrideMode: locked|simple|expert
    failOpen: boolean
```

### Outputs
```yaml
outputs:
  resolvedGrammar: ResolvedGrammar
  resolvedControls: ResolvedControls
  trace: ResolveTrace
  warnings: [ResolveWarning]
  errors: [ResolveError]
```
If errors is non-empty:
- failOpen=false => stop
- failOpen=true  => proceed only if validators say "usable"

---

## Deterministic guarantees
1. Pure function: same inputs => same outputs
2. Canonicalization: all outputs normalized to canonical forms
3. No generation: no notes/chords/rhythms are created here

---

## What the resolver may repair
- clamp numeric bounds
- drop unknown IDs and substitute defaults (with warnings)
- intersect illegal sets/masks with grammar legality
- renormalize weights
- repair plans (phrase/cadence) to fit bars and grammar requirements

---

## Required traceability
For each field in both Grammar and Controls:
- final value
- contributors (source/value/origin)
- merge operator
- normalizations and repairs performed
