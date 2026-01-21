# Case 001 — Inheritance (Grammar + Controls)

## Setup
- upstreamResolvedGrammar exists (style=rock_classic)
- inheritFromUpstream=true
- user sets profile=lofi (bias layer)

## Expected
- Stage G: grammar defaults inherit from upstream (then style family/variant if overridden)
- Stage C: controls inherit from upstream, then profile/pane biases applied
- locked/simple: profile does not widen grammar legality
