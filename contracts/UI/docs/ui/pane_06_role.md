# Pane 06 — Role

## What this pane controls
Role defines the functional job this Thought performs in the arrangement (hook, comp, pad, groove, etc.).
Role mainly shapes **priority**, **density**, and **interaction coupling**.

## Deterministic choices
### roleBehavior
- hook: high motif reuse, clear contour, strong cadence targets
- lead_line: clear melodic identity, moderate reuse, strong chord-tone anchoring
- counterline: supports lead, avoids collision, simpler motif
- fill: localized high density near gaps
- pad: sustained tones, low motion, low syncopation
- comp: chord rhythm support, stable patterns
- anchor: bass-like stability, strong tonal center
- groove: rhythmic identity, repeated onset patterns

### priority
- lead: wins conflict resolution (kept when density caps force drops)
- support: kept unless collisions occur
- background: first dropped if conflict resolution needed

### interaction
- followsHarmony: pitch decisions follow chord changes strongly
- followsRhythm: onset decisions follow beat groove strongly
- callResponseGroup: string/group id; nodes in same group alternate motif cells

## Resolver handoff (must map)
Must affect:
- `ResolvedControls` defaults:
  - rhythm density/syncopation/restPolicy
  - pitch range / register center
  - motif reuse plan
- conflict resolution policy in PartAssembler (priority + collision avoidance)

## Generator decision sites (must move audio)
- RhythmRealizer density targets per roleBehavior.
- MotifPlanner scheme + similarity targets per role.
- PitchSelector chord-tone bonus scaling if followsHarmony.
- PartAssembler collision avoidance + drop policy uses priority.

## Must-move metrics
Must-move metrics:
- `motif_similarity` (hook higher than pad)
- `density` / `rest_ratio` (fill > counterline > pad)
- `collision_rate` (counterline aims lower than lead)

## Common pitfalls / anti-patterns
- Role does nothing but rename tracks (dead role).
- Counterline collides constantly with melody (ignores interaction intent).
