import unittest

from mido import Message

from mind.theory.counterpoint import analyze_counterpoint


def _events_from_pitches(pitches):
    return [
        (idx * 120, Message("note_on", note=pitch, velocity=64, time=0))
        for idx, pitch in enumerate(pitches)
    ]


class TestCounterpoint(unittest.TestCase):
    def test_parallel_fifths(self):
        melody = _events_from_pitches([72, 74])
        harmony = _events_from_pitches([65, 67])
        analysis = analyze_counterpoint(melody, harmony)
        self.assertEqual(len(analysis["parallel_fifths"]), 1)
        self.assertEqual(analysis["parallel_octaves"], [])

    def test_parallel_octaves(self):
        melody = _events_from_pitches([72, 74])
        harmony = _events_from_pitches([60, 62])
        analysis = analyze_counterpoint(melody, harmony)
        self.assertEqual(len(analysis["parallel_octaves"]), 1)
        self.assertEqual(analysis["parallel_fifths"], [])

    def test_voice_crossing(self):
        melody = _events_from_pitches([60, 62])
        harmony = _events_from_pitches([64, 65])
        analysis = analyze_counterpoint(melody, harmony)
        self.assertEqual(len(analysis["voice_crossings"]), 2)


if __name__ == "__main__":
    unittest.main()
