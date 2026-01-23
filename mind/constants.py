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

STYLE_RHYTHM_ARCHETYPES = {
    "pop": [
        ("straight_pop", 0.55),
        ("four_on_floor", 0.35),
        ("half_time", 0.10),
    ],
    "modern_pop": [
        ("four_on_floor", 0.45),
        ("straight_pop", 0.30),
        ("half_time", 0.15),
        ("bouncy", 0.10),
    ],
    "jazz": [
        ("bouncy", 0.70),
        ("straight_pop", 0.20),
        ("half_time", 0.10),
    ],
    "classical": [
        ("straight_pop", 0.55),
        ("half_time", 0.45),
    ],
    "rock": [
        ("straight_pop", 0.55),
        ("four_on_floor", 0.30),
        ("half_time", 0.15),
    ],
    "early_rock_roll": [
        ("straight_pop", 0.45),
        ("bouncy", 0.35),
        ("four_on_floor", 0.20),
    ],
}

STYLE_SWING_DEFAULTS = {
    "pop": (0.05, 0.15),
    "modern_pop": (0.02, 0.12),
    "jazz": (0.55, 0.65),
    "classical": (0.0, 0.10),
    "rock": (0.0, 0.08),
    "early_rock_roll": (0.02, 0.12),
}

STYLE_CHROMATICISM_DEFAULTS = {
    "pop": (0.15, 0.45),
    "modern_pop": (0.30, 0.65),
    "jazz": (0.45, 0.80),
    "classical": (0.05, 0.30),
    "rock": (0.10, 0.40),
    "early_rock_roll": (0.08, 0.30),
}

STYLE_EXTENSION_RICHNESS_DEFAULTS = {
    "pop": (0.20, 0.55),
    "modern_pop": (0.35, 0.75),
    "jazz": (0.55, 0.90),
    "classical": (0.15, 0.45),
    "rock": (0.18, 0.50),
    "early_rock_roll": (0.15, 0.40),
}

STYLE_FUNCTIONAL_CLARITY_DEFAULTS = {
    "pop": (0.55, 0.85),
    "modern_pop": (0.45, 0.75),
    "jazz": (0.40, 0.75),
    "classical": (0.70, 0.95),
    "rock": (0.60, 0.85),
    "early_rock_roll": (0.70, 0.90),
}

STYLE_GROOVE_ARCHETYPES = {
    "pop": (
        ("straight_pop", 0.55),
        ("four_on_floor", 0.30),
        ("bouncy", 0.15),
    ),
    "modern_pop": (
        ("four_on_floor", 0.45),
        ("straight_pop", 0.25),
        ("bouncy", 0.20),
        ("half_time", 0.10),
    ),
    "jazz": (
        ("swing", 0.55),
        ("laid_back", 0.30),
        ("latin", 0.15),
    ),
    "classical": (
        ("straight", 0.70),
        ("waltz", 0.20),
        ("march", 0.10),
    ),
    "rock": (
        ("straight_pop", 0.55),
        ("four_on_floor", 0.30),
        ("bouncy", 0.15),
    ),
    "early_rock_roll": (
        ("straight_pop", 0.45),
        ("bouncy", 0.35),
        ("four_on_floor", 0.20),
    ),
}

LEVEL2_KNOB_METADATA = {
    "functional_clarity": {
        "display_name": "Functional Clarity",
        "tooltip": "How clearly the harmony resolves to functional centers.",
        "range": (0.0, 1.0),
    },
    "chromaticism": {
        "display_name": "Chromaticism",
        "tooltip": "Amount of non-diatonic tones and borrowed color.",
        "range": (0.0, 1.0),
    },
    "extension_richness": {
        "display_name": "Extension Richness",
        "tooltip": "Density of chord extensions beyond triads.",
        "range": (0.0, 1.0),
    },
    "turnaround_intensity": {
        "display_name": "Turnaround Intensity",
        "tooltip": "Strength of cadential pull at phrase ends.",
        "range": (0.0, 1.0),
    },
    "groove_archetype": {
        "display_name": "Groove Archetype",
        "tooltip": "Core rhythmic feel family used by the drummer.",
        "range": None,
    },
    "swing_amount": {
        "display_name": "Swing Amount",
        "tooltip": "Delay off-beat subdivisions for swing or shuffle feel.",
        "range": (0.0, 1.0),
        "style_labels": {
            "rock": "Swing/Shuffle",
            "early_rock_roll": "Swing/Shuffle",
            "jazz": "Swing",
        },
    },
    "syncopation": {
        "display_name": "Syncopation",
        "tooltip": "Emphasis on off-beats and unexpected accents.",
        "range": (0.0, 1.0),
    },
    "chord_tone_anchoring": {
        "display_name": "Chord Tone Anchoring",
        "tooltip": "How strongly melodies land on chord tones.",
        "range": (0.0, 1.0),
    },
    "melodic_range": {
        "display_name": "Melodic Range",
        "tooltip": "Span between lowest and highest melody notes.",
        "range": (0.0, 1.0),
    },
    "motif_repetition": {
        "display_name": "Motif Repetition",
        "tooltip": "Reuse of melodic motifs across phrases.",
        "range": (0.0, 1.0),
    },
    "form_strictness": {
        "display_name": "Form Strictness",
        "tooltip": "How rigidly phrases adhere to form templates.",
        "range": (0.0, 1.0),
    },
    "lift_profile": {
        "display_name": "Lift Profile",
        "tooltip": "Energy-lift pattern across sections.",
        "range": None,
    },
}


def level2_knob_label(knob_key: str, style: str | None = None) -> str:
    meta = LEVEL2_KNOB_METADATA.get(knob_key, {})
    if style:
        style_key = style.strip().lower()
        style_labels = meta.get("style_labels", {})
        if style_key in style_labels:
            return style_labels[style_key]
    return meta.get("display_name", knob_key)


def level2_knob_range(knob_key: str) -> tuple[float, float] | None:
    meta = LEVEL2_KNOB_METADATA.get(knob_key, {})
    return meta.get("range")
