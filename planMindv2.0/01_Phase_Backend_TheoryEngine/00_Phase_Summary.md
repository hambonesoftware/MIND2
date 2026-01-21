# Phase 1 — Backend “Theory Engine” (Python / FastAPI)

## Goal
Create an API that takes:
- a text DSL string
- a style profile ID
- optional context (tempo, harmonic anchor)

…and returns a **mathematically valid**, schedulable event sequence.

## In-scope (PoC)
- FastAPI service with `/generate`, `/profiles`, `/health`
- `StyleProfile` definitions and validation
- DSL v0 parser (regex + tokenization)
- Heuristic generator producing deterministic-ish output (seedable)
- Error model: structured errors for invalid DSL or missing profiles

## Out-of-scope (PoC)
- Full-blown parser generator / AST tooling
- Deep harmonic analysis
- ML-based generation

## Required artifacts (produced by Agents)
- `backend/app/profiles.py`
- `backend/app/dsl_parser.py`
- `backend/app/generator.py`
- `backend/app/models.py`
- `backend/app/api.py`
- `backend/app/main.py`
- `backend/tests/` basic unit tests

## Agent Tasks (assumed to exist)
- Agent.Backend.SetupFastAPI
- Agent.Backend.StyleProfiles
- Agent.Backend.DSLParserV0
- Agent.Backend.HeuristicGenerator
- Agent.Backend.ErrorModelAndTests

## Phase acceptance criteria
- `GET /health` returns OK
- `GET /profiles` lists at least 3 profiles
- `POST /generate` with valid DSL returns a Thought with:
  - non-empty sequence
  - all events pass schema validation
- Invalid DSL returns a structured error with actionable message

