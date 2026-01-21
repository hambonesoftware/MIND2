# 10 — Legality Validators

Legality = “output is allowed” under `ResolvedGrammar` and `ResolvedControls`.

These checks are **hard** (ERROR) unless explicitly marked as warnings.

---

## L1) Timeline coverage and bounds
### What it checks
- all events have startTick >= 0
- durationTicks > 0
- startTick + durationTicks <= totalTicks
- no NaNs, no negative MIDI, velocity bounds 1..127

### Inputs used
- thoughtMeta: bars, meter, grid
- generatedPart events

### Suggested repairs
- generator: clamp to bounds, or drop illegal event and backtrack.

---

## L2) Meter/grid alignment (pre- and post-humanization)
### What it checks
- pre-humanization onsets must lie on grid ticks
- post-humanization timing offsets must remain within allowed humanization bounds

### Inputs used
- ResolvedControls.rhythm.grid
- ResolvedControls.performance.timingVariance
- ResolvedGrammar.performanceGrammar.humanizationBounds

### Severity
- ERROR if pre-humanization off-grid
- WARN if post-humanization exceeds intended jitter but within absolute bounds

---

## L3) Pitch legality
### What it checks
- note pitch classes must be a subset of `ResolvedControls.pitch.allowedPitchClasses`
  - unless explicitly allowed by chromatic policy (borrow/approach) AND within caps

### Inputs used
- ResolvedControls.pitch.allowedPitchClasses
- ResolvedControls.harmony.chromaticCaps
- ResolvedGrammar.harmonyGrammar.chromaticPolicy

### Severity
- ERROR if illegal pitch class and no chromatic allowance
- ERROR if chromatic caps exceeded

---

## L4) Register legality
### What it checks
- midi is within [minMidi, maxMidi] for the part

### Inputs used
- ResolvedControls.pitch.voiceLeadingRules.register or resolved register bounds per part

---

## L5) Voice-leading hard rules
### What it checks
- maxLeap not exceeded
- leading tone resolution if `resolveLeadingTone=true` (in cadence windows)

### Inputs used
- ResolvedControls.pitch.voiceLeadingRules
- FormPlan phrase boundaries
- HarmonyPlan cadences (if available)

### Severity
- ERROR if maxLeap exceeded
- WARN if resolution preference not met (unless marked hard)

---

## L6) Harmony legality
### What it checks
- chord qualities used are allowed by `ResolvedControls.harmony.chordQualities`
- cadence types used are allowed by cadence typology
- function path legality (if function labels used)

### Inputs used
- ResolvedControls.harmony.chordQualities
- ResolvedControls.harmony.cadenceConstraints
- ResolvedGrammar.harmonyGrammar.cadenceTypology
- ResolvedGrammar.harmonyGrammar.functionStateMachine

---

## L7) Rhythm legality (onset masks)
### What it checks
- all pre-humanization onsets are included in the resolved onset legality mask
- beat patterns conform to allowed instruments/vocab (if style restricts)

### Inputs used
- ResolvedControls.rhythm.onsetMask
- ResolvedGrammar.rhythmGrammar.onsetLegality
- ResolvedGrammar.rhythmGrammar.grooveTemplates

---

## L8) Motif transform legality
### What it checks
- applied transforms are in allowed set
- transform magnitudes are within caps

### Inputs used
- ResolvedControls.motif.transformPlan
- ResolvedGrammar.motifGrammar.allowedTransforms
- ResolvedGrammar.motifGrammar.transformMagnitudeCaps
