# Resolver Field Spec — rhythm (Grammar-aware)

Rhythm splits into:
- RhythmGrammar: grid policy, onset legality, accent archetypes, groove templates
- RhythmControls: ResolvedControls.rhythm.* (grid, onsetMask, accentModel, microtimingProfile)

v9.14 controls remain frozen; they must be legal under Grammar.

This file is intentionally lighter than harmony/pitch/form and can be expanded later.

## Compatibility Note

Prior versions placed microtiming controls under `ResolvedControls.performance`. In v9.14 these controls live exclusively in `ResolvedControls.rhythm.microtimingProfile`. If a `ThoughtSpec.performance.microtimingProfile` or `ResolvedControls.performance.microtimingProfile` field is encountered for backward compatibility, the resolver will deterministically map it to `ResolvedControls.rhythm.microtimingProfile` and discard the legacy field.
