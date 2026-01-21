# Pane 12 — Contour (Macro Shape)

## What this pane controls
Contour describes the macro pitch/energy movement across the thought: direction, motion character, and smoothness.

## Deterministic choices
### shape
- static: flat pitch center
- arch: rise then fall
- ascending: overall up
- descending: overall down
- wave: multiple rises/falls

Audible must-move:
- macro trend of pitch and/or dynamics matches shape.

### motion
- static: repeated tones
- mostly_stepwise: small intervals
- mixed: stepwise + some leaps
- leapy: frequent larger intervals

Audible must-move:
- interval histogram shifts to larger bins for leapy.

### smoothness
- low: jagged contour allowed
- medium
- high: smooth arc enforcement

Audible must-move:
- adjacent pitch changes become more stepwise/smoothed.

### targets
- phraseStart / phraseEnd: relative target degrees or register offsets
- peakPosition: 0..1 for where the top occurs

Audible must-move:
- the peak occurs near peakPosition (pitch and/or velocity).

## Resolver handoff (must map)
Must affect:
- `ResolvedControls.form.phrasePlan.contourShape`
- `ResolvedControls.form.phrasePlan.peakPosition`
- pitch selection scoring (contour proximity terms)

## Generator decision sites (must move audio)
- FormPlanner emits contour targets.
- PitchSelector enforces contour via scoring.
- PerformanceHumanizer may mirror contour in velocity.

## Must-move metrics
Must-move metrics:
- `contour_correlation` (macro pitch track vs target curve)
- `interval_histogram` (motion changes)
- `peak_position_error` (|observedPeakPos - target|)

## Common pitfalls / anti-patterns
- Contour fields only change UI visuals, not pitch scoring (dead contour).
- High smoothness but generator still produces jagged jumps (no constraint).
