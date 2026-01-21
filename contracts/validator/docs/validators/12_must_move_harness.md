# 12 — Must‑Move Harness

Purpose: enforce the “no dead knobs” rule by perturbing controls and measuring metric changes. Each row below defines a harness test: the control to perturb, how to perturb it, the metric to observe, and the expected direction/threshold of change. If the expected metric change falls below `minDelta`, a MUST_MOVE violation is reported.

| controlPath | perturbation | expectedMetric | minDelta | expectedDirection | testFixture | validator |
| --- | --- | --- | --- | --- | --- | --- |
| `ResolvedControls.pitch.pitchWeights` | Increase weight of a specific pitch class by +0.5 (renormalize) | `pitch_class_histogram` KL divergence; mass of that pitch class | 0.05; 0.03 for mass increase | + | fixed seed; 4‑bar melody; default style and profile | style_conformance and must_move validators |
| `ResolvedControls.pitch.voiceLeadingRules.maxLeap` | Decrease maxLeap from 12 to 5 semitones | `interval_histogram` mass in bins >5 semitones | 0.10 | – (decrease) | fixed seed; simple melodic line; default style | legality and must_move validators |
| `ResolvedControls.rhythm.microtimingProfile.swing` | Change swing from off to heavy | `swing_ratio` | 0.10 | + | fixed seed; 4/4 beat with medium density | style_conformance and must_move validators |
| `ResolvedControls.performance.velocityCurve.accentScale` | Increase accentScale from 0.8 to 1.2 | `accent_contrast` | 0.10 | + | fixed seed; medium‑intensity part; default accent model | style_conformance and must_move validators |
| `ResolvedControls.harmony.cadenceConstraints.allowedCadenceTypes` | Remove **PAC** from allowed set | `cadence_type_distribution_at_phrase_ends` (PAC count) | 100 % removal (count→0) | – (decrease) | fixed seed; 8‑bar form with explicit cadences | legality and must_move validators |

## Harness runner specification

- **Deterministic seed handling** – The harness uses the same RNG seed for baseline and perturbed runs to ensure only the control change affects the output.  
- **Fixtures** – Each test uses a simple, well‑defined thought (number of bars, default style/profile) appropriate for the control under test. The harness may run multiple fixtures (e.g., different time signatures) if a control affects different contexts.  
- **Failure reporting** – If the metric change between baseline and perturbed runs does not meet `minDelta` in the expected direction, the harness reports a MUST_MOVE violation with details of the control, perturbation, observed delta, and a suggestion for implementation.  
