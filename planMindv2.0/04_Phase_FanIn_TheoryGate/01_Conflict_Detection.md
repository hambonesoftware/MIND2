# Conflict Detection (PoC)

## The PoC definition of “clash”

A clash occurs if, at the same time slot:
- two melodic roles contain pitch classes that form a “bad” interval (profile-defined), OR
- lead and bass produce contradictory 3rds over the same implied harmony

PoC minimal checks:
1. Same-time pitch-class interval check:
   - compute interval between pitches mod 12
   - if interval in `avoid_intervals`, flag
2. Third-quality mismatch:
   - if a bass note implies minor third while lead implies major third at same time
   - (PoC may approximate by relative intervals from anchor)

## Input needed
- sequences with canonical times
- role labels per sequence (bass/lead)

If role is not provided, default:
- first input = bass, second = lead (document as PoC rule)

