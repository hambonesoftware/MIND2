from __future__ import annotations

from dataclasses import dataclass
from .theory.chords import ChordSpec


@dataclass(frozen=True)
class StyleMoodControls:
    """
    Level 1 controls (human-facing).

    All values are normalized 0..1.
    """

    style: str
    mood_valence: float
    mood_arousal: float
    intensity: float
    complexity: float
    tightness: float
    tempo_bpm: float | None = None
    key_name: str | None = None


@dataclass(frozen=True)
class Level2Knobs:
    """Level 2 controls derived from the Level 1 intent."""

    functional_clarity: float
    chromaticism: float
    extension_richness: float
    turnaround_intensity: float
    groove_archetype: str
    swing_amount: float
    syncopation: float
    chord_tone_anchoring: float
    melodic_range: float
    motif_repetition: float
    form_strictness: float
    lift_profile: str


@dataclass(frozen=True)
class StyleProfile:
    """Defaults/ranges per style used by the mapper."""

    density_range: tuple[float, float]
    syncopation_range: tuple[float, float]
    swing_range: tuple[float, float]
    chord_complexity_range: tuple[float, float]
    repetition_range: tuple[float, float]
    variation_range: tuple[float, float]
    energy_range: tuple[float, float]
    cadence_strength_range: tuple[float, float]
    groove_archetypes: tuple[tuple[str, float], ...]
    lift_profiles: tuple[tuple[str, float], ...]


@dataclass(frozen=True)
class DerivedControls:
    """Controls used by the engine after mapping."""

    level1: StyleMoodControls
    level2: Level2Knobs
    style_profile: StyleProfile
    progression_style: str
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


@dataclass
class Controls:
    length_bars: int
    bpm: int
    key_name: str
    mode: str  # "major" or "minor" (minor is natural minor)
    seed: int
    style_mood: StyleMoodControls
    derived: DerivedControls


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
