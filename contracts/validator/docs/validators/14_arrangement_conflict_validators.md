# 14 — Arrangement / Conflict Validators

These validators check multi-part interactions.

## A1) Register collisions
- melody and harmony overlap too frequently in same octave band
- bass overlaps melody register too often

Metric suggestions:
- collision_rate (shared pitch classes at same tick)
- register_overlap_ratio

Severity:
- WARN by default
- ERROR if role.priority mandates separation

## A2) Density conflicts
- too many simultaneous onsets exceed density caps for style

Metric:
- simultaneous_onset_count_distribution

## A3) Cadence masking
- cadence chord occurs but melody/bass avoid cadence targets strongly (cadence weakened)

Metric:
- cadence_alignment_score (phrase-end note membership in target degrees)

Suggested repair:
- increase cadenceTargets.strength
- increase chordToneStrength near phrase ends
