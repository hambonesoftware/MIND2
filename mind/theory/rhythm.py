from __future__ import annotations

from ..utils import step_of_tick_in_bar


def analyze_rhythm(note_on_ticks: list[int], total_bars: int) -> dict[str, float | str]:
    total_hits = len(note_on_ticks)
    if total_hits == 0 or total_bars <= 0:
        return {"syncopation": 0.0, "density": 0.0, "groove_type": "silence"}

    steps = [int(step_of_tick_in_bar(tick)) for tick in note_on_ticks]
    strong_steps = {0, 4, 8, 12}
    offbeat_steps = {2, 6, 10, 14}

    strong_hits = sum(1 for s in steps if s in strong_steps)
    offbeat_hits = sum(1 for s in steps if s in offbeat_steps)
    weak_hits = total_hits - strong_hits - offbeat_hits

    sync_raw = (offbeat_hits + 1.5 * weak_hits) / total_hits
    syncopation = max(0.0, min(1.0, sync_raw))
    density = total_hits / max(1, total_bars)

    even_hits = sum(1 for s in steps if s % 2 == 0)
    strong_ratio = strong_hits / total_hits
    offbeat_ratio = offbeat_hits / total_hits
    weak_ratio = weak_hits / total_hits
    even_ratio = even_hits / total_hits

    if strong_ratio >= 0.6:
        groove_type = "on_beat"
    elif offbeat_ratio >= 0.6 and strong_hits == 0:
        groove_type = "offbeat"
    elif even_ratio >= 0.85 and strong_hits > 0 and offbeat_hits > 0:
        groove_type = "straight"
    elif weak_ratio >= 0.35:
        groove_type = "syncopated"
    else:
        groove_type = "mixed"

    return {"syncopation": syncopation, "density": density, "groove_type": groove_type}
