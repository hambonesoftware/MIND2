# Heuristic Generator (PoC)

## Inputs
- Intent:
  - pattern offsets
  - modifiers (density, vel, seed, etc.)
- Style Profile:
  - interval gravity, voicing spread, mute probability, etc.
- Context (optional in PoC):
  - tempo
  - harmonic anchor pitch (midi)
  - role (bass vs lead)

## Output
A `Thought` sequence: list of time-stamped events.

## Time grid
PoC default:
- time signature: 4/4
- division: 16 steps per bar (16th notes)
- bar length: 16 slots

## Basic algorithm (v0)

1. **Resolve parameters**:
   - start from profile defaults
   - apply DSL overrides (dens, vel, slap, sync, oct, seed)
2. **Select anchor pitch**:
   - PoC default anchor: MIDI 60 (C4) unless provided
   - apply octave offset
3. **Create a slot plan** (0..15):
   - choose slots based on `note_density`
   - optionally apply `syncopation` by shifting some chosen slots
4. **Emit events**:
   - for each chosen slot:
     - pick next pattern value
     - apply “interval gravity” by occasionally pulling toward smaller steps
     - map to MIDI pitch (anchor + offset)
     - choose velocity from:
       - base velocity curve + accent_strength + vel scalar
     - emit note event with optional duration (e.g., one slot)
   - between notes, emit mutes based on `mute_probability`
5. **Normalize & validate**:
   - ensure time strings are valid
   - ensure midi in 0..127
   - ensure velocities consistent

## Deterministic output
- Use `seed` to seed RNG
- Avoid Python global RNG bleed; use local `random.Random(seed)` instance

## Role-based behavior (optional but recommended in PoC)
If `role=bass`:
- clamp pitches to lower register
- prioritize roots/5ths
If `role=lead`:
- allow higher register
- prefer extensions and stepwise motion when gravity high

