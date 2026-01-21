# Pane 01 — Identity

## What this pane controls
Identity is metadata and lifecycle control. It should not “compose” music, but it **must** affect playback deterministically via enable/freeze semantics.

## Deterministic choices
### thoughtId
- Type: string (UUID or stable hash)
- Deterministic effect: used as part of subseed derivation so reordering nodes doesn’t change audio.

### label
- Type: string
- Audible effect: none (UI only). Must not affect generation.

### enabled
- true: this Thought contributes events to playback.
- false: this Thought contributes no events.
- Audible must-move: silence vs sound for this node output.

### frozen
- true: resolver and generators must treat this Thought as “locked”: no regeneration occurs unless explicitly forced.
- false: normal generation allowed.
- Audible must-move: changes upstream should NOT alter this Thought if frozen.

## Resolver handoff (must map)
- `enabled` → generator pipeline gating (skip all stages)
- `frozen` → resolver/generator caching policy (do not recompute)
- `thoughtId` → deterministic subseed identity (stableKey component)

## Generator decision sites (must move audio)
- Pipeline runner decides whether to include this Thought in render graph.
- Seed derivation uses `thoughtId` (or stable hash) to keep determinism across UI edits unrelated to sound.

## Must-move metrics
- `determinism_hash` (internal): unchanged when only label changes
- `event_count` (notes/chords/beats): becomes 0 when enabled=false

## Common pitfalls / anti-patterns
- Letting `label` affect RNG seed (bad): renaming would change audio.
- Frozen nodes that still regenerate due to upstream changes (breaks promise).
