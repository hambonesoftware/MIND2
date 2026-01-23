from __future__ import annotations

import random
from typing import TYPE_CHECKING, Iterable

from .constants import NOTE_NAMES, NAME_TO_PC, PPQ
from .theory.scales import get_scale

if TYPE_CHECKING:
    from .models import Level2Knobs


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def map_tightness_to_timing(tightness_0_1: float, swing_range: tuple[float, float]) -> tuple[float, float, float]:
    tightness_0_1 = clamp01(tightness_0_1)
    swing_min, swing_max = swing_range
    swing_amount = clamp01(lerp(swing_min, swing_max, 1 - tightness_0_1))
    humanize_timing_ms = lerp(2.0, 14.0, 1 - tightness_0_1)
    humanize_velocity = clamp01(lerp(0.04, 0.22, 1 - tightness_0_1))
    return swing_amount, humanize_timing_ms, humanize_velocity


def derive_groove_sync(level2: Level2Knobs, rhythm_archetype: str | None = None) -> tuple[float, float]:
    groove_bias_map = {
        "straight": 0.55,
        "straight_pop": 0.58,
        "four_on_floor": 0.62,
        "half_time": 0.48,
        "bouncy": 0.68,
        "swing": 0.70,
        "laid_back": 0.52,
        "latin": 0.66,
        "waltz": 0.50,
        "march": 0.56,
    }
    groove_key = rhythm_archetype or level2.groove_archetype
    groove_bias = groove_bias_map.get(groove_key, 0.56)
    swing_influence = level2.swing_amount * 0.6 + level2.syncopation * 0.4
    groove = clamp01(lerp(groove_bias, 1.0, swing_influence))
    syncopation = clamp01(lerp(level2.syncopation, min(1.0, level2.syncopation + groove * 0.18), 0.5))
    return groove, syncopation


def pick_weighted(rng: random.Random, items_with_weights):
    total = sum(w for _, w in items_with_weights) or 1.0
    r = rng.random() * total
    acc = 0.0
    for item, w in items_with_weights:
        acc += w
        if r <= acc:
            return item
    return items_with_weights[-1][0]


def pc_to_name(pc: int) -> str:
    return NOTE_NAMES[pc % 12]


