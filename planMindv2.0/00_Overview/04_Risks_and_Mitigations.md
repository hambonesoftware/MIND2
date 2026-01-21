# Risks & Mitigations

## Audio scheduling risks
- **Risk:** double-scheduling on rapid edits → overlapping loops  
  **Mitigation:** runtime store tracks active parts per node; quantized swap replaces parts atomically.

- **Risk:** drift between backend bar-grid and Tone.Transport  
  **Mitigation:** single canonical tempo/timeSignature, included in Thought packet metadata.

## Theory conflicts complexity
- **Risk:** “conflict resolution” becomes a research project  
  **Mitigation:** PoC uses a **small, explicit rule set**:
  - pitch-class collision detection
  - chord-tone preference
  - profile-defined priorities (bass protected, lead adjusts, etc.)

## DSL scope creep
- **Risk:** grammar expands rapidly and becomes fragile  
  **Mitigation:** define a strict v0 grammar; reject unknown tokens with clear errors.

## UI complexity
- **Risk:** custom text editing inside canvas becomes messy  
  **Mitigation:** start with LiteGraph’s built-in widgets or an overlay textarea anchored to node position.

## Performance
- **Risk:** high-frequency calls overload backend during typing  
  **Mitigation:** debounce, cancel in-flight requests, and cache last successful generation.

