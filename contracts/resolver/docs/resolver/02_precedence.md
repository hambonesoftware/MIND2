# 02 — Precedence Order (Grammar vs Controls)

Precedence differs by stage.

---

## Stage G (ResolvedGrammar) precedence
Unless overridden by field rules, Grammar precedence is:

1. S7 implicit grammar defaults
2. S0 upstream grammar (if inheritFromUpstream)
3. S2 styleFamily grammar
4. S3 styleVariant grammar
5. S5 pane tighten-only (locked/simple) or full edits (expert)
6. S6 expert overrides (expert only)

Notes:
- In locked/simple, S5 can only tighten legality (intersection/min), never widen.
- S4 profiles do not write grammar in locked/simple.

---

## Stage C (ResolvedControls) precedence
Controls precedence is closer to classic “defaults → user”:

1. S7 implicit control defaults
2. S0 upstream controls (if inheritFromUpstream)
3. S2 styleFamily control defaults (bias presets)
4. S3 styleVariant control deltas
5. S4 profile biases
6. S5 pane preferences
7. S6 expert overrides (expert only)

---

## Operator exceptions (still apply)
- Caps (upper bounds): `min()` across contributors
- Sets/masks legality: intersection in locked/simple (must be subset of grammar)
- Weight maps: blend then normalize
- Plans: replace then repair for coherence
