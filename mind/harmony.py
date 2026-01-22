from __future__ import annotations

import random
import re
from typing import List, Tuple

from mido import Message

from .constants import GM_PIANO, HARMONY_CH
from .models import ChordSegment, Controls, SongPlan
from .planning import build_song_plan
from .utils import (
    bar_step_to_abs_tick,
    chord_tones_in_range,
    scale_pcs,
    scale_tones_in_range,
    clamp01,
    clamp,
    lerp,
    pick_weighted,
    degree_to_pc,
    diatonic_triad_quality,
    degree_label,
    build_triad,
    build_seventh,
    unique_pcs,
    apply_swing_to_step,
    humanize_ticks,
    velocity_humanize,
    key_to_pc,
    choose_register_base,
    nearest_in_set,
)


def finalize_events(absolute_events: List[Tuple[int, Message]]) -> List[Message]:
    """Convert a list of (absolute_tick, Message) into MIDI-friendly delta-time messages.

    MIDO expects *delta* times (time since the previous event) on each message.
    Internally, most of the generators in this project emit (absolute_tick, msg)
    pairs because they are easier to compose.

    This helper makes the output "drop-in ready" for direct insertion into a
    MidiTrack.

    Ordering: when multiple events share the same tick, we force a stable
    ordering so note-offs happen before note-ons to avoid stuck notes.
    """

    def _prio(msg: Message) -> int:
        t = getattr(msg, "type", "")
        if t == "program_change":
            return 0
        if t == "note_off":
            return 1
        if t == "note_on":
            return 2
        return 3

    absolute_events.sort(key=lambda x: (int(x[0]), _prio(x[1])))

    delta_events: List[Message] = []
    last_tick = 0
    for tick, msg in absolute_events:
        tick_i = int(tick)
        delta = tick_i - last_tick
        msg.time = int(max(0, delta))
        delta_events.append(msg)
        last_tick = tick_i
    return delta_events


