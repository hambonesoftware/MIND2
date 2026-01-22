from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from ..utils import unique_pcs


@dataclass(frozen=True)
class ChordSpec:
    root_pc: int
    quality: str  # maj/min/dim/aug
    extension: str  # triad/7/9/11/13/add9/sus2/sus4 etc
    inversion: int  # 0=root position, 1=first inversion, ...
    function: str  # tonic/dominant/subdominant/other

    def to_pcs(self) -> list[int]:
        return chord_pcs(self.root_pc, self.quality, self.extension)


def chord_pcs(root_pc: int, quality: str, extension: str) -> list[int]:
    base = build_triad(root_pc, quality)
    pcs = base[:]

    def _drop_fifth(_pcs: list[int]) -> list[int]:
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
        pcs = build_seventh(root_pc, quality, dominant7=(quality == "maj"))
        return unique_pcs(pcs)
    if extension == "9":
        pcs = build_seventh(root_pc, quality, dominant7=(quality == "maj"))
        pcs = _drop_fifth(pcs) + [(root_pc + 2) % 12]
        return unique_pcs(pcs)
    if extension == "11":
        pcs = build_seventh(root_pc, quality, dominant7=(quality == "maj"))
        pcs = _drop_fifth(pcs) + [(root_pc + 5) % 12]
        return unique_pcs(pcs)
    if extension == "13":
        pcs = build_seventh(root_pc, quality, dominant7=(quality == "maj"))
        pcs = _drop_fifth(pcs) + [(root_pc + 2) % 12, (root_pc + 9) % 12]
        return unique_pcs(pcs)
    if extension == "maj9":
        pcs = build_seventh(root_pc, "maj", dominant7=False)
        pcs = _drop_fifth(pcs) + [(root_pc + 2) % 12]
        return unique_pcs(pcs)
    if extension == "min9":
        pcs = build_seventh(root_pc, "min", dominant7=False)
        pcs = _drop_fifth(pcs) + [(root_pc + 2) % 12]
        return unique_pcs(pcs)
    if extension == "dom9":
        pcs = build_seventh(root_pc, "maj", dominant7=True)
        pcs = _drop_fifth(pcs) + [(root_pc + 2) % 12]
        return unique_pcs(pcs)
    return unique_pcs(pcs)


def build_triad(root_pc: int, quality: str) -> list[int]:
    if quality == "maj":
        intervals = [0, 4, 7]
    elif quality == "min":
        intervals = [0, 3, 7]
    elif quality == "dim":
        intervals = [0, 3, 6]
    elif quality == "aug":
        intervals = [0, 4, 8]
    else:
        intervals = [0, 4, 7]
    return [(root_pc + i) % 12 for i in intervals]


def build_seventh(root_pc: int, quality: str, dominant7: bool = False) -> list[int]:
    if dominant7:
        intervals = [0, 4, 7, 10]
    else:
        if quality == "maj":
            intervals = [0, 4, 7, 11]
        elif quality == "min":
            intervals = [0, 3, 7, 10]
        elif quality == "dim":
            intervals = [0, 3, 6, 10]
        elif quality == "aug":
            intervals = [0, 4, 8, 11]
        else:
            intervals = [0, 4, 7, 11]
    return [(root_pc + i) % 12 for i in intervals]


def guess_inversion(pcs: Iterable[int], root_pc: int) -> int:
    unique = list(unique_pcs(list(pcs)))
    if root_pc not in unique:
        return 0
    return unique.index(root_pc)


def harmonic_function(label: str, quality: str) -> str:
    normalized = label.replace("♭", "b")
    if normalized.startswith("V") or "/V" in normalized or normalized.startswith("subV"):
        return "dominant"
    if normalized.startswith("IV") or normalized in ("ii", "iv"):
        return "subdominant"
    if normalized.startswith("I") or normalized in ("vi", "i"):
        return "tonic"
    if quality == "dim":
        return "dominant"
    return "other"
