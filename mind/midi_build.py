from __future__ import annotations

import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage

from .constants import PPQ
from .models import Controls
from .planning import build_song_plan
from .harmony import build_chord_segments, generate_harmony_track
from .bass import generate_bass_track
from .melody import generate_melody_track
from .drums import generate_drums_track
from .reporting import build_song_report


def build_midifile(ctrl: Controls, include_parts=("melody", "harmony", "bass", "drums")) -> MidiFile:
    """Build a standard MIDI file."""
    mid = MidiFile(ticks_per_beat=PPQ)

    meta = MidiTrack()
    mid.tracks.append(meta)
    meta.append(MetaMessage("set_tempo", tempo=mido.bpm2tempo(ctrl.bpm), time=0))
    meta.append(MetaMessage("time_signature", numerator=4, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))
    meta.append(MetaMessage("track_name", name="PopKnobPlayer", time=0))

    plan = build_song_plan(ctrl)
    chord_segments = build_chord_segments(ctrl, plan)

    part_events: dict[str, list[tuple[int, Message]]] = {}

    if "harmony" in include_parts:
        part_events["harmony"] = generate_harmony_track(ctrl, chord_segments, plan)
    if "bass" in include_parts:
        part_events["bass"] = generate_bass_track(ctrl, chord_segments, plan)
    if "melody" in include_parts:
        part_events["melody"] = generate_melody_track(ctrl, chord_segments, plan)
    if "drums" in include_parts:
        part_events["drums"] = generate_drums_track(ctrl, plan)

    for part_name in ["melody", "harmony", "bass", "drums"]:
        if part_name not in part_events:
            continue
        tr = MidiTrack()
        mid.tracks.append(tr)
        tr.append(MetaMessage("track_name", name=part_name, time=0))

        evs = sorted(part_events[part_name], key=lambda x: x[0])
        last_tick = 0
        for abs_tick, msg in evs:
            delta = max(0, abs_tick - last_tick)
            last_tick = abs_tick
            msg2 = msg.copy(time=delta)
            tr.append(msg2)

        tr.append(MetaMessage("end_of_track", time=0))

    return mid


def build_song_bundle(ctrl: Controls, include_parts=("melody", "harmony", "bass", "drums")):
    """
    Build:
      - mid
      - plan
      - chord_segments
      - part_events
      - report
    """
    plan = build_song_plan(ctrl)
    chord_segments = build_chord_segments(ctrl, plan)

    part_events: dict[str, list[tuple[int, Message]]] = {}

    if "harmony" in include_parts:
        part_events["harmony"] = generate_harmony_track(ctrl, chord_segments, plan)
    if "bass" in include_parts:
        part_events["bass"] = generate_bass_track(ctrl, chord_segments, plan)
    if "melody" in include_parts:
        part_events["melody"] = generate_melody_track(ctrl, chord_segments, plan)
    if "drums" in include_parts:
        part_events["drums"] = generate_drums_track(ctrl, plan)

    mid = MidiFile(ticks_per_beat=PPQ)
    meta = MidiTrack()
    mid.tracks.append(meta)
    meta.append(MetaMessage("set_tempo", tempo=mido.bpm2tempo(ctrl.bpm), time=0))
    meta.append(MetaMessage("time_signature", numerator=4, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))
    meta.append(MetaMessage("track_name", name="PopKnobPlayer", time=0))

    for part_name in ["melody", "harmony", "bass", "drums"]:
        if part_name not in part_events:
            continue
        tr = MidiTrack()
        mid.tracks.append(tr)
        tr.append(MetaMessage("track_name", name=part_name, time=0))

        evs = sorted(part_events[part_name], key=lambda x: x[0])
        last_tick = 0
        for abs_tick, msg in evs:
            delta = max(0, abs_tick - last_tick)
            last_tick = abs_tick
            tr.append(msg.copy(time=delta))

        tr.append(MetaMessage("end_of_track", time=0))

    report = build_song_report(ctrl, plan, chord_segments, part_events)
    return mid, plan, chord_segments, part_events, report
