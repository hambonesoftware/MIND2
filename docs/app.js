const $ = (id) => document.getElementById(id);
const TRACK_NAMES = ["melody", "harmony", "bass", "drums"];
const COLORS = { melody: "#ffa778", harmony: "#c7a4d9", bass: "#a3dbb4", drums: "#f0d38e" };
const SLIDERS = ["brightness", "energy", "intensity", "complexity", "tightness"];
const LABELS = { melody: "Melody", harmony: "Harmony", bass: "Bass", drums: "Drums" };

let composition = null;
let workerReady = false;
let busy = false;
let requestId = 0;
const muted = new Set();

const worker = new Worker(new URL("./engine-worker.js", import.meta.url), { type: "module" });

function setStatus(message, mode = "loading") {
  $("engineStatus").textContent = message;
  $("engineLight").className = `status-dot ${mode === "ready" ? "ready" : mode === "error" ? "error" : ""}`;
}

function setBusy(value) {
  busy = value;
  $("composeButton").disabled = !workerReady || busy;
  $("composeButton").innerHTML = busy
    ? '<span aria-hidden="true">◌</span> Composing… <span aria-hidden="true">✦</span>'
    : '<span aria-hidden="true">✦</span> Compose an idea <span aria-hidden="true">↗</span>';
}

function readControls() {
  const data = {
    style: $("style").value,
    key: $("key").value,
    mode: $("mode").value,
    bars: Number($("bars").value),
    bpm: Number($("bpm").value),
    seed: Number($("seed").value),
  };
  for (const id of SLIDERS) data[id] = Number($(id).value) / 100;
  if (!Number.isInteger(data.bpm) || data.bpm < 60 || data.bpm > 200) throw new Error("Tempo must be 60–200 BPM.");
  if (!Number.isInteger(data.seed) || data.seed < 0 || data.seed > 2147483647) throw new Error("The idea seed must be a positive integer below 2147483648.");
  return data;
}

function markModified() {
  if (composition && !busy) {
    $("compositionBadge").textContent = "CHANGES NOT COMPOSED";
    $("transportState").textContent = "Adjustments waiting — compose to hear";
  }
}

function restoreControls() {
  try {
    const saved = JSON.parse(localStorage.getItem("mind2-riverbed-controls") || "null");
    if (!saved) return;
    const allowed = ["style", "key", "mode", "bars", "bpm", "seed"];
    for (const key of allowed) if (saved[key] != null && $(key)) $(key).value = String(saved[key]);
    for (const key of SLIDERS) if (Number.isFinite(saved[key])) $(key).value = String(Math.round(saved[key] * 100));
  } catch { /* Some browsers disable storage. The studio still works. */ }
}

function rememberControls(controls) {
  try { localStorage.setItem("mind2-riverbed-controls", JSON.stringify(controls)); }
  catch { /* Storage is optional. */ }
}

function formatTime(seconds) {
  const total = Math.max(0, Math.floor(seconds || 0));
  return `${Math.floor(total / 60)}:${String(total % 60).padStart(2, "0")}`;
}

function titleFor(song) {
  const style = $("style").selectedOptions[0]?.textContent || "Music";
  return `${style} · ${song.meta.key} ${song.meta.mode}`;
}

function compose() {
  if (!workerReady || busy) return;
  let controls;
  try { controls = readControls(); }
  catch (error) { setStatus(error.message, "error"); return; }
  audio.stop();
  rememberControls(controls);
  setBusy(true);
  setStatus("Composing your Thought…");
  worker.postMessage({ type: "generate", id: ++requestId, controls });
}

worker.addEventListener("message", (event) => {
  const data = event.data;
  if (data.type === "status") {
    setStatus(data.message);
  } else if (data.type === "ready") {
    workerReady = true;
    setBusy(false);
    setStatus("Musical engine ready", "ready");
    compose();
  } else if (data.type === "result" && data.id === requestId) {
    composition = data.composition;
    muted.clear();
    setBusy(false);
    setStatus("Musical engine ready", "ready");
    displayComposition(composition);
    $("playButton").disabled = false;
    $("stopButton").disabled = false;
    $("exportButton").disabled = false;
  } else if (data.type === "error") {
    if (data.id != null && data.id !== requestId) return;
    setBusy(false);
    setStatus(`Engine error — ${data.message}`, "error");
    $("transportState").textContent = "Could not compose. See engine status above.";
  }
});

