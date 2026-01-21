# 13 — Determinism Validator

## Purpose
Guarantee that for a given:
- ThoughtSpec
- ResolvedGrammar
- ResolvedControls
- seed

…the generator output is identical.

## D1) Hashing output
Compute a stable hash over:
- sorted events (by partId, voiceId, startTick, durationTicks, midi, velocity)
- chord events (sorted similarly)
- beat events
- and optionally trace step chosen outputs (not required for audio determinism)

## D2) What it reports
- `determinism.identical=true/false`
- hashA/hashB

## Severity
- ERROR in strict mode if non-identical
- WARN otherwise

## Common causes
- non-stable iteration order (dict keys)
- random without seeded RNG
- time-based jitter generation
- floating rounding not standardized
