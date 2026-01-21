# Validator Documentation — MIND v9.14

Generated: 2026-01-13

This docset describes the **validator stage** that runs after generation (and optionally during generation as a candidate filter).

Validators consume:
- `ResolvedGrammar`
- `ResolvedControls`
- `GeneratedPart` (events + traces + metrics)

Validators produce:
- `ValidationReport` (errors/warnings + must-move outcomes + suggested repairs)
- optional: `ValidationMetrics` (standardized computed metrics)

## Read order
1. `00_shared_conventions.md`
2. `01_validator_interfaces.md`
3. `10_legality_validators.md`
4. `11_style_conformance_validators.md`
5. `12_must_move_harness.md`
6. `13_determinism_validator.md`
7. `14_arrangement_conflict_validators.md`
8. `15_music21_analysis_hooks.md`
9. examples in `examples/`

## Core rule (PLC discipline)
Validation is not “opinion.” It is a set of deterministic checks that:
- enforce **legality** (grammar + controls)
- enforce **audible intent** (must-move metrics)
- enforce **stability** (determinism, freeze behavior)
