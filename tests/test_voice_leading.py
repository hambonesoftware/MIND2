import unittest

from mind.theory.voice_leading import smooth_voice_leading
from mind.utils import chord_tones_in_range


class TestVoiceLeading(unittest.TestCase):
    def test_smooth_voice_leading_minimizes_motion(self):
        prev_voicing = [60, 64, 67]
        chord_pcs = [7, 11, 2]
        low, high = 55, 76

        voicing = smooth_voice_leading(prev_voicing, chord_pcs, low, high)

        self.assertEqual(voicing, [59, 62, 67])
        self.assertTrue(all(low <= n <= high for n in voicing))
        self.assertTrue(all(n in chord_tones_in_range(chord_pcs, low, high) for n in voicing))

    def test_common_tones_preserved(self):
        prev_voicing = [60, 67, 72]
        chord_pcs = [0, 4, 7]
        low, high = 52, 76

        voicing = smooth_voice_leading(prev_voicing, chord_pcs, low, high)

        self.assertEqual(voicing, prev_voicing)


if __name__ == "__main__":
    unittest.main()
