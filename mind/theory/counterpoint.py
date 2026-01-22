from __future__ import annotations

from typing import Any

from mido import Message


def _extract_note_ons(events: list[tuple[int, Message]]) -> list[tuple[int, Message]]:
    note_ons = []
    for abs_tick, msg in events:
        if msg.type != "note_on":
            continue
        if msg.velocity is None or msg.velocity <= 0:
            continue
        note_ons.append((abs_tick, msg))
    return note_ons


def _pair_voices(
    melody_events: list[tuple[int, Message]],
    harmony_events: list[tuple[int, Message]],
) -> list[tuple[int, int, int]]:
    melody_notes = sorted(_extract_note_ons(melody_events), key=lambda item: item[0])
    harmony_notes = sorted(_extract_note_ons(harmony_events), key=lambda item: item[0])
    pair_count = min(len(melody_notes), len(harmony_notes))
    pairs: list[tuple[int, int, int]] = []
    for idx in range(pair_count):
        melody_tick, melody_msg = melody_notes[idx]
        harmony_tick, harmony_msg = harmony_notes[idx]
        tick = max(melody_tick, harmony_tick)
        pairs.append((tick, melody_msg.note, harmony_msg.note))
    return pairs


def analyze_counterpoint(
    melody_events: list[tuple[int, Message]],
    harmony_events: list[tuple[int, Message]],
) -> dict[str, Any]:
    pairs = _pair_voices(melody_events, harmony_events)

    parallel_fifths = []
    parallel_octaves = []
    voice_crossings = []

    for tick, melody_note, harmony_note in pairs:
        if melody_note < harmony_note:
            voice_crossings.append({"tick": tick, "melody": melody_note, "harmony": harmony_note})

    for idx in range(len(pairs) - 1):
        tick_a, melody_a, harmony_a = pairs[idx]
        tick_b, melody_b, harmony_b = pairs[idx + 1]
        interval_a = abs(melody_a - harmony_a)
        interval_b = abs(melody_b - harmony_b)
        melody_motion = melody_b - melody_a
        harmony_motion = harmony_b - harmony_a
        same_direction = melody_motion * harmony_motion > 0

        if same_direction and interval_a % 12 == 7 and interval_b % 12 == 7:
            parallel_fifths.append(
                {
                    "start_tick": tick_a,
                    "end_tick": tick_b,
                    "melody": [melody_a, melody_b],
                    "harmony": [harmony_a, harmony_b],
                    "intervals": [interval_a, interval_b],
                }
            )

        if same_direction and interval_a % 12 == 0 and interval_b % 12 == 0:
            parallel_octaves.append(
                {
                    "start_tick": tick_a,
                    "end_tick": tick_b,
                    "melody": [melody_a, melody_b],
                    "harmony": [harmony_a, harmony_b],
                    "intervals": [interval_a, interval_b],
                }
            )

    return {
        "parallel_fifths": parallel_fifths,
        "parallel_octaves": parallel_octaves,
        "voice_crossings": voice_crossings,
    }
