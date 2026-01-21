# 05 — Repair Policy (Grammar-aware)

The resolver repairs invalid inputs deterministically.

## Hard rule
Controls cannot violate Grammar.
If a pane value violates Grammar, resolver must:
- clamp / intersect / drop illegal elements
- warn (and trace) the repair
- error if repair makes the result unusable (e.g., empty legality set)

## Repair order
1. clamp numeric bounds
2. drop unknown IDs and substitute defaults
3. enforce Grammar legality (intersection / zero illegal weights)
4. renormalize weights
5. repair plans (drop invalid events, insert required cadences)
6. if still invalid => error
