from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Any

from ..constants import NOTE_NAMES
from ..utils import pc_to_name
from .chords import chord_pcs
from .scales import get_scale


@dataclass(frozen=True)
class Exercise:
    kind: str
    prompt: str
    answer: str
    metadata: dict[str, Any]


_QUALITY_LABELS = {
    "maj": "major",
    "min": "minor",
    "dim": "diminished",
    "aug": "augmented",
}

_SEVENTH_LABELS = {
    "maj": "dominant seventh",
    "min": "minor seventh",
    "dim": "half-diminished seventh",
    "aug": "augmented major seventh",
}


def _format_chord_answer(root_name: str, quality: str, extension: str) -> str:
    if extension == "triad":
        quality_label = _QUALITY_LABELS.get(quality, quality)
        return f"{root_name} {quality_label} triad"
    if extension == "7":
        seventh_label = _SEVENTH_LABELS.get(quality, "seventh")
        return f"{root_name} {seventh_label}"
    quality_label = _QUALITY_LABELS.get(quality, quality)
    return f"{root_name} {quality_label} chord"


def generate_chord_identification_question(rng: random.Random | None = None) -> Exercise:
    rng = rng or random.Random()
    root_pc = rng.randint(0, 11)
    quality = rng.choice(tuple(_QUALITY_LABELS.keys()))
    extension = rng.choice(("triad", "7"))
    pcs = chord_pcs(root_pc, quality, extension)
    note_names = [pc_to_name(pc) for pc in pcs]
    prompt = f"Identify the chord built from: {', '.join(note_names)}."
    root_name = NOTE_NAMES[root_pc % 12]
    answer = _format_chord_answer(root_name, quality, extension)
    return Exercise(
        kind="chord_identification",
        prompt=prompt,
        answer=answer,
        metadata={
            "root_pc": root_pc,
            "quality": quality,
            "extension": extension,
            "notes": note_names,
        },
    )


def generate_scale_construction_question(rng: random.Random | None = None) -> Exercise:
    rng = rng or random.Random()
    tonic_pc = rng.randint(0, 11)
    scale_name = rng.choice(("major", "natural minor", "harmonic minor", "melodic minor"))
    scale = get_scale(scale_name)
    note_names = [pc_to_name((tonic_pc + interval) % 12) for interval in scale.intervals]
    tonic_name = NOTE_NAMES[tonic_pc % 12]
    prompt = f"Construct the {tonic_name} {scale.name} scale."
    answer = " ".join(note_names)
    return Exercise(
        kind="scale_construction",
        prompt=prompt,
        answer=answer,
        metadata={
            "tonic_pc": tonic_pc,
            "scale_name": scale.name,
            "notes": note_names,
        },
    )

