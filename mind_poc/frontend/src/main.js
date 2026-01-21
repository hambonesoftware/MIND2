import "litegraph.js/css/litegraph.css";
import { LiteGraph, LGraph, LGraphCanvas } from "litegraph.js";
import { ApiClient } from "./api/client.js";
import { ToneScheduler } from "./audio/toneScheduler.js";
import { RuntimeStore } from "./state/runtimeStore.js";
import { registerNodes } from "./graph/litegraphNodes.js";

const canvasElement = document.getElementById("graph-canvas");

const graph = new LGraph();
const canvas = new LGraphCanvas(canvasElement, graph);

const runtimeStore = new RuntimeStore();
const scheduler = new ToneScheduler({ runtimeStore });
const apiClient = new ApiClient({ baseUrl: "http://localhost:8000" });

async function init() {
  let profiles = [];

  try {
    const response = await apiClient.fetchProfiles();
    profiles = response.profiles ?? [];
  } catch (error) {
    console.warn("Failed to fetch profiles; using fallback", error);
    profiles = [
      { id: "wide_acoustic" },
      { id: "percussive_fingerstyle" },
      { id: "dark_pulse_synth" }
    ];
  }

  registerNodes({ LiteGraph, apiClient, scheduler, runtimeStore, profiles });

  const thoughtNode = LiteGraph.createNode("mind/MusicalThought");
  thoughtNode.pos = [50, 50];
  graph.add(thoughtNode);

  const gateNode = LiteGraph.createNode("mind/TheoryGate");
  gateNode.pos = [450, 80];
  graph.add(gateNode);

  canvas.resize();
  graph.start();
}

init();
