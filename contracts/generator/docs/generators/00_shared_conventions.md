# 00 — Shared Conventions

## 0) Inputs
All generators accept:

```yaml
inputs:
  resolvedGrammar: ResolvedGrammar
  resolvedControls: ResolvedControls
  thoughtMeta:
    thoughtId: string
    seed: int
    bars: int
    meter: string
    grid: "1/4"|"1/8"|"1/16"|"1/32"
    bpm: float
  runtime:
    generatorVersion: string
    strict: boolean               # if true, fail instead of fallback on repairs
    maxBacktracks: int
```

## 1) Deterministic seed discipline
Generators may use randomness, but must be deterministic for a given thought seed.

### Sub-seed derivation (required)
Use a stable function:

- `subseed = hash64(seed || generatorName || stageName || stableKey)`

Where:
- generatorName: `"HarmonyPlanner"`, `"RhythmRealizer"`, ...
- stageName: `"candidate"`, `"score"`, `"repair"`, ...
- stableKey: phraseIndex / barIndex / voiceId / etc.

Rules:
- never use system time
- never use hash-map iteration order (sort keys)

## 2) Timeline representation
### Ticks
Pick ticksPerBeat based on grid:

- 1/4  => 1 tick per beat
- 1/8  => 2 ticks per beat
- 1/16 => 4 ticks per beat
- 1/32 => 8 ticks per beat

`barTicks = beatsPerBar * ticksPerBeat`

### Meter
Meter provides beatsPerBar and beatUnit.
Example:
- 4/4 => beatsPerBar=4, beatUnit=4
- 6/8 => beatsPerBar=6, beatUnit=8 (interpretation policy must be documented)

## 3) Event outputs (canonical)
Generators ultimately produce events:

```yaml
ChordEvent:
  startTick: int
  durationTicks: int
  chordPcs: [int]          # 0..11
  romanNumeral: string|null
  function: "T"|"PD"|"D"|null
  cadenceTag: string|null  # "PAC"|"HC"|...

NoteEvent:
  partId: string           # "melody"|"bass"|"harmony"|"texture"
  voiceId: string|null     # for multi-voice harmony
  startTick: int
  durationTicks: int
  midi: int                # 0..127
  velocity: int            # 1..127
  tie: "start"|"stop"|null

BeatEvent:
  startTick: int
  instrument: string       # "kick"|"snare"|"hat"|...
  velocity: int            # 1..127
```

## 4) Trace (required)
Each generator emits `GeneratorTrace`:

```yaml
GeneratorTrace:
  generatorName: string
  generatorVersion: string
  thoughtId: string
  steps:
    - stepId: string
      decision: string
      inputsUsed: [string]        # ResolvedControls paths + any Grammar paths consulted
      chosen: any
      candidates: any|null
      scoreSummary: any|null
      repairs: any|null
      metrics: any|null
```

## 5) “No dead knobs” enforcement
A generator README must list “Decision Sites” with:
- which control fields affect which decision
- which metric must move when that field changes
