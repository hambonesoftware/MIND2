# Pane 11 — Register (Tessitura)

## What this pane controls
Controls where in pitch space the part lives and how wide it spreads.

## Deterministic choices
### center
- low | mid_low | mid | mid_high | high
Audible must-move: mean_pitch shifts.

### span
- narrow | medium | wide
Audible must-move: pitch range / variance changes.

### climaxLift
- none | small | medium | large
Audible must-move:
- raises register near climax sections (per phrasePlan peakPosition).

### octaveBias
- preferredOctaves: list of integers (e.g., [3,4,5])
- penalizeOuterOctaves: bool
Audible must-move:
- distribution concentrates in preferredOctaves when set.

## Resolver handoff (must map)
Must affect:
- `ResolvedControls.pitch.voiceLeadingRules.register` (minMidi/maxMidi)
- pitch candidate weighting around preferred octaves
- form/performance coupling for climaxLift

## Generator decision sites (must move audio)
- PitchSelector restricts candidate MIDI notes to the register band.
- PerformanceHumanizer and FormPlanner coordinate climaxLift shaping.

## Must-move metrics
Must-move metrics:
- `mean_pitch` (or proxy from pitch histogram)
- `span_semitones` (range)
- `peak_pitch_position_correlation` (if tracked)

## Common pitfalls / anti-patterns
- center/span values not reflected in range constraints (dead register pane).
- climaxLift always applied even when set to none (bug).
