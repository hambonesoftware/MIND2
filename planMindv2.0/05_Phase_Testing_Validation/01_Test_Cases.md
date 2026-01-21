# Test Cases (PoC)

## Test Case A — Acoustic Flow
Setup:
- Style profile: `wide_acoustic`
- DSL: `[0 2 4]`

Expected:
- “open” feel, wider spacing
- possible octave lift
- fewer mutes

## Test Case B — Percussive Groove
Setup:
- Style profile: `percussive_fingerstyle`
- DSL: `[0 2 4]` (same)

Expected:
- tighter spacing
- mutes inserted between pitches
- more rhythmic saliency (accented backbeat feel)

## Test Case C — Rapid typing stability
Setup:
- hold a key to spam edits for 5 seconds

Expected:
- no overlapping parts
- last good loop continues
- new loop swaps at next bar

## Test Case D — Conflict resolution
Setup:
- Bass node: `[0]` role=bass
- Lead node: `[4]` role=lead
- Style profile uses avoid interval that forces adjustment (configure for test)

Expected:
- clash detected at time 0
- lead shifted (e.g., +1 or -1 depending on rules)
- both streams audible and stable

