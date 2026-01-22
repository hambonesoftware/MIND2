import random
import unittest

from mind.theory.exercises import (
    _QUALITY_LABELS,
    _SEVENTH_LABELS,
    generate_chord_identification_question,
    generate_scale_construction_question,
)
from mind.theory.chords import chord_pcs
from mind.theory.scales import get_scale
from mind.utils import pc_to_name
from mind.constants import NOTE_NAMES


class TestExercises(unittest.TestCase):
    def test_chord_identification_prompt_answer(self):
        rng = random.Random(14)
        exercise = generate_chord_identification_question(rng)

        expected_pcs = chord_pcs(
            exercise.metadata["root_pc"],
            exercise.metadata["quality"],
            exercise.metadata["extension"],
        )
        expected_notes = [pc_to_name(pc) for pc in expected_pcs]
        self.assertEqual(exercise.metadata["notes"], expected_notes)

        expected_prompt = f"Identify the chord built from: {', '.join(expected_notes)}."
        self.assertEqual(exercise.prompt, expected_prompt)

        root_name = NOTE_NAMES[exercise.metadata["root_pc"] % 12]
        quality = exercise.metadata["quality"]
        extension = exercise.metadata["extension"]
        if extension == "triad":
            expected_answer = f"{root_name} {_QUALITY_LABELS[quality]} triad"
        else:
            expected_answer = f"{root_name} {_SEVENTH_LABELS[quality]}"
        self.assertEqual(exercise.answer, expected_answer)

    def test_scale_construction_prompt_answer(self):
        rng = random.Random(23)
        exercise = generate_scale_construction_question(rng)

        scale = get_scale(exercise.metadata["scale_name"])
        tonic_pc = exercise.metadata["tonic_pc"]
        expected_notes = [pc_to_name((tonic_pc + interval) % 12) for interval in scale.intervals]
        self.assertEqual(exercise.metadata["notes"], expected_notes)

        tonic_name = NOTE_NAMES[tonic_pc % 12]
        expected_prompt = f"Construct the {tonic_name} {scale.name} scale."
        self.assertEqual(exercise.prompt, expected_prompt)
        self.assertEqual(exercise.answer, " ".join(expected_notes))


if __name__ == "__main__":
    unittest.main()
