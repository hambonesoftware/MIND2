# 13 — PitchSelector

## Purpose
Assign pitches to onsets producing NoteEvents that:
- respect allowed pitch classes
- respect register bounds and voice-leading caps
- achieve chord-tone ratio targets under HarmonyPlan chords
- follow contour targets from FormPlan

## Inputs (fields used)
### Controls
- `ResolvedControls.pitch.allowedPitchClasses`
- `ResolvedControls.pitch.pitchWeights`
- `ResolvedControls.pitch.voiceLeadingRules`
- `ResolvedControls.harmony.chromaticCaps`
- `ResolvedControls.form.phrasePlan`
- `ResolvedControls.form.cadencePlan`
- `ResolvedControls.rhythm.onsetMask` (or RhythmPlan onset sequences)

### Grammar consulted
- `ResolvedGrammar.pitchGrammar.scaleVocabulary`
- `ResolvedGrammar.pitchGrammar.voiceLeadingHardRules`
- `ResolvedGrammar.harmonyGrammar.chordVocabulary`
- `ResolvedGrammar.harmonyGrammar.chromaticPolicy`

## Output
- NoteEvents + optional PitchPlan snapshot

---

## Algorithm

### Stage P0 — Build legal pitch-class set
- `legalPcs = ResolvedControls.pitch.allowedPitchClasses` (non-empty)

### Stage P1 — Define scoring
Score(candidateMidi) = weighted sum of:
- pitchWeights[pc]
- chordTone bonus if pc ∈ active chord
- contour proximity toward peakPosition
- cadence target bonus near phrase ends
- stepwise preference / leap penalties
- chromatic penalties (bounded by caps)

Decision site fields:
- pitchWeights, chordTone bias, voiceLeadingRules, cadence targets, contour targets

Metrics:
- `pitch_class_histogram`
- `interval_histogram`
- `chord_tone_ratio`

### Stage P2 — Choose notes per onset
For each onset:
- enumerate MIDI candidates in range [minMidi,maxMidi] with pc ∈ legalPcs
- compute score
- choose best or soft-sample among top-K deterministically

### Stage P3 — Validate and repair
Validate:
- illegal pcs none
- leaps within maxLeap
- caps met (non-diatonic and non-chord-tone)

Repair/backtrack:
- local search on final phrase notes
- drop ornament notes (convert some onsets to rests) if allowed

---

## Minimum tests
- changing allowedPitchClasses changes histogram support set
- changing pitchWeights changes histogram probabilities (KL divergence)
- lowering maxLeap reduces large interval mass
- increasing chordTone bias increases chord_tone_ratio
