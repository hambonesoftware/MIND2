const TIME_REGEX = /^\d+:\d+:\d+$/;

export function validateThought(thought) {
  if (!thought || typeof thought !== "object") {
    return { ok: false, error: "Thought is not an object" };
  }

  if (thought.schema_version !== "thought.v0") {
    return { ok: false, error: "Unsupported schema version" };
  }

  const required = ["node_id", "status", "style_profile", "meta", "sequence"];
  for (const key of required) {
    if (!(key in thought)) {
      return { ok: false, error: `Missing required field: ${key}` };
    }
  }

  if (!Array.isArray(thought.sequence)) {
    return { ok: false, error: "Sequence must be an array" };
  }

  for (const event of thought.sequence) {
    const eventCheck = validateEvent(event);
    if (!eventCheck.ok) {
      return eventCheck;
    }
  }

  return { ok: true };
}

function validateEvent(event) {
  if (!event || typeof event !== "object") {
    return { ok: false, error: "Event must be an object" };
  }

  if (!TIME_REGEX.test(event.time ?? "")) {
    return { ok: false, error: "Event time must match bar:beat:sixteenth" };
  }

  if (!event.type) {
    return { ok: false, error: "Event type is required" };
  }

  if (event.velocity === undefined || event.velocity === null) {
    return { ok: false, error: "Event velocity is required" };
  }

  if (event.type === "note") {
    if (typeof event.midi !== "number") {
      return { ok: false, error: "Note event requires midi" };
    }
    return { ok: true };
  }

  if (event.type === "mute") {
    return { ok: true };
  }

  if (event.type === "cc") {
    if (typeof event.cc !== "number" || typeof event.value !== "number") {
      return { ok: false, error: "CC event requires cc and value" };
    }
    return { ok: true };
  }

  return { ok: false, error: `Unknown event type: ${event.type}` };
}
