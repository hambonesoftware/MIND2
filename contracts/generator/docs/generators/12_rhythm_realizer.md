# 12 — RhythmRealizer

## Purpose
Produce a **RhythmPlan** and/or per-part onset sequences that:
- respect RhythmGrammar onset legality
- express density/syncopation/swing/accent archetypes
- feed onset positions to PitchSelector / MotifPlanner

## Inputs (fields used)
### Controls
- `ResolvedControls.rhythm.grid`
- `ResolvedControls.rhythm.onsetMask`
- `ResolvedControls.rhythm.accentModel`
- `ResolvedControls.rhythm.microtimingProfile`
- performance cap: `ResolvedControls.performance.timingVariance`

### Grammar consulted
- `ResolvedGrammar.rhythmGrammar.meter`
- `ResolvedGrammar.rhythmGrammar.gridPolicy`
- `ResolvedGrammar.rhythmGrammar.onsetLegality`
- `ResolvedGrammar.rhythmGrammar.accentGrammar`
- `ResolvedGrammar.rhythmGrammar.grooveTemplates`
- `ResolvedGrammar.performanceGrammar.humanizationBounds`

## Output
- `RhythmPlan` (see `contracts/RhythmPlan.schema.json`)

---

## Algorithm

### Stage R0 — Compute tick lattice
From meter + grid:
- ticksPerBeat, barTicks, totalTicks

### Stage R1 — Build legal onset set
Start with Grammar legality:
- `legalTicks = rhythmGrammar.onsetLegality.styleMask`

Apply forbidden zones (grammar):
- remove ticks in forbidden ranges

Apply Controls tightening:
- intersect with user onsetMask subset (if any)

Repair if empty:
- fallback to grammar.styleMask or nearest groove template (deterministic)

Decision site fields:
- `ResolvedControls.rhythm.onsetMask`
Metrics:
- `onset_ngram_stability`
- `syncopation_index`

### Stage R2 — Generate onset sequences per part
For each part:
- derive target onset count from density
- sample from legalTicks with bias:
  - strong beats if preferStrongBeats
  - offbeats if syncopation high
  - ensure min rests per bar

Beat part uses accent archetypes:
- kick/snare/hat placements matched to accentModel/backbeatBias

Decision site fields:
- density, syncopation, restPolicy, accentModel

Metrics:
- `syncopation_index`
- `backbeat_strength`
- `rest_ratio` (if tracked)

### Stage R3 — Microtiming (swing/pocket)
MicrotimingProfile defines:
- swing enum -> swing ratio target
- pocket bias (ahead/behind)
- jitterStdMs (clamped)

Decision site fields:
- `ResolvedControls.rhythm.microtimingProfile.*`
- `ResolvedControls.performance.timingVariance` (cap)

Metrics:
- `swing_ratio`
- `quantization_error`

---

## Minimum tests
- increasing syncopation increases syncopation_index
- increasing swing increases swing_ratio
- increasing backbeatBias increases backbeat_strength
