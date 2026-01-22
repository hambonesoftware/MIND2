# MindV2.0 — Pop Knob Player (Chords-First)

This is a Tkinter + Mido pop generator that:
- Plans song sections (intro/verse/chorus/bridge/outro) in 4-bar phrases
- Generates chords first (templates + turnarounds + cadences + modal-mixture tokens)
- Generates melody (contour + motif reuse), harmony (voice-leading comp), bass (rhythm DNA), drums (rhythm DNA + fills)
- Plays via MIDI output (mido + python-rtmidi) and can save a MIDI file
- Can export a JSON analysis report

## Requirements

- Python 3.10+ (recommended 3.12)
- `mido`
- `python-rtmidi` (recommended for realtime MIDI out on Windows/macOS/Linux)

Install:
```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Notes

- If you do not have any MIDI output devices, use **Save MIDI...** and open the `.mid` in a DAW.
- On Windows, a common output is **Microsoft GS Wavetable Synth** (if present).
