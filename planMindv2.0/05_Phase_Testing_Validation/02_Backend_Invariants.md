# Backend Output Invariants (must always hold)

For every `thought.v0` returned by backend:

1. `schema_version == "thought.v0"`
2. `sequence` sorted by time ascending
3. Every event:
   - `time` matches regex: `^\d+:\d+:\d+$`
   - `type` is allowed
   - if note: midi 0..127, velocity 0..1
4. No more than one note per time slot per Thought (PoC rule)
5. Loop length matches meta.loop_bars and meta.division

These invariants should be covered by unit tests.

