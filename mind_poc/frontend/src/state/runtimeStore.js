export class RuntimeStore {
  constructor() {
    this.nodes = new Map();
  }

  initNode(nodeId) {
    if (!this.nodes.has(nodeId)) {
      this.nodes.set(nodeId, { state: "idle", detail: null });
      this.logState(nodeId, "idle");
    }
  }

  setNodeState(nodeId, state, detail = null) {
    this.initNode(nodeId);
    const node = this.nodes.get(nodeId);
    node.state = state;
    node.detail = detail;
    this.logState(nodeId, state, detail);
  }

  getNodeState(nodeId) {
    return this.nodes.get(nodeId) ?? { state: "unknown", detail: null };
  }

  logState(nodeId, state, detail) {
    const message = detail ? `${state} (${detail})` : state;
    console.info(`[Node:${nodeId}] ${message}`);
  }
}
