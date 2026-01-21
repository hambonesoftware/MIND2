# Backlog (post-PoC) — v2.x

## Musical improvements
- Scale/mode support: `scale:major`, `mode:dorian`
- Chord/harmonic anchor integration
- Multi-bar patterns and polymeter
- Groove templates / swing / humanization
- Multi-note chords per time slot (polyphonic Thought events)

## UI improvements
- Dedicated Transport node (tempo, play/pause, loop length)
- Per-node instrument selection
- Visual timeline preview inside node
- Preset library for DSL snippets

## Backend improvements
- Real AST parser (PEG/parsimonious/lark)
- Better voice leading rules
- Advanced conflict resolution (voice separation, chord inference)

## Persistence
- Save/load patch graph and node states
- Export to MIDI

