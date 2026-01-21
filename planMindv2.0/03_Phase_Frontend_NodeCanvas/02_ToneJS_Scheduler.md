# Tone.js Scheduler & Quantized Swap (PoC)

## Objectives
- Stable loop playback
- No glitching on edit
- Immediate “feel” without rescheduling chaos

## Core idea
Each Thought node owns:
- a `Tone.Part` or `Tone.Sequence` (active)
- a `nextPart` (prepared)
- a swap event scheduled at next bar boundary

## Quantized swap procedure (canonical)

1. When new Thought arrives:
   - create a new Part from the sequence
   - do NOT start it immediately
2. Compute next bar time:
   - `Tone.Transport.nextSubdivision("1m")` (or manual)
3. Schedule:
   - at next bar:
     - stop and dispose old part
     - start new part at that exact boundary
4. Mark node status “active”

## Edge cases
- Multiple updates before swap:
  - keep only latest `nextPart`
  - swap uses latest sequence
- Transport stopped:
  - apply immediately on start, or store pending
- Backend returns empty:
  - treat as muted (stop part at next bar)

## Tempo/time signature
PoC: start with fixed 120 bpm, 4/4, loop 1 bar.
Later: accept from backend meta.