def _resolve_token_to_chord(tonic_pc: int, mode: str, token, rng: random.Random):
    """
    token can be:
      - int: diatonic degree 0..6
      - str:
          - modal interchange: "bVII", "bVI", "bIII", "iv", "bII" (Neapolitan)
          - roman numerals: "I", "ii", "V", "iv" (case implies quality)
          - secondary dominants: "V/<target>" (e.g. "V/V", "V/ii", "V/5")
          - tritone subs: "subV/<target>" (e.g. "subV/V")
    Returns (root_pc, quality, label, is_borrowed, token_tag)
    """
    if isinstance(token, int):
        deg = token % 7
        root_pc = degree_to_pc(tonic_pc, mode, deg)
        quality = diatonic_triad_quality(mode, deg)
        label = degree_label(deg)
        return root_pc, quality, label, False, f"deg:{deg}"

    t = str(token).strip()
    if not t:
        root_pc = tonic_pc
        quality = "maj" if mode == "major" else "min"
        return root_pc, quality, "I", True, "tok:empty"

    # -----------------------------
    # Secondary dominants + tritone substitutions
    # -----------------------------
    # V/<target> or subV/<target> where <target> can be:
    #   - roman numeral (V, ii, etc.)
    #   - numeric degree (1..7 or 0..6)
    #   - a supported borrowed token (bVII, bII, etc.)
    if t.startswith("V/") or t.startswith("subV/"):
        is_tritone = t.startswith("subV/")
        target_ref = t.split("/", 1)[1].strip()
        # Resolve the target's root first (supports roman numerals, numeric degrees, and other tokens).
        target_root, _tq, target_label, _tb, _tt = _resolve_token_to_chord(tonic_pc, mode, target_ref, rng)
        root_pc = (target_root + (1 if is_tritone else 7)) % 12
        quality = "maj"  # treated as dominant-function triad by default
        label = f"subV/{target_label}" if is_tritone else f"V/{target_label}"
        return root_pc, quality, label, True, ("tritone_sub" if is_tritone else "sec_dom")
    if t == "bVII":
        root_pc = (tonic_pc + 10) % 12
        quality = "maj"
        label = "♭VII"
        return root_pc, quality, label, True, "tok:bVII"
    if t == "bVI":
        root_pc = (tonic_pc + 8) % 12
        quality = "maj"
        label = "♭VI"
        return root_pc, quality, label, True, "tok:bVI"
    if t == "bIII":
        root_pc = (tonic_pc + 3) % 12
        quality = "maj"
        label = "♭III"
        return root_pc, quality, label, True, "tok:bIII"
    if t == "bII":
        # Neapolitan (♭II) borrowed from Phrygian
        root_pc = (tonic_pc + 1) % 12
        quality = "maj"
        label = "♭II"
        return root_pc, quality, label, True, "tok:bII"
    if t == "iv":
        root_pc = degree_to_pc(tonic_pc, "major", 3) if mode == "major" else degree_to_pc(tonic_pc, mode, 3)
        quality = "min"
        label = "iv"
        return root_pc, quality, label, True, "tok:iv"

    # -----------------------------
    # Roman numerals (with optional accidentals)
    # -----------------------------
    # Examples:
    #   - I, ii, V, vi
    #   - bII (handled above) and bVII/bVI/bIII (handled above)
    #   - #iv (rare but supported)
    roman_re = re.compile(r"^([b#]*)([ivIV]{1,4})([°o]?)$")
    m = roman_re.match(t)
    if m:
        acc, roman_raw, dim_mark = m.group(1), m.group(2), m.group(3)
        roman_up = roman_raw.upper()
        roman_map = {"I": 0, "II": 1, "III": 2, "IV": 3, "V": 4, "VI": 5, "VII": 6}
        if roman_up in roman_map:
            deg = roman_map[roman_up]
            root_pc = degree_to_pc(tonic_pc, mode, deg)
            # accidentals (e.g., bII, #iv)
            semis = acc.count("#") - acc.count("b")
            root_pc = (root_pc + semis) % 12

            diatonic_q = diatonic_triad_quality(mode, deg)
            if dim_mark:
                quality = "dim"
            else:
                quality = "maj" if roman_raw.isupper() else "min"
                # If the user's roman numeral doesn't explicitly include diminished but the
                # diatonic quality is diminished, honor the diatonic chord.
                if diatonic_q == "dim" and quality != "dim":
                    quality = "dim"

            label = t
            borrowed = (semis != 0) or (quality != diatonic_q)
            return root_pc, quality, label, borrowed, f"roman:{t}"

    root_pc = tonic_pc
    quality = "maj" if mode == "major" else "min"
    return root_pc, quality, t, True, f"tok:{t}"


def _choose_extension(ctrl, rng: random.Random, section: str, label: str, quality: str) -> str:
    c = clamp01(ctrl.chord_complexity)
    if section == "chorus":
        c = clamp01(c * 1.15)

    is_dominant = (label in ("V", "V/V") or label.startswith("V"))

    if c < 0.25:
        return pick_weighted(rng, [("triad", 0.70), ("sus2", 0.15), ("sus4", 0.15)])
    if c < 0.55:
        return pick_weighted(rng, [("triad", 0.30), ("add9", 0.45), ("sus2", 0.10), ("sus4", 0.10), ("7", 0.05)])
    if c < 0.80:
        return pick_weighted(rng, [("triad", 0.18), ("add9", 0.30), ("7", 0.32), ("sus4", 0.10), ("maj9", 0.05), ("min9", 0.05)])
    if is_dominant:
        return pick_weighted(rng, [("7", 0.45), ("dom9", 0.40), ("add9", 0.10), ("sus4", 0.05)])
    return pick_weighted(rng, [("7", 0.30), ("maj9", 0.30), ("min9", 0.20), ("add9", 0.15), ("sus2", 0.05)])


