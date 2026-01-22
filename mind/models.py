from __future__ import annotations

from dataclasses import dataclass

from .theory.chords import ChordSpec


@dataclass
class Controls:
    length_bars: int
    bpm: int
    key_name: str
    mode: str  # "major" or "minor" (minor is natural minor)

    # normalized knobs 0..1
    density: float
    syncopation: float
    swing: float
    chord_complexity: float
    repetition: float
    variation: float
    energy: float
    cadence_strength: float

    humanize_timing_ms: float
    humanize_velocity: float

    seed: int


@dataclass
class SectionDef:
    name: str  # "verse", "chorus", "bridge", "intro", "outro"
    bar_start: int
    bar_end_excl: int


@dataclass
class BarModifiers:
    section: str
    density_mul: float
    energy_mul: float
    sync_mul: float
    chord_comp_mul: float
    variation_mul: float
    repetition_mul: float
    melody_shift_semitones: int
    is_phrase_end: bool
    is_section_start: bool
    is_section_end: bool


@dataclass
class RhythmProfile:
    archetype: str
    base_kick_steps: list[int]
    base_snare_steps: list[int]
    base_hat_steps: list[int]
    hat_16th_bias: float
    kick_sync_bias: float
    fill_style: str  # "snare_roll" or "tom_fill"


@dataclass
class MelodyContourProfile:
    kind: str  # "arch", "descending", "ascending", "wave", "plateau"
    intensity: float  # 0..1


@dataclass
class SongPlan:
    sections: list[SectionDef]
    bar_mods: list[BarModifiers]
    rhythm: RhythmProfile
    contour: MelodyContourProfile
    templates: dict  # section_name -> template dict
    phrase_len_bars: int = 4


@dataclass
class ChordSegment:
    bar_index: int
    start_step: int  # 0..15
    end_step: int    # 1..16
    label: str
    pcs: list[int]   # pitch classes in the chord
    root_pc: int
    quality: str
    extension: str
    is_borrowed: bool
    section: str
    template_tag: str
    chord: ChordSpec
