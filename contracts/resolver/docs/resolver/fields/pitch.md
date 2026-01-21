# Resolver Field Spec — pitch (Theory-first)

This file specifies compilation of:
- **PitchGrammar** (legal pitch materials + voice-leading hard rules)
- **PitchControls** (ResolvedControls.pitch.*)

---

## A) PitchGrammar (ResolvedGrammar.pitchGrammar)

### A1) Scale vocabulary / mode space
**Theory object:** allowed scale/mode families and their pitch-class sets.

**Compilation:**
- styleFamily defines allowedScales and base pitch-class legality
- styleVariant refines (e.g., mixolydian tolerance in rock)
- pane can only tighten allowedScales in locked/simple

**Hard invariants:**
- allowedScales non-empty
- base allowedPitchClasses non-empty

### A2) Chord-tone vs non-chord-tone policy
**Theory object:** chord-tone anchoring and non-chord tone taxonomy bounds.

This is partly harmony-driven:
- harmony.chromaticPolicy + chordVocabulary influence what non-diatonic behavior is legal

**Compilation rules:**
- chordToneStrengthRange is style-defined
- tendency-tone mappings are style-defined (leading tone resolution, 4→3/5 norms)
- in locked/simple, user may only choose chordToneStrength (low/med/high) and cannot violate caps

### A3) Voice-leading hard rules
**Theory object:** constraints that define what “good” voice leading means in a style:
- maximum leaps
- parallel perfect constraints
- spacing rules (optional, texture-dependent)

**Compilation rules:**
- maxLeapSemitonesMax: min() in locked/simple
- parallelPerfectsForbidden: style-defined in locked/simple
- spacingRules: style-defined in locked/simple; expert may override if enabled

**Voice-leading semantics**

Voice-leading rules define what is absolutely forbidden and what is merely discouraged:

- **Hard illegal** – leaps that exceed `maxLeapSemitonesMax` semitones or parallel perfect fifths/octaves when `parallelPerfectsForbidden` is true. Such motions must not appear in the generated melody or will be repaired.
- **Soft penalized** – large leaps that are within the maximum are discouraged relative to stepwise motion or small intervals; the pitch selector assigns them lower scores but does not forbid them entirely.
- **Spacing rules** – optional constraints that require simultaneous voices to maintain minimum and maximum intervals between them. If specified by the grammar, these are enforced strictly in locked/simple modes.

Generators should treat hard rules as inviolable and soft rules as preferences in their scoring functions.

---

## B) PitchControls (ResolvedControls.pitch.*)

### 1) ResolvedControls.pitch.allowedPitchClasses
Controls select a specific legal pitch-class set *within* scale vocabulary.

- locked/simple: subset of grammar legality (intersection)
- expert: may widen only if policy allows (v9.14 default: no widening)

### 2) ResolvedControls.pitch.pitchWeights
Controls are *preferences* over legal pitch classes.

- illegal pitch classes get zero weight in locked/simple
- weights normalized to sum=1
- chordToneBias mode maps to target chord-tone ratio (unless expert overrides)

### 3) ResolvedControls.pitch.voiceLeadingRules
Controls may tighten hard rules (smaller leaps, narrower register range) and set “soft preferences”.
They may not violate grammar hard caps in locked/simple.

---

## C) Audible “must move” invariants (tests)
- allowedPitchClasses change shifts pitch-class histogram
- pitchWeights change shifts probability of scale degrees / pcs
- maxLeap changes interval histogram (fewer large intervals)
- register range changes mean MIDI pitch and variance
- chordToneBias changes chord-tone ratio in output

---

## D) Generator guarantees
- non-empty legal pcs set
- all weight mass on legal pcs
- voice-leading rules ranges coherent
