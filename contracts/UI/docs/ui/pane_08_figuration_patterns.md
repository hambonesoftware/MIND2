# Pane 08 — Figuration / Patterns

## What this pane controls
Figuration selects *how* notes are laid out (riff, arpeggio, strum, walking bass, etc.).
This pane is the “pattern family” knob with parameterized variants.

## Deterministic choices
### patternFamilyId (examples)
- melody: scalar_run | pentatonic_hook | chord_tone_motif | blues_riff | ornamented_line
- harmony: block_chords | arpeggio | strum | broken_chord | ostinato
- bass: root_fifth | walking | pedal | octave_pulse | funk_sync
- beat: backbeat_rock | boom_bap | trap_hats | four_on_floor | bossa_groove
- texture: pad_sustain | shimmer_arp | drone | pulsing_8ths

### patternVariantId
A named variant within family, e.g.:
- strum_downup_16ths
- arpeggio_updown
- walking_quarter_notes

### intensity
- low: fewer notes / simpler pattern
- medium: default
- high: more subdivisions/ornaments

### params (pattern-specific)
Examples:
- `arpDirection`: up|down|updown|random
- `strumSpreadMs`: 0..30
- `riffRepetition`: low|med|high
- `ghostNoteRate`: 0..0.3
Audible must-move:
- changes onset n-grams and note density patterns.

## Resolver handoff (must map)
Must affect:
- `ResolvedControls.rhythm.onsetMask` (pattern implies allowable onset shapes)
- `ResolvedControls.motif.motifReusePlan` (riff repetition)
- optional: `ResolvedControls.pitch.pitchWeights` (pattern families can bias pentatonic, etc.)

## Generator decision sites (must move audio)
- RhythmRealizer should use pattern family to seed onset templates.
- MotifPlanner uses riff repetition to set scheme/reuse.
- PitchSelector uses family constraints for interval shapes (e.g., walking bass prefers stepwise).

## Must-move metrics
Must-move metrics:
- `onset_ngram_stability` (riff/ostinato higher)
- `density` and `rest_ratio`
- `interval_histogram` (walking bass stepwise vs riff leapy)

## Common pitfalls / anti-patterns
- Pattern selected but onset generation remains generic (dead figuration).
- Intensity changes but event_count unchanged (dead intensity).
