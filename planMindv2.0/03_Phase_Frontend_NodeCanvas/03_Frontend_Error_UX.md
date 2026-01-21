# Frontend Error UX (PoC)

## Principles
- Never crash audio.
- Never wipe a last-good loop due to a new error.
- Show the user what to fix.

## Node error display
MusicalThoughtNode shows:
- error_code
- message
- hint
- highlights offending span in text editor (optional PoC)

## Network failure
- display “backend unreachable”
- continue playing last good loops

## Schema validation failure
- display “invalid Thought packet”
- include first failing field path

