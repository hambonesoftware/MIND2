# Phase 2 — Thought Contract (JSON Schema)

## Goal
Define a versioned, strict JSON schema for the payload flowing between nodes.

## In-scope (PoC)
- `thought.v0` schema defined in JSON Schema draft-07 (or newer)
- A small set of event types: `note`, `mute`, optional `cc`
- Validation tooling:
  - backend validates before returning
  - frontend validates before scheduling

## Agent Tasks (assumed to exist)
- Agent.Contract.DefineThoughtSchema
- Agent.Contract.AddValidatorsBackendFrontend
- Agent.Contract.AddCompatibilityRules

## Phase acceptance criteria
- Schema file exists and validates example packets
- Backend rejects packets failing schema
- Frontend refuses to schedule invalid packets and shows the user a readable error

