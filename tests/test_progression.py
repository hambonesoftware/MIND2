import random
import unittest

from mind.theory.progression import ProgressionGenerator


class TestProgressionGenerator(unittest.TestCase):
    def test_deterministic_selection_by_seed(self):
        rng_a = random.Random(1234)
        rng_b = random.Random(1234)

        gen_a = ProgressionGenerator(rng_a)
        gen_b = ProgressionGenerator(rng_b)

        seq_a = [gen_a.choose_template("jazz", "major")["name"] for _ in range(5)]
        seq_b = [gen_b.choose_template("jazz", "major")["name"] for _ in range(5)]

        self.assertEqual(seq_a, seq_b)

    def test_deterministic_across_styles(self):
        rng_a = random.Random(42)
        rng_b = random.Random(42)

        gen_a = ProgressionGenerator(rng_a)
        gen_b = ProgressionGenerator(rng_b)

        seq_a = [
            gen_a.choose_template("pop", "major")["name"],
            gen_a.choose_template("classical", "major")["name"],
        ]
        seq_b = [
            gen_b.choose_template("pop", "major")["name"],
            gen_b.choose_template("classical", "major")["name"],
        ]

        self.assertEqual(seq_a, seq_b)


if __name__ == "__main__":
    unittest.main()
