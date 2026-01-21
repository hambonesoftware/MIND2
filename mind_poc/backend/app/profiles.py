PROFILES = {
    "wide_acoustic": {
        "id": "wide_acoustic",
        "label": "Wide-Interval Acoustic",
        "avoid_intervals": [1, 2, 6, 11],
        "clash_policy": "shift",
        "shift_choices": [2, -2, 5, -5]
    },
    "percussive_fingerstyle": {
        "id": "percussive_fingerstyle",
        "label": "Percussive Fingerstyle",
        "avoid_intervals": [1, 6, 10, 11],
        "clash_policy": "shift",
        "shift_choices": [1, -1, 2, -2]
    },
    "dark_pulse_synth": {
        "id": "dark_pulse_synth",
        "label": "Dark Pulse Synth",
        "avoid_intervals": [1, 2, 6],
        "clash_policy": "shift",
        "shift_choices": [2, -2, 3, -3]
    }
}


def list_profiles():
    return [
        {"id": profile["id"], "label": profile["label"], "params": profile}
        for profile in PROFILES.values()
    ]


def get_profile(profile_id):
    return PROFILES.get(profile_id)
