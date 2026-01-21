# Phase 3 — Frontend Node Canvas (LiteGraph + Tone.js)

## Goal
Build the visual interface where users type DSL text, connect wires, and hear playback.

## In-scope (PoC)
- LiteGraph canvas bootstrapped
- Custom node types:
  - `MusicalThoughtNode`
  - `StyleProfileNode` (optional if style is embedded in ThoughtNode for PoC)
  - `TheoryGateNode`
- A debounced listener that calls backend `/generate`
- Tone.js scheduling with quantized swap at next bar

## Agent Tasks (assumed to exist)
- Agent.Frontend.SetupLiteGraph
- Agent.Frontend.CustomNodes
- Agent.Frontend.ApiClient
- Agent.Frontend.ToneSchedulerQuantizedSwap
- Agent.Frontend.ErrorUX

## Phase acceptance criteria
- A single Thought node can play audio
- Edits update sound only at next bar
- Invalid DSL shows error in node UI without crashing audio

