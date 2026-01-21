# Style Profiles (Descriptive) — v0

## Purpose
Style Profiles bias generation and conflict resolution without hard-coding “one sound”.

## Profile schema (PoC)

Each profile is a JSON-like dict (or pydantic model) with:

### Core musical controls
- `interval_gravity` (0..1): higher = prefer stepwise motion
- `preferred_intervals` (list[int]): pitch-class intervals favored (0..11)
- `avoid_intervals` (list[int]): pitch-class intervals discouraged (0..11)
- `register_bias` (e.g., -2..+2 octaves relative to anchor)
- `voicing_spread` ("open" | "cluster")
- `note_density` (0..1): probability of filling available time slots

### Articulation controls
- `mute_probability` (0..1): chance to emit “mute” event between notes
- `accent_strength` (0..1): velocity contour emphasis
- `syncopation` (0..1): shift events off strong beats

### Conflict resolution controls
- `priority_role` ("bass" | "lead" | "pad" | "drums")
- `clash_policy` ("shift" | "drop" | "revoice")
- `shift_choices` (list[int]): allowed shift intervals (e.g., [+2, -2, +5, -5])

## Starter profiles (minimum PoC set)

### 1) wide_acoustic
- low interval gravity (allows leaps)
- open voicing spread
- prefers consonant extensions (5th, 9th, 7th)

### 2) percussive_fingerstyle
- high rhythmic saliency
- moderate mute probability (dead notes)
- cluster voicing to keep tight

### 3) dark_pulse_synth
- medium gravity
- strong syncopation
- prefers minor-ish color tones, tight register bias

## Profile validation
- reject missing required keys
- clamp numeric ranges
- ensure interval lists are 0..11

## Determinism
Support optional `seed` in `/generate` so repeats are stable:
- same (dsl, profile, seed) → same output

