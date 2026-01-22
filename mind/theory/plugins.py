from __future__ import annotations

from typing import Any


class SamplePlugin:
    """Example plugin stub for theory engine integrations."""

    name = "sample_plugin"

    def analyze(self, music_data: dict[str, Any]) -> dict[str, Any]:
        return {
            "message": "Sample plugin stub.",
            "keys": sorted(music_data.keys()),
        }


def register_sample_plugin() -> SamplePlugin:
    """Return a sample plugin instance for manual registration."""
    return SamplePlugin()