worker.addEventListener("error", (event) => {
  setBusy(false);
  setStatus(`Could not load the music engine: ${event.message || "network error"}`, "error");
});

function displayComposition(song) {
  const { meta } = song;
  const duration = meta.bars * 4 * 60 / meta.bpm;
  const name = titleFor(song);
  $("songTitle").textContent = name;
  $("songSubtitle").textContent = `${meta.bars} measures · ${meta.bpm} BPM · Seed ${meta.seed}`;
  $("songDuration").textContent = formatTime(duration);
  $("transportTitle").textContent = name;
  $("transportState").textContent = "Ready to play";
  $("timeTotal").textContent = formatTime(duration);
  $("timeElapsed").textContent = "0:00";
  $("progressFill").style.width = "0%";
  $("compositionBadge").textContent = "COMPOSED · READY";
  $("timelineMeta").textContent = `${meta.bars} BARS · 4/4`;
  $("emptyState").hidden = true;
  $("songContent").hidden = false;
  $("playhead").style.display = "none";
  drawSections(song);
  drawBarRuler(meta.bars);
  drawTracks(song);
  $("chordCount").textContent = String(song.chords.length);
  $("melodyCount").textContent = String(song.analysis.noteCounts.melody);
  $("sectionCount").textContent = String(song.sections.length);
  $("contourType").textContent = song.analysis.melody.contour || "—";
}

function drawSections(song) {
  const strip = $("sectionStrip");
  strip.replaceChildren();
  for (const section of song.sections) {
    const element = document.createElement("div");
    element.className = `section section-${section.name}`;
    element.style.flexGrow = String(section.end - section.start);
    element.style.flexBasis = "0";
    element.textContent = section.name.toUpperCase();
    element.title = `${section.name}, bars ${section.start + 1}–${section.end}`;
    strip.appendChild(element);
  }
}

function drawBarRuler(bars) {
  const ruler = $("barRuler");
  ruler.replaceChildren();
  for (let bar = 0; bar < bars; bar++) {
    const tick = document.createElement("span");
    if (bar % (bars === 32 ? 4 : 2) === 0) tick.textContent = String(bar + 1);
    ruler.appendChild(tick);
  }
}

function drawTracks(song) {
  const container = $("tracks");
  container.replaceChildren();
  const totalBeats = song.meta.bars * 4;
  for (const name of TRACK_NAMES) {
    const notes = song.parts[name] || [];
    const row = document.createElement("div");
    row.className = `track track-${name}`;
    const toggle = document.createElement("button");
    toggle.className = "track-label";
    toggle.type = "button";
    toggle.title = `Mute or unmute ${name}`;
    toggle.setAttribute("aria-label", `Mute ${name}`);
    const color = document.createElement("span");
    color.className = "track-color";
    const label = document.createElement("span");
    label.textContent = LABELS[name];
    toggle.append(color, label);
    toggle.addEventListener("click", () => {
      if (muted.has(name)) muted.delete(name); else muted.add(name);
      toggle.classList.toggle("muted", muted.has(name));
      toggle.setAttribute("aria-label", `${muted.has(name) ? "Unmute" : "Mute"} ${name}`);
    });
    const lane = document.createElement("div");
    lane.className = "note-lane";
    lane.setAttribute("aria-label", `${notes.length} ${name} notes`);
    const pitches = notes.map((note) => note.pitch);
    const minPitch = name === "drums" ? 30 : Math.min(...pitches, 40);
    const maxPitch = name === "drums" ? 48 : Math.max(...pitches, 80);
    const span = Math.max(1, maxPitch - minPitch);
    const notesFragment = document.createDocumentFragment();
    for (const note of notes) {
      const block = document.createElement("div");
      block.className = "note-block";
      block.style.left = `${Math.max(0, note.beat / totalBeats * 100)}%`;
      block.style.width = `${Math.max(.18, Math.min(100 - note.beat / totalBeats * 100, note.duration / totalBeats * 100))}%`;
      block.style.bottom = `${7 + Math.min(1, Math.max(0, (note.pitch - minPitch) / span)) * 73}%`;
      block.title = `${LABELS[name]} · MIDI ${note.pitch} · beat ${note.beat + 1}`;
      notesFragment.appendChild(block);
    }
    lane.appendChild(notesFragment);
    row.append(toggle, lane);
    container.appendChild(row);
  }
}

