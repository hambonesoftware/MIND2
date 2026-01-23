from __future__ import annotations

import random

from mido import Message

from .constants import (
    DRUM_CHANNEL,
    DRUM_CRASH,
    DRUM_HAT_CLOSED,
    DRUM_HAT_OPEN,
    DRUM_KICK,
    DRUM_SNARE,
    DRUM_TOM_HIGH,
    DRUM_TOM_LOW,
    DRUM_TOM_MID,
)
from .models import Controls, SongPlan
from .utils import bar_step_to_abs_tick, clamp01, lerp, humanize_ticks, apply_swing_to_step, velocity_humanize, derive_groove_sync


def _vary_steps(rng: random.Random, steps: list[int], add_prob: float, remove_prob: float, allowed_range=(0, 15)):
    steps = sorted(set([s for s in steps if allowed_range[0] <= s <= allowed_range[1]]))
    if steps and rng.random() < remove_prob:
        removable = [s for s in steps if s not in (0, 4, 8, 12)]
        if removable:
            steps.remove(rng.choice(removable))
    if rng.random() < add_prob:
        candidates = [s for s in range(allowed_range[0], allowed_range[1] + 1) if s not in steps]
        if candidates:
            weighted = []
            for s in candidates:
                w = 1.0
                if s % 2 == 1:
                    w *= 1.7
                if s in (6, 10, 14):
                    w *= 1.5
                weighted.append((s, w))
            from .utils import pick_weighted
            steps.append(pick_weighted(rng, weighted))
            steps = sorted(set(steps))
    return steps


