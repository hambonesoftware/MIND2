from __future__ import annotations

from typing import Any, Protocol


class TheoryPlugin(Protocol):
    name: str

    def analyze(self, music_data: dict[str, Any]) -> Any:
        ...


_registry: dict[str, TheoryPlugin] = {}


def register(plugin: TheoryPlugin) -> None:
    name = getattr(plugin, "name", plugin.__class__.__name__)
    _registry[name] = plugin


def registered() -> dict[str, TheoryPlugin]:
    return dict(_registry)


def clear_registry() -> None:
    _registry.clear()


def analyze(music_data: dict[str, Any]) -> dict[str, Any]:
    return {name: plugin.analyze(music_data) for name, plugin in _registry.items()}
