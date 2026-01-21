# UI Pane Readme — Thought Editor (14 Panes) — MIND v9.14

Generated: 2026-01-13

This zip is **UI-only**: it defines what the user sees, chooses, and what each choice must change **audibly**.
It also names the **resolver handoff**: which `ResolvedGrammar` / `ResolvedControls` fields each UI choice must influence.

## Read order
1. `field_index.md` (canonical pane→field grouping)
2. Pane files in order:
   - `pane_01_identity.md`
   - `pane_02_style_family_and_variant.md`
   - `pane_03_profile_bias.md`
   - `pane_04_bars_meter_tempo_type.md`
   - `pane_05_form_and_phrasing.md`
   - `pane_06_role.md`
   - `pane_07_harmony_language.md`
   - `pane_08_figuration_patterns.md`
   - `pane_09_pitch_tonality.md`
   - `pane_10_rhythm_placement.md`
   - `pane_11_register_tessitura.md`
   - `pane_12_contour_macroshape.md`
   - `pane_13_motif_variation.md`
   - `pane_14_performance_and_rendering.md`

## “No dead knobs” rule
Every choice in every pane must:
- map to at least one resolver output field (ResolvedGrammar or ResolvedControls)
- and have at least one **must-move** metric (see resolver metrics) that changes when the choice changes.

If a choice cannot guarantee an audible change, it must be removed or flagged `EXPERT_ONLY` with clear impact limits.
