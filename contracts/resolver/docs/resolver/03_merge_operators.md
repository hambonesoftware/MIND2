# 03 — Merge Operators (Grammar-aware)

Merge operators apply in both Grammar and Controls stages, but legality rules are stricter:

- Controls MUST be legal under Grammar.
- In locked/simple, any attempt to widen legality is ignored or repaired (policy-defined).

## Scalars
- replace by precedence

## Caps (upper bounds)
- `min()` across contributors

## Ranges
- intersect ranges; repair if empty per policy

## Sets/masks (legality)
- locked/simple: intersection with Grammar legality
- expert: may widen only if policy allows, otherwise still intersection

## Weight maps (preferences)
- blend then normalize
- zero illegal weights (then renormalize) in locked/simple

## Plans
- replace then repair to fit bars and Grammar cadence requirements
