# Resolver Field Spec — harmony (Theory-first)

This file specifies how we compile:
- **HarmonyGrammar** (theory legality/vocabulary)
- **HarmonyControls** (the frozen control surface in ResolvedControls.harmony)

It is intentionally written in theory terms first.

---

## A) HarmonyGrammar (ResolvedGrammar.harmonyGrammar)

### A1) Function state machine
**Theory object:** tonic (T), predominant (PD), dominant (D) function categories with transition probabilities.

**Resolver intent:**
- Style defines the legal function vocabulary and default transition tendencies.
- Variant refines transitions (e.g., “more dominant prolongation”).
- Pane edits can only tighten or select presets in locked/simple.

**Compilation:**
- Start: styleFamily functionStateMachine
- Apply: styleVariant deltas
- Apply: upstream grammar if inheritFromUpstream=true (as a default)
- Expert: may edit transition edges; rows renormalized

**State definitions and semantics**

The function state machine formalizes tonic (T), predominant (PD) and dominant (D) functions as discrete states in a Markov model:

- **T** (Tonic) – points of tonal rest, typically chords built on the tonic scale degree. A return to **T** provides resolution.
- **PD** (Predominant) – harmonies that prepare the dominant, such as ii or IV chords. PD functions connect T and D.
- **D** (Dominant) – harmonies that create tension and lead back to T, including V and vii° chords.

Transition weights describe the relative likelihood of moving from one function to another. After compilation and any numeric edits, each row is renormalized so the probabilities for transitions out of a state sum to 1 and no value is negative. This normalization ensures the state machine functions as a proper probability distribution and captures stylistic tendencies (e.g., high T→PD weight in classical styles).

**Hard invariants:**
- states include [T, PD, D]
- each row sums to 1 (after normalization)
- no negative probabilities

### A2) Progression template library
**Theory object:** progression archetypes expressed as roman numerals (I–V–vi–IV, etc.),
plus a harmonic-rhythm model (how often chords change).

**Resolver intent:**
- Style supplies a library; variant adds/removes or retags archetypes.
- Pane may choose among templates; in locked/simple it may not invent new templates.

**Hard invariants:**
- template ids are unique
- templates reference allowed chord vocabulary

### A3) Chord vocabulary
**Theory object:** which chord qualities/extensions/alterations are legal.

**Compilation rules:**
- allowedQualities: intersection in locked/simple (cannot widen)
- maxExtension: min() in locked/simple
- alterationsAllowed: AND in locked/simple
- modalInterchangeAllowed / secondaryDominantsAllowed: style-defined in locked/simple

### A4) Cadence typology + placement norms
**Theory object:** cadence types (PAC/IAC/HC/DC/plagal/etc.) and where cadences are expected/required.

**Compilation rules:**
- allowedCadences: intersection in locked/simple
- requiredAtPhraseEnd: OR (if any layer requires it, it is required)
- cadence windows: tighter wins (min barsFromEnd)

**Cadence label definitions**

Cadence labels in this system have precise meanings:

- **PAC (Perfect Authentic Cadence)** – dominant (V) chord resolving to tonic (I) with the tonic scale degree in the highest voice. Yields the strongest sense of closure.
- **IAC (Imperfect Authentic Cadence)** – dominant–tonic motion without the tonic in the top voice or with the tonic inverted. Provides softer resolution.
- **HC (Half Cadence)** – phrase ending on the dominant harmony (V); feels open and invites continuation.
- **DC (Deceptive Cadence)** – dominant (V) resolving deceptively to vi (or another submediant function) instead of tonic; surprises the listener.
- **Plagal** – subdominant (IV) moving to tonic (I); sometimes called the “Amen” cadence.
- **Avoided** – progressions where an expected cadence motion is elided (e.g., V–vi) but still implies a cadence.
- **Modal** – cadence conventions derived from modal systems (e.g., Mixolydian ♭VII–I).

`cadenceConstraints` in `ResolvedControls.harmony.cadenceConstraints` select a subset of these labels and can bias their relative strengths. Controls may not add cadences that are illegal under the grammar in locked or simple modes.

### A5) Chromatic policy (non-diatonic behavior)
**Theory object:** allowed types of non-chord tones and upper bounds on chromatic usage.

**Compilation rules:**
- caps: min() always
- allowedNCTTypes: intersection in locked/simple

**Chromatic note definitions and caps**

“Chromatic” notes are non‑diatonic pitch classes relative to the prevailing scale or harmony. Caps impose upper bounds on chromatic usage over different time horizons:

- **nonChordToneRateMax** – the maximum fraction of notes within a bar or phrase that may be non‑chord tones (passing, neighbor, suspension, anticipation, appoggiatura, etc.).
- **nonDiatonicPitchRateMax** – the maximum fraction of notes that fall outside the diatonic scale in a bar or phrase.
- **approachToneRateMax** – the maximum fraction of notes that function solely as approach tones leading into chord tones.

These rates are applied per bar, per phrase, and across the entire thought, with the strictest cap prevailing. For example, a `nonDiatonicPitchRateMax` of 0.1 means that in any bar or phrase, no more than 10 % of notes may be non‑diatonic.

---

## B) HarmonyControls (ResolvedControls.harmony.*)

These are the frozen generator controls derived *within* HarmonyGrammar.

### 1) ResolvedControls.harmony.functionTransitions
Derived from HarmonyGrammar.functionStateMachine, possibly with user preset selection.

- locked/simple: user selects among style-provided presets; no numeric edits
- expert: numeric edits allowed; rows renormalized

### 2) ResolvedControls.harmony.progressionTemplates
Derived from HarmonyGrammar.progressionTemplateLibrary.

- templates list: from grammar library
- weights: blended preferences (style/profile/user), then normalized
- illegal templates (not in grammar library): dropped in locked/simple

### 3) ResolvedControls.harmony.chordQualities
Derived from HarmonyGrammar.chordVocabulary.

- allowedQualities: grammar legality
- maxExtension: grammar legality
- alterationsAllowed: grammar legality
User can tighten (subset) in locked/simple.

### 4) ResolvedControls.harmony.chromaticCaps
Derived from HarmonyGrammar.chromaticPolicy.caps (min across contributors).

### 5) ResolvedControls.harmony.cadenceConstraints
Derived from HarmonyGrammar.cadenceTypology.
Controls can bias cadence strength or choose among allowed cadence types, but cannot add illegal cadences in locked/simple.

---

## C) Audible “must move” invariants (tests)
Minimum test expectations:
- Changing chordVocabulary changes chord-quality histogram (maj7/dom7/sus usage)
- Tightening chromatic caps lowers non-diatonic pitch rate
- Changing progression template weights changes progression archetype frequency
- Changing cadence typology changes cadence type distribution at phrase ends

---

## D) Generator guarantees
- Every cadence type referenced in controls is legal under grammar
- No empty chord vocabulary
- All weights normalized, all caps bounded
