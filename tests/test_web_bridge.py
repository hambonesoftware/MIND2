import base64
import json
import unittest

import mido

from web.engine_bridge import generate


class TestWebBridge(unittest.TestCase):
    def setUp(self):
        self.request = {
            "style": "pop",
            "brightness": 0.55,
            "energy": 0.55,
            "intensity": 0.55,
            "complexity": 0.40,
            "tightness": 0.65,
            "key": "C",
            "mode": "major",
            "bpm": 112,
            "bars": 16,
            "seed": 48291,
        }

    def test_generates_playable_notes_and_valid_midi(self):
        response = json.loads(generate(json.dumps(self.request)))
        self.assertEqual(response["meta"]["bars"], 16)
        self.assertEqual(set(response["parts"]), {"melody", "harmony", "bass", "drums"})
        self.assertTrue(response["sections"])
        self.assertTrue(response["chords"])
        for part, notes in response["parts"].items():
            self.assertTrue(notes, part)
            self.assertTrue(all(note["duration"] > 0 for note in notes))
            self.assertTrue(all(0 <= note["pitch"] <= 127 for note in notes))
        midi_bytes = base64.b64decode(response["midiBase64"])
        self.assertTrue(midi_bytes.startswith(b"MThd"))
        self.assertGreater(len(midi_bytes), 100)

    def test_same_request_is_deterministic(self):
        request = json.dumps(self.request)
        self.assertEqual(generate(request), generate(request))

    def test_unknown_style_is_rejected(self):
        self.request["style"] = "not_a_style"
        with self.assertRaises(ValueError):
            generate(json.dumps(self.request))

    def test_non_finite_control_is_rejected(self):
        self.request["intensity"] = float("nan")
        with self.assertRaises(ValueError):
            generate(json.dumps(self.request))


if __name__ == "__main__":
    unittest.main()
