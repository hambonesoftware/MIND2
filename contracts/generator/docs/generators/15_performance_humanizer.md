# 15 — PerformanceHumanizer

## Purpose
Apply timing and dynamics to events while respecting bounds.

## Inputs
### Controls
- `ResolvedControls.performance.timingVariance`
- `ResolvedControls.performance.velocityCurve`
- `ResolvedControls.rhythm.microtimingProfile`
- `ResolvedControls.rhythm.accentModel`
- `ResolvedControls.form.phrasePlan`

### Grammar consulted
- `ResolvedGrammar.performanceGrammar.humanizationBounds`
- `ResolvedGrammar.performanceGrammar.articulationNorms`

## Output
- Modified events + optional PerformancePlan snapshot

---

## Algorithm

### Stage V0 — Timing offsets
- pocket bias shifts overall
- swing ratio shifts offbeats
- jitter adds noise (deterministic via subseed)
Clamp to bounds.

Metrics:
- `timing_jitter_std_ms`
- `swing_ratio`

### Stage V1 — Velocity curve
- baseVelocity
- phrase shaping: crescendo/arch using peakPosition
- accent scaling from accentModel
Clamp to MIDI bounds and grammar accent max.

Metrics:
- `velocity_mean_and_range`
- `accent_contrast`

---

## Minimum tests
- increasing jitterStdMs increases timing_jitter_std_ms but stays within bounds
- increasing accentScale increases accent_contrast
