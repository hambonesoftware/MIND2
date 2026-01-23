import unittest

from mind.control_mapping import StyleMoodControls, map_controls
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
        style_mood = StyleMoodControls(
            style="pop",
            mood_valence=0.6,
            mood_arousal=0.5,
            intensity=0.55,
            complexity=0.35,
            tightness=0.7,
        )
        ctrl = Controls(
            length_bars=4,
            bpm=120,
            key_name="C",
            mode="major",
            seed=7,
            style_mood=style_mood,
            derived=map_controls(style_mood, seed=7),
        )
        _, _, _, _, report = build_song_bundle(ctrl)
        self.assertIn("plugins", report)
        self.assertEqual(report["plugins"], {"tagger": {"tag": "ok"}})


if __name__ == "__main__":
    unittest.main()
