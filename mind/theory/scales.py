from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Scale:
    name: str
    intervals: tuple[int, ...]
    mode_names: tuple[str, ...]
    characteristic_tones: tuple[int, ...]
    diatonic_chord_qualities: tuple[str, ...] | None = None


_MAJOR_INTERVALS = (0, 2, 4, 5, 7, 9, 11)
_NATURAL_MINOR_INTERVALS = (0, 2, 3, 5, 7, 8, 10)
_HARMONIC_MINOR_INTERVALS = (0, 2, 3, 5, 7, 8, 11)
_MELODIC_MINOR_INTERVALS = (0, 2, 3, 5, 7, 9, 11)

_MAJOR_MODE_NAMES = (
    "ionian",
    "dorian",
    "phrygian",
    "lydian",
    "mixolydian",
    "aeolian",
    "locrian",
)

_MAJOR_MODE_CHARACTERISTIC = {
    "ionian": (4, 11),
    "dorian": (3, 9),
    "phrygian": (1, 8),
    "lydian": (6,),
    "mixolydian": (10,),
    "aeolian": (3, 8, 10),
    "locrian": (1, 6, 10),
}

_SCALES: dict[str, Scale] = {
    "major": Scale(
        name="major",
        intervals=_MAJOR_INTERVALS,
        mode_names=_MAJOR_MODE_NAMES,
        characteristic_tones=(4, 11),
        diatonic_chord_qualities=("maj", "min", "min", "maj", "maj", "min", "dim"),
    ),
    "natural minor": Scale(
        name="natural minor",
        intervals=_NATURAL_MINOR_INTERVALS,
        mode_names=("natural minor",),
        characteristic_tones=(3, 8, 10),
        diatonic_chord_qualities=("min", "dim", "maj", "min", "min", "maj", "maj"),
    ),
    "harmonic minor": Scale(
        name="harmonic minor",
        intervals=_HARMONIC_MINOR_INTERVALS,
        mode_names=(
            "harmonic minor",
            "locrian #6",
            "ionian #5",
            "dorian #4",
            "phrygian dominant",
            "lydian #2",
            "ultralocrian",
        ),
        characteristic_tones=(3, 8, 11),
    ),
    "melodic minor": Scale(
        name="melodic minor",
        intervals=_MELODIC_MINOR_INTERVALS,
        mode_names=(
            "melodic minor",
            "dorian b2",
            "lydian augmented",
            "lydian dominant",
            "mixolydian b6",
            "locrian #2",
            "altered",
        ),
        characteristic_tones=(3, 9, 11),
    ),
}

_SCALE_ALIASES = {
    "major": "major",
    "ionian": "major",
    "minor": "natural minor",
    "natural minor": "natural minor",
    "harmonic minor": "harmonic minor",
    "melodic minor": "melodic minor",
}


def _normalize_scale_name(name: str) -> str:
    return " ".join(name.strip().lower().replace("_", " ").split())


def _rotate_intervals(intervals: Iterable[int], start_index: int) -> tuple[int, ...]:
    intervals_list = list(intervals)
    if not intervals_list:
        return ()
    start = intervals_list[start_index % len(intervals_list)]
    rotated = intervals_list[start_index:] + intervals_list[:start_index]
    return tuple((step - start) % 12 for step in rotated)


def get_scale(name: str) -> Scale:
    normalized = _normalize_scale_name(name)
    if normalized in _SCALE_ALIASES:
        return _SCALES[_SCALE_ALIASES[normalized]]

    if normalized in _MAJOR_MODE_NAMES:
        mode_index = _MAJOR_MODE_NAMES.index(normalized)
        intervals = _rotate_intervals(_MAJOR_INTERVALS, mode_index)
        characteristic = _MAJOR_MODE_CHARACTERISTIC.get(normalized, ())
        return Scale(
            name=normalized,
            intervals=intervals,
            mode_names=(normalized,),
            characteristic_tones=characteristic,
        )

    raise KeyError(f"Unknown scale or mode: {name}")


def get_modes(scale_name: str) -> list[Scale]:
    normalized = _normalize_scale_name(scale_name)
    base_scale = get_scale(normalized)
    if base_scale.name != "major":
        return []

    modes: list[Scale] = []
    for idx, mode_name in enumerate(_MAJOR_MODE_NAMES):
        intervals = _rotate_intervals(base_scale.intervals, idx)
        characteristic = _MAJOR_MODE_CHARACTERISTIC.get(mode_name, ())
        modes.append(
            Scale(
                name=mode_name,
                intervals=intervals,
                mode_names=(mode_name,),
                characteristic_tones=characteristic,
            )
        )
    return modes
