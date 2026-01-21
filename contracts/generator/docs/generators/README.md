# Generator Documentation — MIND v9.14

Generated: 2026-01-13

This docset describes the **generator stage** that consumes:

- `ResolvedGrammar` (legality + vocab + typologies)
- `ResolvedControls` (frozen control surface)

…and produces **events** (notes/chords/beats) for playback/export.

## Read order
1. `00_shared_conventions.md`
2. `01_interfaces.md`
3. `10_harmony_planner.md`
4. `11_form_planner.md`
5. `12_rhythm_realizer.md`
6. `13_pitch_selector.md`
7. `14_motif_planner.md`
8. `15_performance_humanizer.md`
9. `16_part_assembler.md`
10. `20_validation_suite.md`
11. examples in `examples/`

### Execution order

The generator pipeline runs modules in a different order than the numbering of these documents. The execution order reflects data dependencies and should be used when reasoning about generator behavior:

1. **FormPlanner** (described in `11_form_planner.md`)
2. **HarmonyPlanner** (`10_harmony_planner.md`)
3. **RhythmRealizer** (`12_rhythm_realizer.md`)
4. **MotifPlanner** (`14_motif_planner.md`)
5. **PitchSelector** (`13_pitch_selector.md`)
6. **PerformanceHumanizer** (`15_performance_humanizer.md`)
7. **PartAssembler** (`16_part_assembler.md`)

The numbering of the files is historical and represents the documentation order rather than the runtime pipeline. Always refer to the execution order above when following the flow of data between modules.

## Architectural rule (PLC discipline)
Each generator is a **pure transform**:

**inputs → constraints → generate candidates → validate → repair/backtrack → output**

No “dead knobs”:
- every field in `ResolvedControls` must be referenced by at least one generator decision site
- any field not referenced must be removed or mapped to an implementation TODO
