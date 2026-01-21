# File Creation Order (recommended)

This ordering reduces churn and rework:

1. Create `contracts/` schemas (thought.v0 + resolve.v0)
2. Backend models/pydantic align to schema
3. Backend profiles + DSL parser
4. Backend generator + invariants tests
5. Frontend schema validator + API client
6. Frontend Tone scheduler + quantized swap
7. Frontend LiteGraph nodes
8. Conflict resolver backend + TheoryGate node
9. Integration manual tests + evidence writeups

