import unittest

from mind.theory.chords import ChordSpec, chord_pcs, harmonic_function


class TestChords(unittest.TestCase):
    def test_triad_qualities(self):
        self.assertEqual(chord_pcs(0, "maj", "triad"), [0, 4, 7])
        self.assertEqual(chord_pcs(0, "min", "triad"), [0, 3, 7])
        self.assertEqual(chord_pcs(0, "dim", "triad"), [0, 3, 6])
        self.assertEqual(chord_pcs(0, "aug", "triad"), [0, 4, 8])

    def test_extensions_map_to_pitch_classes(self):
        self.assertCountEqual(chord_pcs(0, "maj", "7"), [0, 4, 7, 10])
        self.assertCountEqual(chord_pcs(0, "maj", "9"), [0, 4, 10, 2])
        self.assertCountEqual(chord_pcs(0, "maj", "11"), [0, 4, 10, 5])
        self.assertCountEqual(chord_pcs(0, "maj", "13"), [0, 4, 10, 2, 9])

    def test_chord_spec_to_pcs(self):
        chord = ChordSpec(root_pc=2, quality="min", extension="9", inversion=0, function="tonic")
        self.assertCountEqual(chord.to_pcs(), chord_pcs(2, "min", "9"))

    def test_harmonic_function_mapping(self):
        self.assertEqual(harmonic_function("I", "maj"), "tonic")
        self.assertEqual(harmonic_function("V", "maj"), "dominant")
        self.assertEqual(harmonic_function("IV", "maj"), "subdominant")
        self.assertEqual(harmonic_function("ii", "min"), "subdominant")


if __name__ == "__main__":
    unittest.main()