def _build_pcs_with_extension(root_pc: int, quality: str, extension: str, rng: random.Random, mode: str, label: str):
    base = build_triad(root_pc, quality)
    pcs = base[:]

    def _drop_fifth(_pcs: list[int]) -> list[int]:
        """Shell voicing helper: drop the 5th to make room for color tones."""
        fifth = (root_pc + 7) % 12
        return [pc for pc in _pcs if pc != fifth]

    if extension == "triad":
        return unique_pcs(pcs)

    if extension in ("sus2", "sus4"):
        sus_pc = (root_pc + (2 if extension == "sus2" else 5)) % 12
        pcs = pcs[:]
        if len(pcs) >= 2:
            pcs[1] = sus_pc
        return unique_pcs(pcs)

    if extension == "add9":
        pcs = pcs + [(root_pc + 2) % 12]
        return unique_pcs(pcs)

    if extension == "7":
        dominant7 = (mode == "major" and (label in ("V", "V/V") or label.startswith("V")) and rng.random() < 0.80)
        pcs = build_seventh(root_pc, quality, dominant7=dominant7)
        return unique_pcs(pcs)

    if extension == "maj9":
        pcs = build_seventh(root_pc, "maj", dominant7=False)
        pcs = _drop_fifth(pcs) + [(root_pc + 2) % 12]
        # Optional color tone (13) when things get "lush".
        if rng.random() < 0.20:
            pcs = pcs + [(root_pc + 9) % 12]
        return unique_pcs(pcs)

    if extension == "min9":
        pcs = build_seventh(root_pc, "min", dominant7=False)
        pcs = _drop_fifth(pcs) + [(root_pc + 2) % 12]
        if rng.random() < 0.15:
            pcs = pcs + [(root_pc + 9) % 12]
        return unique_pcs(pcs)

    if extension == "dom9":
        pcs = build_seventh(root_pc, "maj", dominant7=True)
        pcs = _drop_fifth(pcs) + [(root_pc + 2) % 12]
        # Dominants love 13s (and it stays cleaner when the 5th is gone).
        if rng.random() < 0.25:
            pcs = pcs + [(root_pc + 9) % 12]
        return unique_pcs(pcs)

    return unique_pcs(pcs)


def make_chord_segment(
    ctrl: Controls,
    tonic_pc: int,
    bar: int,
    start_step: int,
    end_step: int,
    token,
    forced_label: str | None,
    section: str,
    template_tag: str,
    rng: random.Random,
    plan: SongPlan,
) -> ChordSegment:
    mod = plan.bar_mods[bar]
    chord_complexity_eff = clamp01(ctrl.chord_complexity * mod.chord_comp_mul)

    root_pc, quality, label, is_borrowed, _tok_tag = _resolve_token_to_chord(tonic_pc, ctrl.mode, token, rng)

    if forced_label is not None:
        label = forced_label

    if ctrl.mode == "major":
        mixture_prob = clamp01(lerp(0.00, 0.12, chord_complexity_eff) * lerp(0.25, 1.00, ctrl.variation))
        mixture_prob *= (1.05 if section in ("bridge", "chorus") else 0.80)
        if (not is_borrowed) and rng.random() < mixture_prob:
            # Expanded modal interchange palette (major-key defaults).
            # - ♭VII / ♭VI are classic pop/rock mixture
            # - iv is the "sad lift"
            # - ♭II (Neapolitan) adds a cinematic pull
            # - ♭III is a strong color in many modern progressions
            choice = pick_weighted(
                rng,
                [
                    ("bVII", 0.45),
                    ("iv", 0.26),
                    ("bVI", 0.12),
                    ("bIII", 0.10),
                    ("bII", 0.07),
                ],
            )
            root_pc2, quality2, label2, borrowed2, _ = _resolve_token_to_chord(tonic_pc, ctrl.mode, choice, rng)
            root_pc, quality, label, is_borrowed = root_pc2, quality2, label2, borrowed2

    # temp ctrl for extension choice
    class _CtrlTmp:
        pass

    ctrl_tmp = _CtrlTmp()
    ctrl_tmp.chord_complexity = chord_complexity_eff

    extension = _choose_extension(ctrl_tmp, rng, section, label, quality)
    pcs = _build_pcs_with_extension(root_pc, quality, extension, rng, ctrl.mode, label)

    return ChordSegment(
        bar_index=bar,
        start_step=start_step,
        end_step=end_step,
        label=label,
        pcs=pcs,
        root_pc=root_pc,
        quality=quality,
        extension=extension,
        is_borrowed=is_borrowed,
        section=section,
        template_tag=template_tag,
    )