def midi_note_name(n: int) -> str:
    pc = n % 12
    octave = (n // 12) - 1
    return f"{pc_to_name(pc)}{octave}"


def key_to_pc(key_name: str) -> int:
    return NAME_TO_PC.get(key_name, 0)


def scale_pcs(tonic_pc: int, mode: str):
    scale = get_scale(mode)
    return [(tonic_pc + x) % 12 for x in scale.intervals]


def degree_to_pc(tonic_pc: int, mode: str, degree_index_0_based: int) -> int:
    pcs = scale_pcs(tonic_pc, mode)
    return pcs[degree_index_0_based % 7]


def diatonic_triad_quality(mode: str, degree_index_0_based: int):
    # In major: I maj, ii min, iii min, IV maj, V maj, vi min, vii dim
    # In natural minor: i min, ii dim, III maj, iv min, v min, VI maj, VII maj
    scale = get_scale(mode)
    if scale.diatonic_chord_qualities:
        qualities = scale.diatonic_chord_qualities
    elif mode == "major":
        qualities = ("maj", "min", "min", "maj", "maj", "min", "dim")
    else:
        qualities = ("min", "dim", "maj", "min", "min", "maj", "maj")
    return qualities[degree_index_0_based % 7]


def build_triad(root_pc: int, quality: str):
    # Return pitch classes for triad
    if quality == "maj":
        intervals = [0, 4, 7]
    elif quality == "min":
        intervals = [0, 3, 7]
    elif quality == "dim":
        intervals = [0, 3, 6]
    else:
        intervals = [0, 4, 7]
    return [(root_pc + i) % 12 for i in intervals]


def build_seventh(root_pc: int, quality: str, dominant7: bool = False):
    # Very simplified: maj7, min7, dom7, half-dim7 (for dim)
    if dominant7:
        intervals = [0, 4, 7, 10]
    else:
        if quality == "maj":
            intervals = [0, 4, 7, 11]  # maj7
        elif quality == "min":
            intervals = [0, 3, 7, 10]  # min7
        elif quality == "dim":
            intervals = [0, 3, 6, 10]  # half-diminished
        else:
            intervals = [0, 4, 7, 11]
    return [(root_pc + i) % 12 for i in intervals]


def unique_pcs(pcs: list[int]) -> list[int]:
    out = []
    seen = set()
    for p in pcs:
        p2 = p % 12
        if p2 not in seen:
            seen.add(p2)
            out.append(p2)
    return out


def degree_label(degree_0_based: int) -> str:
    labels = ["I", "ii", "iii", "IV", "V", "vi", "vii°"]
    return labels[degree_0_based % 7]


def step_to_tick(step_index_0_15: int) -> int:
    # 16 steps per bar, each step is a 16th note.
    ticks_per_16th = PPQ // 4  # 480 / 4 = 120
    return step_index_0_15 * ticks_per_16th


def bar_step_to_abs_tick(bar_index: int, step_index: int, beats_per_bar: int = 4) -> int:
    ticks_per_bar = PPQ * beats_per_bar
    return bar_index * ticks_per_bar + step_to_tick(step_index)


def apply_swing_to_step(step_index: int, swing_amount_0_1: float) -> int:
    """
    Very simple swing on off-beat 8ths:
    - Off-beat 8th positions in 16th grid are steps: 2, 6, 10, 14
    - We delay these by up to ~45 ticks (less than half a 16th at PPQ=480)
    """
    offbeat_8ths = {2, 6, 10, 14}
    if step_index in offbeat_8ths:
        max_delay = 45
        return int(round(max_delay * clamp01(swing_amount_0_1)))
    return 0


def humanize_ticks(rng: random.Random, humanize_ms: float, bpm: int) -> int:
    """
    Convert +/- humanize_ms to ticks.
    ticks_per_second = PPQ * bpm / 60
    """
    if humanize_ms <= 0.0:
        return 0
    delta_ms = (rng.random() * 2.0 - 1.0) * humanize_ms
    ticks_per_second = (PPQ * bpm) / 60.0
    return int(round((delta_ms / 1000.0) * ticks_per_second))


def velocity_humanize(rng: random.Random, base_vel: int, humanize_amt_0_1: float) -> int:
    humanize_amt_0_1 = clamp01(humanize_amt_0_1)
    spread = int(round(lerp(0, 18, humanize_amt_0_1)))
    v = base_vel + rng.randint(-spread, spread)
    return max(1, min(127, v))


def choose_register_base():
    """
    Basic register defaults for pop:
    - melody around C5 (72)
    - harmony around C4 (60)
    - bass around C2 (36)
    """
    return 72, 60, 36


def chord_tones_in_range(chord_pcs: list[int], low_note: int, high_note: int):
    out = []
    for n in range(low_note, high_note + 1):
        if (n % 12) in chord_pcs:
            out.append(n)
    return out


def scale_tones_in_range(scale_pcs_list: list[int], low_note: int, high_note: int):
    out = []
    for n in range(low_note, high_note + 1):
        if (n % 12) in scale_pcs_list:
            out.append(n)
    return out


def nearest_in_set(target: int, choices: list[int]) -> int:
    if not choices:
        return target
    best = choices[0]
    best_d = abs(best - target)
    for c in choices[1:]:
        d = abs(c - target)
        if d < best_d:
            best = c
            best_d = d
    return best


def ticks_to_time_seconds(ticks: int, bpm: int) -> float:
    # ticks per second = PPQ * bpm / 60
    return ticks / ((PPQ * bpm) / 60.0)


def bar_of_tick(abs_tick: int) -> int:
    ticks_per_bar = PPQ * 4
    return int(abs_tick // ticks_per_bar)


def step_of_tick_in_bar(abs_tick: int) -> int:
    ticks_per_bar = PPQ * 4
    tick_in_bar = abs_tick % ticks_per_bar
    ticks_per_16th = PPQ // 4
    return int(round(tick_in_bar / ticks_per_16th))
