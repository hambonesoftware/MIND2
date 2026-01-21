# Error Codes (canonical list for PoC)

DSL errors:
- `DSL_SYNTAX_ERROR`
- `DSL_PATTERN_TOKEN_ERROR`
- `DSL_UNKNOWN_MODIFIER`
- `DSL_VALUE_RANGE_ERROR`

Schema / contract errors:
- `SCHEMA_VERSION_UNSUPPORTED`
- `SCHEMA_VALIDATION_ERROR`

Profile errors:
- `PROFILE_NOT_FOUND`
- `PROFILE_VALIDATION_ERROR`

Runtime errors:
- `BACKEND_UNREACHABLE`
- `INTERNAL_ERROR`

All errors should be returned as:
```json
{
  "error": {
    "error_code": "...",
    "message": "...",
    "hint": "...",
    "span": [start, end]
  }
}
```

`span` may be omitted if unknown.