def build_chord_segments(ctrl: Controls, plan: SongPlan | None = None):
    """
    Chords-first with seed-driven progression templates + sectioning + pop turnarounds.
    """
    if plan is None:
        plan = build_song_plan(ctrl)

    rng = random.Random(ctrl.seed)
    tonic_pc = key_to_pc(ctrl.key_name)
    segments: list[ChordSegment] = []

    length = max(1, int(ctrl.length_bars))
    base_two_prob = clamp01(lerp(0.06, 0.40, (ctrl.density * 0.55 + ctrl.variation * 0.45)))

    for bar in range(length):
        mod = plan.bar_mods[bar]
        section = mod.section
        tpl = plan.templates.get(section) or plan.templates.get("verse")
        degrees = tpl["degrees"]
        tpl_name = tpl["name"]

        pos_in_phrase = bar % plan.phrase_len_bars
        token = degrees[pos_in_phrase % len(degrees)]

        do_turnaround = False
        if mod.is_phrase_end and bar != length - 1:
            do_turnaround = (rng.random() < clamp01(lerp(0.20, 0.75, ctrl.cadence_strength)))

        if bar == length - 1 and ctrl.cadence_strength >= 0.45:
            cadence_choice = pick_weighted(rng, [("V_I", 0.75), ("IV_I", 0.25)])
            if cadence_choice == "V_I":
                tok1, tok2 = 4, 0
                lab1, lab2 = "V", "I"
            else:
                tok1, tok2 = 3, 0
                lab1, lab2 = "IV", "I"

            seg1 = make_chord_segment(
                ctrl=ctrl,
                tonic_pc=tonic_pc,
                bar=bar,
                start_step=0,
                end_step=8,
                token=tok1,
                forced_label=lab1,
                section=section,
                template_tag=tpl_name,
                rng=rng,
                plan=plan,
            )
            seg2 = make_chord_segment(
                ctrl=ctrl,
                tonic_pc=tonic_pc,
                bar=bar,
                start_step=8,
                end_step=16,
                token=tok2,
                forced_label=lab2,
                section=section,
                template_tag=tpl_name,
                rng=rng,
                plan=plan,
            )
            segments.extend([seg1, seg2])
            continue

        two_prob = base_two_prob
        if section == "chorus":
            two_prob = clamp01(two_prob * 1.25)
        if section in ("intro", "outro"):
            two_prob = clamp01(two_prob * 0.85)

        if do_turnaround:
            # Turnaround "push" into the next phrase.
            # We keep it mostly diatonic (V), but sometimes color it with a secondary dominant
            # (V/V) or a tritone substitute (subV/V) for a more sophisticated cadence.
            push_token = (
                pick_weighted(rng, [("V/V", 0.26), ("subV/V", 0.10), (4, 0.64)])
                if ctrl.mode == "major"
                else 4
            )
            seg_main = make_chord_segment(
                ctrl=ctrl,
                tonic_pc=tonic_pc,
                bar=bar,
                start_step=0,
                end_step=12,
                token=token,
                forced_label=None,
                section=section,
                template_tag=f"{tpl_name}|turnaround",
                rng=rng,
                plan=plan,
            )
            seg_push = make_chord_segment(
                ctrl=ctrl,
                tonic_pc=tonic_pc,
                bar=bar,
                start_step=12,
                end_step=16,
                token=push_token,
                forced_label="subV/V" if str(push_token) == "subV/V" else ("V/V" if str(push_token) == "V/V" else "V"),
                section=section,
                template_tag=f"{tpl_name}|turnaround",
                rng=rng,
                plan=plan,
            )
            segments.extend([seg_main, seg_push])
            continue

        if rng.random() < two_prob:
            next_token = degrees[(pos_in_phrase + 1) % len(degrees)]
            if rng.random() < lerp(0.18, 0.42, ctrl.energy):
                next_token = 4
            seg1 = make_chord_segment(
                ctrl=ctrl,
                tonic_pc=tonic_pc,
                bar=bar,
                start_step=0,
                end_step=8,
                token=token,
                forced_label=None,
                section=section,
                template_tag=tpl_name,
                rng=rng,
                plan=plan,
            )
            seg2 = make_chord_segment(
                ctrl=ctrl,
                tonic_pc=tonic_pc,
                bar=bar,
                start_step=8,
                end_step=16,
                token=next_token,
                forced_label=None,
                section=section,
                template_tag=tpl_name,
                rng=rng,
                plan=plan,
            )
            segments.extend([seg1, seg2])
        else:
            seg = make_chord_segment(
                ctrl=ctrl,
                tonic_pc=tonic_pc,
                bar=bar,
                start_step=0,
                end_step=16,
                token=token,
                forced_label=None,
                section=section,
                template_tag=tpl_name,
                rng=rng,
                plan=plan,
            )
            segments.append(seg)

    return segments


