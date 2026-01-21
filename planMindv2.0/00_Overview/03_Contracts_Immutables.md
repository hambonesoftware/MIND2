# Contracts & Immutables (PoC)

These are “non-negotiable” rules for PoC stability.  
If a later change breaks one of these, it must be treated as a **breaking change** and re-tested.

## Immutable #1 — Quantized Swap

A Thought sequence update MUST NOT interrupt playback mid-measure.  
All swaps occur at:
- `Tone.Transport` next measure boundary, e.g. `@1m`, or computed next bar.

## Immutable #2 — Time format

Event times use a single canonical format end-to-end.

PoC canonical time string format:
- `"bar:beat:sixteenth"` as a string (e.g., `"0:2:0"`)
- bars are 0-based in packets, but frontend maps it to Tone.js relative scheduling

## Immutable #3 — Thought packet shape

The Thought JSON must include:
- `schema_version`
- `node_id`
- `status`
- `style_profile`
- `sequence[]` of events with:
  - `time` (canonical string)
  - `type` ("note" | "mute" | "cc")
  - `midi` (nullable)
  - `velocity` (0-127 or 0-1 normalized, but be consistent)
  - optional `duration` for notes

## Immutable #4 — Backend is the source of “theory truth”

Frontend is allowed to:
- schedule
- quantize swaps
- show UI feedback

Frontend is NOT allowed to:
- “fix” theoretical clashes silently
- reinterpret the meaning of DSL beyond display

## Immutable #5 — No “artist cloning”

Style profiles are **descriptive**: wide-open voicings, percussive mutes, etc.
Do not name or tune profiles to mimic a real, living artist.

