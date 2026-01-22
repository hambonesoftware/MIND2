from __future__ import annotations

from typing import Any

from mido import Message

from ..utils import midi_note_name


def _extract_note_ons(events: list[tuple[int, Message]]) -> list[tuple[int, Message]]:
    note_ons = []
    for abs_tick, msg in events:
        if msg.type != "note_on":
            continue
        if msg.velocity is None or msg.velocity <= 0:
            continue
        note_ons.append((abs_tick, msg))
    return note_ons


def _contour_type(pitches: list[int]) -> str:
    if len(pitches) < 2:
        return "static"

    deltas = [b - a for a, b in zip(pitches, pitches[1:])]
    if all(d >= 0 for d in deltas) and any(d > 0 for d in deltas):
        return "ascending"
    if all(d <= 0 for d in deltas) and any(d < 0 for d in deltas):
        return "descending"

    start = pitches[0]
    end = pitches[-1]
    max_pitch = max(pitches)
    min_pitch = min(pitches)
    max_idx = pitches.index(max_pitch)
    min_idx = pitches.index(min_pitch)

    if max_idx not in (0, len(pitches) - 1) and max_pitch > start and max_pitch > end:
        return "arch"
    if min_idx not in (0, len(pitches) - 1) and min_pitch < start and min_pitch < end:
        return "valley"

    return "mixed"


def analyze_melody_events(events: list[tuple[int, Message]]) -> dict[str, Any]:
    note_ons = sorted(_extract_note_ons(events), key=lambda item: item[0])
    if not note_ons:
        return {"contour": "silence", "leap_count": 0, "stepwise_ratio": 0.0, "climax_note": None}

    pitches = [msg.note for _, msg in note_ons]
    contour = _contour_type(pitches)
    if len(pitches) < 2:
        return {
            "contour": contour,
            "leap_count": 0,
            "stepwise_ratio": 0.0,
            "climax_note": {"note": pitches[0], "note_name": midi_note_name(int(pitches[0]))},
        }

    deltas = [b - a for a, b in zip(pitches, pitches[1:])]
    total_intervals = len(deltas)
    stepwise_count = sum(1 for d in deltas if abs(d) <= 2)
    leap_count = sum(1 for d in deltas if abs(d) >= 3)
    stepwise_ratio = stepwise_count / total_intervals if total_intervals > 0 else 0.0

    climax = max(pitches)
    return {
        "contour": contour,
        "leap_count": leap_count,
        "stepwise_ratio": stepwise_ratio,
        "climax_note": {"note": climax, "note_name": midi_note_name(int(climax))},
    }
