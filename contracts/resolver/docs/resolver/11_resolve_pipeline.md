# 11 — Resolve Pipeline (NEW)

This is the deterministic compilation pipeline.

## Stage G — ResolveGrammar
Inputs:
- S2/S3 styleFamily/styleVariant grammar
- S0 upstream grammar (if inheritFromUpstream)
- S6 expert overrides (expert only)
- S7 implicit grammar defaults (only if absolutely required)

Output:
- ResolvedGrammar (hard legality + vocab)

Key rule:
- Profiles (S4) do NOT write grammar in locked/simple.
- Panes (S5) only tighten grammar in locked/simple (intersection/min).

## Stage C — ResolveControls (within Grammar)
Inputs:
- ResolvedGrammar (from Stage G)
- style/profile biases
- pane preferences (weights/masks/plans/curves)
- upstream controls (if inheritFromUpstream)

Output:
- ResolvedControls (canonical control surface), guaranteed legal under grammar

## Stage V — Validate
- post-resolve validators confirm:
  - legality (sets/masks within grammar)
  - non-emptiness (no empty masks/sets)
  - canonicalization (normalized weights, bounded caps)
  - plan coherence (phrase/cadence within bars)

## Stage T — Trace
- Both Stage G and Stage C must emit trace entries.
Trace MUST answer:
- what was chosen
- why (contributors + precedence)
- how (merge operator)
- repairs applied
