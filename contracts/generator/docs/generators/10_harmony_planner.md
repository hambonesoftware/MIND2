# 10 — HarmonyPlanner

## Purpose
Produce a **HarmonyPlan** (chord timeline + cadences) that:
- satisfies HarmonyGrammar legality (vocab + cadence typology + chromatic caps)
- follows FormPlan cadence windows
- matches style/profile biases and pane preferences

## Inputs (fields used)
### Controls
- `ResolvedControls.harmony.functionTransitions`
- `ResolvedControls.harmony.progressionTemplates`
- `ResolvedControls.harmony.chordQualities`
- `ResolvedControls.harmony.chromaticCaps`
- `ResolvedControls.harmony.cadenceConstraints`
- `ResolvedControls.form.cadencePlan` (if user authored explicit cadence events)

### Grammar consulted
- `ResolvedGrammar.harmonyGrammar.functionStateMachine`
- `ResolvedGrammar.harmonyGrammar.progressionTemplateLibrary`
- `ResolvedGrammar.harmonyGrammar.chordVocabulary`
- `ResolvedGrammar.harmonyGrammar.cadenceTypology`
- `ResolvedGrammar.harmonyGrammar.chromaticPolicy`
- `ResolvedGrammar.formGrammar.cadencePlacementNorms` (optional)

## Output
- `HarmonyPlan` (see `contracts/HarmonyPlan.schema.json`)

---

## Algorithm (constraint → generate → validate)

### Stage H0 — Establish harmonic clock
Decision: how often chords may change (harmonic rhythm)
Decision sources:
- progression template harmonic rhythm model
- style defaults
- profile bias (ballad => slower)

Audible must move:
- cadence placement patterns
- chord-change density

### Stage H1 — Choose progression template(s)
If `progressionTemplates.selectedId` is set:
- choose it (validate in grammar library)
Else:
- sample deterministically from template weights

Decision site fields:
- `ResolvedControls.harmony.progressionTemplates.weights`
Metric:
- `progression_archetype_frequency`

### Stage H2 — Generate function path (T/PD/D)
Use:
- function transition matrix (controls, within grammar)
Generate a function label per chord slot.

Decision site fields:
- `ResolvedControls.harmony.functionTransitions`
Metric:
- `function_path_statistics` (optional)

### Stage H3 — Realize roman numerals into chord roots/qualities
Constraints:
- chordVocabulary legality (qualities/extensions/alterations)
- chordQualities selections (subset)
- chromatic caps (upper bounds on non-diatonic borrow rate)

Decision site fields:
- `ResolvedControls.harmony.chordQualities.*`
- `ResolvedControls.harmony.chromaticCaps.*`
Metrics:
- `chord_quality_histogram`
- `non_diatonic_pitch_rate`

### Stage H4 — Place cadences
Respect:
- cadence typology allowed set
- required-at-phrase-end constraint
- cadence windows (phrase_end/section_end)

If `ResolvedControls.form.cadencePlan` exists:
- validate and repair (drop illegal cadence types, insert required ones)

Else:
- choose cadence events from `ResolvedControls.harmony.cadenceConstraints` bias.

Decision site fields:
- `ResolvedControls.harmony.cadenceConstraints`
Metrics:
- `cadence_type_distribution_at_phrase_ends`
- `cadence_success_rate`

### Stage H5 — Validate + repair
Validators:
- cadence types allowed
- chord qualities legal
- plan covers whole thought

Repairs:
- replace illegal chord quality with nearest legal (style default)
- insert cadence at phrase end if missing (deterministic)

Trace:
- record every repair with before/after

---

## Decision Sites (No-dead-knobs map)
1) Template selection ← `progressionTemplates`
2) Function flow ← `functionTransitions`
3) Chord quality set ← `chordQualities`
4) Cadence choice/strength ← `cadenceConstraints`
5) Chromatic bounds ← `chromaticCaps`

---

## Minimum tests (must pass)
- Changing `progressionTemplates.weights` changes progression archetype frequency
- Tightening `chordQualities.allowedQualities` removes those qualities from histogram
- Tightening allowed cadences removes illegal cadence types and triggers repair with trace
