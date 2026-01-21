# Pane 07 — Harmony Language

## What this pane controls
Harmony defines chord progressions, cadence norms, and allowable chord colors (qualities/extensions/borrow).
This pane is the primary UI for `ResolvedControls.harmony.*`.

## Deterministic choices
### progressionTemplateId
- null/auto: choose from style library by weights
- explicit: pick a named template (e.g., I–V–vi–IV)

Audible must-move:
- changes progression archetype frequency and chord-change positions.

### harmonicRhythm
- slow: chords hold longer
- medium: typical
- fast: more chord changes per bar
Audible must-move:
- chord-change density shifts.

### functionTransitionsPresetId
- selects a transition “feel”:
  - functional_strict (classical-like)
  - pop_loop (stable loops)
  - modal_static (few dominant pushes)
Audible must-move:
- frequency of dominant-function events changes.

### chordQualitiesPresetId
- selects allowed chord colors:
  - triads_only
  - sevenths_common
  - extended_9_11_13
  - powerchords_sus
Audible must-move:
- chord_quality_histogram shifts.

### chromaticCapsPresetId
- caps for chromaticism:
  - strict_diatonic
  - light_borrow
  - medium_chromatic
  - heavy_chromatic (within style limits)
Audible must-move:
- non_diatonic_pitch_rate shifts.

### cadenceConstraintsPresetId
- cadence allowed types + strength bias:
  - strong_authentic (PAC favored)
  - half_cadence_friendly
  - avoid_cadence (ambient)
Audible must-move:
- cadence distribution shifts at phrase ends.

### userChordProgression (optional explicit)
- list of chord symbols or roman numerals with durations.
If provided:
- overrides template selection and function transitions (must still validate legality).

## Resolver handoff (must map)
Must affect:
- `ResolvedControls.harmony.functionTransitions`
- `ResolvedControls.harmony.progressionTemplates`
- `ResolvedControls.harmony.chordQualities`
- `ResolvedControls.harmony.chromaticCaps`
- `ResolvedControls.harmony.cadenceConstraints`
- optional: `ResolvedGrammar.harmonyGrammar` via style + overridePatch (pane 02)

## Generator decision sites (must move audio)
- HarmonyPlanner:
  - chooses template
  - generates function path
  - realizes chord qualities
  - places cadences
- PitchSelector uses chord-tone membership from HarmonyPlan.

## Must-move metrics
Must-move metrics:
- `progression_archetype_frequency`
- `chord_quality_histogram`
- `cadence_type_distribution_at_phrase_ends`
- `non_diatonic_pitch_rate`
- `chord_tone_ratio` (indirectly, by changing chord definitions)

## Common pitfalls / anti-patterns
- Letting explicit chords bypass cadence legality (breaks style).
- Template selected but harmonicRhythm ignored (no density change).
