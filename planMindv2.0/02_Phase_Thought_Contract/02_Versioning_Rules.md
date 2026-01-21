# Versioning & Compatibility Rules

## Schema versions
- `thought.v0` — PoC baseline
- Future: `thought.v1` etc.

## Breaking change examples (require new version)
- Changing time encoding
- Changing velocity scale 0..1 to 0..127
- Removing required fields
- Changing meaning of existing modifiers

## Non-breaking change examples (same version)
- Adding optional fields
- Adding new style profile IDs
- Adding new nodes in the UI

## Client behavior
- Frontend checks `schema_version`:
  - if unknown → show error and do not schedule
- Backend checks incoming `schema_version`:
  - if unknown → return `SCHEMA_VERSION_UNSUPPORTED`

