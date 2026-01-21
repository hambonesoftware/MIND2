import * as Tone from "tone";

function toTimeString(value) {
  if (typeof value === "string") {
    return value;
  }
  if (typeof value === "number") {
    return Tone.Time(value).toString();
  }
  return "0:0:1";
}

function buildPartEvents(sequence) {
  return sequence.map((event) => {
    return {
      time: event.time,
      event
    };
  });
}

export class ToneScheduler {
  constructor({ runtimeStore }) {
    this.runtimeStore = runtimeStore;
    this.nodes = new Map();
  }

  ensureNode(nodeId) {
    if (!this.nodes.has(nodeId)) {
      const synth = new Tone.Synth().toDestination();
      this.nodes.set(nodeId, {
        synth,
        activePart: null,
        nextPart: null,
        swapEventId: null
      });
    }
  }

  scheduleThought(nodeId, thought) {
    this.ensureNode(nodeId);
    const nodeState = this.nodes.get(nodeId);

    if (thought.status !== "active") {
      this.queueStop(nodeId);
      return;
    }

    const events = buildPartEvents(thought.sequence);
    const part = new Tone.Part((time, payload) => {
      const event = payload.event;
      if (event.type === "note") {
        const duration = toTimeString(event.duration ?? "0:0:1");
        nodeState.synth.triggerAttackRelease(
          Tone.Frequency(event.midi, "midi"),
          duration,
          time,
          event.velocity
        );
      }
    }, events);

    part.loop = true;
    part.loopEnd = `${thought.meta.loop_bars}:0:0`;

    this.queueSwap(nodeId, part);
  }

  queueSwap(nodeId, nextPart) {
    const nodeState = this.nodes.get(nodeId);
    nodeState.nextPart = nextPart;

    const swapTime = Tone.Transport.nextSubdivision("1m");

    if (nodeState.swapEventId !== null) {
      Tone.Transport.clear(nodeState.swapEventId);
    }

    nodeState.swapEventId = Tone.Transport.scheduleOnce(() => {
      if (nodeState.activePart) {
        nodeState.activePart.stop();
        nodeState.activePart.dispose();
      }
      nodeState.activePart = nodeState.nextPart;
      nodeState.nextPart = null;
      nodeState.activePart.start(0);
      this.runtimeStore.setNodeState(nodeId, "active", "swap complete");
    }, swapTime);

    this.runtimeStore.setNodeState(nodeId, "scheduled", `swap at ${swapTime}`);

    if (Tone.Transport.state !== "started") {
      Tone.start();
      Tone.Transport.start();
    }
  }

  queueStop(nodeId) {
    this.ensureNode(nodeId);
    const nodeState = this.nodes.get(nodeId);

    const swapTime = Tone.Transport.nextSubdivision("1m");
    if (nodeState.swapEventId !== null) {
      Tone.Transport.clear(nodeState.swapEventId);
    }

    nodeState.swapEventId = Tone.Transport.scheduleOnce(() => {
      if (nodeState.activePart) {
        nodeState.activePart.stop();
        nodeState.activePart.dispose();
        nodeState.activePart = null;
      }
      this.runtimeStore.setNodeState(nodeId, "muted", "stop scheduled");
    }, swapTime);

    if (Tone.Transport.state !== "started") {
      Tone.start();
      Tone.Transport.start();
    }
  }
}
