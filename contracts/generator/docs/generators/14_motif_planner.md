# 14 — MotifPlanner

## Purpose
Plan motif reuse + transformations so output is recognizably structured.

## Inputs
### Controls
- `ResolvedControls.motif.motifReusePlan`
- `ResolvedControls.motif.transformPlan`
- `ResolvedControls.form.phrasePlan`
- (optional) `ResolvedControls.rhythm.onsetMask` if motifs include rhythm cells

### Grammar consulted
- `ResolvedGrammar.motifGrammar.allowedTransforms`
- `ResolvedGrammar.motifGrammar.transformMagnitudeCaps`
- `ResolvedGrammar.motifGrammar.reuseExpectations`

## Output
- `MotifPlan` (see `contracts/MotifPlan.schema.json`)

---

## Algorithm

### Stage M0 — Scheme realization
- AAAA: one motif cell reused each phrase
- AABA: A reused (0,1,3), B contrast (2)
- ABAC: A reused (0,2)
- evolving: drift within caps

### Stage M1 — Similarity targets
Compute similarityTarget per phrase:
- derived from repeatStrength + variationAmount
- clamped to grammar expectations

Metric:
- `motif_similarity`

### Stage M2 — Transform assignment
For each phrase:
- start with grammar allowed transforms
- apply control subset
- clamp magnitudes

Repair:
- if similarity too low in required repeats, reduce transforms or raise reuse strength deterministically

---

## Minimum tests
- AAAA yields motif_similarity above threshold
- disabling a transform removes it from transform usage
