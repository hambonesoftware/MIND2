from app.conflict_resolver import resolve_conflicts
from app.profiles import get_profile


def _make_thought(node_id, midi_value):
    return {
        "schema_version": "thought.v0",
        "node_id": node_id,
        "status": "active",
        "style_profile": "wide_acoustic",
        "meta": {
            "tempo": 120,
            "time_signature": "4/4",
            "loop_bars": 1,
            "division": 16
        },
        "sequence": [
            {"time": "0:0:0", "type": "note", "midi": midi_value, "velocity": 0.8}
        ]
    }


def test_conflict_resolver_shifts_lead():
    payload = {
        "schema_version": "resolve.v0",
        "style_profile": "wide_acoustic",
        "inputs": [
            {"node_id": "bass_01", "role": "bass", "thought": _make_thought("bass_01", 60)},
            {"node_id": "lead_01", "role": "lead", "thought": _make_thought("lead_01", 61)}
        ]
    }
    profile = get_profile("wide_acoustic")
    response = resolve_conflicts(payload, profile)

    assert response["schema_version"] == "resolve.v0"
    assert response["meta"]["clashes_detected"] == 1
    actions = response["meta"]["actions"]
    assert actions[0]["action"] == "shift"
    resolved_lead = next(
        item["thought"] for item in response["resolved"] if item["node_id"] == "lead_01"
    )
    lead_event = resolved_lead["sequence"][0]
    assert lead_event["midi"] != 61
