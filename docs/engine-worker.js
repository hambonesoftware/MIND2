// MIND2's original Python composer runs entirely inside a browser Web Worker.
// No user composition data is uploaded to a server.
import { loadPyodide } from "https://cdn.jsdelivr.net/pyodide/v0.27.7/full/pyodide.mjs";

const status = (message) => self.postMessage({ type: "status", message });

const ready = (async () => {
  status("Loading Python runtime…");
  const python = await loadPyodide({
    indexURL: "https://cdn.jsdelivr.net/pyodide/v0.27.7/full/",
  });

  status("Installing MIDI tools…");
  await python.loadPackage("micropip");
  await python.runPythonAsync('import micropip; await micropip.install("mido==1.3.3")');

  status("Loading the MIND2 engine…");
  const response = await fetch("./engine.zip");
  if (!response.ok) throw new Error(`MIND2 engine package unavailable (${response.status})`);
  python.unpackArchive(await response.arrayBuffer(), "zip");
  await python.runPythonAsync("import engine_bridge");

  self.postMessage({ type: "ready" });
  return python;
})();

ready.catch((error) => self.postMessage({ type: "error", message: String(error) }));

self.addEventListener("message", async (event) => {
  if (event.data?.type !== "generate") return;
  const { id, controls } = event.data;
  try {
    const python = await ready;
    status("Composing melody, harmony, bass and drums…");
    python.globals.set("MIND_INPUT_JSON", JSON.stringify(controls));
    const result = await python.runPythonAsync("engine_bridge.generate(MIND_INPUT_JSON)");
    python.globals.delete("MIND_INPUT_JSON");
    self.postMessage({ type: "result", id, composition: JSON.parse(result) });
  } catch (error) {
    self.postMessage({ type: "error", id, message: String(error) });
  }
});
