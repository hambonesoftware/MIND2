# 11 — Style Conformance Validators

Style conformance = “output is legal AND sounds like the chosen style/profile/role *on average*.”

These checks are usually WARNs (not hard errors) unless the user selected a strict mode.

---

## S1) Groove / swing expectation
### What it checks
- swing_ratio within expected range for styleVariant
- backbeat_strength within expected range for rock/hiphop/latin variants

### Inputs used
- ResolvedGrammar.rhythmGrammar.grooveTemplates (expected ranges)
- ResolvedControls.rhythm.microtimingProfile / accentModel
- computed metrics: swing_ratio, backbeat_strength

### Example thresholds
- jazz_swing: swing_ratio >= 1.15
- rock_classic: swing_ratio approx 1.0 (off), backbeat_strength high
- latin_bossa: offbeat_ratio and groove_match(bossa) high

---

## S2) Harmonic color expectation
### What it checks
- chord_quality_histogram aligns with expected palette (triads vs extensions)
- non_diatonic_pitch_rate within chromatic caps AND style typical range

### Inputs used
- ResolvedControls.harmony.chordQualities, chromaticCaps
- computed metrics

---

## S3) Motif reuse expectation
### What it checks
- motif_similarity near target for pop hooks vs ambient textures
- repetition expectations for ostinato styles

### Inputs used
- ResolvedControls.motif.motifReusePlan
- ResolvedGrammar.motifGrammar.reuseExpectations
- metric: motif_similarity, onset_ngram_stability

---

## S4) Register and density expectation by role
### What it checks
- bass stays low; melody stays above bass on average
- pad has longer mean durations and lower density than fill

### Inputs used
- role and thoughtType derived defaults in ResolvedControls
- metrics: mean_pitch, density, note_duration_mean

---

## Outputs
Violations should explain:
- expected range
- observed metric
- which control(s) likely caused the mismatch
- suggested repair knob (generator or UI)
