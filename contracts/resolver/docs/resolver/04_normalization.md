# 04 — Normalization Rules (Grammar-aware)

Canonicalization keeps generators simple and deterministic.

## Weight maps
- remove negative weights
- zero weights for illegal items (locked/simple), then renormalize
- if sum=0 => fallback to defaults + warning

## Sets/masks
- canonical representation, sorted unique
- MUST be non-empty
- MUST be subset of Grammar legality

## Plans
- indices in range [0..totalBars-1]
- cadence types must be allowed by Grammar.cadenceTypology
