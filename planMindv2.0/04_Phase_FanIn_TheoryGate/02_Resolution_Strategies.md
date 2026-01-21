# Resolution Strategies (PoC)

## Profile-driven strategy selection

Each active style profile exposes:
- `clash_policy` ("shift" | "drop" | "revoice")
- `shift_choices` e.g. `[+2, -2, +5, -5]`

## Canonical PoC resolution order

1. Protect bass (if present)
2. Adjust lead (shift preferred)
3. If cannot shift without leaving MIDI range:
   - drop note (mute)
4. If both are melodic and neither is bass:
   - shift the higher pitch

## Shift logic (PoC)

Given a lead note at time T:
- try each `shift_choice` in order
- choose first shift that:
  - resolves the avoid-interval conflict
  - stays within MIDI range 0..127
  - stays within a preferred register window if profile requires

## Output options

Option A (simpler):
- return corrected sequences per input:
  - `{ "resolved": [thought1, thought2] }`

Option B (merged stream):
- return a single merged Thought with combined sequence

PoC recommendation: **Option A**, because it preserves node identity.

