from __future__ import annotations

import json
import tkinter as tk
from dataclasses import asdict
from tkinter import filedialog, messagebox, ttk

import mido
from mido import Message, MidiFile

from .constants import DEFAULT_SEED, NOTE_NAMES
from .models import Controls
from .midi_build import build_midifile, build_song_bundle
from .planning import build_song_plan
from .harmony import build_chord_segments
from .player import MidiPlayer
from .utils import clamp01, key_to_pc, scale_pcs, pc_to_name
from .utils import midi_note_name


def _fmt(x):
    if x is None:
        return "None"
    try:
        return f"{float(x):.2f}"
    except Exception:
        return str(x)


class App(tk.Tk):
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

        self.var_density = tk.DoubleVar(value=0.55)
        self.var_syncopation = tk.DoubleVar(value=0.30)
        self.var_swing = tk.DoubleVar(value=0.06)
        self.var_chord_complexity = tk.DoubleVar(value=0.35)
        self.var_repetition = tk.DoubleVar(value=0.70)
        self.var_variation = tk.DoubleVar(value=0.35)
        self.var_energy = tk.DoubleVar(value=0.60)
        self.var_cadence_strength = tk.DoubleVar(value=0.70)

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

        grp_knobs = ttk.LabelFrame(left, text="Knobs (0..1 unless noted)")
        grp_knobs.pack(fill="both", expand=True)

        self._add_slider(grp_knobs, "Density", self.var_density, 0.0, 1.0, self._regenerate)
        self._add_slider(grp_knobs, "Syncopation", self.var_syncopation, 0.0, 1.0, self._regenerate)
        self._add_slider(grp_knobs, "Swing", self.var_swing, 0.0, 1.0, self._regenerate)
        self._add_slider(grp_knobs, "Chord Complexity", self.var_chord_complexity, 0.0, 1.0, self._regenerate)
        self._add_slider(grp_knobs, "Repetition", self.var_repetition, 0.0, 1.0, self._regenerate)
        self._add_slider(grp_knobs, "Variation", self.var_variation, 0.0, 1.0, self._regenerate)
        self._add_slider(grp_knobs, "Energy", self.var_energy, 0.0, 1.0, self._regenerate)
        self._add_slider(grp_knobs, "Cadence Strength", self.var_cadence_strength, 0.0, 1.0, self._regenerate)

        self._add_slider(grp_knobs, "Humanize Timing (ms)", self.var_humanize_timing_ms, 0.0, 25.0, self._regenerate, resolution=0.5)
        self._add_slider(grp_knobs, "Humanize Velocity", self.var_humanize_velocity, 0.0, 0.35, self._regenerate, resolution=0.01)

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
        return Controls(
            length_bars=int(self.var_length_bars.get()),
            bpm=int(self.var_bpm.get()),
            key_name=str(self.var_key.get()),
            mode=str(self.var_mode.get()),
            density=clamp01(float(self.var_density.get())),
            syncopation=clamp01(float(self.var_syncopation.get())),
            swing=clamp01(float(self.var_swing.get())),
            chord_complexity=clamp01(float(self.var_chord_complexity.get())),
            repetition=clamp01(float(self.var_repetition.get())),
            variation=clamp01(float(self.var_variation.get())),
            energy=clamp01(float(self.var_energy.get())),
            cadence_strength=clamp01(float(self.var_cadence_strength.get())),
            humanize_timing_ms=max(0.0, float(self.var_humanize_timing_ms.get())),
            humanize_velocity=clamp01(float(self.var_humanize_velocity.get())),
            seed=int(self.var_seed.get() or DEFAULT_SEED),
        )

    def _regenerate(self):
        try:
            ctrl = self._get_controls()
            self._cached_ctrl = ctrl

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

        lines.append("Knobs:")
        lines.append(f"  density={ctrl.density:.2f}, syncopation={ctrl.syncopation:.2f}, swing={ctrl.swing:.2f}")
        lines.append(f"  chord_complexity={ctrl.chord_complexity:.2f}, repetition={ctrl.repetition:.2f}, variation={ctrl.variation:.2f}")
        lines.append(f"  energy={ctrl.energy:.2f}, cadence_strength={ctrl.cadence_strength:.2f}")
        lines.append(f"  humanize_timing_ms={ctrl.humanize_timing_ms:.1f}, humanize_velocity={ctrl.humanize_velocity:.2f}")
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