class BrowserSynth {
  constructor(onProgress, onStop) {
    this.onProgress = onProgress;
    this.onStop = onStop;
    this.context = null;
    this.master = null;
    this.active = new Set();
    this.interval = null;
    this.frame = null;
    this.playing = false;
    this.events = [];
    this.next = 0;
    this.base = 0;
    this.duration = 0;
    this.noiseBuffer = null;
  }

  async initialize() {
    if (this.context) return;
    const AudioContextCtor = window.AudioContext || window.webkitAudioContext;
    if (!AudioContextCtor) throw new Error("This browser does not support Web Audio.");
    this.context = new AudioContextCtor();
    const compressor = this.context.createDynamicsCompressor();
    compressor.threshold.value = -18;
    compressor.ratio.value = 3;
    compressor.attack.value = .006;
    compressor.release.value = .18;
    this.master = this.context.createGain();
    this.master.gain.value = .62;
    this.master.connect(compressor);
    compressor.connect(this.context.destination);
    this.noiseBuffer = this.context.createBuffer(1, this.context.sampleRate * .6, this.context.sampleRate);
    const data = this.noiseBuffer.getChannelData(0);
    for (let i = 0; i < data.length; i++) data[i] = Math.random() * 2 - 1;
  }

  async play(song) {
    this.stop(false);
    await this.initialize();
    await this.context.resume();
    const secondsPerBeat = 60 / song.meta.bpm;
    this.duration = song.meta.bars * 4 * secondsPerBeat;
    this.events = TRACK_NAMES.flatMap((part) => (song.parts[part] || []).map((note) => ({
      ...note, part,
      second: note.beat * secondsPerBeat,
      seconds: note.duration * secondsPerBeat,
    }))).sort((a, b) => a.second - b.second);
    this.next = 0;
    this.base = this.context.currentTime + .09;
    this.playing = true;
    this.interval = setInterval(() => this.schedule(), 65);
    this.schedule();
    const frame = () => {
      if (!this.playing) return;
      const time = Math.max(0, this.context.currentTime - this.base);
      this.onProgress(Math.min(time, this.duration), this.duration);
      if (time > this.duration + .25) { this.stop(); return; }
      this.frame = requestAnimationFrame(frame);
    };
    this.frame = requestAnimationFrame(frame);
  }

  schedule() {
    if (!this.playing) return;
    const horizon = this.context.currentTime + .38;
    while (this.next < this.events.length) {
      const event = this.events[this.next];
      const when = this.base + event.second;
      if (when > horizon) break;
      this.next++;
      if (muted.has(event.part) || when < this.context.currentTime - .08) continue;
      if (event.part === "drums") this.drum(event, Math.max(when, this.context.currentTime));
      else this.tone(event, Math.max(when, this.context.currentTime));
    }
  }

  remember(source) {
    this.active.add(source);
    source.addEventListener("ended", () => this.active.delete(source), { once: true });
  }

  tone(event, when) {
    const ctx = this.context;
    const frequency = 440 * Math.pow(2, (event.pitch - 69) / 12);
    const gain = ctx.createGain();
    const velocity = event.velocity / 127;
    const duration = Math.max(.07, event.seconds);
    const settings = {
      melody: { type: "triangle", attack: .018, release: .22, volume: .24 },
      harmony: { type: "sine", attack: .11, release: .26, volume: .16 },
      bass: { type: "sine", attack: .012, release: .14, volume: .34 },
    }[event.part];
    const attack = Math.min(settings.attack, duration * .45);
    const heldEnd = when + Math.max(attack, duration - Math.min(settings.release, duration * .45));
    gain.gain.setValueAtTime(.0001, when);
    gain.gain.linearRampToValueAtTime(settings.volume * velocity, when + attack);
    gain.gain.setTargetAtTime(.0001, heldEnd, Math.max(.025, settings.release / 4));
    gain.connect(this.master);
    const oscillator = ctx.createOscillator();
    oscillator.type = settings.type;
    oscillator.frequency.setValueAtTime(frequency, when);
    oscillator.connect(gain);
    oscillator.start(when);
    oscillator.stop(when + duration + settings.release * 1.5);
    this.remember(oscillator);
    if (event.part === "melody") {
      const overtone = ctx.createOscillator();
      const overtoneGain = ctx.createGain();
      overtone.type = "sine";
      overtone.frequency.value = frequency * 2;
      overtoneGain.gain.value = .12;
      overtone.connect(overtoneGain);
      overtoneGain.connect(gain);
      overtone.start(when);
      overtone.stop(when + duration + settings.release * 1.5);
      this.remember(overtone);
    }
  }

