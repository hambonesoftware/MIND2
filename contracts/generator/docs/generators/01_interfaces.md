# 01 — Intermediate Interfaces (Plans)

Generators are staged: form → harmony → rhythm → motif → pitch → performance → assemble.

Each module produces a plan (intermediate IR) that the next module consumes.

## A) FormPlan
```yaml
FormPlan:
  totalBars: int
  barsPerPhrase: [int]             # e.g., [4,4] for 8-bar thought
  phraseBoundariesTicks: [int]     # phrase end ticks (exclusive)
  peakPosition: float              # 0..1 (for contour/performance)
  contourShape: string             # "arch"|"ascending"|...
  climaxLift: string               # none|small|medium|large
```

## B) HarmonyPlan
```yaml
HarmonyPlan:
  chordEvents: [ChordEvent]
  cadenceEvents:
    - tick: int
      cadenceType: string          # "PAC"|"HC"|...
      strength: string             # soft|medium|strong
  keyCenter: string|null           # optional symbolic
  progressionTemplateId: string|null
```

## C) RhythmPlan
```yaml
RhythmPlan:
  grid: string
  onsetMaskByPart:
    melody: [int]
    bass: [int]
    harmony: [int]
    beat: [int]
  accentModel:
    archetype: string
    params: object
  microtiming:
    swing: string
    pocketBias: string             # ahead|behind|center
    jitterStdMs: float
```

## D) MotifPlan
```yaml
MotifPlan:
  scheme: string                    # AAAA|AABA|ABAC|evolving
  motifCells:
    - id: string
      phraseIndices: [int]          # where it appears
      similarityTarget: float       # 0..1
  transformsByPhrase:
    - phraseIndex: int
      allowedTransforms: [string]
      caps: object
```

## E) PitchPlan
```yaml
PitchPlan:
  allowedPitchClasses: [int]         # 0..11
  pitchWeights: {int: float}         # pc -> weight
  voiceLeadingRules: object
  register:
    minMidi: int
    maxMidi: int
```

## F) PerformancePlan
```yaml
PerformancePlan:
  timingVariance:
    pocketBias: string
    jitterStdMs: float
  velocityCurve:
    baseVelocity: int
    accentScale: float
    phraseShape: string              # "crescendo"|"arch"|...
```

## G) Final output
```yaml
GeneratedPart:
  chords: [ChordEvent]
  notes: [NoteEvent]
  beats: [BeatEvent]
  traces: [GeneratorTrace]
  metrics: object
```
