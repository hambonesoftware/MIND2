# Product Spec (PoC)

## Problem statement

We want a **live-coding music environment** where users can:
- type short musical pattern text (Tidal-like)
- connect nodes visually (n8n-like)
- hear immediate playback with safe quantization
- rely on a theory-aware backend that can:
  - generate musically-valid sequences
  - adapt behavior via descriptive “Style Profiles”
  - resolve conflicts when multiple nodes play together

## User stories (PoC)

1. As a user, I can create a Thought node, type a pattern, and hear it loop.
2. As a user, I can switch style profiles and hear the same text render differently.
3. As a user, I can wire two Thought nodes into a Gate and the system avoids obvious clashes.
4. As a user, I can change text during playback and the system updates cleanly at the next bar.

## Non-goals (explicitly out of scope for PoC)

- Full DAW export (MIDI file / stems)
- Complex polymeter, Euclidean rhythm, swing templates beyond a small starter set
- Full key detection / advanced harmonic analysis
- Large instrument library, sampler UI, mixing UI
- Multi-user collaboration
- Persistent saves and cloud accounts

## Key constraints

- Must work locally (dev) with minimal friction.
- Must keep audio stable: avoid dropouts, schedule glitches, “double-play” bugs.
- Must be modular: backend logic is separate from frontend scheduling.

## Definitions

- **Thought**: One node’s musical intent + generated sequence (time-stamped events).
- **Style Profile**: A descriptive rule-set that biases generation and resolution.
- **Theory Gate**: A fan-in node that resolves multi-stream conflicts.
- **Quantized Swap**: Replace a playing loop only at a measure boundary.

