# 15 — music21 Analysis Hooks (Optional)

music21 can provide additional analysis for validation and debug traces.

## What music21 is used for (validator-only)
- key detection / tonal center estimation
- RomanNumeral identification (given chord pitch classes)
- voice-leading and interval analysis helpers
- cadence heuristics (limited; depends on context)

## What music21 is NOT used for here
- generating music directly (that’s generator stage)
- being the source of truth for legality (ResolvedGrammar is)

## Recommended integration pattern
1) Convert GeneratedPart events to a `music21.stream.Score` or `Part`
2) Run targeted analyzers:
   - `analysis.discrete.KrumhanslSchmuckler` for key
   - `roman.romanNumeralFromChord` for RN labeling
3) Attach results into `ValidationReport.computedMetrics` and `violations.evidence`

## Determinism caution
music21 analysis can be deterministic, but:
- ensure consistent quantization and rounding before building streams
- avoid operations that depend on floating ordering without sorting
