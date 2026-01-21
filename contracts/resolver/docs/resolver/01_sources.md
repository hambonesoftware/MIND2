# 01 — Input Sources (Grammar vs Controls)

Resolver inputs write to either:
- Grammar (hard legality / vocab)
- Controls (weights/masks/plans within grammar)

## Source S0 — Upstream inheritance
- upstream ResolvedGrammar + ResolvedControls (if inheritFromUpstream)

## Source S1 — Global setup defaults
- may influence rhythmGrammar.meter or form defaults if modeled

## Source S2 — StyleFamily catalog
- primary writer of Grammar + default Biases

## Source S3 — StyleVariant catalog
- grammar deltas + bias deltas

## Source S4 — Profile catalog
- bias-only writer in locked/simple
- may write limited grammar only in expert (if you allow that at all)

## Source S5 — Pane values (UI)
- writes Controls
- may tighten Grammar in locked/simple (intersection/min) for select legality fields
- may widen Grammar only in expert and only where policy permits

## Source S6 — Expert overrides
- may write Grammar + Controls (expert only)

## Source S7 — Implicit defaults
- used only when required values are missing after catalogs/inheritance

---

## Trace requirement
Each contribution must identify:
- stage: Grammar or Controls
- sourceId (S0..S7)
- origin (styleFamilyId/panePath/etc.)
- value
