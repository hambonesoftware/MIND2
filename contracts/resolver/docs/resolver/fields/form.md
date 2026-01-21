# Resolver Field Spec — form (Theory-first)

This file specifies compilation of:
- **FormGrammar** (section/phrase/cadence norms)
- **FormControls** (ResolvedControls.form.*)

---

## A) FormGrammar (ResolvedGrammar.formGrammar)

### A1) Section archetypes
**Theory object:** intro/verse/chorus/bridge/outro as formal roles with typical lengths.

Style provides:
- which archetypes are allowed
- typical lengths (bars)
- cadence norms by archetype boundary

### A2) Phrase grammar
**Theory object:** allowable phrase lengths and grouping schemes (AAAA/AABA/etc.).

Hard invariants:
- phraseLengthOptionsBars non-empty
- groupingOptions non-empty

### A3) Cadence placement norms
**Theory object:** probability/strength expectations for cadences at phrase/section boundaries.

Links to harmony grammar:
- cadence typology allowedCadences
- requiredAtPhraseEnd rule

---

## B) FormControls (ResolvedControls.form.*)

### 1) ResolvedControls.form.phrasePlan
Controls choose actual phrase segmentation for this Thought.

- if user provides boundaries: validate against bars and grammar options
- otherwise derive deterministically from chosen phraseLengthBars (must be allowed by grammar)

### 2) ResolvedControls.form.cadencePlan
Controls choose actual cadence events for this Thought.

- must use cadence types allowed by harmony grammar
- if requiredAtPhraseEnd=true, resolver inserts missing cadences at phrase ends

---

## C) Audible “must move” invariants (tests)
- changing phrasePlan changes where motives repeat and where cadences occur
- changing cadencePlan changes harmonic arrival distribution
- required cadence insertion is traceable and deterministic

---

## D) Generator guarantees
- phrase boundaries coherent and in-range
- cadence events legal and in-range
