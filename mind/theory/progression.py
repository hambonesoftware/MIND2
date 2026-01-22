from __future__ import annotations

import random

_POP_TEMPLATES = [
    {"name": "I-V-vi-IV", "degrees": [0, 4, 5, 3], "tags": ["pop", "anthem"]},
    {"name": "I-vi-IV-V", "degrees": [0, 5, 3, 4], "tags": ["pop", "classic"]},
    {"name": "vi-IV-I-V", "degrees": [5, 3, 0, 4], "tags": ["pop", "uplift"]},
    {"name": "IV-V-I-I", "degrees": [3, 4, 0, 0], "tags": ["pop", "simple"]},
    {"name": "I-IV-V-IV", "degrees": [0, 3, 4, 3], "tags": ["pop", "rockish"]},
    {"name": "ii-V-I-vi", "degrees": [1, 4, 0, 5], "tags": ["functional", "smooth"]},
    {"name": "I-iii-IV-V", "degrees": [0, 2, 3, 4], "tags": ["pop", "forward"]},
    {"name": "I-bVII-IV-I", "degrees": [0, "bVII", 3, 0], "tags": ["mixture", "rockish"]},
    {"name": "I-iv-bVII-IV", "degrees": [0, "iv", "bVII", 3], "tags": ["mixture", "moody"]},
    {"name": "vi-bVII-I-IV", "degrees": [5, "bVII", 0, 3], "tags": ["mixture", "arena"]},
    {"name": "I-IV-V-V/V", "degrees": [0, 3, 4, "V/V"], "tags": ["functional", "lift"]},
]

_JAZZ_TEMPLATES = [
    {"name": "ii-V-I-vi", "degrees": [1, 4, 0, 5], "tags": ["jazz", "functional", "smooth"]},
    {"name": "I-vi-ii-V", "degrees": [0, 5, 1, 4], "tags": ["jazz", "turnaround", "functional"]},
    {"name": "iii-vi-ii-V", "degrees": [2, 5, 1, 4], "tags": ["jazz", "cycle", "smooth"]},
    {"name": "ii-V-I-IV", "degrees": [1, 4, 0, 3], "tags": ["jazz", "cadence"]},
    {"name": "I-vi-ii-V/V", "degrees": [0, 5, 1, "V/V"], "tags": ["jazz", "color", "functional"]},
]

_CLASSICAL_TEMPLATES = [
    {"name": "I-IV-V-I", "degrees": [0, 3, 4, 0], "tags": ["classical", "cadential", "classic", "simple"]},
    {"name": "I-vi-ii-V", "degrees": [0, 5, 1, 4], "tags": ["classical", "functional", "cadential"]},
    {"name": "I-ii-V-I", "degrees": [0, 1, 4, 0], "tags": ["classical", "cadential", "classic"]},
    {"name": "I-V-vi-iii", "degrees": [0, 4, 5, 2], "tags": ["classical", "sequence"]},
    {"name": "vi-ii-V-I", "degrees": [5, 1, 4, 0], "tags": ["classical", "cadential"]},
    {"name": "I-IV-ii-V", "degrees": [0, 3, 1, 4], "tags": ["classical", "functional"]},
]

_STYLE_LIBRARY = {
    "pop": _POP_TEMPLATES,
    "jazz": _JAZZ_TEMPLATES,
    "classical": _CLASSICAL_TEMPLATES,
}


class ProgressionGenerator:
    def __init__(self, rng: random.Random):
        self._rng = rng

    def templates_for_style(self, style: str | None, mode: str) -> list[dict]:
        style_key = (style or "pop").strip().lower()
        templates = _STYLE_LIBRARY.get(style_key, _STYLE_LIBRARY["pop"])

        if mode != "major":
            filtered = [t for t in templates if "mixture" not in (t.get("tags") or [])]
            return filtered if filtered else templates

        return templates

    def choose_template(self, style: str | None, mode: str) -> dict:
        templates = self.templates_for_style(style, mode)
        return self._rng.choice(templates)
