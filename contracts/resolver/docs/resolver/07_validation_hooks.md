# 07 — Post-Resolve Validation Hooks (Grammar-aware)

After resolution:
- validate Grammar internal consistency (non-empty vocab sets, normalized transitions)
- validate Controls are legal under Grammar
- validate canonicalization and plan coherence

Errors stop generation (unless failOpen and "usable" policy exists).
