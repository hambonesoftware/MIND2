# Pane 02 — Style Family & Variant (Grammar)

## What this pane controls
Style chooses the **music grammar**: what harmony/rhythm/pitch practices are legal and typical.
This pane primarily defines **ResolvedGrammar** and sets defaults for ResolvedControls.

## Deterministic choices
### inheritFromUpstream
- true: use nearest upstream Style as defaults (unless overridden here)
- false: Style set explicitly in this Thought

Audible impact:
- true: cohesive “same world” across connected Thoughts
- false: allows scene-change (genre shift)

### styleFamilyId (starter families)
- pop | rock | jazz | classical | electronic | hiphop | ambient | folk | latin
Audible must-move:
- changes chord vocabulary norms, rhythmic feel defaults, motif repetition expectations.

### styleVariantId (examples)
- pop_modern | pop_ballad | pop_80s | pop_acoustic
- rock_classic | rock_hard | rock_alt | rock_punk | rock_ballad
- jazz_swing | jazz_bebop | jazz_modal | jazz_fusion | jazz_ballad
- classical_common_practice | classical_baroque | classical_romantic | classical_modern
- electronic_house | electronic_techno | electronic_dnb | electronic_ambient
- hiphop_boom_bap | hiphop_trap | hiphop_lofi
- ambient_drone | ambient_textural
- folk_trad | folk_modern | folk_ballad
- latin_bossa | latin_samba | latin_reggaeton

### allowOverrides (expert)
- false: derived grammar is authoritative; UI panes can only operate within it.
- true: enable overridePatch (below)

### overridePatch (expert)
- Partial overrides to derived grammar defaults (NOT arbitrary):
  - allowed cadence types subset
  - chromatic caps tightening/loosening
  - allowed chord qualities subset
  - groove template selection subset

## Resolver handoff (must map)
Must produce/affect:
- `ResolvedGrammar.harmonyGrammar` (chord vocab, cadence typology, function grammar)
- `ResolvedGrammar.rhythmGrammar` (groove templates, accent grammar, swing legality)
- `ResolvedGrammar.pitchGrammar` (scale vocabulary, borrowed-tone permissions)
- `ResolvedGrammar.motifGrammar` (reuse expectations, allowed transforms)
- `ResolvedGrammar.performanceGrammar` (humanization bounds and norms)
- Default fill of `ResolvedControls.*` when user didn’t override panes 05–14.

If overridePatch used:
- must be applied BEFORE generating ResolvedControls so controls remain consistent with grammar.

## Generator decision sites (must move audio)
- HarmonyPlanner reads grammar vocab + cadence typology.
- RhythmRealizer reads groove templates and accent grammar.
- PitchSelector reads scale vocabulary and chromatic policy.
- MotifPlanner reads reuse expectations/allowed transforms.
- PerformanceHumanizer reads humanization bounds.

Changing styleFamilyId must measurably shift these decision sites.

## Must-move metrics
Must-move metrics (examples):
- `chord_quality_histogram` (jazz vs pop differs)
- `chromatic_approach_rate` / `non_diatonic_pitch_rate`
- `swing_ratio` (jazz_swing vs rock)
- `backbeat_strength` (rock/hiphop vs classical)
- `motif_similarity` expectations (pop higher than ambient)

## Common pitfalls / anti-patterns
- Treating Style as “just a label” (dead knob). Style must change grammar + defaults.
- Letting overridePatch break grammar invariants (e.g., allow a cadence type that grammar removed).
