# Resolver Documentation — MIND v9.14 (Theory-first)

Generated: 2026-01-13

This revision introduces a **two-layer compilation model**:

1) **ResolvedGrammar** (theory legality + vocabulary)
2) **ResolvedControls** (generator-ready controls derived *within* the grammar)

Think of it as:

- **Grammar** = “what is allowed / what counts as this style” (hard constraints + vocab)
- **Controls** = “what we will actually do this time” (weights, masks, plans, curves)

This separation prevents style from being “just a bag of knobs” and makes the resolver read
like music theory first, engineering second.

## Read order
1. `00_contract.md`
2. `01_sources.md`
3. `02_precedence.md`
4. `10_resolved_grammar.md`  ← new
5. `11_resolve_pipeline.md` ← new
6. `03_merge_operators.md`
7. `04_normalization.md`
8. `05_repair_policy.md`
9. `06_determinism.md`
10. `07_validation_hooks.md`
11. `08_trace_format.md`
12. Per-field specs in `fields/`
13. Worked cases in `cases/`

## Frozen control surface (unchanged IR)
You asked to freeze `ResolvedControls` groups as:

ResolvedControls:
  harmony: functionTransitions, progressionTemplates, chordQualities, chromaticCaps, cadenceConstraints
  rhythm: grid, onsetMask, accentModel, microtimingProfile
  pitch: allowedPitchClasses, pitchWeights, voiceLeadingRules
  form: phrasePlan, cadencePlan
  motif: motifReusePlan, transformPlan
  performance: timingVariance, velocityCurve

This revision does **not** change that freeze.
It adds **ResolvedGrammar** as the explicit “theory legality” layer that `ResolvedControls` must obey.
