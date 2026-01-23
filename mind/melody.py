from __future__ import annotations

import math
import random

from mido import Message

from .constants import GM_EPIANO, MELODY_CH
from .models import ChordSegment, Controls, SongPlan
from .harmony import segment_for_step
from .utils import (
    bar_step_to_abs_tick,
    chord_tones_in_range,
    scale_pcs,
    scale_tones_in_range,
    clamp01,
    clamp,
    lerp,
    pick_weighted,
    apply_swing_to_step,
    humanize_ticks,
    velocity_humanize,
    key_to_pc,
    choose_register_base,
    nearest_in_set,
    derive_groove_sync,
)


def contour_offset(contour, bar_index: int, length_bars: int) -> float:
    if length_bars <= 1:
        return 0.0

    t = bar_index / max(1, length_bars - 1)
    intensity = contour.intensity

    if contour.kind == "arch":
        val = 1.0 - (2.0 * (t - 0.5)) ** 2
        return lerp(-1.5, +4.0, clamp01(val)) * intensity
    if contour.kind == "descending":
        return lerp(+4.0, -2.0, t) * intensity
    if contour.kind == "ascending":
        return lerp(-2.0, +4.0, t) * intensity
    if contour.kind == "wave":
        val = math.sin(2.0 * math.pi * (t * 2.0))
        return (val * 3.0) * intensity
    if contour.kind == "plateau":
        return (lerp(0.0, 2.0, clamp01((t - 0.65) / 0.35))) * intensity

    return 0.0


