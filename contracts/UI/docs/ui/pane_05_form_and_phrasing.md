# Pane 05 — Form & Phrasing

## What this pane controls
Controls phrase segmentation and cadence placement. This is the bridge between “container length” and “composition.”

## Deterministic choices
### phrasePlan.mode
- auto: system chooses phrase boundaries based on style norms
- explicit: user sets barsPerPhrase / boundaries

### phrasePlan.barsPerPhrase
- examples: [4,4] for 8 bars, [2,2,4], [8]
Audible must-move:
- phrase boundaries change where contour peaks and cadences occur.

### phrasePlan.peakPosition
- float 0..1 (relative position across thought)
Audible must-move:
- melodic pitch peak and/or velocity peak shifts toward this position.

### phrasePlan.contourShape
- static | arch | ascending | descending | wave
Audible must-move:
- macro-direction of melody/energy changes.

### phrasePlan.climaxLift
- none | small | medium | large
Audible must-move:
- register expands upward near the climax; louder velocity at climax.

### cadencePlan.mode
- auto: HarmonyPlanner chooses cadences matching style
- explicit: user pins cadence events

### cadencePlan.events[]
Each event:
- atBar (1-based) or atTick
- cadenceType (PAC|HC|DC|... allowed by style)
- strength (soft|medium|strong)
Audible must-move:
- stronger cadences create clearer arrivals (dominant→tonic behavior, longer durations, stronger accents).

## Resolver handoff (must map)
Must affect:
- `ResolvedControls.form.phrasePlan`
- `ResolvedControls.form.cadencePlan`
- `ResolvedControls.harmony.cadenceConstraints` (if cadencePlan is explicit, it constrains it)

## Generator decision sites (must move audio)
- FormPlanner generates FormPlan.
- HarmonyPlanner must place cadences at phrase ends per cadencePlan.
- PitchSelector must bias cadenceTargets near phrase end.
- PerformanceHumanizer should shape velocity around phrase boundaries.

## Must-move metrics
Must-move metrics:
- `cadence_type_distribution_at_phrase_ends`
- `cadence_success_rate`
- `phrase_dynamic_correlation` (velocity peaks aligned to peakPosition)
- `contour_correlation` (macro pitch trend matches contourShape)

## Common pitfalls / anti-patterns
- User sets explicit cadences that style grammar forbids → must repair or clearly error.
- phrasePlan changes but harmony and melody ignore phrase ends (no audible phrasing).
