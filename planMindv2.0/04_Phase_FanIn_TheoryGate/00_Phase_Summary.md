# Phase 4 — Fan-In Logic (Theory Gate)

## Goal
Prove that two nodes can play together without obvious clashes.

## In-scope (PoC)
- LiteGraph TheoryGate node sends multiple Thought inputs to backend
- Backend endpoint `/resolve-conflict` detects simple clashes and resolves using profile rules

## Agent Tasks (assumed to exist)
- Agent.Backend.ConflictResolverV0
- Agent.Frontend.TheoryGateNode
- Agent.Integration.FanInPlayback

## Phase acceptance criteria
- Two Thought nodes routed through Gate produce audible output
- At least one scripted “clash case” is detected and corrected
- Resolution is deterministic with a fixed seed

