# Case 003 — Widening legality blocked (locked/simple)

## Setup
- Grammar allowedPitchClassesBase = diatonic major
- user attempts to add chromatic pcs via pane

## Expected
- Stage G: grammar stays diatonic (locked/simple)
- Stage C: user pcs intersected with grammar legality => chromatic pcs removed
- trace shows intersection and removed pcs
