"""MindV2.0 package.

Option B structure:
- mind/constants.py  : fixed constants (PPQ, GM programs, drum notes)
- mind/models.py     : dataclasses for controls and musical plan artifacts
- mind/utils.py      : small helpers + music theory primitives
- mind/planning.py   : sectioning + rhythm DNA + contour + chord templates
- mind/harmony.py    : chords-first progression + voice-leading harmony generator
- mind/bass.py       : bass generator
- mind/melody.py     : melody generator
- mind/drums.py      : drums generator
- mind/reporting.py  : analysis report builder
- mind/midi_build.py : midi + bundle builder
- mind/player.py     : realtime MIDI playback helper
- mind/ui.py         : Tkinter GUI app
"""