  drum(event, when) {
    const ctx = this.context;
    const pitch = event.pitch;
    const level = Math.min(1, event.velocity / 127);
    if (pitch === 35 || pitch === 36) {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = "sine";
      osc.frequency.setValueAtTime(140, when);
      osc.frequency.exponentialRampToValueAtTime(46, when + .12);
      gain.gain.setValueAtTime(.4 * level, when);
      gain.gain.exponentialRampToValueAtTime(.0001, when + .26);
      osc.connect(gain); gain.connect(this.master);
      osc.start(when); osc.stop(when + .27); this.remember(osc);
    } else {
      const source = ctx.createBufferSource();
      source.buffer = this.noiseBuffer;
      const filter = ctx.createBiquadFilter();
      const gain = ctx.createGain();
      const snare = pitch === 38 || pitch === 40;
      filter.type = snare ? "bandpass" : "highpass";
      filter.frequency.value = snare ? 1800 : 6500;
      filter.Q.value = snare ? .8 : .5;
      const duration = snare ? .16 : .065;
      gain.gain.setValueAtTime((snare ? .22 : .09) * level, when);
      gain.gain.exponentialRampToValueAtTime(.0001, when + duration);
      source.connect(filter); filter.connect(gain); gain.connect(this.master);
      source.start(when); source.stop(when + duration + .005); this.remember(source);
    }
  }

  stop(notify = true) {
    this.playing = false;
    if (this.interval) clearInterval(this.interval);
    if (this.frame) cancelAnimationFrame(this.frame);
    this.interval = null;
    this.frame = null;
    if (this.context) {
      for (const node of this.active) {
        try { node.stop(this.context.currentTime); } catch { /* Already stopped. */ }
      }
    }
    this.active.clear();
    if (notify) this.onStop();
  }
}

const audio = new BrowserSynth(
  (time, total) => {
    $("timeElapsed").textContent = formatTime(time);
    $("progressFill").style.width = `${Math.min(100, time / total * 100)}%`;
    const lane = document.querySelector(".note-lane");
    if (lane) {
      $("playhead").style.display = "block";
      $("playhead").style.left = `${lane.offsetLeft + lane.clientWidth * Math.min(1, time / total)}px`;
    }
  },
  () => {
    $("timeElapsed").textContent = "0:00";
    $("progressFill").style.width = "0%";
    $("playhead").style.display = "none";
    $("playButton").textContent = "▶";
    $("playButton").setAttribute("aria-label", "Play");
    $("transportState").textContent = composition ? "Ready to play" : "Waiting for an idea";
  },
);

function downloadMidi() {
  if (!composition) return;
  const binary = atob(composition.midiBase64);
  const bytes = Uint8Array.from(binary, (character) => character.charCodeAt(0));
  const url = URL.createObjectURL(new Blob([bytes], { type: "audio/midi" }));
  const a = document.createElement("a");
  a.href = url;
  a.download = `mind2-${composition.meta.style}-${composition.meta.seed}.mid`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 10000);
}

restoreControls();
for (const id of SLIDERS) {
  const input = $(id);
  const update = () => { $(`${id}Value`).textContent = input.value; markModified(); };
  input.addEventListener("input", update);
  update();
}
for (const id of ["style", "key", "mode", "bars", "bpm", "seed"]) $(id).addEventListener("change", markModified);
$("composeForm").addEventListener("submit", (event) => { event.preventDefault(); compose(); });
$("newSeedButton").addEventListener("click", () => {
  const array = new Uint32Array(1);
  crypto.getRandomValues(array);
  $("seed").value = String(array[0] & 0x7fffffff);
  markModified();
  compose();
});
$("playButton").addEventListener("click", async () => {
  if (!composition) return;
  if (audio.playing) { audio.stop(); return; }
  try {
    await audio.play(composition);
    $("playButton").textContent = "Ⅱ";
    $("playButton").setAttribute("aria-label", "Stop playback");
    $("transportState").textContent = "Playing original MIND2 arrangement";
  } catch (error) {
    setStatus(`Audio unavailable: ${error.message}`, "error");
  }
});
$("stopButton").addEventListener("click", () => audio.stop());
$("exportButton").addEventListener("click", downloadMidi);
document.addEventListener("visibilitychange", () => { if (document.hidden && audio.playing) audio.stop(); });
