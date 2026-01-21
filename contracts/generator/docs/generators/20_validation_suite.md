# 20 — Validation Suite (Generator-level)

Ensures:
- legality (respect Grammar)
- “must-move” (controls affect sound measurably)
- determinism (same seed => same output)

## A) Determinism
Run generator pipeline twice with same inputs and assert identical outputs.

## B) Legality
- pitch classes subset of allowedPitchClasses
- cadence types subset of allowedCadences
- onset ticks subset of legal onset mask
- timing variance within bounds
- velocity within MIDI bounds

## C) Must-move examples
- Change `pitch.pitchWeights` → pitch_class_histogram KL divergence > threshold
- Change `pitch.voiceLeadingRules.maxLeap` → interval_histogram high bins decrease
- Change `rhythm.onsetMask.syncopationBias` → syncopation_index increases
- Change `performance.velocityCurve.accentScale` → accent_contrast increases
- Change `harmony.progressionTemplates.weights` → progression archetype frequency changes

## D) Repair trace
When invalid values appear:
- repair deterministically
- trace includes before/after and reason
