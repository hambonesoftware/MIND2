from __future__ import annotations

import random

from ..utils import chord_tones_in_range, nearest_in_set


def initial_voicing(
    rng: random.Random,
    chord_pcs: list[int],
    low: int,
    high: int,
    center: int,
    voice_count: int,
) -> list[int]:
    """Pick a starting voicing anchored around a center pitch."""
    chord_notes = chord_tones_in_range(chord_pcs, low, high)
    if not chord_notes:
        return []

    chord_notes_sorted = sorted(set(chord_notes))
    first = nearest_in_set(center, chord_notes_sorted)

    voicing = [first]
    idx = chord_notes_sorted.index(first) if first in chord_notes_sorted else 0

    while len(voicing) < voice_count:
        step = rng.choices([2, 4, 6, 7], weights=[0.45, 0.35, 0.15, 0.05])[0]
        ni = min(len(chord_notes_sorted) - 1, idx + step)
        cand = chord_notes_sorted[ni]
        if cand not in voicing:
            voicing.append(cand)
            continue
        ni2 = min(len(chord_notes_sorted) - 1, ni + 1)
        cand2 = chord_notes_sorted[ni2]
        if cand2 not in voicing:
            voicing.append(cand2)
        else:
            break

    return sorted(voicing)


def smooth_voice_leading(prev_voicing: list[int], chord_pcs: list[int], low: int, high: int) -> list[int]:
    """Return a new voicing that minimizes movement and preserves common tones."""
    if not prev_voicing:
        return []

    target_notes = chord_tones_in_range(chord_pcs, low, high)
    if not target_notes:
        return prev_voicing[:]

    target_notes_sorted = sorted(set(target_notes))
    new_voicing: list[int] = []
    last_assigned = low - 1

    for v in sorted(prev_voicing):
        if (v % 12) in chord_pcs and low <= v <= high:
            chosen = v
        else:
            chosen = nearest_in_set(v, target_notes_sorted)

        if chosen <= last_assigned:
            higher = [n for n in target_notes_sorted if n > last_assigned]
            if higher:
                chosen = nearest_in_set(v, higher)
            else:
                chosen = min(high, last_assigned + 1)

        new_voicing.append(chosen)
        last_assigned = chosen

    fixed: list[int] = []
    used = set()
    last = low - 1
    for n in new_voicing:
        cand = max(n, last + 1)
        while cand in used and (cand + 12) <= high:
            cand += 12
        if cand in used:
            higher = [x for x in target_notes_sorted if x > last]
            if higher:
                cand = higher[0]
        cand = min(high, max(low, cand))
        fixed.append(cand)
        used.add(cand)
        last = cand

    return fixed
