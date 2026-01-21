# Case 002 — Illegal cadence type rejected by Grammar

## Setup
- Grammar allowedCadences = [PAC, HC]
- user cadencePlan requests plagal

## Expected (locked/simple)
- Stage G defines allowedCadences=[PAC,HC]
- Stage C drops illegal plagal events and warns (or errors if plan becomes invalid and fallback disabled)
- trace clearly shows grammar legality causing repair
