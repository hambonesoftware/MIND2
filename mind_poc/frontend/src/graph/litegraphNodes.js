import { validateThought } from "../validate/thoughtSchema.js";

function createDebounce(delayMs, fn) {
  let handle = null;
  return (...args) => {
    if (handle) {
      clearTimeout(handle);
    }
    handle = setTimeout(() => {
      fn(...args);
    }, delayMs);
  };
}

export function registerNodes({ LiteGraph, apiClient, scheduler, runtimeStore, profiles }) {
  function MusicalThoughtNode() {
    this.addOutput("Stream_Data", "thought");
    this.properties = {
      node_id: `node_${Math.floor(Math.random() * 10000)}`,
      intent_text: "[0 7 12]",
      style_profile: profiles[0]?.id ?? "wide_acoustic"
    };

    this.size = [320, 200];
    this.status = "idle";
    this.error = null;

    this.textWidget = this.addWidget("text", "DSL", this.properties.intent_text, (value) => {
      this.properties.intent_text = value;
      this.requestGenerate();
    });

    this.profileWidget = this.addWidget(
      "combo",
      "Profile",
      this.properties.style_profile,
      (value) => {
        this.properties.style_profile = value;
        this.requestGenerate();
      },
      {
        values: profiles.map((profile) => profile.id)
      }
    );

    this.requestGenerate = createDebounce(500, () => {
      this.generateThought();
    });
  }

  MusicalThoughtNode.title = "MusicalThought";
  MusicalThoughtNode.desc = "Generate a Thought from DSL";

  MusicalThoughtNode.prototype.onAdded = function onAdded() {
    runtimeStore.initNode(this.properties.node_id);
    this.requestGenerate();
  };

  MusicalThoughtNode.prototype.onDrawForeground = function onDrawForeground(ctx) {
    ctx.save();
    ctx.fillStyle = this.error ? "#ff6b6b" : "#22c55e";
    ctx.fillRect(10, this.size[1] - 30, 10, 10);
    ctx.fillStyle = "#111";
    ctx.font = "12px sans-serif";
    ctx.fillText(this.error ? "error" : this.status, 30, this.size[1] - 20);
    ctx.restore();
  };

  MusicalThoughtNode.prototype.setStatus = function setStatus(status, error = null) {
    this.status = status;
    this.error = error;
    this.setDirtyCanvas(true, true);
  };

  MusicalThoughtNode.prototype.generateThought = async function generateThought() {
    const nodeId = this.properties.node_id;

    if (this.abortController) {
      this.abortController.abort();
    }

    this.abortController = new AbortController();
    this.setStatus("pending");
    runtimeStore.setNodeState(nodeId, "pending");

    try {
      const payload = {
        schema_version: "thought.v0",
        node_id: nodeId,
        style_profile: this.properties.style_profile,
        intent_text: this.properties.intent_text,
        context: {
          tempo: 120,
          time_signature: "4/4",
          anchor_midi: 60,
          role: "lead"
        }
      };

      const thought = await apiClient.generateThought(payload, this.abortController.signal);
      const validation = validateThought(thought);
      if (!validation.ok) {
        this.setStatus("error", validation.error);
        runtimeStore.setNodeState(nodeId, "error", validation.error);
        return;
      }

      scheduler.scheduleThought(nodeId, thought);
      this.setStatus("scheduled");
      this.setOutputData(0, thought);
    } catch (error) {
      const message = error?.error?.message ?? "Backend error";
      this.setStatus("error", message);
      runtimeStore.setNodeState(nodeId, "error", message);
    }
  };

  function TheoryGateNode() {
    this.addInput("Stream_A", "thought");
    this.addInput("Stream_B", "thought");
    this.addOutput("Resolved_Stream", "thought");
    this.properties = {
      style_profile: profiles[0]?.id ?? "wide_acoustic"
    };
    this.size = [260, 120];

    this.profileWidget = this.addWidget(
      "combo",
      "Profile",
      this.properties.style_profile,
      (value) => {
        this.properties.style_profile = value;
        this.requestResolve();
      },
      {
        values: profiles.map((profile) => profile.id)
      }
    );

    this.requestResolve = createDebounce(300, () => {
      this.resolve();
    });
  }

  TheoryGateNode.title = "TheoryGate";
  TheoryGateNode.desc = "Resolve clashes between inputs";

  TheoryGateNode.prototype.onConnectionsChange = function onConnectionsChange() {
    this.requestResolve();
  };

  TheoryGateNode.prototype.resolve = async function resolve() {
    const inputs = [this.getInputData(0), this.getInputData(1)].filter(Boolean);
    if (inputs.length === 0) {
      return;
    }

    if (this.abortController) {
      this.abortController.abort();
    }

    this.abortController = new AbortController();

    const payload = {
      schema_version: "resolve.v0",
      style_profile: this.properties.style_profile,
      inputs: inputs.map((thought, index) => ({
        node_id: thought.node_id,
        role: index === 0 ? "bass" : "lead",
        thought
      }))
    };

    try {
      const response = await apiClient.resolveConflict(payload, this.abortController.signal);
      const resolved = response.resolved ?? [];
      if (resolved.length > 0) {
        this.setOutputData(0, resolved[0].thought);
      }
    } catch (error) {
      console.error("TheoryGate resolve error", error);
    }
  };

  LiteGraph.registerNodeType("mind/MusicalThought", MusicalThoughtNode);
  LiteGraph.registerNodeType("mind/TheoryGate", TheoryGateNode);
}
