# LiteGraph Node Types (PoC)

## 1) MusicalThoughtNode

### UI requirements
- Text input area (overlay textarea is acceptable)
- Style selector (dropdown) or style input pin
- Status indicator:
  - green: active
  - yellow: pending update
  - red: error

### Inputs
- `Clock` (optional PoC; can be implicit)
- `HarmonicAnchor` (optional PoC)

### Outputs
- `Stream_Data` (Thought packet)

### Behavior
- On text change:
  - debounce 500ms
  - cancel in-flight request (AbortController)
  - set state “pending”
  - call `/generate`
  - on success:
    - validate packet
    - store as “nextThought”
    - schedule quantized swap
  - on error:
    - show error text
    - keep last good loop playing

## 2) TheoryGateNode

### UI requirements
- 2–4 input pins for `Stream_Data`
- 1 output pin `Resolved_Stream` (or per-input outputs, choose one for PoC and document it)

### Behavior
- When inputs change:
  - gather latest thoughts
  - call `/resolve-conflict`
  - output resolved packet(s)
  - quantized swap applies to downstream scheduling

## 3) TransportNode (optional)
- play/pause, tempo, time signature
- PoC can hard-code tempo and add this later