def generate_drums_track(ctrl: Controls, plan: SongPlan):
    rng = random.Random(ctrl.seed + 404)
    events = []

    base_kick_vel = int(round(lerp(70, 112, ctrl.derived.energy)))
    base_snare_vel = int(round(72))
    base_hat_vel = int(round(lerp(40, 90, ctrl.derived.energy)))

    rp = plan.rhythm
    groove_level, sync_base = derive_groove_sync(ctrl.derived.level2, rp.archetype)

    for bar in range(ctrl.length_bars):
        mod = plan.bar_mods[bar]

        density_eff = clamp01(ctrl.derived.density * lerp(0.85, 1.12, groove_level) * mod.density_mul)
        sync_eff = clamp01(sync_base * mod.sync_mul)
        energy_eff = clamp01(ctrl.derived.energy * mod.energy_mul)
        variation_eff = clamp01(ctrl.derived.variation * mod.variation_mul)

        kick_vel = int(round(lerp(70, 115, energy_eff)))
        snare_vel = int(round(lerp(72, 118, energy_eff)))
        hat_vel = int(round(lerp(38, 92, energy_eff)))

        kick_steps = rp.base_kick_steps[:]
        snare_steps = rp.base_snare_steps[:]
        hat_steps = rp.base_hat_steps[:]

        hat_16th_prob = clamp01(rp.hat_16th_bias * lerp(0.55, 1.20, density_eff))
        if mod.section == "chorus":
            hat_16th_prob = clamp01(hat_16th_prob * 1.15)

        if rng.random() < hat_16th_prob:
            for s in [1, 3, 5, 7, 9, 11, 13, 15]:
                if rng.random() < clamp01(lerp(0.25, 0.95, density_eff)):
                    hat_steps.append(s)
        hat_steps = sorted(set([s for s in hat_steps if 0 <= s <= 15]))

        extra_kick_prob = clamp01(rp.kick_sync_bias * lerp(0.65, 1.35, sync_eff))
        if mod.section == "chorus":
            extra_kick_prob = clamp01(extra_kick_prob * 1.10)
        if rng.random() < extra_kick_prob:
            kick_steps = _vary_steps(rng, kick_steps, add_prob=0.75, remove_prob=0.0)
        if rng.random() < extra_kick_prob * 0.45:
            kick_steps = _vary_steps(rng, kick_steps, add_prob=0.55, remove_prob=0.0)

        ghost_prob = clamp01(lerp(0.05, 0.40, sync_eff))
        if rng.random() < ghost_prob:
            snare_steps.append(3)
        if rng.random() < ghost_prob:
            snare_steps.append(11)
        snare_steps = sorted(set([s for s in snare_steps if 0 <= s <= 15]))

        if mod.is_section_start and bar != 0:
            on_tick = bar_step_to_abs_tick(bar, 0) + humanize_ticks(rng, ctrl.derived.humanize_timing_ms, ctrl.bpm)
            off_tick = bar_step_to_abs_tick(bar, 1)
            v = velocity_humanize(rng, int(round(lerp(85, 120, energy_eff))), ctrl.derived.humanize_velocity)
            events.append((max(0, on_tick), Message("note_on", channel=DRUM_CHANNEL, note=DRUM_CRASH, velocity=v, time=0)))
            events.append((max(0, off_tick), Message("note_off", channel=DRUM_CHANNEL, note=DRUM_CRASH, velocity=0, time=0)))

        do_fill = False
        if mod.is_phrase_end and bar != ctrl.length_bars - 1:
            do_fill = rng.random() < clamp01(lerp(0.20, 0.85, variation_eff) * lerp(0.70, 1.25, energy_eff))
        if mod.is_section_end and bar != ctrl.length_bars - 1:
            do_fill = do_fill or (rng.random() < clamp01(lerp(0.20, 0.90, variation_eff) * 1.10))

        kick_steps = sorted(set([s for s in kick_steps if 0 <= s <= 15]))
        for s in kick_steps:
            on_tick = bar_step_to_abs_tick(bar, s) + humanize_ticks(rng, ctrl.derived.humanize_timing_ms, ctrl.bpm)
            off_tick = bar_step_to_abs_tick(bar, min(16, s + 1))
            vel = velocity_humanize(rng, kick_vel, ctrl.derived.humanize_velocity)
            events.append((max(0, on_tick), Message("note_on", channel=DRUM_CHANNEL, note=DRUM_KICK, velocity=vel, time=0)))
            events.append((max(0, off_tick), Message("note_off", channel=DRUM_CHANNEL, note=DRUM_KICK, velocity=0, time=0)))

        for s in snare_steps:
            on_tick = bar_step_to_abs_tick(bar, s) + humanize_ticks(rng, ctrl.derived.humanize_timing_ms, ctrl.bpm)
            off_tick = bar_step_to_abs_tick(bar, min(16, s + 1))
            is_ghost = (s in (3, 11))
            v0 = int(round(snare_vel * (0.45 if is_ghost else 1.0)))
            vel = velocity_humanize(rng, v0, ctrl.derived.humanize_velocity)
            events.append((max(0, on_tick), Message("note_on", channel=DRUM_CHANNEL, note=DRUM_SNARE, velocity=vel, time=0)))
            events.append((max(0, off_tick), Message("note_off", channel=DRUM_CHANNEL, note=DRUM_SNARE, velocity=0, time=0)))

        for s in hat_steps:
            on_tick = bar_step_to_abs_tick(bar, s) + apply_swing_to_step(s, ctrl.derived.swing) + humanize_ticks(rng, ctrl.derived.humanize_timing_ms, ctrl.bpm)
            off_tick = bar_step_to_abs_tick(bar, min(16, s + 1))
            vel = velocity_humanize(rng, hat_vel, ctrl.derived.humanize_velocity)
            events.append((max(0, on_tick), Message("note_on", channel=DRUM_CHANNEL, note=DRUM_HAT_CLOSED, velocity=vel, time=0)))
            events.append((max(0, off_tick), Message("note_off", channel=DRUM_CHANNEL, note=DRUM_HAT_CLOSED, velocity=0, time=0)))

        if do_fill:
            if rp.fill_style == "snare_roll":
                roll_steps = [12, 13, 14, 15]
                for i, s in enumerate(roll_steps):
                    on_tick = bar_step_to_abs_tick(bar, s) + humanize_ticks(rng, ctrl.derived.humanize_timing_ms, ctrl.bpm)
                    off_tick = bar_step_to_abs_tick(bar, min(16, s + 1))
                    ramp = lerp(0.65, 1.10, i / max(1, len(roll_steps) - 1))
                    vel = velocity_humanize(rng, int(round(snare_vel * ramp)), ctrl.derived.humanize_velocity)
                    events.append((max(0, on_tick), Message("note_on", channel=DRUM_CHANNEL, note=DRUM_SNARE, velocity=vel, time=0)))
                    events.append((max(0, off_tick), Message("note_off", channel=DRUM_CHANNEL, note=DRUM_SNARE, velocity=0, time=0)))
                if rng.random() < 0.35:
                    s = 14
                    on_tick = bar_step_to_abs_tick(bar, s)
                    on_tick += apply_swing_to_step(s, ctrl.derived.swing)
                    on_tick += humanize_ticks(rng, ctrl.derived.humanize_timing_ms, ctrl.bpm)
                    off_tick = bar_step_to_abs_tick(bar, min(16, s + 1))
                    vel = velocity_humanize(rng, int(round(hat_vel * 0.95)), ctrl.derived.humanize_velocity)
                    events.append((max(0, on_tick), Message("note_on", channel=DRUM_CHANNEL, note=DRUM_HAT_OPEN, velocity=vel, time=0)))
                    events.append((max(0, off_tick), Message("note_off", channel=DRUM_CHANNEL, note=DRUM_HAT_OPEN, velocity=0, time=0)))
            else:
                tom_seq = [(12, DRUM_TOM_LOW), (13, DRUM_TOM_MID), (14, DRUM_TOM_HIGH), (15, DRUM_SNARE)]
                for i, (s, drum_note) in enumerate(tom_seq):
                    on_tick = bar_step_to_abs_tick(bar, s) + humanize_ticks(rng, ctrl.derived.humanize_timing_ms, ctrl.bpm)
                    off_tick = bar_step_to_abs_tick(bar, min(16, s + 1))
                    ramp = lerp(0.70, 1.10, i / max(1, len(tom_seq) - 1))
                    vel = velocity_humanize(rng, int(round(snare_vel * ramp)), ctrl.derived.humanize_velocity)
                    events.append((max(0, on_tick), Message("note_on", channel=DRUM_CHANNEL, note=drum_note, velocity=vel, time=0)))
                    events.append((max(0, off_tick), Message("note_off", channel=DRUM_CHANNEL, note=drum_note, velocity=0, time=0)))

    return events
