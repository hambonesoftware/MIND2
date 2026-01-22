import unittest

from mido import Message

from mind.theory.melody_analysis import analyze_melody_events


def _events_from_pitches(pitches):
    return [
        (idx * 120, Message("note_on", note=pitch, velocity=64, time=0))
        for idx, pitch in enumerate(pitches)
    ]


class TestMelodyAnalysis(unittest.TestCase):
    def test_stepwise_ascending(self):
        events = _events_from_pitches([60, 62, 64, 65])
        analysis = analyze_melody_events(events)
        self.assertEqual(analysis["contour"], "ascending")
        self.assertEqual(analysis["leap_count"], 0)
        self.assertEqual(analysis["stepwise_ratio"], 1.0)
        self.assertEqual(analysis["climax_note"]["note"], 65)

    def test_arch_with_leaps(self):
        events = _events_from_pitches([60, 64, 67, 64, 60])
        analysis = analyze_melody_events(events)
        self.assertEqual(analysis["contour"], "arch")
        self.assertEqual(analysis["leap_count"], 4)
        self.assertEqual(analysis["stepwise_ratio"], 0.0)
        self.assertEqual(analysis["climax_note"]["note"], 67)

    def test_silence(self):
        analysis = analyze_melody_events([])
        self.assertEqual(analysis["contour"], "silence")
        self.assertEqual(analysis["leap_count"], 0)
        self.assertEqual(analysis["stepwise_ratio"], 0.0)
        self.assertIsNone(analysis["climax_note"])


if __name__ == "__main__":
    unittest.main()
