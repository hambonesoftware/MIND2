# Example — Wonderwall-like opening (high-level)

Goal: create an 8-bar acoustic-rock/pop opening with a repeating strum/pick pattern.

## ResolvedControls highlights (illustrative)
- harmony.progressionTemplates.selectedId: a pop/rock loop template
- rhythm.grid: "1/16"
- rhythm.onsetMask: strum-friendly (dense 8ths/16ths), min rests moderate
- rhythm.accentModel: light backbeat, preferStrongBeats=true
- motif.scheme: AAAA with high repeatStrength
- pitch.allowedPitchClasses: diatonic major (song key)
- pitch.chordToneStrength: high
- performance: timingVariance low-medium, velocityCurve gentle arch

## Expected must-move outcomes
- chord_tone_ratio high
- onset_ngram_stability high (repeating strum)
- motif_similarity high (opening cell repeats)
