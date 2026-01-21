# Pane 03 — Profile (Bias)

## What this pane controls
Profile is an affect/energy bias **inside** the chosen Style grammar.
It should not change legality much; it changes what is *likely* (weights, densities, registers, dynamics).

## Deterministic choices
### inheritFromUpstream
- true: adopt nearest upstream profile
- false: choose profile explicitly

### profileId (starter set)
- bright | dark | chill | emotional | aggressive | virtuosic | power_ballad | lofi | anthemic | intimate

Per-choice audible must-move (examples):
- bright: higher register center, more major/modal-bright scales, sharper articulation
- dark: lower register, minor/dorian tolerance, smoother attacks
- chill: lower density, more rests, softer accents
- aggressive: higher density, stronger accents, shorter durations
- virtuosic: wider span, more ornaments/runs (within caps)
- power_ballad: strong contour lift into climaxes, stronger cadences at section ends
- lofi: more timing variance, softer velocities, slower harmonic rhythm

### biasOverrides (expert)
- fine-tune weights that profile supplies:
  - densityBias, restRatioBias
  - registerCenterBias, spanBias
  - cadenceStrengthBias
  - velocityMeanBias, accentContrastBias

## Resolver handoff (must map)
Must affect:
- default parameters in `ResolvedControls.rhythm` (density/syncopation defaults)
- default parameters in `ResolvedControls.pitch.pitchWeights` or pitch class emphasis
- (without changing the allowedPitchClasses unless explicitly configured as a profile behavior)
- `ResolvedControls.performance` (timingVariance, velocityCurve)
- optional: `ResolvedControls.form` (climaxLift/peakPosition preferences)

## Generator decision sites (must move audio)
- RhythmRealizer uses density/syncopation/rest biases.
- PitchSelector uses pitchWeights bias and register bias.
- PerformanceHumanizer uses timingVariance and velocityCurve biases.
- HarmonyPlanner uses cadenceStrength bias (ballad vs chill).

## Must-move metrics
Must-move metrics (examples):
- `mean_pitch` / `register_center` proxy (bright vs dark)
- `density` and `rest_ratio` (chill vs aggressive)
- `accent_contrast` / `velocity_range` (anthemic vs intimate)
- `timing_jitter_std_ms` (lofi vs tight)

## Common pitfalls / anti-patterns
- Overloading profiles to secretly change chord legality (should be Style’s job).
- Profiles that don’t move any measurable metric (dead profile).
