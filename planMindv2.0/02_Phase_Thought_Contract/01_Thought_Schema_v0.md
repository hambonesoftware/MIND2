# Thought Schema — `thought.v0`

## Schema identity
- `schema_version`: must equal `"thought.v0"`

## Top-level fields

- `schema_version` (string, required)
- `node_id` (string, required)
- `status` ("active" | "muted" | "error", required)
- `style_profile` (string, required)
- `meta` (object, required)
  - `tempo` (number, required)
  - `time_signature` (string, required, `"4/4"` in PoC)
  - `loop_bars` (integer, required, default 1)
  - `division` (integer, required, default 16)
- `sequence` (array[Event], required, may be empty only if status != active)

## Event object

Required:
- `time` (string: `"bar:beat:sixteenth"`)
- `type` ("note" | "mute" | "cc")
- `velocity` (number; PoC recommends 0..1)

Conditional:
- if `type == "note"`:
  - `midi` (integer 0..127, required)
  - `duration` (time string or numeric seconds; PoC recommends time string)
- if `type == "mute"`:
  - `midi` must be null or omitted
- if `type == "cc"`:
  - `cc` (0..127) and `value` (0..127)

## Ordering
- `sequence` must be sorted by time ascending.
- Events at same time are allowed, but:
  - at most 1 `note` per node per time slot in PoC v0 (enforced by backend generator)

## Forward compatibility rules
- Frontend must accept unknown **top-level** keys (ignore) but not unknown required fields.
- Frontend must reject unknown `type` values.

