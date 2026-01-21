# Phase 5 — Testing & Validation

## Goal
Verify robustness across styles and ensure audio scheduling stays stable.

## In-scope (PoC)
- Unit tests (backend):
  - DSL parsing
  - profile validation
  - generator output invariants
  - conflict detection/resolution
- Basic frontend tests (lightweight):
  - schema validation
  - swap logic state machine tests
- Manual “musical” test scripts

## Agent Tasks (assumed to exist)
- Agent.Tests.BackendUnit
- Agent.Tests.FrontendLogic
- Agent.Tests.ManualScripts

## Phase acceptance criteria
- All backend unit tests pass
- Manual test cases A and B produce expected audible differences
- “Rapid edit” test does not cause double loops or audio collapse

