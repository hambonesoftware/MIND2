import unittest

from mind.constants import PPQ
from mind.control_mapping import map_controls
from mind.midi_build import build_song_bundle
from mind.models import Controls, StyleMoodControls


class TestMotifContinuity(unittest.TestCase):
    def test_two_bar_motif_never_silences_the_second_measure(self):
        """Repeated two-bar motifs must cache both bars, not only bar zero."""
        intent = StyleMoodControls(
            style="pop",
            mood_valence=0.5,
            mood_arousal=0.5,
            intensity=0.5,
            complexity=0.5,
            tightness=0.5,
        )
        controls = Controls(
            length_bars=32,
            bpm=120,
            key_name="C",
            mode="major",
            seed=17,
            style_mood=intent,
            derived=map_controls(intent, seed=17),
        )
        _, _, _, parts, _ = build_song_bundle(controls)
        counts = [0] * controls.length_bars
        for tick, message in parts["melody"]:
            if message.type == "note_on" and message.velocity > 0:
                bar = min(controls.length_bars - 1, tick // (PPQ * 4))
                counts[bar] += 1

        self.assertTrue(all(count > 0 for count in counts), counts)

    def test_motif_generation_remains_reproducible(self):
        intent = StyleMoodControls(
            style="jazz",
            mood_valence=0.45,
            mood_arousal=0.65,
            intensity=0.6,
            complexity=0.7,
            tightness=0.4,
        )
        controls = Controls(
            length_bars=16,
            bpm=110,
            key_name="D",
            mode="minor",
            seed=4021,
            style_mood=intent,
            derived=map_controls(intent, seed=4021),
        )
        first = build_song_bundle(controls)[3]["melody"]
        second = build_song_bundle(controls)[3]["melody"]
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
