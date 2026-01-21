from app.profiles import list_profiles


def test_profiles_include_minimum_set():
    profiles = list_profiles()
    ids = {profile["id"] for profile in profiles}
    assert {"wide_acoustic", "percussive_fingerstyle", "dark_pulse_synth"}.issubset(ids)
