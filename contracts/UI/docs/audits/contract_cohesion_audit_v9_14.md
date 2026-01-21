# Contract Cohesion Audit — MIND v9.14

## Overview

This audit enumerates the `ResolvedControls.*` and `ResolvedGrammar.*` paths referenced across the UI, resolver, generator and validator documentation for MIND v9.14. It highlights mismatches that were resolved in this update and provides a short changelog and proof that there are no “dead knobs”.

## ResolvedControls paths referenced

The following canonical control paths are mentioned across the docsets:

* `ResolvedControls.harmony.functionTransitions`
* `ResolvedControls.harmony.progressionTemplates`
* `ResolvedControls.harmony.chordQualities`
* `ResolvedControls.harmony.chromaticCaps`
* `ResolvedControls.harmony.cadenceConstraints`
* `ResolvedControls.rhythm.grid`
* `ResolvedControls.rhythm.onsetMask`
* `ResolvedControls.rhythm.accentModel`
* `ResolvedControls.rhythm.microtimingProfile`
* `ResolvedControls.pitch.allowedPitchClasses`
* `ResolvedControls.pitch.pitchWeights`
* `ResolvedControls.pitch.voiceLeadingRules`
* `ResolvedControls.form.phrasePlan`
* `ResolvedControls.form.cadencePlan`
* `ResolvedControls.motif.motifReusePlan`
* `ResolvedControls.motif.transformPlan`
* `ResolvedControls.performance.timingVariance`
* `ResolvedControls.performance.velocityCurve`

## ResolvedGrammar paths referenced

The grammar references include:

* `ResolvedGrammar.harmonyGrammar.functionStateMachine`
* `ResolvedGrammar.harmonyGrammar.progressionTemplateLibrary`
* `ResolvedGrammar.harmonyGrammar.chordVocabulary`
* `ResolvedGrammar.harmonyGrammar.cadenceTypology`
* `ResolvedGrammar.harmonyGrammar.chromaticPolicy`
* `ResolvedGrammar.rhythmGrammar.meter`
* `ResolvedGrammar.rhythmGrammar.gridPolicy`
* `ResolvedGrammar.rhythmGrammar.onsetLegality`
* `ResolvedGrammar.rhythmGrammar.accentGrammar`
* `ResolvedGrammar.rhythmGrammar.grooveTemplates`
* `ResolvedGrammar.pitchGrammar.scaleVocabulary`
* `ResolvedGrammar.pitchGrammar.voiceLeadingHardRules`
* `ResolvedGrammar.formGrammar.phraseGrammar`
* `ResolvedGrammar.formGrammar.cadencePlacementNorms`
* `ResolvedGrammar.formGrammar.sectionArchetypes`
* `ResolvedGrammar.motifGrammar.allowedTransforms`
* `ResolvedGrammar.motifGrammar.transformMagnitudeCaps`
* `ResolvedGrammar.motifGrammar.reuseExpectations`
* `ResolvedGrammar.performanceGrammar.humanizationBounds`
* `ResolvedGrammar.performanceGrammar.articulationNorms`

## Mismatches and resolutions

* **microtimingProfile location** – Some documents referred to `ResolvedControls.performance.microtimingProfile`. This update resolves the mismatch by placing microtiming exclusively under `ResolvedControls.rhythm.microtimingProfile` and updating all references accordingly. A compatibility note explains how legacy fields are remapped.

* **Missing mapping tables** – The pane‑to‑controls and controls‑to‑generator mapping documents were previously stubs. They are now fully populated with tables that map UI fields to grammar and controls, and controls to generator stages and metrics.

* **Validator placeholders** – The must‑move harness document contained placeholders. It has been replaced with a concrete harness table and runner specification.

* **Generator ordering confusion** – The generator README now distinguishes between documentation order and execution order.

* **Theory definitions** – Additional formal definitions were added for function transitions, cadence labels, voice‑leading semantics and chromatic caps to strengthen the theory-first approach.

## Changelog

* Updated UI pane 14 and field index to map `thought.performance.microtimingProfile` to `ResolvedControls.rhythm.microtimingProfile` and added a compatibility note.
* Added compatibility notes to resolver rhythm and performance field specs.
* Expanded harmony and pitch field specs with formal definitions for function transitions, cadence labels, voice‑leading semantics and chromatic caps.
* Filled `docs/mappings/pane_to_grammar_controls.md` and `docs/mappings/grammar_controls_to_generators.md` with complete tables.
* Added execution order clarification to generator README.
* Replaced must‑move harness document with a tabular specification and harness runner spec.
* Added canonical schema file defining ThoughtSpec, ResolvedControls, ResolvedGrammar, GeneratedPart and ValidationReport shapes.

## No Dead Knobs Proof Summary

Every UI‑exposed control field now maps to at least one entry in `ResolvedControls` or influences grammar selection. The generator mapping table shows that every control path is read by at least one generator decision site or validator metric. The must‑move harness provides explicit tests for representative controls to ensure that perturbing a control yields a measurable change in output metrics. Together, these artefacts demonstrate that there are no dead knobs in the v9.14 MIND processing chain.