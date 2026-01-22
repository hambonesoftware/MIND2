import unittest

from mind.midi_build import build_song_bundle
from mind.models import Controls
from mind.theory import engine


class EchoPlugin:
    name = "echo"

    def analyze(self, music_data):
        return {"received": sorted(music_data.keys())}


class PluginTagPlugin:
    name = "tagger"

    def analyze(self, music_data):
        return {"tag": "ok"}


class TestTheoryEngine(unittest.TestCase):
    def tearDown(self):
        engine.clear_registry()

    def test_register_and_analyze(self):
        engine.register(EchoPlugin())
        result = engine.analyze({"one": 1, "two": 2})
        self.assertIn("echo", result)
        self.assertEqual(result["echo"]["received"], ["one", "two"])

    def test_report_includes_plugins(self):
        engine.register(PluginTagPlugin())
        ctrl = Controls(
            length_bars=4,
            bpm=120,
            key_name="C",
            mode="major",
            density=0.5,
            syncopation=0.4,
            swing=0.0,
            chord_complexity=0.3,
            repetition=0.5,
            variation=0.4,
            energy=0.6,
            cadence_strength=0.5,
            humanize_timing_ms=0.0,
            humanize_velocity=0.0,
            progression_style="pop",
            seed=7,
        )
        _, _, _, _, report = build_song_bundle(ctrl)
        self.assertIn("plugins", report)
        self.assertEqual(report["plugins"], {"tagger": {"tag": "ok"}})


if __name__ == "__main__":
    unittest.main()
