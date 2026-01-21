import logging
from copy import deepcopy

logger = logging.getLogger(__name__)


def _build_note_index(thought):
    index = {}
    for event in thought.get("sequence", []):
        if event.get("type") == "note" and event.get("time"):
            index.setdefault(event["time"], []).append(event)
    return index


def _interval(a, b):
    return abs((a - b) % 12)


def resolve_conflicts(payload, profile):
    resolved_inputs = deepcopy(payload.get("inputs", []))
    actions = []
    clashes_detected = 0

    if len(resolved_inputs) < 2:
        logger.info("resolve_conflicts: fewer than two inputs, skipping")
        return {
            "schema_version": "resolve.v0",
            "style_profile": payload.get("style_profile", ""),
            "resolved": [
                {"node_id": item.get("node_id"), "thought": item.get("thought")}
                for item in resolved_inputs
            ],
            "meta": {"clashes_detected": 0, "actions": []}
        }

    bass_id = next((item.get("node_id") for item in resolved_inputs if item.get("role") == "bass"), None)
    lead_id = next((item.get("node_id") for item in resolved_inputs if item.get("role") == "lead"), None)

    if bass_id is None and resolved_inputs:
        bass_id = resolved_inputs[0].get("node_id")
    if lead_id is None and len(resolved_inputs) > 1:
        lead_id = resolved_inputs[1].get("node_id")

    thought_by_id = {item.get("node_id"): item.get("thought") for item in resolved_inputs}
    bass_thought = thought_by_id.get(bass_id)
    lead_thought = thought_by_id.get(lead_id)

    if not bass_thought or not lead_thought:
        logger.info("resolve_conflicts: missing bass or lead thought, skipping")
        return {
            "schema_version": "resolve.v0",
            "style_profile": payload.get("style_profile", ""),
            "resolved": [
                {"node_id": item.get("node_id"), "thought": item.get("thought")}
                for item in resolved_inputs
            ],
            "meta": {"clashes_detected": 0, "actions": []}
        }

    avoid_intervals = profile.get("avoid_intervals", [])
    shift_choices = profile.get("shift_choices", [2, -2])
    logger.info(
        "resolve_conflicts: using profile=%s avoid_intervals=%s shift_choices=%s",
        profile.get("id"),
        avoid_intervals,
        shift_choices,
    )

    bass_index = _build_note_index(bass_thought)
    lead_index = _build_note_index(lead_thought)

    for time, bass_events in bass_index.items():
        lead_events = lead_index.get(time, [])
        if not lead_events:
            continue
        for bass_event in bass_events:
            for lead_event in lead_events:
                interval = _interval(bass_event["midi"], lead_event["midi"])
                if interval in avoid_intervals:
                    clashes_detected += 1
                    resolved = False
                    for shift in shift_choices:
                        candidate = lead_event["midi"] + shift
                        candidate_interval = _interval(bass_event["midi"], candidate)
                        if 0 <= candidate <= 127 and candidate_interval not in avoid_intervals:
                            lead_event["midi"] = candidate
                            actions.append({
                                "time": time,
                                "node_id": lead_id,
                                "action": "shift",
                                "semitones": shift
                            })
                            resolved = True
                            break
                    if not resolved:
                        lead_event.clear()
                        lead_event.update({
                            "time": time,
                            "type": "mute",
                            "velocity": 0,
                            "midi": None
                        })
                        actions.append({
                            "time": time,
                            "node_id": lead_id,
                            "action": "drop",
                            "semitones": 0
                        })

    resolved = [
        {"node_id": item.get("node_id"), "thought": item.get("thought")}
        for item in resolved_inputs
    ]

    return {
        "schema_version": "resolve.v0",
        "style_profile": payload.get("style_profile", ""),
        "resolved": resolved,
        "meta": {"clashes_detected": clashes_detected, "actions": actions}
    }
