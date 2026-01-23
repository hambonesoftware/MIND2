from __future__ import annotations

from dataclasses import dataclass
import random

from .utils import clamp01, lerp, pick_weighted


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


STYLE_PROFILES: dict[str, StyleProfile] = {
    "pop": StyleProfile(
        density_range=(0.45, 0.78),
        syncopation_range=(0.20, 0.62),
        swing_range=(0.00, 0.14),
        chord_complexity_range=(0.20, 0.60),
        repetition_range=(0.55, 0.88),
        variation_range=(0.22, 0.60),
        energy_range=(0.42, 0.82),
        cadence_strength_range=(0.45, 0.82),
        groove_archetypes=(
            ("straight_pop", 0.50),
            ("four_on_floor", 0.30),
            ("bouncy", 0.20),
        ),
        lift_profiles=(
            ("lift", 0.50),
            ("plateau", 0.30),
            ("drop", 0.20),
        ),
    ),
    "jazz": StyleProfile(
        density_range=(0.40, 0.72),
        syncopation_range=(0.35, 0.85),
        swing_range=(0.08, 0.32),
        chord_complexity_range=(0.55, 0.95),
        repetition_range=(0.35, 0.68),
        variation_range=(0.40, 0.85),
        energy_range=(0.35, 0.80),
        cadence_strength_range=(0.50, 0.90),
        groove_archetypes=(
            ("swing", 0.55),
            ("laid_back", 0.30),
            ("latin", 0.15),
        ),
        lift_profiles=(
            ("lift", 0.35),
            ("plateau", 0.40),
            ("drop", 0.25),
        ),
    ),
    "classical": StyleProfile(
        density_range=(0.30, 0.60),
        syncopation_range=(0.10, 0.35),
        swing_range=(0.00, 0.05),
        chord_complexity_range=(0.30, 0.65),
        repetition_range=(0.40, 0.70),
        variation_range=(0.30, 0.70),
        energy_range=(0.30, 0.75),
        cadence_strength_range=(0.55, 0.95),
        groove_archetypes=(
            ("straight", 0.70),
            ("waltz", 0.20),
            ("march", 0.10),
        ),
        lift_profiles=(
            ("lift", 0.25),
            ("plateau", 0.45),
            ("drop", 0.30),
        ),
    ),
}


def map_controls(level1: StyleMoodControls, seed: int) -> DerivedControls:
    """
    Map Level 1 controls into normalized engine parameters plus style defaults.

    Examples:
        >>> level1 = StyleMoodControls(
        ...     style="pop",
        ...     mood_valence=0.70,
        ...     mood_arousal=0.55,
        ...     intensity=0.60,
        ...     complexity=0.40,
        ...     tightness=0.65,
        ... )
        >>> derived = map_controls(level1, seed=17)
        >>> round(derived.density, 2)
        0.61
        >>> round(derived.swing, 2)
        0.06
        >>> derived.level2.groove_archetype
        'four_on_floor'
    """

    style_key = (level1.style or "pop").strip().lower()
    profile = STYLE_PROFILES.get(style_key, STYLE_PROFILES["pop"])

    valence = clamp01(level1.mood_valence)
    arousal = clamp01(level1.mood_arousal)
    intensity = clamp01(level1.intensity)
    complexity = clamp01(level1.complexity)
    tightness = clamp01(level1.tightness)

    rng = random.Random(seed)

    groove_weights = []
    for name, base_w in profile.groove_archetypes:
        if "swing" in name:
            adj = lerp(0.7, 1.3, 1 - tightness)
        elif "four_on_floor" in name:
            adj = lerp(1.1, 0.8, 1 - tightness)
        else:
            adj = lerp(0.9, 1.2, intensity)
        groove_weights.append((name, base_w * adj))
    groove_archetype = pick_weighted(rng, groove_weights)

    lift_weights = []
    for name, base_w in profile.lift_profiles:
        if name == "lift":
            adj = lerp(0.8, 1.35, valence)
        elif name == "drop":
            adj = lerp(1.3, 0.8, valence)
        else:
            adj = 1.0
        lift_weights.append((name, base_w * adj))
    lift_profile = pick_weighted(rng, lift_weights)

    swing_amount = clamp01(lerp(profile.swing_range[0], profile.swing_range[1], (1 - tightness) * 0.7 + intensity * 0.3))
    syncopation = clamp01(lerp(profile.syncopation_range[0], profile.syncopation_range[1], 1 - tightness))

    level2 = Level2Knobs(
        functional_clarity=clamp01(lerp(0.90, 0.35, complexity)),
        chromaticism=clamp01(lerp(0.10, 0.75, complexity)),
        extension_richness=clamp01(lerp(0.20, 0.92, complexity)),
        turnaround_intensity=clamp01(lerp(0.25, 0.90, intensity)),
        groove_archetype=groove_archetype,
        swing_amount=swing_amount,
        syncopation=syncopation,
        chord_tone_anchoring=clamp01(lerp(0.82, 0.28, complexity)),
        melodic_range=clamp01(lerp(0.30, 0.85, intensity)),
        motif_repetition=clamp01(lerp(0.25, 0.86, 1 - intensity)),
        form_strictness=clamp01(lerp(0.35, 0.95, tightness)),
        lift_profile=lift_profile,
    )

    density = clamp01(
        lerp(
            profile.density_range[0],
            profile.density_range[1],
            intensity * 0.6 + (1 - tightness) * 0.4,
        )
    )
    chord_complexity = clamp01(lerp(profile.chord_complexity_range[0], profile.chord_complexity_range[1], complexity))
    repetition = clamp01(lerp(profile.repetition_range[0], profile.repetition_range[1], level2.motif_repetition))
    variation = clamp01(lerp(profile.variation_range[0], profile.variation_range[1], intensity * 0.5 + (1 - level2.motif_repetition) * 0.5))
    energy = clamp01(lerp(profile.energy_range[0], profile.energy_range[1], intensity * 0.65 + arousal * 0.35))
    cadence_strength = clamp01(lerp(profile.cadence_strength_range[0], profile.cadence_strength_range[1], level2.turnaround_intensity))

    humanize_timing_ms = lerp(2.0, 14.0, 1 - tightness)
    humanize_velocity = clamp01(lerp(0.04, 0.22, 1 - tightness))

    return DerivedControls(
        level1=StyleMoodControls(
            style=style_key,
            mood_valence=valence,
            mood_arousal=arousal,
            intensity=intensity,
            complexity=complexity,
            tightness=tightness,
        ),
        level2=level2,
        style_profile=profile,
        progression_style=style_key,
        density=density,
        syncopation=level2.syncopation,
        swing=level2.swing_amount,
        chord_complexity=chord_complexity,
        repetition=repetition,
        variation=variation,
        energy=energy,
        cadence_strength=cadence_strength,
        humanize_timing_ms=humanize_timing_ms,
        humanize_velocity=humanize_velocity,
    )
