# Pane 14 — Performance & Rendering

## What this pane controls
Controls how the generated notes are performed (timing/dynamics/articulation) and how parts map to instruments.

## Deterministic choices
### microtimingProfile
- tight: near-quantized, low jitter
- pocket: slight behind-the-beat feel
- laidback: more behind + more jitter
- swingy: swing ratios emphasized (if style allows)

Audible must-move:
- quantization_error increases with looser profiles
- swing_ratio increases with swingy

### timingVariance
- none | small | medium | large
Audible must-move: timing_jitter_std_ms changes.

### velocityCurve
- flat: uniform dynamics
- gentle_arch: small arc per phrase
- crescendo: rising
- decrescendo: falling
- strong_arch: big arc (ballad/anthemic)

Audible must-move: velocity_range and phrase_dynamic_correlation change.

### articulationBias
- legato | mixed | staccato
Audible must-move:
- mean note duration (relative to grid) shifts; overlap rules respected.

### render.partInstrument
- maps thoughtType/role to instrument programs (e.g., nylon_guitar, strings, piano, synth_pad)
Audible must-move:
- timbre changes, but note content stays identical (unless instrument implies performance defaults, which must be explicit).

### render.mixer (optional)
- level: -inf..0 dB equivalent
- pan: L..R
Audible must-move:
- loudness/pan changes, not pitch/rhythm.

## Resolver handoff (must map)
Must affect:
- `ResolvedControls.rhythm.microtimingProfile` (this parameter lives in the rhythm control group even though the UI lists it under performance)
- `ResolvedControls.performance.timingVariance`
- `ResolvedControls.performance.velocityCurve`
- optional articulation constraints in performance grammar
- render routing config (not in ResolvedControls, but in render config stage)

## Generator decision sites (must move audio)
- PerformanceHumanizer applies microtiming + velocity curve.
- Renderer maps partInstrument and mixer.

## Must-move metrics
Must-move metrics:
- `quantization_error`
- `swing_ratio`
- `timing_jitter_std_ms`
- `velocity_mean_and_range`
- `accent_contrast` (interaction with rhythm accent model)

## Common pitfalls / anti-patterns
- Instrument mapping accidentally changes RNG seed (timbre change should not change notes).
- Velocity curve exists but is clamped so hard it sounds flat (bounds too tight).

## Compatibility Note

In earlier revisions the microtiming controls were located under `ResolvedControls.performance`. Starting with v9.14 they are part of the rhythm group (`ResolvedControls.rhythm.microtimingProfile`). The `thought.performance.microtimingProfile` field still exists in the ThoughtSpec for UI grouping, but the resolver deterministically maps it into `ResolvedControls.rhythm.microtimingProfile` and ignores any legacy `ResolvedControls.performance.microtimingProfile` field. This ensures swing/pocket/jitter settings are always treated as part of the rhythm controls.
