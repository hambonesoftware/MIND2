"""JSON-only bridge between the MIND2 Python composer and a static web page.

This module runs in both CPython (for tests) and Pyodide (in the browser).
It deliberately does not import Tkinter or any native MIDI output drivers.
"""

from __future__ import annotations

import base64
from collections import defaultdict, deque
from io import BytesIO
import json
import math

from mind.constants import PPQ
from mind.control_mapping import STYLE_PROFILES, map_controls
from mind.midi_build import build_song_bundle
from mind.models import Controls, StyleMoodControls


def _bounded_number(data: dict, field: str, default: float, lower: float, upper: float) -> float:
    value = data.get(field, default)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field} must be a number")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{field} must be finite")
    return max(lower, min(upper, result))


def _extract_notes(events: list) -> list[dict]:
    """Convert absolute-tick MIDI messages into browser-friendly note spans."""
    sounding: dict[tuple[int, int], deque] = defaultdict(deque)
    notes: list[dict] = []

    # Process note-offs before note-ons at the same tick to avoid stuck notes.
    def order(item):
        tick, message = item
        off = message.type == "note_off" or (
            message.type == "note_on" and message.velocity == 0
        )
        return (tick, 0 if off else 1)

    for tick, message in sorted(events, key=order):
        if message.type not in ("note_on", "note_off"):
            continue
        key = (message.channel, message.note)
        if message.type == "note_on" and message.velocity > 0:
            sounding[key].append((tick, message.velocity))
        elif sounding[key]:
            start, velocity = sounding[key].popleft()
            notes.append(
                {
                    "beat": round(start / PPQ, 5),
                    "duration": round(max(1, tick - start) / PPQ, 5),
                    "pitch": message.note,
                    "velocity": velocity,
                }
            )

    return sorted(notes, key=lambda item: (item["beat"], item["pitch"]))


def generate(request_json: str) -> str:
    """Generate one composition and return note events, form, and a MIDI file."""
    data = json.loads(request_json)
    if not isinstance(data, dict):
        raise ValueError("The composition request must be an object")

    style = str(data.get("style", "pop")).strip().lower()
    if style not in STYLE_PROFILES:
        raise ValueError(f"Unsupported style: {style}")

    mode = str(data.get("mode", "major")).lower()
    if mode not in ("major", "minor"):
        raise ValueError("Mode must be major or minor")

    key = str(data.get("key", "C"))
    if key not in ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"):
        raise ValueError("Unsupported key")

    bars = int(_bounded_number(data, "bars", 16, 4, 32))
    bpm = int(_bounded_number(data, "bpm", 112, 60, 200))
    seed = int(_bounded_number(data, "seed", 48291, 0, 2**31 - 1))

    intent = StyleMoodControls(
        style=style,
        mood_valence=_bounded_number(data, "brightness", 0.55, 0, 1),
        mood_arousal=_bounded_number(data, "energy", 0.55, 0, 1),
        intensity=_bounded_number(data, "intensity", 0.55, 0, 1),
        complexity=_bounded_number(data, "complexity", 0.40, 0, 1),
        tightness=_bounded_number(data, "tightness", 0.65, 0, 1),
        tempo_bpm=bpm,
        key_name=key,
    )
    controls = Controls(
        length_bars=bars,
        bpm=bpm,
        key_name=key,
        mode=mode,
        seed=seed,
        style_mood=intent,
        derived=map_controls(intent, seed),
    )

    midi, plan, chords, parts, report = build_song_bundle(controls)
    midi_stream = BytesIO()
    midi.save(file=midi_stream)

    response = {
        "meta": {"bpm": bpm, "bars": bars, "key": key, "mode": mode, "style": style, "seed": seed},
        "sections": [
            {"name": section.name, "start": section.bar_start, "end": section.bar_end_excl}
            for section in plan.sections
        ],
        "chords": [
            {"bar": chord.bar_index, "step": chord.start_step, "label": chord.label}
            for chord in chords
        ],
        "parts": {part: _extract_notes(events) for part, events in parts.items()},
        "analysis": {
            "melody": report["melody"],
            "noteCounts": {
                part: report["layers"][part]["note_on_count"] for part in parts
            },
            "phraseCount": sum(1 for bar in report["bars"] if bar["is_phrase_end"]),
        },
        "midiBase64": base64.b64encode(midi_stream.getvalue()).decode("ascii"),
    }
    return json.dumps(response, separators=(",", ":"))
