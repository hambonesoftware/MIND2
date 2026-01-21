# DSL Grammar v0 (PoC)

The DSL is intentionally small. It must be:
- easy to type
- easy to parse with regex/tokenization
- easy to validate and produce good error messages

## Canonical example

`"[0 7 12] | slap:0.5 | vel:0.8 | oct:+1 | dens:0.6 | seed:123"`

## Concepts

- A **pattern** is a bracket list: `[ ... ]`
- Inside brackets: integers represent semitone offsets from an anchor pitch
- Pipes `|` separate **modifiers**

## v0 Tokens

### Pattern
- `[<int> <int> <int> ...]`
- Whitespace-separated
- Integers allowed: negative and positive

### Modifiers (key:value)
- `slap:<0..1>` → maps to mute_probability override (frontend may show as “slap”)
- `vel:<0..1>` → velocity scalar
- `oct:<int>` → octave offset (+/-)
- `dens:<0..1>` → note_density override
- `sync:<0..1>` → syncopation override
- `seed:<int>` → RNG seed override
- `len:<bars>` → loop length in bars (default 1)
- `div:<int>` → grid division (e.g., 16 for 16th notes; default 16)

### Reserved modifiers (not in PoC)
- `scale:`, `chord:`, `mode:` (future expansions)

## Parse output structure (Intent)

```json
{
  "pattern": [0, 7, 12],
  "modifiers": {
    "slap": 0.5,
    "vel": 0.8,
    "oct": 1,
    "dens": 0.6,
    "seed": 123,
    "len": 1,
    "div": 16
  }
}
```

## Error model
- Missing brackets → `DSL_SYNTAX_ERROR`
- Non-integer in pattern → `DSL_PATTERN_TOKEN_ERROR`
- Unknown modifier key → `DSL_UNKNOWN_MODIFIER`
- Value out of range → `DSL_VALUE_RANGE_ERROR`

Error responses must include:
- `error_code`
- `message`
- `hint`
- `span` (optional start/end indices in the input string)

