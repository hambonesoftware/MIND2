PPQ = 480  # ticks per beat (quarter note)
DEFAULT_SEED = 123456789

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
NAME_TO_PC = {name: i for i, name in enumerate(NOTE_NAMES)}

DRUM_CHANNEL = 9  # MIDI channel 10 (0-based index)
DRUM_KICK = 36
DRUM_SNARE = 38
DRUM_HAT_CLOSED = 42
DRUM_HAT_OPEN = 46
DRUM_CRASH = 49  # Crash Cymbal 1
DRUM_RIDE = 51
DRUM_TOM_LOW = 45
DRUM_TOM_MID = 47
DRUM_TOM_HIGH = 50

MELODY_CH = 0
HARMONY_CH = 1
BASS_CH = 2

# General MIDI program numbers (0-based in MIDI messages):
# 0 Acoustic Grand Piano, 4 Electric Piano 1, 24 Nylon Guitar, 32 Acoustic Bass, etc.
GM_PIANO = 0
GM_EPIANO = 4
GM_GUITAR = 24
GM_BASS = 32
