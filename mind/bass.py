from __future__ import annotations

import random

from mido import Message

from .constants import BASS_CH, GM_BASS
from .models import ChordSegment, Controls, SongPlan
from .utils import (
    bar_step_to_abs_tick,
    chord_tones_in_range,
    scale_pcs,
    scale_tones_in_range,
    clamp01,
    lerp,
    pick_weighted,
    apply_swing_to_step,
    humanize_ticks,
    velocity_humanize,
    key_to_pc,
    choose_register_base,
    nearest_in_set,
)


def _choose_bass_cell(rng: random.Random, archetype: str, style: str | None):
    patterns = []
    style_key = (style or "").strip().lower()
    if style_key == "jazz":
        patterns = [
            ([0, 2, 4, 6, 8, 10, 12, 14], 0.40),
            ([0, 2, 4, 8, 10, 12, 14], 0.25),
            ([0, 2, 6, 8, 10, 12, 14], 0.20),
            ([0, 4, 6, 8, 10, 12, 14], 0.15),
        ]
    elif style_key == "pop":
        patterns = [
            ([0, 4, 8, 12], 0.35),
            ([0, 6, 8, 14], 0.25),
            ([0, 3, 8, 11, 14], 0.20),
            ([0, 2, 8, 10, 14], 0.20),
        ]
    elif style_key == "classical":
        patterns = [
            ([0, 4, 8, 12], 0.40),
            ([0, 2, 4, 6, 8, 10, 12, 14], 0.25),
            ([0, 4, 6, 8, 10, 12], 0.20),
            ([0, 2, 6, 8, 12, 14], 0.15),
        ]
    elif archetype == "four_on_floor":
        patterns = [
            ([0, 4, 8, 12], 0.35),
            ([0, 6, 8, 14], 0.25),
            ([0, 8, 10, 12], 0.20),
            ([0, 2, 8, 10, 12, 14], 0.20),
        ]
    elif archetype == "half_time":
        patterns = [
            ([0, 6, 8, 14], 0.35),
            ([0, 8, 12], 0.25),
            ([0, 3, 8, 11, 14], 0.20),
            ([0, 2, 6, 8, 10, 14], 0.20),
        ]
    elif archetype == "bouncy":
        patterns = [
            ([0, 3, 7, 10, 14], 0.35),
            ([0, 2, 7, 10, 12, 14], 0.25),
            ([0, 5, 7, 10, 15], 0.20),
            ([0, 2, 6, 10, 14], 0.20),
        ]
    else:  # straight_pop
        patterns = [
            ([0, 8], 0.30),
            ([0, 4, 8, 12], 0.30),
            ([0, 6, 8, 14], 0.20),
            ([0, 2, 8, 10, 14], 0.20),
        ]

    return pick_weighted(rng, patterns)


