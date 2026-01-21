# 16 — PartAssembler (Final Assembly)

## Purpose
Combine outputs from planners/realizers into final parts and compute metrics.

## Inputs
- FormPlan, HarmonyPlan, RhythmPlan, MotifPlan
- NoteEvents by part (pre-performance)
- BeatEvents
- Performance controls/plans

## Outputs
- GeneratedPart (events + traces + metrics)

---

## Assembly steps

### A0 — Align plans
- ensure totalTicks consistent
- strict: error on mismatch
- non-strict: clamp to min totalTicks and trace repair

### A1 — Allocate harmony voicings
- block chords vs arpeggiated texture based on figuration/pattern family
- assign voiceIds deterministically

### A2 — Conflict resolution
Starter rules:
- avoid melody/harmony same-register collisions (octave shift harmony if legal)
- preserve bass anchoring, adjust harmony first, melody second
- enforce density caps by dropping lowest-priority events if needed

### A3 — Compute metrics summary
Compute:
- pitch_class_histogram
- chord_tone_ratio
- non_diatonic_pitch_rate
- interval_histogram
- syncopation/backbeat/swing
- cadence distributions
- motif_similarity

### A4 — Merge traces
Concatenate all generator traces and include per-part metric deltas.

---

## Minimum tests
- metrics exist and change when upstream controls change
- legality preserved (no illegal pcs/onsets)
