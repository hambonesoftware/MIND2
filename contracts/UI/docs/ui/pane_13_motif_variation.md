# Pane 13 — Motive & Variation

## What this pane controls
Controls reuse and transformation of material across phrases.
This is the “compositional memory” pane.

## Deterministic choices
### scheme
- AAAA: same motif repeated each phrase
- AABA: A repeated with B contrast
- ABAC: A returns; B and C contrasts
- evolving: gradual drift

Audible must-move:
- repeated phrases share recognizable interval/rhythm cells when reuse is high.

### variation
- none | small | medium | large
Audible must-move:
- degree of change between repeats (ornamentation, transposition, rhythmic tweaks).

### repeatStrength
- high | medium | low
Audible must-move:
- motif_similarity metric increases with higher repeatStrength.

### transformAllow
- transpose: shift pitch level while retaining shape
- invert: flip interval directions
- augment: longer durations
- diminish: shorter durations
- fragment: use subset of motif

Audible must-move:
- transform_usage changes; similarity vs contrast shifts by scheme.

## Resolver handoff (must map)
Must affect:
- `ResolvedControls.motif.motifReusePlan`
- `ResolvedControls.motif.transformPlan`
- style grammar transform caps (from pane 02) constrain what’s allowed

## Generator decision sites (must move audio)
- MotifPlanner chooses motif cells and transformations.
- PitchSelector and RhythmRealizer may instantiate motif cells at pitch/rhythm level.

## Must-move metrics
Must-move metrics:
- `motif_similarity` (phrase-to-phrase)
- `transform_usage_histogram` (optional)
- `onset_ngram_stability` (when motif includes rhythm)

## Common pitfalls / anti-patterns
- Scheme selected but generator still produces unrelated phrases (dead motif).
- TransformAllow includes invert but no inversion ever appears (dead transform).
