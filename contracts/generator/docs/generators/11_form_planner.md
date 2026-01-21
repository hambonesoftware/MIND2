# 11 — FormPlanner

## Purpose
Produce a **FormPlan** that segments bars into phrases and supplies cadence windows / peak targets.

## Inputs (fields used)
### Controls
- `ResolvedControls.form.phrasePlan`
- `ResolvedControls.form.cadencePlan` (optional)

### Grammar consulted
- `ResolvedGrammar.formGrammar.phraseGrammar`
- `ResolvedGrammar.formGrammar.sectionArchetypes` (optional)
- `ResolvedGrammar.harmonyGrammar.cadenceTypology` (for validating cadence plan)

## Output
- `FormPlan` (see `contracts/FormPlan.schema.json`)

---

## Algorithm

### Stage F0 — Determine total bars
From thought meta (bars). Validate >=1.

### Stage F1 — Choose phrase boundaries
If UI authored explicit phrase boundaries:
- validate: boundaries align to bar boundaries and totalBars
- repair: snap to nearest bar boundary if policy allows; else error (strict)

Else:
- choose a phrase length from grammar options (e.g., 2/4/8)
- derive boundaries deterministically (chunk bars)

Decision site fields:
- `ResolvedControls.form.phrasePlan` (explicit or preference)
Metric:
- `phrase_boundary_positions`

### Stage F2 — Apply contour targets
- peakPosition (0..1)
- contourShape (arch/ascending/...)
- climaxLift

These parameters guide PitchSelector and PerformanceHumanizer.

Decision site fields:
- `ResolvedControls.form.phrasePlan.contourShape`
- `ResolvedControls.form.phrasePlan.peakPosition`
- `ResolvedControls.form.phrasePlan.climaxLift`

### Stage F3 — Validate cadence plan compatibility
If `ResolvedControls.form.cadencePlan` exists:
- ensure cadence events fall within cadence windows and use allowed cadence types
- repair/drop illegal cadence types

---

## Minimum tests
- phrase boundary edits are reflected in FormPlan boundaries
- peakPosition shifts later velocity peak and/or melodic pitch peak
