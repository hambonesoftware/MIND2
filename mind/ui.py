from __future__ import annotations

import json
import tkinter as tk
from dataclasses import replace
from tkinter import filedialog, messagebox, ttk

import mido
from mido import Message, MidiFile

from .constants import DEFAULT_SEED, NOTE_NAMES
from .control_mapping import map_controls
from .models import Controls, Level2Knobs, StyleMoodControls
from .midi_build import build_midifile, build_song_bundle
from .planning import build_song_plan
from .harmony import build_chord_segments
from .player import MidiPlayer
from .utils import clamp01, key_to_pc, lerp, scale_pcs, pc_to_name
from .utils import midi_note_name


def _fmt(x):
    if x is None:
        return "None"
    try:
        return f"{float(x):.2f}"
    except Exception:
        return str(x)


class App(tk.Tk):
    STYLE_LABELS = {
        "Modern Pop": "pop",
        "Early Rock & Roll": "rock",
        "Jazz": "jazz",
    }

    def __init__(self):
        super().__init__()
        self.title("Pop Knob Player (Chords-First) - Tkinter + Mido")
        self.geometry("980x700")

        self.player = MidiPlayer()

        # Variables
        self.var_length_bars = tk.IntVar(value=8)
        self.var_bpm = tk.IntVar(value=120)
        self.var_key = tk.StringVar(value="C")
        self.var_mode = tk.StringVar(value="major")

        self.var_style = tk.StringVar(value="Modern Pop")
        self.var_mood_brightness = tk.DoubleVar(value=0.65)
        self.var_mood_energy = tk.DoubleVar(value=0.55)
        self.var_mood_tension = tk.DoubleVar(value=0.40)
        self.var_intensity = tk.DoubleVar(value=0.60)
        self.var_complexity = tk.DoubleVar(value=0.35)
        self.var_tightness = tk.DoubleVar(value=0.65)

        self.var_show_advanced = tk.BooleanVar(value=False)
        self.var_override_level2 = tk.BooleanVar(value=False)
        self.var_level2_functional_clarity = tk.DoubleVar(value=0.70)
        self.var_level2_chromaticism = tk.DoubleVar(value=0.35)
        self.var_level2_extension_richness = tk.DoubleVar(value=0.40)
        self.var_level2_turnaround_intensity = tk.DoubleVar(value=0.55)
        self.var_level2_swing_amount = tk.DoubleVar(value=0.12)
        self.var_level2_syncopation = tk.DoubleVar(value=0.35)
        self.var_level2_chord_tone_anchoring = tk.DoubleVar(value=0.70)
        self.var_level2_melodic_range = tk.DoubleVar(value=0.55)
        self.var_level2_motif_repetition = tk.DoubleVar(value=0.60)
        self.var_level2_form_strictness = tk.DoubleVar(value=0.55)
        self.var_level2_groove = tk.StringVar(value="")
        self.var_level2_lift = tk.StringVar(value="")

        self.var_humanize_timing_ms = tk.DoubleVar(value=8.0)
        self.var_humanize_velocity = tk.DoubleVar(value=0.10)

        self.var_seed = tk.IntVar(value=DEFAULT_SEED)

        self.var_output = tk.StringVar(value="")
        self.status_text = tk.StringVar(value="Ready.")

        self._cached_ctrl: Controls | None = None
        self._cached_mid_full: MidiFile | None = None
        self._cached_plan = None
        self._cached_chords = None
        self._cached_part_events = None
        self._cached_report = None
        self._level2_groove_combo: ttk.Combobox | None = None
        self._level2_lift_combo: ttk.Combobox | None = None

        self._build_ui()
        self._refresh_outputs()
        self._regenerate()

    def _build_ui(self):
        root = ttk.Frame(self, padding=12)
        root.pack(fill="both", expand=True)

        top = ttk.Frame(root)
        top.pack(fill="x")

        ttk.Label(top, text="MIDI Output:").pack(side="left")
        self.output_combo = ttk.Combobox(top, textvariable=self.var_output, state="readonly", width=52)
        self.output_combo.pack(side="left", padx=(6, 12))

        ttk.Button(top, text="Refresh Outputs", command=self._refresh_outputs).pack(side="left", padx=6)

        ttk.Label(top, text="Seed:").pack(side="left", padx=(18, 6))
        seed_entry = ttk.Entry(top, textvariable=self.var_seed, width=12)
        seed_entry.pack(side="left")

        ttk.Button(top, text="Regenerate", command=self._regenerate).pack(side="left", padx=8)

        main = ttk.Frame(root)
        main.pack(fill="both", expand=True, pady=(12, 0))

        left = ttk.Frame(main)
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))

        right = ttk.Frame(main)
        right.pack(side="right", fill="both", expand=True)

        grp_basic = ttk.LabelFrame(left, text="Thought Inputs (Pop)")
        grp_basic.pack(fill="x", pady=(0, 10))

        row1 = ttk.Frame(grp_basic)
        row1.pack(fill="x", pady=4)
        ttk.Label(row1, text="Length (bars):", width=16).pack(side="left")
        sb_len = ttk.Spinbox(row1, from_=1, to=32, textvariable=self.var_length_bars, width=8, command=self._regenerate)
        sb_len.pack(side="left")
        ttk.Label(row1, text="BPM:", width=6).pack(side="left", padx=(12, 0))
        sb_bpm = ttk.Spinbox(row1, from_=60, to=200, textvariable=self.var_bpm, width=8, command=self._regenerate)
        sb_bpm.pack(side="left")

        row2 = ttk.Frame(grp_basic)
        row2.pack(fill="x", pady=4)
        ttk.Label(row2, text="Key:", width=16).pack(side="left")
        key_combo = ttk.Combobox(row2, textvariable=self.var_key, values=NOTE_NAMES, state="readonly", width=6)
        key_combo.pack(side="left")
        key_combo.bind("<<ComboboxSelected>>", lambda e: self._regenerate())

        ttk.Label(row2, text="Mode:", width=6).pack(side="left", padx=(12, 0))
        mode_combo = ttk.Combobox(row2, textvariable=self.var_mode, values=["major", "minor"], state="readonly", width=8)
        mode_combo.pack(side="left")
        mode_combo.bind("<<ComboboxSelected>>", lambda e: self._regenerate())

        grp_style = ttk.LabelFrame(left, text="Style + Mood (Level 1)")
        grp_style.pack(fill="x", pady=(0, 10))

        style_row = ttk.Frame(grp_style)
        style_row.pack(fill="x", pady=4)
        ttk.Label(style_row, text="Style:", width=16).pack(side="left")
        style_combo = ttk.Combobox(
            style_row,
            textvariable=self.var_style,
            values=list(self.STYLE_LABELS.keys()),
            state="readonly",
            width=18,
        )
        style_combo.pack(side="left")
        style_combo.bind("<<ComboboxSelected>>", lambda e: self._regenerate())

        self._add_slider(grp_style, "Bright ↔ Dark", self.var_mood_brightness, 0.0, 1.0, self._regenerate)
        self._add_slider(grp_style, "Calm ↔ Energetic", self.var_mood_energy, 0.0, 1.0, self._regenerate)
        self._add_slider(grp_style, "Tense ↔ Relaxed", self.var_mood_tension, 0.0, 1.0, self._regenerate)
        self._add_slider(grp_style, "Intensity", self.var_intensity, 0.0, 1.0, self._regenerate)
        self._add_slider(grp_style, "Complexity", self.var_complexity, 0.0, 1.0, self._regenerate)
        self._add_slider(grp_style, "Tightness", self.var_tightness, 0.0, 1.0, self._regenerate)

        grp_performance = ttk.LabelFrame(left, text="Performance")
        grp_performance.pack(fill="x", pady=(0, 10))
        self._add_slider(
            grp_performance,
            "Humanize Timing (ms)",
            self.var_humanize_timing_ms,
            0.0,
            25.0,
            self._regenerate,
            resolution=0.5,
        )
        self._add_slider(
            grp_performance,
            "Humanize Velocity",
            self.var_humanize_velocity,
            0.0,
            0.35,
            self._regenerate,
            resolution=0.01,
        )

        adv_toggle_row = ttk.Frame(left)
        adv_toggle_row.pack(fill="x", pady=(0, 4))
        ttk.Checkbutton(
            adv_toggle_row,
            text="Show Advanced Level 2",
            variable=self.var_show_advanced,
            command=self._toggle_advanced,
        ).pack(side="left")

        self.grp_advanced = ttk.LabelFrame(left, text="Advanced: Level 2 Overrides")
        if self.var_show_advanced.get():
            self.grp_advanced.pack(fill="x")
        override_row = ttk.Frame(self.grp_advanced)
        override_row.pack(fill="x", pady=4)
        ttk.Checkbutton(
            override_row,
            text="Override derived Level 2 values",
            variable=self.var_override_level2,
            command=self._regenerate,
        ).pack(side="left")

        self._add_slider(
            self.grp_advanced,
            "Functional Clarity",
            self.var_level2_functional_clarity,
            0.0,
            1.0,
            self._regenerate,
        )
        self._add_slider(
            self.grp_advanced,
            "Chromaticism",
            self.var_level2_chromaticism,
            0.0,
            1.0,
            self._regenerate,
        )
        self._add_slider(
            self.grp_advanced,
            "Extension Richness",
            self.var_level2_extension_richness,
            0.0,
            1.0,
            self._regenerate,
        )
        self._add_slider(
            self.grp_advanced,
            "Turnaround Intensity",
            self.var_level2_turnaround_intensity,
            0.0,
            1.0,
            self._regenerate,
        )
        self._add_slider(
            self.grp_advanced,
            "Swing Amount",
            self.var_level2_swing_amount,
            0.0,
            1.0,
            self._regenerate,
        )
        self._add_slider(
            self.grp_advanced,
            "Syncopation",
            self.var_level2_syncopation,
            0.0,
            1.0,
            self._regenerate,
        )
        self._add_slider(
            self.grp_advanced,
            "Chord Tone Anchoring",
            self.var_level2_chord_tone_anchoring,
            0.0,
            1.0,
            self._regenerate,
        )
        self._add_slider(
            self.grp_advanced,
            "Melodic Range",
            self.var_level2_melodic_range,
            0.0,
            1.0,
            self._regenerate,
        )
        self._add_slider(
            self.grp_advanced,
            "Motif Repetition",
            self.var_level2_motif_repetition,
            0.0,
            1.0,
            self._regenerate,
        )
        self._add_slider(
            self.grp_advanced,
            "Form Strictness",
            self.var_level2_form_strictness,
            0.0,
            1.0,
            self._regenerate,
        )

        l2_rows = ttk.Frame(self.grp_advanced)
        l2_rows.pack(fill="x", pady=4)
        ttk.Label(l2_rows, text="Groove Archetype:", width=18).pack(side="left")
        self._level2_groove_combo = ttk.Combobox(
            l2_rows,
            textvariable=self.var_level2_groove,
            values=[],
            state="readonly",
            width=18,
        )
        self._level2_groove_combo.pack(side="left", padx=(0, 6))
        self._level2_groove_combo.bind("<<ComboboxSelected>>", lambda e: self._regenerate())
        ttk.Label(l2_rows, text="Lift Profile:", width=12).pack(side="left")
        self._level2_lift_combo = ttk.Combobox(
            l2_rows,
            textvariable=self.var_level2_lift,
            values=[],
            state="readonly",
            width=12,
        )
        self._level2_lift_combo.pack(side="left")
        self._level2_lift_combo.bind("<<ComboboxSelected>>", lambda e: self._regenerate())

        grp_play = ttk.LabelFrame(right, text="Playback")
        grp_play.pack(fill="x")

        btn_row1 = ttk.Frame(grp_play)
        btn_row1.pack(fill="x", pady=6)
        ttk.Button(btn_row1, text="Play FULL", command=self.play_full).pack(side="left", padx=4)
        ttk.Button(btn_row1, text="Play Melody", command=self.play_melody).pack(side="left", padx=4)
        ttk.Button(btn_row1, text="Play Harmony", command=self.play_harmony).pack(side="left", padx=4)
        ttk.Button(btn_row1, text="Play Bass", command=self.play_bass).pack(side="left", padx=4)
        ttk.Button(btn_row1, text="Play Drums", command=self.play_drums).pack(side="left", padx=4)

        btn_row2 = ttk.Frame(grp_play)
        btn_row2.pack(fill="x", pady=6)
        ttk.Button(btn_row2, text="Stop", command=self.stop_playback).pack(side="left", padx=4)
        ttk.Button(btn_row2, text="Save MIDI...", command=self.save_midi).pack(side="left", padx=4)
        ttk.Button(btn_row2, text="Save Report (JSON)...", command=self.save_report).pack(side="left", padx=4)

        grp_info = ttk.LabelFrame(right, text="Info / Report Summary")
        grp_info.pack(fill="both", expand=True, pady=(10, 0))

        self.info = tk.Text(grp_info, height=24, wrap="word")
        self.info.pack(fill="both", expand=True, padx=8, pady=8)
        self.info.configure(state="disabled")

        status = ttk.Frame(root)
        status.pack(fill="x", pady=(10, 0))
        ttk.Label(status, textvariable=self.status_text).pack(side="left")

    def _add_slider(self, parent, label, var, vmin, vmax, on_change, resolution=0.01):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", padx=8, pady=4)

        ttk.Label(frame, text=label, width=18).pack(side="left")
        scale = ttk.Scale(frame, from_=vmin, to=vmax, variable=var, orient="horizontal", command=lambda _e: on_change())
        scale.pack(side="left", fill="x", expand=True, padx=(6, 8))

        val_label = ttk.Label(frame, text=f"{var.get():.2f}", width=8)
        val_label.pack(side="right")

        def update_label(*_):
            v = var.get()
            if "ms" in label.lower():
                val_label.configure(text=f"{v:.1f}")
            else:
                val_label.configure(text=f"{v:.2f}")

        var.trace_add("write", lambda *_: update_label())
        return scale

    def _toggle_advanced(self):
        if self.var_show_advanced.get():
            self.grp_advanced.pack(fill="x")
        else:
            self.grp_advanced.pack_forget()

    def _sync_level2_vars(self, derived):
        if self._level2_groove_combo is not None:
            self._level2_groove_combo["values"] = [name for name, _ in derived.style_profile.groove_archetypes]
        if self._level2_lift_combo is not None:
            self._level2_lift_combo["values"] = [name for name, _ in derived.style_profile.lift_profiles]
        if self.var_override_level2.get():
            return
        lvl2 = derived.level2
        self.var_level2_functional_clarity.set(lvl2.functional_clarity)
        self.var_level2_chromaticism.set(lvl2.chromaticism)
        self.var_level2_extension_richness.set(lvl2.extension_richness)
        self.var_level2_turnaround_intensity.set(lvl2.turnaround_intensity)
        self.var_level2_swing_amount.set(lvl2.swing_amount)
        self.var_level2_syncopation.set(lvl2.syncopation)
        self.var_level2_chord_tone_anchoring.set(lvl2.chord_tone_anchoring)
        self.var_level2_melodic_range.set(lvl2.melodic_range)
        self.var_level2_motif_repetition.set(lvl2.motif_repetition)
        self.var_level2_form_strictness.set(lvl2.form_strictness)
        self.var_level2_groove.set(lvl2.groove_archetype)
        self.var_level2_lift.set(lvl2.lift_profile)

    def _apply_level2_overrides(self, derived):
        if not self.var_override_level2.get():
            return derived

        level2 = Level2Knobs(
            functional_clarity=clamp01(float(self.var_level2_functional_clarity.get())),
            chromaticism=clamp01(float(self.var_level2_chromaticism.get())),
            extension_richness=clamp01(float(self.var_level2_extension_richness.get())),
            turnaround_intensity=clamp01(float(self.var_level2_turnaround_intensity.get())),
            groove_archetype=(self.var_level2_groove.get() or derived.level2.groove_archetype),
            swing_amount=clamp01(float(self.var_level2_swing_amount.get())),
            syncopation=clamp01(float(self.var_level2_syncopation.get())),
            chord_tone_anchoring=clamp01(float(self.var_level2_chord_tone_anchoring.get())),
            melodic_range=clamp01(float(self.var_level2_melodic_range.get())),
            motif_repetition=clamp01(float(self.var_level2_motif_repetition.get())),
            form_strictness=clamp01(float(self.var_level2_form_strictness.get())),
            lift_profile=(self.var_level2_lift.get() or derived.level2.lift_profile),
        )

        intensity = derived.level1.intensity
        profile = derived.style_profile
        repetition = clamp01(lerp(profile.repetition_range[0], profile.repetition_range[1], level2.motif_repetition))
        variation = clamp01(
            lerp(
                profile.variation_range[0],
                profile.variation_range[1],
                intensity * 0.5 + (1 - level2.motif_repetition) * 0.5,
            )
        )
        cadence_strength = clamp01(
            lerp(
                profile.cadence_strength_range[0],
                profile.cadence_strength_range[1],
                level2.turnaround_intensity,
            )
        )

        return replace(
            derived,
            level2=level2,
            syncopation=level2.syncopation,
            swing=level2.swing_amount,
            repetition=repetition,
            variation=variation,
            cadence_strength=cadence_strength,
        )

    def _refresh_outputs(self):
        try:
            names = mido.get_output_names()
        except Exception as e:
            names = []
            print("Could not get MIDI outputs:", e)

        if not names:
            names = ["(no MIDI outputs found)"]

        self.output_combo["values"] = names

        current = self.var_output.get()
        if current not in names:
            self.var_output.set(names[0])

    def _get_controls(self) -> Controls:
        style_label = str(self.var_style.get() or "Modern Pop")
        style = self.STYLE_LABELS.get(style_label, "pop")
        mood_brightness = clamp01(float(self.var_mood_brightness.get()))
        mood_energy = clamp01(float(self.var_mood_energy.get()))
        mood_tension = clamp01(1.0 - float(self.var_mood_tension.get()))
        intensity = clamp01(float(self.var_intensity.get()))
        complexity = clamp01(float(self.var_complexity.get()))
        tightness = clamp01(float(self.var_tightness.get()))
        seed = int(self.var_seed.get() or DEFAULT_SEED)

        mood_valence = mood_brightness
        mood_arousal = mood_energy
        complexity = clamp01(complexity * 0.7 + mood_tension * 0.3)

        style_mood = StyleMoodControls(
            style=style,
            mood_valence=mood_valence,
            mood_arousal=mood_arousal,
            intensity=intensity,
            complexity=complexity,
            tightness=tightness,
        )
        derived = map_controls(style_mood, seed=seed)
        derived = self._apply_level2_overrides(derived)
        derived = replace(
            derived,
            humanize_timing_ms=max(0.0, float(self.var_humanize_timing_ms.get())),
            humanize_velocity=clamp01(float(self.var_humanize_velocity.get())),
        )

        return Controls(
            length_bars=int(self.var_length_bars.get()),
            bpm=int(self.var_bpm.get()),
            key_name=str(self.var_key.get()),
            mode=str(self.var_mode.get()),
            seed=seed,
            style_mood=style_mood,
            derived=derived,
        )

    def _regenerate(self):
        try:
            ctrl = self._get_controls()
            self._cached_ctrl = ctrl
            self._sync_level2_vars(ctrl.derived)

            mid, plan, chord_segments, part_events, report = build_song_bundle(
                ctrl, include_parts=("melody", "harmony", "bass", "drums")
            )

            self._cached_mid_full = mid
            self._cached_plan = plan
            self._cached_chords = chord_segments
            self._cached_part_events = part_events
            self._cached_report = report

            self.status_text.set("Generated new pattern + report.")
            self._render_info(ctrl)
        except Exception as e:
            self.status_text.set(f"Error generating: {e}")
            messagebox.showerror("Generation error", str(e))

    def _render_info(self, ctrl: Controls):
        tonic_pc = key_to_pc(ctrl.key_name)
        scale = scale_pcs(tonic_pc, ctrl.mode)

        plan = self._cached_plan or build_song_plan(ctrl)
        chord_segments = self._cached_chords or build_chord_segments(ctrl, plan)
        report = self._cached_report

        lines = []
        lines.append("POP KNOB PLAYER (Chords-first) — Seed-driven Pop Engine\n")
        lines.append(f"LengthBars: {ctrl.length_bars} | BPM: {ctrl.bpm} | Key: {ctrl.key_name} {ctrl.mode}")
        lines.append(f"Scale PCs: {[pc_to_name(x) for x in scale]}")
        lines.append("")

        lines.append("Seed-driven Profiles:")
        lines.append("  Sections (4-bar phrases): " + " | ".join([f"{s.name.upper()}[{s.bar_start+1}-{s.bar_end_excl}]" for s in plan.sections]))
        lines.append(f"  Melody Contour: {plan.contour.kind} (intensity {plan.contour.intensity:.2f})")
        lines.append(f"  Rhythm DNA: {plan.rhythm.archetype} (fill: {plan.rhythm.fill_style})")
        lines.append("  Templates:")
        for sec_name in ["intro", "verse", "chorus", "bridge", "outro"]:
            t = plan.templates.get(sec_name)
            if t:
                lines.append(f"    {sec_name}: {t['name']} -> {t['degrees']}")
        lines.append("")

        lines.append("Level 1 (Style/Mood):")
        lines.append(
            "  style={style} valence={valence:.2f} arousal={arousal:.2f} intensity={intensity:.2f} "
            "complexity={complexity:.2f} tightness={tightness:.2f}".format(
                style=ctrl.style_mood.style,
                valence=ctrl.style_mood.mood_valence,
                arousal=ctrl.style_mood.mood_arousal,
                intensity=ctrl.style_mood.intensity,
                complexity=ctrl.style_mood.complexity,
                tightness=ctrl.style_mood.tightness,
            )
        )
        lines.append(f"  level2_override={'on' if self.var_override_level2.get() else 'off'}")
        lines.append("")

        lines.append("Derived Knobs:")
        lines.append(f"  density={ctrl.derived.density:.2f}, syncopation={ctrl.derived.syncopation:.2f}, swing={ctrl.derived.swing:.2f}")
        lines.append(f"  chord_complexity={ctrl.derived.chord_complexity:.2f}, repetition={ctrl.derived.repetition:.2f}, variation={ctrl.derived.variation:.2f}")
        lines.append(f"  energy={ctrl.derived.energy:.2f}, cadence_strength={ctrl.derived.cadence_strength:.2f}")
        lines.append(f"  humanize_timing_ms={ctrl.derived.humanize_timing_ms:.1f}, humanize_velocity={ctrl.derived.humanize_velocity:.2f}")
        lines.append(f"  groove={ctrl.derived.level2.groove_archetype}, lift={ctrl.derived.level2.lift_profile}")
        lines.append("  Level 2 Mapping:")
        lines.append(
            "    functional_clarity={:.2f}, chromaticism={:.2f}, extension_richness={:.2f}".format(
                ctrl.derived.level2.functional_clarity,
                ctrl.derived.level2.chromaticism,
                ctrl.derived.level2.extension_richness,
            )
        )
        lines.append(
            "    turnaround_intensity={:.2f}, chord_tone_anchoring={:.2f}, melodic_range={:.2f}".format(
                ctrl.derived.level2.turnaround_intensity,
                ctrl.derived.level2.chord_tone_anchoring,
                ctrl.derived.level2.melodic_range,
            )
        )
        lines.append(
            "    motif_repetition={:.2f}, form_strictness={:.2f}, swing_amount={:.2f}, syncopation={:.2f}".format(
                ctrl.derived.level2.motif_repetition,
                ctrl.derived.level2.form_strictness,
                ctrl.derived.level2.swing_amount,
                ctrl.derived.level2.syncopation,
            )
        )
        lines.append("")

        lines.append("Chord segments (by bar):")
        by_bar = {}
        for seg in chord_segments:
            by_bar.setdefault(seg.bar_index, []).append(seg)
        for bar in range(ctrl.length_bars):
            segs = by_bar.get(bar, [])
            if not segs:
                continue
            parts = []
            for s in segs:
                pcs = ",".join([pc_to_name(pc) for pc in s.pcs])
                borrow = " (borrowed)" if s.is_borrowed else ""
                parts.append(f"{s.label}{borrow} {s.extension} [{s.start_step:02d}-{s.end_step:02d}] ({pcs})")
            mod = plan.bar_mods[bar]
            flags = []
            if mod.is_section_start and bar != 0:
                flags.append("SECTION_START")
            if mod.is_section_end and bar != ctrl.length_bars - 1:
                flags.append("SECTION_END")
            if mod.is_phrase_end and bar != ctrl.length_bars - 1:
                flags.append("PHRASE_END")
            flag_txt = (" | " + ",".join(flags)) if flags else ""
            lines.append(f"  Bar {bar+1:02d} [{mod.section.upper()}]{flag_txt}: " + " | ".join(parts))

        lines.append("")

        lines.append("Layer Summary (from report):")
        if report and "layers" in report:
            for layer in ["melody", "harmony", "bass", "drums"]:
                lr = report["layers"].get(layer, {})
                lines.append(f"  {layer}: note_ons={lr.get('note_on_count')} avg_pitch={_fmt(lr.get('avg_pitch'))} avg_vel={_fmt(lr.get('avg_velocity'))}")
        else:
            lines.append("  (No report cached yet)")

        lines.append("")

        lines.append("Notes:")
        lines.append("  - Save Report (JSON) exports the full per-layer analysis for later review.")
        lines.append("  - If you have no MIDI outputs, use 'Save MIDI...' and open the file in a DAW.")
        lines.append("  - On Windows, a common output is 'Microsoft GS Wavetable Synth' (if present).")
        lines.append("")

        self.info.configure(state="normal")
        self.info.delete("1.0", "end")
        self.info.insert("1.0", "\n".join(lines))
        self.info.configure(state="disabled")

    def _selected_output_name(self):
        name = self.var_output.get()
        if name == "(no MIDI outputs found)":
            return None
        return name

    def stop_playback(self):
        self.player.stop()
        self.status_text.set("Stop requested.")

    def _play_parts(self, parts):
        if self._cached_ctrl is None:
            self._regenerate()
        ctrl = self._cached_ctrl

        mid = build_midifile(ctrl, include_parts=parts)
        out_name = self._selected_output_name()

        if out_name is None:
            self.status_text.set("No MIDI output selected; playback will be silent. Use Save MIDI to listen in a DAW.")
        else:
            self.status_text.set(f"Playing to: {out_name}")

        def on_done():
            self.status_text.set("Playback finished.")

        self.player.play_midifile(mid, out_name, on_done=on_done)

    def play_full(self):
        self._play_parts(("melody", "harmony", "bass", "drums"))

    def play_melody(self):
        self._play_parts(("melody",))

    def play_harmony(self):
        self._play_parts(("harmony",))

    def play_bass(self):
        self._play_parts(("bass",))

    def play_drums(self):
        self._play_parts(("drums",))

    def save_midi(self):
        if self._cached_ctrl is None:
            self._regenerate()
        ctrl = self._cached_ctrl
        mid = self._cached_mid_full or build_midifile(ctrl, include_parts=("melody", "harmony", "bass", "drums"))

        filename = filedialog.asksaveasfilename(
            defaultextension=".mid",
            filetypes=[("MIDI files", "*.mid"), ("All files", "*.*")],
            title="Save MIDI file"
        )
        if not filename:
            return
        try:
            mid.save(filename)
            self.status_text.set(f"Saved MIDI: {filename}")
        except Exception as e:
            messagebox.showerror("Save error", str(e))

    def save_report(self):
        if self._cached_ctrl is None:
            self._regenerate()

        report = self._cached_report
        if not report:
            messagebox.showerror("Report error", "No report cached. Click Regenerate first.")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save Analysis Report (JSON)"
        )
        if not filename:
            return
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2)
            self.status_text.set(f"Saved report: {filename}")
        except Exception as e:
            messagebox.showerror("Save error", str(e))


def main():
    app = App()
    app.mainloop()
