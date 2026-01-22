from __future__ import annotations

from mind.theory.rhythm import analyze_rhythm
from mind.utils import bar_step_to_abs_tick


def _ticks_for_steps(steps: list[int], bar: int = 0) -> list[int]:
    return [bar_step_to_abs_tick(bar, step) for step in steps]


def test_analyze_rhythm_on_beat():
    ticks = _ticks_for_steps([0, 4, 8, 12])
    metrics = analyze_rhythm(ticks, total_bars=1)

    assert metrics["syncopation"] == 0.0
    assert metrics["density"] == 4.0
    assert metrics["groove_type"] == "on_beat"


def test_analyze_rhythm_offbeat():
    ticks = _ticks_for_steps([2, 6, 10, 14])
    metrics = analyze_rhythm(ticks, total_bars=1)

    assert metrics["syncopation"] == 1.0
    assert metrics["density"] == 4.0
    assert metrics["groove_type"] == "offbeat"


def test_analyze_rhythm_straight_eighths():
    ticks = _ticks_for_steps([0, 2, 4, 6, 8, 10, 12, 14])
    metrics = analyze_rhythm(ticks, total_bars=1)

    assert metrics["syncopation"] == 0.5
    assert metrics["density"] == 8.0
    assert metrics["groove_type"] == "straight"
