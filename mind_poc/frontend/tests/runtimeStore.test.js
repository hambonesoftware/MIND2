import assert from "node:assert/strict";
import { RuntimeStore } from "../src/state/runtimeStore.js";

const store = new RuntimeStore();
store.initNode("node_1");

const initial = store.getNodeState("node_1");
assert.equal(initial.state, "idle");

store.setNodeState("node_1", "pending", "waiting");
const pending = store.getNodeState("node_1");
assert.equal(pending.state, "pending");
assert.equal(pending.detail, "waiting");

console.log("runtimeStore tests passed");