def segment_for_step(segments_in_bar: list[ChordSegment], step: int):
    for seg in segments_in_bar:
        if seg.start_step <= step < seg.end_step:
            return seg
    return segments_in_bar[0] if segments_in_bar else None


def _initial_harmony_voicing(rng: random.Random, chord_pcs: list[int], low: int, high: int, center: int, voice_count: int):
    chord_notes = chord_tones_in_range(chord_pcs, low, high)
    if not chord_notes:
        return []

    chord_notes_sorted = sorted(set(chord_notes))
    first = nearest_in_set(center, chord_notes_sorted)

    voicing = [first]
    idx = chord_notes_sorted.index(first) if first in chord_notes_sorted else 0

    while len(voicing) < voice_count:
        step = pick_weighted(rng, [(2, 0.45), (4, 0.35), (6, 0.15), (7, 0.05)])
        ni = idx + step
        if ni >= len(chord_notes_sorted):
            ni = len(chord_notes_sorted) - 1
        cand = chord_notes_sorted[ni]
        if cand not in voicing:
            voicing.append(cand)
        else:
            ni2 = min(len(chord_notes_sorted) - 1, ni + 1)
            cand2 = chord_notes_sorted[ni2]
            if cand2 not in voicing:
                voicing.append(cand2)
            else:
                break

    return sorted(voicing)


def _voice_lead(prev_voicing: list[int], chord_pcs: list[int], low: int, high: int):
    """Advanced (parsimonious) voice-leading.

    Priorities:
      1) Keep common tones if possible
      2) Otherwise move by the smallest distance to a chord tone
      3) Maintain strictly ascending voices (no crossings)
      4) Avoid exact duplicates by bumping upper voices when possible
    """
    if not prev_voicing:
        return []

    target_notes = chord_tones_in_range(chord_pcs, low, high)
    if not target_notes:
        return prev_voicing[:]

    target_notes_sorted = sorted(set(target_notes))

    new_voicing: list[int] = []
    last_assigned = low - 1

    for v in sorted(prev_voicing):
        # 1) Common-tone preservation
        if (v % 12) in chord_pcs and low <= v <= high:
            chosen = v
        else:
            # 2) Minimum-distance move
            chosen = nearest_in_set(v, target_notes_sorted)

        # 3) Keep voices ordered (no crossings)
        if chosen <= last_assigned:
            higher = [n for n in target_notes_sorted if n > last_assigned]
            if higher:
                chosen = nearest_in_set(v, higher)
            else:
                chosen = min(high, last_assigned + 1)

        new_voicing.append(chosen)
        last_assigned = chosen

    # 4) De-duplicate: if two voices land on the same note, bump upper voices
    fixed: list[int] = []
    used = set()
    last = low - 1
    for n in new_voicing:
        cand = max(n, last + 1)
        # If duplicate, try pushing up by octaves first
        while cand in used and (cand + 12) <= high:
            cand += 12
        # Still duplicate (or out of range) -> nudge to the next available tone
        if cand in used:
            higher = [x for x in target_notes_sorted if x > last]
            if higher:
                cand = higher[0]
        cand = min(high, max(low, cand))
        fixed.append(cand)
        used.add(cand)
        last = cand

    return fixed


