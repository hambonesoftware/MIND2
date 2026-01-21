# 06 — Determinism & Seed Discipline

Resolver remains deterministic.

- No randomness in Stage G or Stage C.
- Any derived defaults must be deterministic functions of IDs and version.

Generators derive sub-seeds from resolved seed, but that is outside resolver scope.