def generate_bass_track(ctrl: Controls, chord_segments: list[ChordSegment], plan: SongPlan):
    rng = random.Random(ctrl.seed + 202)
    tonic_pc = key_to_pc(ctrl.key_name)
    scale = scale_pcs(tonic_pc, ctrl.mode)

    _, _, bass_base = choose_register_base()
    low = bass_base - 2
    high = bass_base + 14

    events = []
    events.append((0, Message("program_change", channel=BASS_CH, program=GM_BASS, time=0)))

    base_vel_global = int(round(lerp(62, 98, ctrl.energy)))

    bass_cell = _choose_bass_cell(rng, plan.rhythm.archetype, ctrl.progression_style)

    anticipate_prob_base = clamp01(lerp(0.05, 0.35, ctrl.syncopation))
    approach_prob_base = clamp01(lerp(0.03, 0.16, ctrl.chord_complexity))

    for seg in chord_segments:
        mod = plan.bar_mods[seg.bar_index]

        density_eff = clamp01(ctrl.density * mod.density_mul)
        sync_eff = clamp01(ctrl.syncopation * mod.sync_mul)
        energy_eff = clamp01(ctrl.energy * mod.energy_mul)

        base_vel = int(round(base_vel_global * lerp(0.90, 1.10, energy_eff)))

        root_pc = seg.root_pc % 12
        root_choices = [n for n in range(low, high + 1) if (n % 12) == root_pc]
        if not root_choices:
            root_choices = [bass_base]
        root_note = nearest_in_set(bass_base, root_choices)

        seg_steps = max(1, seg.end_step - seg.start_step)
        cell_steps = [s for s in bass_cell if seg.start_step <= s < seg.end_step]

        if seg_steps <= 8:
            cell_steps = [seg.start_step + int(round((s - seg.start_step) * (seg_steps / 16.0))) for s in bass_cell]
            cell_steps = [s for s in cell_steps if seg.start_step <= s < seg.end_step]

        cell_steps = sorted(set(cell_steps))

        if density_eff < 0.45 and len(cell_steps) > 2:
            keep = [seg.start_step]
            for cand in [8, 4, 12, 6, 10, 14]:
                if seg.start_step <= cand < seg.end_step:
                    keep.append(cand)
                    break
            cell_steps = sorted(set(keep))

        if density_eff > 0.70 and rng.random() < lerp(0.10, 0.55, density_eff):
            extra_candidates = [s for s in range(seg.start_step, seg.end_step) if s not in cell_steps]
            if extra_candidates:
                extra = pick_weighted(
                    rng,
                    [(s, (1.8 if (s % 2 == 1) else 1.0) * lerp(0.8, 1.6, sync_eff)) for s in extra_candidates],
                )
                cell_steps.append(extra)
                cell_steps = sorted(set(cell_steps))

        anticipate_prob = clamp01(anticipate_prob_base * lerp(0.85, 1.25, sync_eff))
        approach_prob = clamp01(approach_prob_base * lerp(0.85, 1.25, density_eff))

        for step in cell_steps:
            place_step = step

            if rng.random() < anticipate_prob and place_step - 2 >= seg.start_step:
                place_step -= 2

            on_tick = bar_step_to_abs_tick(seg.bar_index, place_step)
            on_tick += apply_swing_to_step(place_step, ctrl.swing)
            on_tick += humanize_ticks(rng, ctrl.humanize_timing_ms, ctrl.bpm)

            dur_steps = 2 if (density_eff > 0.60 or mod.section == "chorus") else 4
            off_step = min(seg.end_step, place_step + dur_steps)
            off_tick = bar_step_to_abs_tick(seg.bar_index, off_step)

            if rng.random() < approach_prob and place_step + 1 < seg.end_step:
                scale_notes = scale_tones_in_range(scale, low, high)
                chord_notes = chord_tones_in_range(seg.pcs, low, high)
                pool = chord_notes if chord_notes and rng.random() < 0.55 else scale_notes
                if pool:
                    neigh = nearest_in_set(root_note - 2, pool)
                    if rng.random() < 0.5:
                        neigh = nearest_in_set(root_note + 2, pool)

                    a_on = bar_step_to_abs_tick(seg.bar_index, place_step)
                    a_on += humanize_ticks(rng, ctrl.humanize_timing_ms, ctrl.bpm)
                    a_off = bar_step_to_abs_tick(seg.bar_index, min(seg.end_step, place_step + 1))
                    vel_a = velocity_humanize(rng, int(base_vel * 0.78), ctrl.humanize_velocity)
                    events.append((max(0, a_on), Message("note_on", channel=BASS_CH, note=neigh, velocity=vel_a, time=0)))
                    events.append((max(0, a_off), Message("note_off", channel=BASS_CH, note=neigh, velocity=0, time=0)))

                    on_tick = bar_step_to_abs_tick(seg.bar_index, min(seg.end_step - 1, place_step + 1))
                    on_tick += humanize_ticks(rng, ctrl.humanize_timing_ms, ctrl.bpm)

            note_to_play = root_note

            if mod.section == "chorus" and rng.random() < lerp(0.05, 0.18, density_eff):
                oct_note = root_note + 12
                if oct_note <= high and rng.random() < 0.55:
                    note_to_play = oct_note

            vel = velocity_humanize(rng, base_vel, ctrl.humanize_velocity)
            events.append((max(0, on_tick), Message("note_on", channel=BASS_CH, note=note_to_play, velocity=vel, time=0)))
            events.append((max(0, off_tick), Message("note_off", channel=BASS_CH, note=note_to_play, velocity=0, time=0)))

    return events