def generate_harmony_track(ctrl: Controls, chord_segments: list[ChordSegment], plan: SongPlan):
    rng = random.Random(ctrl.seed + 101)
    tonic_pc = key_to_pc(ctrl.key_name)
    scale = scale_pcs(tonic_pc, ctrl.mode)

    _, harmony_base, _ = choose_register_base()
    low = harmony_base - 10
    high = harmony_base + 14

    events = []
    events.append((0, Message("program_change", channel=HARMONY_CH, program=GM_PIANO, time=0)))

    voice_count = 3
    if ctrl.chord_complexity >= 0.55:
        voice_count = 4
    if ctrl.chord_complexity >= 0.85 and rng.random() < 0.35:
        voice_count = 5

    prev_voicing: list[int] = []

    for seg in chord_segments:
        mod = plan.bar_mods[seg.bar_index]

        density_eff = clamp01(ctrl.density * mod.density_mul)
        energy_eff = clamp01(ctrl.energy * mod.energy_mul)

        chord_notes = chord_tones_in_range(seg.pcs, low, high)
        if not chord_notes:
            chord_notes = scale_tones_in_range(scale, low, high)
        if not chord_notes:
            chord_notes = [harmony_base]

        if not prev_voicing:
            voicing = _initial_harmony_voicing(rng, seg.pcs, low, high, harmony_base, voice_count)
            if not voicing:
                voicing = sorted(set(chord_notes))[:voice_count]
        else:
            voicing = _voice_lead(prev_voicing, seg.pcs, low, high)
            if not voicing:
                voicing = prev_voicing[:]

        prev_voicing = voicing[:]

        seg_start = bar_step_to_abs_tick(seg.bar_index, seg.start_step)
        seg_end = bar_step_to_abs_tick(seg.bar_index, seg.end_step)

        base_vel = int(round(lerp(52, 88, energy_eff)))

        pulse_prob = clamp01(lerp(0.10, 0.68, density_eff))
        if mod.section == "chorus":
            pulse_prob = clamp01(pulse_prob * 1.15)

        do_pulse = (rng.random() < pulse_prob)

        if not do_pulse:
            on_tick = seg_start + apply_swing_to_step(seg.start_step, ctrl.swing) + humanize_ticks(rng, ctrl.humanize_timing_ms, ctrl.bpm)
            off_tick = seg_end
            for n in voicing:
                vel = velocity_humanize(rng, base_vel, ctrl.humanize_velocity)
                events.append((max(0, on_tick), Message("note_on", channel=HARMONY_CH, note=n, velocity=vel, time=0)))
            for n in voicing:
                events.append((max(0, off_tick), Message("note_off", channel=HARMONY_CH, note=n, velocity=0, time=0)))
        else:
            ticks_per_beat = 480
            ticks_per_8th = 240
            start_tick = seg_start
            end_tick = seg_end

            use_8ths = (mod.is_phrase_end and rng.random() < lerp(0.10, 0.45, ctrl.variation))
            pulse_step = ticks_per_8th if use_8ths else ticks_per_beat
            pulse_len = ticks_per_8th

            t = start_tick
            while t < end_tick:
                on_tick = t + humanize_ticks(rng, ctrl.humanize_timing_ms, ctrl.bpm)
                off_tick = min(end_tick, on_tick + pulse_len)
                for n in voicing:
                    vel = velocity_humanize(rng, base_vel, ctrl.humanize_velocity)
                    events.append((max(0, on_tick), Message("note_on", channel=HARMONY_CH, note=n, velocity=vel, time=0)))
                for n in voicing:
                    events.append((max(0, off_tick), Message("note_off", channel=HARMONY_CH, note=n, velocity=0, time=0)))
                t += pulse_step

    return events


def generate_harmony_track_delta(ctrl: Controls, chord_segments: list[ChordSegment], plan: SongPlan):
    """Drop-in MIDI-ready harmony messages.

    This is a convenience wrapper around :func:`generate_harmony_track` that
    converts absolute tick events into delta-time messages suitable for directly
    appending to a MidiTrack.

    The existing generator remains absolute-tick to preserve compatibility with
    internal builders that merge tracks before converting to delta times.
    """

    return finalize_events(generate_harmony_track(ctrl, chord_segments, plan))
