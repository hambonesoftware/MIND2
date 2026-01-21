# Pane 10 — Rhythm (Placement)

## What this pane controls
Controls grid resolution, density, syncopation, swing, rests, and accent bias.
This pane maps mostly to `ResolvedControls.rhythm.*`.

## Deterministic choices
### grid
- 1/4 | 1/8 | 1/16 | 1/32
Audible must-move:
- finer grid enables shorter notes and more intricate patterns; quantization_error baseline changes.

### density
- low: fewer onsets per bar
- medium: typical
- high: many onsets
Audible must-move: event_count and rest_ratio change.

### syncopation
- low: more strong-beat onsets
- medium: balanced
- high: more offbeat onsets
Audible must-move: syncopation_index changes.

### swing
- off | light | medium | heavy
Audible must-move: swing_ratio changes; microtiming applied.

### restPolicy
- minRestBeatsPerBar: 0..beatsPerBar
- allowAnticipations: bool
Audible must-move: rest_ratio changes and anticipatory onsets appear.

### accent
- preferStrongBeats: bool
- backbeatBias: low|medium|high
Audible must-move: backbeat_strength and accent_contrast change (beat/hihat patterns too).

## Resolver handoff (must map)
Must affect:
- `ResolvedControls.rhythm.grid`
- `ResolvedControls.rhythm.onsetMask`
- `ResolvedControls.rhythm.accentModel`
- `ResolvedControls.rhythm.microtimingProfile` (swing)
- cross-cap with performance timing variance

## Generator decision sites (must move audio)
- RhythmRealizer determines onset sets and accent archetypes.
- PerformanceHumanizer applies swing and pocket/jitter.
- Beat generators use backbeatBias heavily.

## Must-move metrics
Must-move metrics:
- `syncopation_index`
- `backbeat_strength`
- `swing_ratio`
- `rest_ratio`
- `quantization_error` (post microtiming)

## Common pitfalls / anti-patterns
- Swing set but renderer ignores microtiming offsets (no audible swing).
- syncopation changes but onsetMask stays the same (dead syncopation).
