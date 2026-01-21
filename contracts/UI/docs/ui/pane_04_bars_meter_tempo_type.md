# Pane 04 — Bars, Meter, Tempo, Type

## What this pane controls
Defines the container length and the Thought’s role category (melody/harmony/bass/beat/texture/setup).
This pane is the “Form container”: it sets the timeline for all downstream plans.

## Deterministic choices
### bars
- integer >= 1
Audible must-move:
- more bars => longer generated material (more events), more phrase opportunities.

### meterOverride (optional)
- examples: 4/4, 3/4, 6/8, 12/8
Audible must-move:
- changes beat hierarchy and accent expectations, and changes how syncopation is computed.

### tempoOverrideBpm (optional)
- float, e.g., 60–200
Audible must-move:
- changes absolute timing and feel; microtiming jitter in ms may clamp differently.

### seed
- integer
Audible must-move:
- changes exact chosen candidates while preserving the same constraints.

### thoughtType
- setup | melody | harmony | bass | beat | texture

Per-type expectations:
- setup: outputs context objects only; may output no events
- melody: creates lead/counter lines (NoteEvents)
- harmony: creates chord events and/or comp textures
- bass: creates low anchor line; strong chord-root relation
- beat: creates BeatEvents; pocket/backbeat clarity
- texture: pads/arps/noise layers (density and articulation differ)

## Resolver handoff (must map)
Must affect:
- `ResolvedControls.form.phrasePlan.totalBars`
- `ResolvedControls.rhythm.grid` default and allowed range (some types constrain grid)
- generator pipeline selection:
  - beat type uses Beat generator path heavily
  - harmony type prioritizes HarmonyPlanner
  - texture type allows longer durations and simpler pitch movement

## Generator decision sites (must move audio)
- FormPlanner consumes bars/meter.
- RhythmRealizer uses meter/grid.
- PitchSelector uses register defaults by type (bass low, melody higher).
- PartAssembler routes events to different parts based on thoughtType.

## Must-move metrics
Must-move metrics:
- `event_count` scales with bars
- `syncopation_index` reference frame changes with meter
- `tempo_bpm` changes rendered duration

## Common pitfalls / anti-patterns
- Bars changed but generators still only output 1 bar (bug).
- Meter override not propagated to rhythm grammar (syncopation becomes meaningless).