def generate_melody_track(
    ctrl: Controls,
    chord_segments: list[ChordSegment],
    plan: SongPlan,
    style: str | None = None,
):
    rng = random.Random(ctrl.seed + 303)
    tonic_pc = key_to_pc(ctrl.key_name)
    scale = scale_pcs(tonic_pc, ctrl.mode)
    style_key = (style or ctrl.derived.progression_style or "pop").strip().lower()
    groove_level, sync_base = derive_groove_sync(ctrl.derived.level2, plan.rhythm.archetype)
    anchor_strength = clamp01(ctrl.derived.level2.chord_tone_anchoring)

    melody_base, _, _ = choose_register_base()

    events = []
    events.append((0, Message("program_change", channel=MELODY_CH, program=GM_EPIANO, time=0)))

    motif_len_bars = 2
    motif_cache: list[tuple[int, int, int, int, int]] | None = None  # (bar_in_motif, step, note, dur, vel)

    def bar_density_energy_sync(bar_index: int):
        mod = plan.bar_mods[bar_index]
        density_eff = clamp01(ctrl.derived.density * lerp(0.85, 1.12, groove_level) * mod.density_mul)
        energy_eff = clamp01(ctrl.derived.energy * mod.energy_mul)
        sync_eff = clamp01(sync_base * mod.sync_mul)
        variation_eff = clamp01(ctrl.derived.variation * mod.variation_mul)
        repetition_eff = clamp01(ctrl.derived.repetition * mod.repetition_mul)
        return mod, density_eff, energy_eff, sync_eff, variation_eff, repetition_eff

    def build_bar_notes(bar_index: int):
        nonlocal motif_cache

        mod, density_eff, energy_eff, sync_eff, variation_eff, repetition_eff = bar_density_energy_sync(bar_index)

        motif_reuse_prob = clamp01(repetition_eff)
        if style_key == "pop":
            motif_reuse_prob = clamp01(motif_reuse_prob * 1.20 + 0.05)
        elif style_key == "jazz":
            motif_reuse_prob = clamp01(motif_reuse_prob * 0.70)
        elif style_key == "classical":
            motif_reuse_prob = clamp01(motif_reuse_prob * 0.95 + 0.02)
        if mod.section == "chorus":
            motif_reuse_prob = clamp01(motif_reuse_prob * 0.85 + 0.05)

        if motif_cache is not None and rng.random() < motif_reuse_prob:
            bar_in_motif = (bar_index % motif_len_bars)
            motif_events = [e for e in motif_cache if e[0] == bar_in_motif]
            if mod.section == "chorus" and rng.random() < lerp(0.12, 0.35, variation_eff):
                transpose = pick_weighted(rng, [(0, 0.55), (2, 0.20), (-2, 0.20), (5, 0.05)])
                adjusted = []
                for e in motif_events:
                    adjusted.append((e[0], e[1], e[2] + transpose, e[3], e[4]))
                return adjusted
            return motif_events

        segs = [s for s in chord_segments if s.bar_index == bar_index]
        if not segs:
            return []

        contour_off = contour_offset(plan.contour, bar_index, ctrl.length_bars)
        center_shift = mod.melody_shift_semitones + contour_off
        center = int(round(melody_base + center_shift))

        range_semitones = int(round(lerp(8, 15, (energy_eff * 0.55 + variation_eff * 0.45))))
        low = center - range_semitones
        high = center + range_semitones

        notes_per_bar = lerp(2.5, 10.0, density_eff)
        notes_per_bar = max(2, min(12, int(round(notes_per_bar))))

        offbeat_prob = clamp01(lerp(0.15, 0.60, sync_eff))
        if style_key == "jazz":
            offbeat_prob = clamp01(offbeat_prob + 0.12)
        elif style_key == "classical":
            offbeat_prob = clamp01(offbeat_prob - 0.12)

        prefer_step_prob = clamp01(lerp(0.82, 0.50, variation_eff))
        if mod.section == "chorus":
            prefer_step_prob = clamp01(prefer_step_prob * 1.05)
        if style_key == "classical":
            prefer_step_prob = clamp01(prefer_step_prob + 0.12)

        candidates = list(range(0, 16))
        weighted = []
        for s in candidates:
            is_strong = (s in (0, 4, 8, 12))
            is_off8 = (s in (2, 6, 10, 14))
            w = 1.0
            if is_strong:
                w *= 2.9
            elif is_off8:
                w *= lerp(0.9, 2.3, offbeat_prob)
            else:
                w *= lerp(0.55, 1.75, offbeat_prob)
            if mod.section == "chorus" and (s % 2 == 0):
                w *= 1.05
            weighted.append((s, w))

        chosen_steps = []
        while len(chosen_steps) < notes_per_bar and weighted:
            s = pick_weighted(rng, weighted)
            if s not in chosen_steps:
                chosen_steps.append(s)
        chosen_steps = sorted(chosen_steps)

        bar_notes = []
        last_note = None

        def step_target(step: int):
            t_in_bar = step / 15.0
            wobble = math.sin(math.pi * t_in_bar) * 2.0
            return center + int(round(wobble * plan.contour.intensity * 0.55))

        for s in chosen_steps:
            seg = segment_for_step(segs, s)
            chord_pcs = seg.pcs if seg else scale

            chord_tones = chord_tones_in_range(chord_pcs, low, high)
            scale_tones = scale_tones_in_range(scale, low, high)

            is_strong = (s in (0, 4, 8, 12))
            is_offbeat = (s in (2, 6, 10, 14))
            strong_anchor_prob = lerp(0.35, 0.95, anchor_strength)
            weak_anchor_prob = lerp(0.10, 0.50, anchor_strength)
            choose_from = scale_tones if scale_tones else chord_tones
            if is_strong and chord_tones and rng.random() < strong_anchor_prob:
                choose_from = chord_tones
            elif (not is_strong) and chord_tones and rng.random() < weak_anchor_prob:
                choose_from = chord_tones + (scale_tones if scale_tones else [])
            if style_key == "pop" and s in (0, 8) and chord_tones:
                choose_from = chord_tones
            if style_key == "jazz" and is_offbeat and chord_tones:
                choose_from = chord_tones + scale_tones
            if style_key == "classical" and mod.is_phrase_end and chord_tones:
                choose_from = chord_tones
            if not choose_from:
                choose_from = [center]

            tgt = step_target(s)

            if last_note is None:
                note = nearest_in_set(tgt, choose_from)
            else:
                chroma_prob = 0.0
                if style_key == "jazz" and is_offbeat:
                    chroma_prob = 0.22
                elif style_key == "pop":
                    chroma_prob = 0.05
                elif style_key == "classical":
                    chroma_prob = 0.02

                if chroma_prob > 0.0 and chord_tones and rng.random() < chroma_prob:
                    approach = rng.choice(chord_tones)
                    direction = rng.choice([-1, 1])
                    note = clamp(approach + direction, low, high)
                elif rng.random() < prefer_step_prob:
                    if style_key == "classical" and mod.is_phrase_end and chord_tones:
                        cadence_target = nearest_in_set(tgt, chord_tones)
                        step_dir = 2 if (cadence_target >= last_note) else -2
                    else:
                        step_dir = 2 if (tgt >= last_note) else -2
                    target = last_note + step_dir
                    target = int(round(lerp(target, tgt, 0.35)))
                    note = nearest_in_set(target, choose_from)
                else:
                    if style_key == "classical":
                        leap = rng.choice([3, 4, -3, -4, 5, -5])
                    else:
                        leap = rng.choice([4, 5, 7, -4, -5, -7, 9, -9])
                    target = last_note + leap
                    target = int(round(lerp(target, tgt, 0.50)))
                    note = nearest_in_set(target, choose_from)

            if last_note is not None and note == last_note and repetition_eff < 0.55:
                note = nearest_in_set(note + (2 if rng.random() < 0.5 else -2), choose_from)

            last_note = note

            if density_eff > 0.62:
                dur_steps = pick_weighted(rng, [(1, 0.38), (2, 0.50), (4, 0.10), (6, 0.02)])
            else:
                dur_steps = pick_weighted(rng, [(2, 0.45), (4, 0.40), (1, 0.10), (6, 0.05)])

            base_vel = int(round(lerp(55, 98, energy_eff)))
            if is_strong:
                vel = int(round(base_vel * lerp(1.05, 1.22, clamp01(energy_eff))))
            else:
                vel = int(round(base_vel * lerp(0.75, 1.00, clamp01(energy_eff))))
            vel = velocity_humanize(rng, vel, ctrl.derived.humanize_velocity)

            bar_notes.append((0, s, note, dur_steps, vel))

        if mod.is_phrase_end and bar_index != ctrl.length_bars - 1:
            if rng.random() < clamp01(lerp(0.12, 0.55, variation_eff) * lerp(0.65, 1.25, sync_eff)):
                next_bar = bar_index + 1
                next_segs = [s for s in chord_segments if s.bar_index == next_bar]
                next_chord = next_segs[0].pcs if next_segs else scale
                next_choices = chord_tones_in_range(next_chord, low, high)
                if not next_choices:
                    next_choices = scale_tones_in_range(scale, low, high)
                if next_choices:
                    pickup_step = 14 if rng.random() < 0.65 else 15
                    tgt2 = step_target(pickup_step) + 2
                    pickup_note = nearest_in_set(tgt2, next_choices)
                    pickup_vel = velocity_humanize(rng, int(lerp(60, 105, energy_eff)), ctrl.derived.humanize_velocity)
                    bar_notes.append((0, pickup_step, pickup_note, 1, pickup_vel))
                    bar_notes = sorted(bar_notes, key=lambda x: x[1])

        if motif_cache is None and bar_index < motif_len_bars:
            motif_cache = []
            for e in bar_notes:
                motif_cache.append((bar_index, e[1], e[2], e[3], e[4]))

        return bar_notes

    for bar in range(ctrl.length_bars):
        bar_events = build_bar_notes(bar)
        for _, step, note, dur_steps, vel in bar_events:
            on_tick = bar_step_to_abs_tick(bar, step)
            on_tick += apply_swing_to_step(step, ctrl.derived.swing)
            on_tick += humanize_ticks(rng, ctrl.derived.humanize_timing_ms, ctrl.bpm)

            off_step = min(16, step + dur_steps)
            off_tick = bar_step_to_abs_tick(bar, off_step)

            events.append((max(0, on_tick), Message("note_on", channel=MELODY_CH, note=note, velocity=vel, time=0)))
            events.append((max(0, off_tick), Message("note_off", channel=MELODY_CH, note=note, velocity=0, time=0)))

    return events
