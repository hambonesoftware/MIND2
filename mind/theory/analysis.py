from __future__ import annotations

from typing import Any, Iterable, Tuple

from ..utils import key_to_pc, scale_pcs


def _parse_key(key: Any) -> Tuple[int, str]:
    if isinstance(key, (tuple, list)) and len(key) >= 2:
        tonic, mode = key[0], key[1]
        tonic_pc = tonic if isinstance(tonic, int) else key_to_pc(str(tonic))
        return tonic_pc, str(mode)
    if isinstance(key, dict):
        mode = str(key.get("mode", "major"))
        if "tonic_pc" in key:
            return int(key["tonic_pc"]) % 12, mode
        if "key_name" in key:
            return key_to_pc(str(key["key_name"])), mode
        if "name" in key:
            return key_to_pc(str(key["name"])), mode
    if isinstance(key, str):
        return key_to_pc(key), "major"
    raise ValueError("Unsupported key format")


def _parse_chord(chord: Any) -> Tuple[int, str]:
    if hasattr(chord, "root_pc"):
        root_pc = int(getattr(chord, "root_pc")) % 12
        quality = str(getattr(chord, "quality", "maj"))
        return root_pc, quality
    if isinstance(chord, dict):
        root_pc = int(chord.get("root_pc", 0)) % 12
        quality = str(chord.get("quality", "maj"))
        return root_pc, quality
    raise ValueError("Unsupported chord format")


def _degree_with_accidentals(root_pc: int, tonic_pc: int, mode: str) -> Tuple[int, int]:
    pcs = scale_pcs(tonic_pc, mode)
    best_degree = 0
    best_diff = 0
    best_abs = 13
    for idx, pc in enumerate(pcs):
        diff = (root_pc - pc) % 12
        if diff > 6:
            diff -= 12
        abs_diff = abs(diff)
        if abs_diff < best_abs:
            best_abs = abs_diff
            best_diff = diff
            best_degree = idx
    return best_degree, best_diff


def roman_numeral(chord: Any, key: Any) -> str:
    tonic_pc, mode = _parse_key(key)
    root_pc, quality = _parse_chord(chord)
    degree, accidental = _degree_with_accidentals(root_pc, tonic_pc, mode)

    roman_base = ["I", "II", "III", "IV", "V", "VI", "VII"][degree]
    if quality == "min":
        numeral = roman_base.lower()
    elif quality == "dim":
        numeral = roman_base.lower() + "°"
    elif quality == "aug":
        numeral = roman_base + "+"
    else:
        numeral = roman_base

    if accidental > 0:
        return "#" * accidental + numeral
    if accidental < 0:
        return "b" * (-accidental) + numeral
    return numeral


def detect_cadence(progression: Iterable[Any], key: Any) -> str | None:
    chords = list(progression)
    if not chords:
        return None

    tonic_pc, mode = _parse_key(key)
    degrees = []
    for chord in chords:
        root_pc, _quality = _parse_chord(chord)
        degree, _acc = _degree_with_accidentals(root_pc, tonic_pc, mode)
        degrees.append(degree)

    if len(degrees) >= 3 and degrees[-3:] == [1, 4, 0]:
        return "ii-V-I"
    if len(degrees) >= 2 and degrees[-2:] == [4, 0]:
        return "authentic"
    if len(degrees) >= 2 and degrees[-2:] == [3, 0]:
        return "plagal"
    return None
