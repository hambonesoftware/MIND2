import unittest

from mind.theory.analysis import detect_cadence, roman_numeral


class TestAnalysis(unittest.TestCase):
    def test_roman_numerals_in_major(self):
        key = {"key_name": "C", "mode": "major"}
        self.assertEqual(roman_numeral({"root_pc": 0, "quality": "maj"}, key), "I")
        self.assertEqual(roman_numeral({"root_pc": 5, "quality": "maj"}, key), "IV")
        self.assertEqual(roman_numeral({"root_pc": 2, "quality": "min"}, key), "ii")

    def test_detect_authentic_cadence(self):
        key = {"key_name": "C", "mode": "major"}
        progression = [
            {"root_pc": 0, "quality": "maj"},
            {"root_pc": 5, "quality": "maj"},
            {"root_pc": 7, "quality": "maj"},
            {"root_pc": 0, "quality": "maj"},
        ]
        self.assertEqual(detect_cadence(progression, key), "authentic")

    def test_detect_ii_v_i(self):
        key = {"key_name": "C", "mode": "major"}
        progression = [
            {"root_pc": 2, "quality": "min"},
            {"root_pc": 7, "quality": "maj"},
            {"root_pc": 0, "quality": "maj"},
        ]
        self.assertEqual(detect_cadence(progression, key), "ii-V-I")

    def test_detect_plagal(self):
        key = {"key_name": "C", "mode": "major"}
        progression = [
            {"root_pc": 5, "quality": "maj"},
            {"root_pc": 0, "quality": "maj"},
        ]
        self.assertEqual(detect_cadence(progression, key), "plagal")


if __name__ == "__main__":
    unittest.main()
