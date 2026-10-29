# MindV2.0 — Pop Knob Player (Chords-First)

## Riverbed for GitHub Pages

The new `docs/` web studio runs this repository's **same Python composition
engine** directly in the browser through Pyodide. It generates real melody,
harmony, bass, drums, song sections, chord progressions, and downloadable MIDI.
There is no server-side music generation, account, or upload. The first visit
downloads the Pyodide runtime and pure-Python `mido` package; an internet
connection is required for that initial load. Preview audio currently uses a
lightweight Web Audio synthesizer, not a SoundFont library.

To test the browser build locally:

```bash
pip install 'mido>=1.3.2'
python -m unittest discover -s tests -v
python scripts/build_web.py
python -m http.server 8000 --directory docs
```

Open `http://localhost:8000`. Do not open `docs/index.html` as a `file://`
URL because the browser needs to fetch the packaged engine.

The `.github/workflows/pages.yml` workflow runs tests, packages the Python
engine, and deploys the `docs/` site on pushes to `main`. In GitHub repository
**Settings → Pages**, set **Build and deployment → Source** to **GitHub Actions**.
Once Pages is enabled, the expected project URL is
`https://hambonesoftware.github.io/MIND2/`.

The older Tkinter app remains available with `python main.py`.

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
