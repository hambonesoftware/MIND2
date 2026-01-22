from __future__ import annotations

from dataclasses import asdict
from typing import Any

from mido import Message

from .constants import DRUM_CHANNEL, PPQ, STYLE_RHYTHM_ARCHETYPES
from .models import Controls, SongPlan, ChordSegment
from .utils import pc_to_name, midi_note_name, clamp, ticks_to_time_seconds, bar_of_tick, step_of_tick_in_bar
from .theory.analysis import detect_cadence, roman_numeral
from .theory.engine import analyze as analyze_plugins, registered as registered_plugins
from .theory.rhythm import analyze_rhythm
from .theory.melody_analysis import analyze_melody_events
from .theory.counterpoint import analyze_counterpoint
from .melody import contour_offset


def _extract_note_ons(events: list[tuple[int, Message]], channel: int | None = None, drum: bool = False):
    note_ons = []
    for abs_tick, msg in events:
        if msg.type != "note_on":
            continue
        if msg.velocity is None or msg.velocity <= 0:
            continue
        if channel is not None and getattr(msg, "channel", None) != channel:
            continue
        if drum and getattr(msg, "channel", None) != DRUM_CHANNEL:
            continue
        note_ons.append((abs_tick, msg))
    return note_ons


def build_song_report(
    ctrl: Controls,
    plan: SongPlan,
    chord_segments: list[ChordSegment],
    part_events: dict[str, list[tuple[int, Message]]],
    run_plugins: bool = True,
):
    """Build a JSON-serializable report for later analysis."""
    style_key = (ctrl.progression_style or "pop").strip().lower()
    report: dict[str, Any] = {
        "report_version": "pop_knob_player_v2",
        "controls": asdict(ctrl),
        "style_profile": {
            "style": style_key,
            "rhythm_archetype": plan.rhythm.archetype,
            "swing_amount": ctrl.swing,
            "style_rules_applied": style_key in STYLE_RHYTHM_ARCHETYPES,
        },
        "profiles": {
            "section_pattern": [{"name": s.name, "bar_start": s.bar_start, "bar_end_excl": s.bar_end_excl} for s in plan.sections],
            "phrase_len_bars": plan.phrase_len_bars,
            "rhythm_profile": {
                "archetype": plan.rhythm.archetype,
                "base_kick_steps": plan.rhythm.base_kick_steps,
                "base_snare_steps": plan.rhythm.base_snare_steps,
                "base_hat_steps": plan.rhythm.base_hat_steps,
                "hat_16th_bias": plan.rhythm.hat_16th_bias,
                "kick_sync_bias": plan.rhythm.kick_sync_bias,
                "fill_style": plan.rhythm.fill_style,
            },
            "melody_contour": {"kind": plan.contour.kind, "intensity": plan.contour.intensity},
            "section_templates": plan.templates,
        },
        "bars": [],
        "chords": [],
        "melody": {},
        "layers": {},
    }

    key_context = {"key_name": ctrl.key_name, "mode": ctrl.mode}
    for b in range(ctrl.length_bars):
        mod = plan.bar_mods[b]
        cadence_type = None
        if mod.is_phrase_end:
            phrase_start = max(0, b - plan.phrase_len_bars + 1)
            phrase_chords = [seg for seg in chord_segments if phrase_start <= seg.bar_index <= b]
            cadence_type = detect_cadence(phrase_chords, key_context)
        report["bars"].append(
            {
                "bar_index": b,
                "section": mod.section,
                "is_phrase_end": mod.is_phrase_end,
                "is_section_start": mod.is_section_start,
                "is_section_end": mod.is_section_end,
                "cadence": cadence_type,
                "multipliers": {
                    "density_mul": mod.density_mul,
                    "energy_mul": mod.energy_mul,
                    "sync_mul": mod.sync_mul,
                    "chord_comp_mul": mod.chord_comp_mul,
                    "variation_mul": mod.variation_mul,
                    "repetition_mul": mod.repetition_mul,
                    "melody_shift_semitones": mod.melody_shift_semitones,
                },
                "contour_offset_semitones": contour_offset(plan.contour, b, ctrl.length_bars),
            }
        )

    for seg in chord_segments:
        numeral = roman_numeral(seg, key_context)
        report["chords"].append(
            {
                "bar_index": seg.bar_index,
                "start_step": seg.start_step,
                "end_step": seg.end_step,
                "section": seg.section,
                "label": seg.label,
                "roman_numeral": numeral,
                "root_pc": seg.root_pc,
                "root_name": pc_to_name(seg.root_pc),
                "quality": seg.quality,
                "extension": seg.extension,
                "pcs": seg.pcs,
                "pc_names": [pc_to_name(p) for p in seg.pcs],
                "is_borrowed": seg.is_borrowed,
                "template_tag": seg.template_tag,
                "inversion": seg.chord.inversion,
                "function": seg.chord.function,
            }
        )

    for layer_name, events in part_events.items():
        ons = _extract_note_ons(events, drum=(layer_name == "drums"))
        pitches = [m.note for _, m in ons]
        velocities = [m.velocity for _, m in ons]
        bars = [bar_of_tick(t) for t, _ in ons]
        steps = [step_of_tick_in_bar(t) for t, _ in ons]

        layer: dict[str, Any] = {
            "note_on_count": len(ons),
            "unique_pitches": sorted(set(pitches)),
            "pitch_range": [min(pitches), max(pitches)] if pitches else None,
            "avg_pitch": (sum(pitches) / len(pitches)) if pitches else None,
            "avg_velocity": (sum(velocities) / len(velocities)) if velocities else None,
            "rhythm": analyze_rhythm([t for t, _ in ons], ctrl.length_bars),
            "notes_per_bar": {},
            "steps_histogram": {},
            "preview": [],
        }

        counts = {}
        for b in bars:
            counts[b] = counts.get(b, 0) + 1
        layer["notes_per_bar"] = {str(k): v for k, v in sorted(counts.items(), key=lambda x: x[0])}

        sh = {}
        for s in steps:
            s = int(clamp(s, 0, 15))
            sh[s] = sh.get(s, 0) + 1
        layer["steps_histogram"] = {str(k): v for k, v in sorted(sh.items(), key=lambda x: x[0])}

        for abs_tick, msg in ons[:60]:
            layer["preview"].append(
                {
                    "time_sec": round(ticks_to_time_seconds(abs_tick, ctrl.bpm), 4),
                    "bar": bar_of_tick(abs_tick),
                    "step": step_of_tick_in_bar(abs_tick),
                    "note": int(msg.note),
                    "note_name": midi_note_name(int(msg.note)) if layer_name != "drums" else int(msg.note),
                    "velocity": int(msg.velocity),
                }
            )

        report["layers"][layer_name] = layer

    melody_events = part_events.get("melody", [])
    report["melody"] = analyze_melody_events(melody_events)
    harmony_events = part_events.get("harmony", [])
    report["counterpoint"] = analyze_counterpoint(melody_events, harmony_events)

    if run_plugins and registered_plugins():
        plugin_data = {
            "controls": ctrl,
            "plan": plan,
            "chord_segments": chord_segments,
            "part_events": part_events,
            "report": report,
        }
        report["plugins"] = analyze_plugins(plugin_data)

    return report
