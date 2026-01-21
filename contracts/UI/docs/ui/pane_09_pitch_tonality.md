# Pane 09 — Pitch / Tonality

## What this pane controls
Controls pitch legality and pitch tendencies: allowed pitch classes, chord-tone anchoring, cadence targeting, and voice-leading constraints.

## Deterministic choices
### tonalCenterPolicy
- inherit: use upstream key/center
- override: user sets center (via scaleOverride or explicit tonal center)

### scaleOverride
- null: use style/profile defaults (and harmony-implied)
- explicit scale: major, natural_minor, dorian, mixolydian, phrygian, blues, pentatonic, harmonic_minor, melodic_minor

Audible must-move:
- allowedPitchClasses change → different pitch-class histogram.

### chordToneStrength
- low: more non-chord tones, floaty lines
- medium: balanced
- high: strong chord-tone anchoring

### nonChordToneRateMax
- 0..1 (cap)
Audible must-move:
- reduces embellishments when lowered.

### nonDiatonicRateMax
- 0..1 (cap)
Audible must-move:
- borrowed/chromatic notes reduce when lowered.

### cadenceTargets
- enabled: true/false
- targets: tonic|mediant|dominant|leading_tone|fifth
- strength: soft|medium|strong
- applyAt: phrase_end|section_end|every_4_bars

Audible must-move:
- phrase endings land more often on target scale degrees.

### range.minMidi / range.maxMidi
Audible must-move:
- shifts register band.

### voiceLeading
- maxLeap: integer semitones
- preferStepwise: bool
- resolveLeadingTone: bool
Audible must-move:
- interval histogram shifts; leading tone resolution success increases.

## Resolver handoff (must map)
Must affect:
- `ResolvedControls.pitch.allowedPitchClasses`
- `ResolvedControls.pitch.pitchWeights`
- `ResolvedControls.pitch.voiceLeadingRules`
- `ResolvedControls.harmony.chromaticCaps` (caps cross-check)
- `ResolvedControls.form.cadencePlan` / pitch cadence targeting policy

## Generator decision sites (must move audio)
- PitchSelector uses these to choose MIDI notes.
- HarmonyPlanner provides chord membership, which chordToneStrength uses.
- FormPlanner provides phrase ends for cadence targets.

## Must-move metrics
Must-move metrics:
- `pitch_class_histogram`
- `chord_tone_ratio`
- `non_diatonic_pitch_rate`
- `interval_histogram`
- `leading_tone_resolution_rate` (if tracked)

## Common pitfalls / anti-patterns
- Setting caps but generator ignores them (chromatic notes still appear).
- range set narrower but melody still exceeds maxMidi (validator missing).
