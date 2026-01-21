# Resolver Field Spec — performance (Grammar-aware)

Performance splits into:
- PerformanceGrammar: humanization bounds and articulation norms
- PerformanceControls: ResolvedControls.performance.*

Controls are clamped to grammar bounds.

## Compatibility Note

Microtiming offsets (`microtimingProfile`) are not part of performance controls in v9.14. They are defined in the rhythm group as `ResolvedControls.rhythm.microtimingProfile`. Any legacy fields or UI controls named `performance.microtimingProfile` will be remapped to the rhythm group and ignored under performance.
