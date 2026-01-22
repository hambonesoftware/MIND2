import unittest

from mind.theory.scales import get_modes, get_scale
from mind.utils import scale_pcs


class TestScales(unittest.TestCase):
    def test_major_scale_intervals(self):
        scale = get_scale("major")
        self.assertEqual(scale.intervals, (0, 2, 4, 5, 7, 9, 11))

    def test_natural_minor_alias(self):
        scale = get_scale("minor")
        self.assertEqual(scale.name, "natural minor")
        self.assertEqual(scale.intervals, (0, 2, 3, 5, 7, 8, 10))

    def test_harmonic_minor_intervals(self):
        scale = get_scale("harmonic minor")
        self.assertEqual(scale.intervals, (0, 2, 3, 5, 7, 8, 11))

    def test_melodic_minor_intervals(self):
        scale = get_scale("melodic minor")
        self.assertEqual(scale.intervals, (0, 2, 3, 5, 7, 9, 11))

    def test_major_modes_intervals(self):
        modes = {mode.name: mode for mode in get_modes("major")}
        self.assertEqual(modes["ionian"].intervals, (0, 2, 4, 5, 7, 9, 11))
        self.assertEqual(modes["dorian"].intervals, (0, 2, 3, 5, 7, 9, 10))
        self.assertEqual(modes["phrygian"].intervals, (0, 1, 3, 5, 7, 8, 10))
        self.assertEqual(modes["lydian"].intervals, (0, 2, 4, 6, 7, 9, 11))
        self.assertEqual(modes["mixolydian"].intervals, (0, 2, 4, 5, 7, 9, 10))
        self.assertEqual(modes["aeolian"].intervals, (0, 2, 3, 5, 7, 8, 10))
        self.assertEqual(modes["locrian"].intervals, (0, 1, 3, 5, 6, 8, 10))

    def test_scale_pcs_uses_database(self):
        pcs = scale_pcs(0, "minor")
        self.assertEqual(pcs, [0, 2, 3, 5, 7, 8, 10])


if __name__ == "__main__":
    unittest.main()
