const state = {
  module: null,
  run: null,
  currentStep: "intake",
  attempts: {},
  selectedCounts: {},
  quizIndex: 0,
  quizItems: [],
  studyIndex: 0,
  stream: null,
  autoDetectInterval: null,
  detectionInFlight: false,
  lastDetection: null,
  stableFrameCount: 0,
  stableCounts: {},
  audioCtx: null,
  overlayBoxes: {},
};

const steps = [
  ["intake", "Intake"],
  ["pre", "Pre-test"],
  ["study", "Study cards"],
  ["quiz", "Quiz"],
  ["practice", "Practice sort"],
  ["post", "Post-test"],
  ["summary", "Summary"],
];

const app = document.querySelector("#app");
const modeStatus = document.querySelector("#modeStatus");
const stepsNav = document.querySelector("#steps");

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  if (!response.ok) throw new Error(await response.text());
  return response.json();
}

function setStep(step) {
  if (state.currentStep !== step && ["pre", "practice", "post"].includes(state.currentStep)) {
    cleanupCamera();
  }
  state.currentStep = step;
  modeStatus.textContent = steps.find(([id]) => id === step)?.[1] || step;
  renderSteps();
  render();
}

function normalizeAnswer(str) {
  return str
    .toLowerCase()
    .replace(/w\//g, "with")
    .replace(/[-/.,#]/g, "")
    .replace(/\s+/g, "")
    .trim();
}

function levenshteinDistance(a, b) {
  const matrix = [];
  for (let i = 0; i <= b.length; i += 1) matrix[i] = [i];
  for (let j = 0; j <= a.length; j += 1) matrix[0][j] = j;
  for (let i = 1; i <= b.length; i += 1) {
    for (let j = 1; j <= a.length; j += 1) {
      matrix[i][j] = b[i - 1] === a[j - 1]
        ? matrix[i - 1][j - 1]
        : Math.min(matrix[i - 1][j - 1] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j] + 1);
    }
  }
  return matrix[b.length][a.length];
}

function similarityScore(a, b) {
  const maxLen = Math.max(a.length, b.length);
  if (maxLen === 0) return 1;
  const distance = levenshteinDistance(a, b);
  return (maxLen - distance) / maxLen;
}

function getValidAnswers(instrument) {
  const answers = new Set();
  answers.add(instrument.display_name);
  for (const alias of instrument.aliases || []) {
    answers.add(alias);
  }
  return Array.from(answers);
}

function isAnswerCorrect(instrument, promptAnswer, userAnswer) {
  const normalizedUser = normalizeAnswer(userAnswer);
  if (normalizedUser.length === 0) return false;

  const allAnswers = [promptAnswer, ...getValidAnswers(instrument)];

  for (const expected of allAnswers) {
    const normalizedExpected = normalizeAnswer(expected);
    if (normalizedExpected.length === 0) continue;

    if (normalizedUser === normalizedExpected) return true;
    if (normalizedExpected.includes(normalizedUser)) return true;
    if (normalizedUser.includes(normalizedExpected)) return true;

    const similarity = similarityScore(normalizedUser, normalizedExpected);
    if (similarity >= 0.7) return true;
  }

  return false;
}

function initAudio() {
  if (!state.audioCtx) {
    state.audioCtx = new AudioContext();
  }
  if (state.audioCtx.state === "suspended") {
    state.audioCtx.resume();
  }
}

function playBeep() {
  if (!state.audioCtx) return;
  if (state.audioCtx.state === "suspended") {
    state.audioCtx.resume();
  }
  const oscillator = state.audioCtx.createOscillator();
  const gain = state.audioCtx.createGain();
  oscillator.frequency.value = 440;
  oscillator.type = "sine";
  gain.gain.value = 0.5;
  oscillator.connect(gain);
  gain.connect(state.audioCtx.destination);
  oscillator.start();
  oscillator.stop(state.audioCtx.currentTime + 0.1);
}

function updateFullscreenList(counts) {
  const container = document.querySelector("#fullscreenListContent");
  if (!container) return;

  const sortedIds = Object.keys(counts).sort((a, b) => {
    const nameA = state.module.instruments[a]?.display_name || a;
    const nameB = state.module.instruments[b]?.display_name || b;
    return nameA.localeCompare(nameB);
  });

  if (sortedIds.length === 0) {
    container.innerHTML = "<p class='muted'>No cards detected</p>";
    return;
  }

  container.innerHTML = sortedIds.map((id) => {
    const instrument = state.module.instruments[id];
    const name = instrument ? instrument.display_name : id;
    const count = counts[id];
    return `<div class="fullscreen-list-item"><span>${name}</span><span class="fullscreen-list-count">${count}</span></div>`;
  }).join("");
}

function drawOverlay(detections) {
  const video = document.querySelector("#video");
  const svg = document.querySelector("#overlaySvg");
  if (!video || !svg || !video.videoWidth) {
    console.log("drawOverlay early return:", { video: !!video, svg: !!svg, videoWidth: video?.videoWidth });
    return;
  }

  const container = video.parentElement;
  const containerWidth = container.clientWidth;
  const containerHeight = container.clientHeight;
  const videoWidth = video.videoWidth;
  const videoHeight = video.videoHeight;
  console.log("drawOverlay", { detections: detections.length, containerWidth, containerHeight, videoWidth, videoHeight });

  // Calculate object-fit: cover scaling
  const scale = Math.max(containerWidth / videoWidth, containerHeight / videoHeight);
  const displayedWidth = videoWidth * scale;
  const displayedHeight = videoHeight * scale;
  const offsetX = (containerWidth - displayedWidth) / 2;
  const offsetY = (containerHeight - displayedHeight) / 2;

  svg.setAttribute("viewBox", `0 0 ${containerWidth} ${containerHeight}`);
  svg.removeAttribute("preserveAspectRatio");

  const now = Date.now();
  const currentIds = new Set();
  const previousIds = new Set(Object.keys(state.overlayBoxes));

  const counts = {};
  for (const detection of detections) {
    if (!detection.instrument_id) {
      console.log("Skipped detection (no instrument_id):", detection);
      continue;
    }
    counts[detection.instrument_id] = (counts[detection.instrument_id] || 0) + 1;
  }

  for (const detection of detections) {
    if (!detection.instrument_id || !detection.corners) continue;
    const id = detection.instrument_id;
    currentIds.add(id);
    state.overlayBoxes[id] = {
      corners: detection.corners,
      lastSeen: now,
      count: counts[id] || 1,
      name: state.module.instruments[id]?.display_name || "Unknown",
    };
  }

  svg.innerHTML = "";

  const BOX_TTL = 1500;
  console.log("overlayBoxes:", Object.keys(state.overlayBoxes), "currentIds:", [...currentIds]);
  for (const [id, box] of Object.entries(state.overlayBoxes)) {
    if (now - box.lastSeen > BOX_TTL) {
      console.log("Expired box:", id);
      delete state.overlayBoxes[id];
      continue;
    }

    const corners = box.corners;
    const transformedCorners = corners.map(([x, y]) => [
      x * scale + offsetX,
      y * scale + offsetY,
    ]);
    const points = transformedCorners.map(([x, y]) => `${x},${y}`).join(" ");

    const polygon = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
    polygon.setAttribute("points", points);
    polygon.setAttribute("stroke", "#00ff00");
    polygon.setAttribute("stroke-width", "3");
    polygon.setAttribute("fill", "none");
    svg.appendChild(polygon);

    const label = `${box.name} (${box.count})`;
    const x = transformedCorners[0][0];
    const y = transformedCorners[0][1] - 8;

    const textBg = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    textBg.setAttribute("x", x);
    textBg.setAttribute("y", y - 14);
    textBg.setAttribute("width", label.length * 8 + 8);
    textBg.setAttribute("height", 18);
    textBg.setAttribute("fill", "rgba(0,0,0,0.6)");
    svg.appendChild(textBg);

    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute("x", x + 4);
    text.setAttribute("y", y);
    text.setAttribute("fill", "#ffffff");
    text.setAttribute("font-size", "14");
    text.setAttribute("font-weight", "bold");
    text.setAttribute("font-family", "Inter, sans-serif");
    text.textContent = label;
    svg.appendChild(text);
  }

  updateFullscreenList(counts);

  const newlyAppeared = [...currentIds].filter((id) => !previousIds.has(id));
  if (newlyAppeared.length > 0) playBeep();
}

function startAutoDetection() {
  if (state.autoDetectInterval) return;
  state.autoDetectInterval = setInterval(() => {
    if (state.detectionInFlight) return;
    const video = document.querySelector("#video");
    if (!video || !video.srcObject) return;
    detectCards(true);
  }, 1000);
}

function stopAutoDetection() {
  if (state.autoDetectInterval) {
    clearInterval(state.autoDetectInterval);
    state.autoDetectInterval = null;
  }
  state.detectionInFlight = false;
  state.lastDetection = null;
  state.stableFrameCount = 0;
  state.overlayBoxes = {};
}

function cleanupCamera() {
  stopAutoDetection();
  const svg = document.querySelector("#overlaySvg");
  if (svg) {
    svg.innerHTML = "";
    svg.style.display = "";
  }
  state.overlayBoxes = {};
  if (state.stream) {
    state.stream.getTracks().forEach((track) => track.stop());
    state.stream = null;
  }
  const video = document.querySelector("#video");
  if (video) {
    video.srcObject = null;
    video.style.display = "";
  }
  const canvas = document.querySelector("#snapshotCanvas");
  if (canvas) {
    canvas.classList.remove("snapshot-visible");
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  }
}

function handleVisibilityChange() {
  if (document.hidden) {
    stopAutoDetection();
  } else if (state.stream && state.stream.active && state.currentStep === "practice") {
    startAutoDetection();
  }
}

document.addEventListener("visibilitychange", handleVisibilityChange);

function drawSnapshot(canvas, detections) {
  const ctx = canvas.getContext("2d");
  for (const detection of detections) {
    if (!detection.instrument_id || !detection.corners) continue;
    const corners = detection.corners;
    const name = state.module.instruments[detection.instrument_id]?.display_name || "Unknown";
    ctx.beginPath();
    ctx.moveTo(corners[0][0], corners[0][1]);
    for (let i = 1; i < corners.length; i += 1) {
      ctx.lineTo(corners[i][0], corners[i][1]);
    }
    ctx.closePath();
    ctx.strokeStyle = "#00ff00";
    ctx.lineWidth = 3;
    ctx.stroke();
    const x = corners[0][0];
    const y = corners[0][1] - 8;
    ctx.font = "bold 14px Inter, sans-serif";
    const textWidth = ctx.measureText(name).width;
    ctx.fillStyle = "rgba(0,0,0,0.6)";
    ctx.fillRect(x, y - 18, textWidth + 8, 20);
    ctx.fillStyle = "#ffffff";
    ctx.fillText(name, x + 4, y);
  }
}

async function captureAndDetect() {
  const video = document.querySelector("#video");
  const canvas = document.querySelector("#snapshotCanvas");
  canvas.width = video.videoWidth || 1280;
  canvas.height = video.videoHeight || 720;
  canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);
  const image = canvas.toDataURL("image/png");
  const result = await api("/api/detect-cards", { method: "POST", body: JSON.stringify({ image }) });
  return result;
}

async function takeSnapshot() {
  const canvas = document.querySelector("#snapshotCanvas");
  const result = await captureAndDetect();
  drawSnapshot(canvas, result.detections);
  canvas.classList.add("snapshot-visible");
  const currentCounts = result.selected_counts || {};
  setManualCounts(currentCounts);
  return result;
}

function toggleFullscreen() {
  const panel = document.querySelector(".camera-panel");
  if (document.fullscreenElement) {
    document.exitFullscreen();
  } else {
    panel.requestFullscreen();
  }
}

document.addEventListener("fullscreenchange", () => {
  const btn = document.querySelector("#fullscreenBtn");
  const exitBtn = document.querySelector("#exitFullscreenBtn");
  if (btn) {
    btn.style.display = document.fullscreenElement ? "none" : "block";
  }
  if (exitBtn) {
    exitBtn.style.display = document.fullscreenElement ? "block" : "none";
  }
});

function setupResizableSplit() {
  const split = document.querySelector(".split");
  const divider = document.querySelector(".divider");
  if (!split || !divider) return;

  let isDragging = false;
  const minLeft = 300;
  const minRight = 280;

  const getContainerWidth = () => split.parentElement?.clientWidth || split.clientWidth;

  const setLeftWidth = (px) => {
    const containerWidth = getContainerWidth();
    const maxLeft = containerWidth - minRight - 4; // 4px divider
    const clamped = Math.max(minLeft, Math.min(px, maxLeft));
    split.style.gridTemplateColumns = `${clamped}px 4px 1fr`;
    return clamped;
  };

  divider.addEventListener("mousedown", (e) => {
    isDragging = true;
    divider.classList.add("dragging");
    e.preventDefault();
  });

  document.addEventListener("mousemove", (e) => {
    if (!isDragging) return;
    const rect = split.getBoundingClientRect();
    const relativeX = e.clientX - rect.left;
    setLeftWidth(relativeX);
  });

  document.addEventListener("mouseup", () => {
    if (!isDragging) return;
    isDragging = false;
    divider.classList.remove("dragging");
    const currentWidth = parseInt(split.style.gridTemplateColumns, 10);
    if (currentWidth) {
      localStorage.setItem("trayguard_split_width", `${currentWidth}px`);
    }
  });
}

function renderSteps() {
  const isCollapsed = stepsNav.classList.contains("collapsed");
  stepsNav.innerHTML = "";
  if (isCollapsed) {
    const restoreBtn = document.createElement("button");
    restoreBtn.className = "toggle-steps-restore";
    restoreBtn.textContent = "▶";
    restoreBtn.title = "Expand sidebar";
    restoreBtn.onclick = () => {
      stepsNav.classList.remove("collapsed");
      localStorage.setItem("trayguard_steps_collapsed", "false");
      renderSteps();
    };
    stepsNav.appendChild(restoreBtn);
    return;
  }
  const toggleBtn = document.createElement("button");
  toggleBtn.className = "toggle-steps";
  toggleBtn.textContent = "◀";
  toggleBtn.title = "Collapse sidebar";
  toggleBtn.onclick = () => {
    stepsNav.classList.add("collapsed");
    localStorage.setItem("trayguard_steps_collapsed", "true");
    renderSteps();
  };
  stepsNav.appendChild(toggleBtn);
  for (const [id, label] of steps) {
    const button = document.createElement("button");
    button.className = `step ${state.currentStep === id ? "active" : ""}`;
    button.textContent = label;
    button.disabled = !state.run && id !== "intake";
    button.onclick = () => setStep(id);
    stepsNav.appendChild(button);
  }
}

function instrumentsForTray() {
  const required = Object.keys(state.module.required_items);
  const distractors = state.module.distractor_item_ids;
  return [...required, ...distractors].map((id) => state.module.instruments[id]);
}

function variantByMode(mode) {
  return Object.values(state.module.assessment_variants).find((variant) => variant.mode === mode);
}

function seededRandom(seed) {
  let hash = 2166136261;
  for (let index = 0; index < seed.length; index += 1) {
    hash ^= seed.charCodeAt(index);
    hash = Math.imul(hash, 16777619);
  }
  return () => {
    hash += 0x6d2b79f5;
    let value = hash;
    value = Math.imul(value ^ (value >>> 15), value | 1);
    value ^= value + Math.imul(value ^ (value >>> 7), value | 61);
    return ((value ^ (value >>> 14)) >>> 0) / 4294967296;
  };
}

function shuffled(ids, seed) {
  const random = seededRandom(seed || "trayguard");
  const result = [...ids];
  for (let index = result.length - 1; index > 0; index -= 1) {
    const swapIndex = Math.floor(random() * (index + 1));
    [result[index], result[swapIndex]] = [result[swapIndex], result[index]];
  }
  return result;
}

function instrumentsForVariant(variantId) {
  const variant = state.module.assessment_variants[variantId];
  if (!variant) return instrumentsForTray();
  const ids = [...variant.required_item_ids, ...variant.distractor_item_ids];
  return shuffled(ids, variant.random_seed).map((id) => state.module.instruments[id]);
}

function selectedCountsFromInputs() {
  const counts = {};
  document.querySelectorAll("[data-instrument-id]").forEach((input) => {
    const value = Number.parseInt(input.value || "0", 10);
    if (value > 0) counts[input.dataset.instrumentId] = value;
  });
  return counts;
}

function setManualCounts(counts) {
  document.querySelectorAll("[data-instrument-id]").forEach((input) => {
    input.value = counts[input.dataset.instrumentId] || 0;
  });
}

function renderIntake() {
  app.innerHTML = `
    <section class="panel">
      <h2>Start learner run</h2>
      <p class="muted">Use an anonymous participant ID. The app stores a hash, not the raw value.</p>
      <label>Participant ID <input id="learnerId" autocomplete="off" value="demo"></label>
      <label>Participant group <input id="participantGroup" value="novice"></label>
      <label>Prior experience
        <select id="priorExperience">
          <option value="none">None</option>
          <option value="some_classroom">Some classroom exposure</option>
          <option value="hands_on">Hands-on instrument exposure</option>
        </select>
      </label>
      <div class="button-row"><button class="primary" id="startRun">Start pre-test</button></div>
    </section>
  `;
  document.querySelector("#startRun").onclick = async () => {
    const btn = document.querySelector("#startRun");
    btn.disabled = true;
    btn.textContent = "Starting...";
    try {
      state.run = await api("/api/runs", {
        method: "POST",
        body: JSON.stringify({
          learner_id: document.querySelector("#learnerId").value,
          participant_group: document.querySelector("#participantGroup").value,
          prior_experience_level: document.querySelector("#priorExperience").value,
        }),
      });
      setStep("pre");
    } catch (err) {
      app.innerHTML += `<div class="notice error">${err.message}</div>`;
      btn.disabled = false;
      btn.textContent = "Start pre-test";
    }
  };
}

function renderTraySort({ mode, variantId, title, copy, feedback }) {
  const startedAt = new Date();
  const template = document.querySelector("#tray-sort-template").content.cloneNode(true);
  template.querySelector("[data-title]").textContent = title;
  template.querySelector("[data-copy]").textContent = copy;
  const controls = template.querySelector("#manualControls");
  const sortedInstruments = [...instrumentsForVariant(variantId)].sort((a, b) =>
    a.display_name.localeCompare(b.display_name)
  );
  for (const instrument of sortedInstruments) {
    const row = document.createElement("div");
    row.className = "manual-row";
    row.innerHTML = `<span class="manual-name">${instrument.display_name}</span><input type="number" min="0" value="0" data-instrument-id="${instrument.id}">`;
    controls.appendChild(row);
  }
  app.innerHTML = "";
  app.appendChild(template);
  const split = document.querySelector(".split");
  const savedWidth = localStorage.getItem("trayguard_split_width");
  if (savedWidth && split) {
    split.style.gridTemplateColumns = `${savedWidth} 4px 1fr`;
  }
  setupResizableSplit();
  const startBtn = document.querySelector("#startCamera");
  if (startBtn) {
    startBtn.textContent = state.stream ? "Stop camera" : "Start camera";
    startBtn.onclick = startCamera;
  }
  const fullscreenBtn = document.querySelector("#fullscreenBtn");
  if (fullscreenBtn) fullscreenBtn.onclick = toggleFullscreen;
  const exitFullscreenBtn = document.querySelector("#exitFullscreenBtn");
  if (exitFullscreenBtn) exitFullscreenBtn.onclick = toggleFullscreen;
  const submitBtn = document.querySelector("#submitSort");
  submitBtn.onclick = async () => {
    if (mode === "practice") {
      const selectedCounts = selectedCountsFromInputs();
      const result = await api(`/api/runs/${state.run.run_id}/score`, {
        method: "POST",
        body: JSON.stringify({
          mode,
          variant_id: variantId,
          selected_counts: selectedCounts,
          started_at: startedAt.toISOString(),
          duration_seconds: (Date.now() - startedAt.getTime()) / 1000,
          overall_confidence: Number.parseInt(document.querySelector("#confidence").value, 10),
        }),
      });
      state.attempts[mode] = result;
      renderAttemptResult(result, feedback, mode);
      return;
    }

    const video = document.querySelector("#video");
    const summary = document.querySelector("#detectionSummary");
    if (!video.srcObject) {
      summary.textContent = "Please start the camera first.";
      summary.classList.add("error");
      return;
    }

    const detectResult = await takeSnapshot();
    if (!detectResult) {
      summary.textContent = "Snapshot failed. You can still use manual fallback.";
      summary.classList.add("error");
      return;
    }

    stopAutoDetection();
    video.style.display = "none";
    const svg = document.querySelector("#overlaySvg");
    if (svg) svg.style.display = "none";

    summary.textContent = "Snapshot taken. Review detected cards.";
    summary.classList.remove("error");
    submitBtn.textContent = "Next";
    submitBtn.onclick = async () => {
      const selectedCounts = selectedCountsFromInputs();
      const result = await api(`/api/runs/${state.run.run_id}/score`, {
        method: "POST",
        body: JSON.stringify({
          mode,
          variant_id: variantId,
          selected_counts: selectedCounts,
          started_at: startedAt.toISOString(),
          duration_seconds: (Date.now() - startedAt.getTime()) / 1000,
          overall_confidence: Number.parseInt(document.querySelector("#confidence").value, 10),
        }),
      });
      state.attempts[mode] = result;
      renderAttemptResult(result, feedback, mode);
    };
  };
}

async function startCamera() {
  const video = document.querySelector("#video");
  const summary = document.querySelector("#detectionSummary");
  const startBtn = document.querySelector("#startCamera");

  if (state.stream) {
    cleanupCamera();
    if (startBtn) startBtn.textContent = "Start camera";
    summary.textContent = "Camera stopped.";
    return false;
  }

  summary.textContent = "Requesting camera access...";
  if (!navigator.mediaDevices?.getUserMedia) {
    summary.textContent = "Camera API is not available in this browser. Use Chrome/Safari on http://127.0.0.1 or use manual fallback.";
    return false;
  }
  try {
    try {
      state.stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: { ideal: "environment" } }, audio: false });
    } catch (_error) {
      state.stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
    }
  } catch (error) {
    summary.textContent = `Camera could not start: ${error.name || "Error"}${error.message ? ` - ${error.message}` : ""}. You can still use manual fallback.`;
    return false;
  }
  video.srcObject = state.stream;
  video.onstalled = () => {
    stopAutoDetection();
    summary.textContent = "Camera paused. Click Stop then Start to resume.";
  };
  await video.play();
  initAudio();
  if (state.currentStep === "practice") {
    startAutoDetection();
  }
  if (startBtn) startBtn.textContent = "Stop camera";
  summary.textContent = "Camera is live.";
  if (state.currentStep === "practice") {
    summary.textContent += " Auto-detecting cards...";
  }
  return true;
}

async function detectCards(skipStart = false) {
  const video = document.querySelector("#video");
  if (!video.srcObject && !skipStart) {
    const started = await startCamera();
    if (!started) return false;
  }
  if (state.detectionInFlight) return false;
  state.detectionInFlight = true;

  let result;
  try {
    result = await captureAndDetect();
  } catch (error) {
    const summary = document.querySelector("#detectionSummary");
    summary.textContent = "Detection failed. Using manual fallback.";
    summary.classList.add("error");
    state.detectionInFlight = false;
    return false;
  }

  const summary = document.querySelector("#detectionSummary");
  summary.classList.remove("error");
  console.log("detectCards result:", result);
  if (result.detections && result.detections.length > 0) {
    console.log("Detected marker_ids:", result.detections.map(d => d.marker_id));
    console.log("Module marker_cards:", (state.module.marker_cards || []).map(c => c.marker_id));
  }
  drawOverlay(result.detections);

  const currentCounts = result.selected_counts || {};
  const countsChanged = JSON.stringify(currentCounts) !== JSON.stringify(state.lastDetection?.counts);

  if (countsChanged) {
    state.stableFrameCount = 0;
    state.lastDetection = { counts: currentCounts, detections: result.detections };
  } else {
    state.stableFrameCount += 1;
  }

  const previousStable = JSON.stringify(state.stableCounts);
  const newStable = JSON.stringify(currentCounts);
  if (previousStable !== newStable) {
    console.log("Updating manual counts:", currentCounts);
    setManualCounts(currentCounts);
    state.stableCounts = currentCounts;
  }

  summary.textContent = `Scanning... ${result.detections.length} card(s) detected.`;
  state.detectionInFlight = false;
  return true;
}

function renderAttemptResult(result, showFeedback, mode) {
  const attempt = result.attempt;
  const rows = result.items.map((item) => `
    <tr>
      <td>${item.error_category}</td>
      <td>${item.expected_instrument_name || "-"}</td>
      <td>${item.selected_instrument_name || "-"}</td>
      <td>${item.feedback_message_id || "-"}</td>
    </tr>
  `).join("");
  app.innerHTML = `
    <section class="panel">
      <h2>${mode === "practice" ? "Practice feedback" : "Attempt submitted"}</h2>
      <div class="summary-grid">
        <div class="metric"><span>Accuracy</span><strong>${attempt.accuracy_score}%</strong></div>
        <div class="metric"><span>Recall</span><strong>${attempt.required_recall}%</strong></div>
        <div class="metric"><span>Error points</span><strong>${attempt.error_points}</strong></div>
        <div class="metric"><span>Selected units</span><strong>${attempt.selected_units}</strong></div>
      </div>
      ${showFeedback ? `<table><thead><tr><th>Category</th><th>Expected</th><th>Selected</th><th>Feedback</th></tr></thead><tbody>${rows}</tbody></table>` : `<p class="muted">Feedback is hidden for assessment mode.</p>`}
      <div class="button-row"><button class="primary" id="nextStep">Continue</button></div>
    </section>
  `;
  document.querySelector("#nextStep").onclick = () => {
    if (mode === "pre_test") setStep("study");
    else if (mode === "practice") setStep("post");
    else if (mode === "post_test") setStep("summary");
  };
}

function studyImage(instrument) {
  if (!instrument || !instrument.id) return `<div class="image-placeholder">No image</div>`;
  return `<img src="/api/instrument-image/${instrument.id}" alt="${instrument.display_name}" class="study-img" onerror="this.parentElement.innerHTML='<div class=image-placeholder>Image not found</div>'">`;
}

function renderStudy() {
  const cards = instrumentsForTray();
  const instrument = cards[state.studyIndex % cards.length];
  const required = state.module.required_items[instrument.id];
  app.innerHTML = `
    <section class="panel study-card">
      <h2>Study card ${state.studyIndex + 1} of ${cards.length}</h2>
      <p class="muted">Prompt before reveal: identify the instrument and its key distinguishing features.</p>
      <div class="card study-layout">
        <div class="study-image">${studyImage(instrument)}</div>
        <div class="study-details">
          <h3>${instrument.display_name}</h3>
          <p><strong>Family:</strong> ${instrument.family}</p>
          <p><strong>Required count:</strong> ${required ? required.quantity : "Distractor"}</p>
          <p><strong>Aliases:</strong> ${instrument.aliases.join(", ") || "-"}</p>
          <ul class="feature-list">${instrument.distinguishing_features.map((feature) => `<li>${feature}</li>`).join("")}</ul>
        </div>
      </div>
      <div class="button-row">
        <button id="prevCard">Previous</button>
        <button id="nextCard">Next</button>
        <button class="primary" id="goQuiz">Start quiz</button>
      </div>
    </section>
  `;
  document.querySelector("#prevCard").onclick = () => { state.studyIndex = Math.max(0, state.studyIndex - 1); renderStudy(); };
  document.querySelector("#nextCard").onclick = () => { state.studyIndex = Math.min(cards.length - 1, state.studyIndex + 1); renderStudy(); };
  document.querySelector("#goQuiz").onclick = () => {
    state.quizItems = cards.flatMap((item) => (item.study_prompts || []).filter((prompt) => prompt.id === "name").map((prompt) => ({ instrument: item, prompt }))).slice(0, 12);
    state.quizIndex = 0;
    setStep("quiz");
  };
}

function renderQuiz() {
  if (!state.quizItems.length) {
    state.quizItems = instrumentsForTray().flatMap((item) => (item.study_prompts || []).filter((prompt) => prompt.id === "name").map((prompt) => ({ instrument: item, prompt }))).slice(0, 12);
  }
  if (state.quizIndex >= state.quizItems.length) {
    setStep("practice");
    return;
  }
  const item = state.quizItems[state.quizIndex];
  app.innerHTML = `
    <section class="panel">
      <h2>Quiz ${state.quizIndex + 1} of ${state.quizItems.length}</h2>
      <div class="study-image">${studyImage(item.instrument)}</div>
      <p class="muted">Name this instrument.</p>
      <label>Your answer <input id="quizAnswer" autocomplete="off"></label>
      <label>Confidence <input id="quizConfidence" type="range" min="1" max="5" value="3"></label>
      <div class="button-row"><button class="primary" id="submitQuiz">Submit</button></div>
      <div id="quizFeedback"></div>
    </section>
  `;
  document.querySelector("#submitQuiz").onclick = async () => {
    const answer = document.querySelector("#quizAnswer").value;
    const correct = answer.trim().length > 0 && isAnswerCorrect(item.instrument, item.prompt.answer, answer);
    await api(`/api/runs/${state.run.run_id}/quiz`, {
      method: "POST",
      body: JSON.stringify({
        prompt_id: item.prompt.id,
        instrument_id: item.instrument.id,
        answer,
        correct,
        confidence: Number.parseInt(document.querySelector("#quizConfidence").value, 10),
      }),
    });
    document.querySelector("#quizFeedback").innerHTML = `<div class="feedback ${correct ? "" : "error"}">${correct ? "Correct." : `Review: ${item.prompt.answer}`}</div><div class="button-row"><button class="primary" id="nextQuiz">Next</button></div>`;
    document.querySelector("#nextQuiz").onclick = () => { state.quizIndex += 1; renderQuiz(); };
  };
}

async function renderSummary() {
  await api(`/api/runs/${state.run.run_id}/complete`, { method: "POST", body: "{}" });
  const exports = await api(`/api/runs/${state.run.run_id}/export`);
  const pre = state.attempts.pre_test?.attempt;
  const post = state.attempts.post_test?.attempt;
  app.innerHTML = `
    <section class="panel">
      <h2>Run summary</h2>
      <div class="summary-grid">
        <div class="metric"><span>Pre accuracy</span><strong>${pre ? `${pre.accuracy_score}%` : "-"}</strong></div>
        <div class="metric"><span>Post accuracy</span><strong>${post ? `${post.accuracy_score}%` : "-"}</strong></div>
        <div class="metric"><span>Gain</span><strong>${pre && post ? `${(post.accuracy_score - pre.accuracy_score).toFixed(1)} pts` : "-"}</strong></div>
        <div class="metric"><span>Run ID</span><strong>${state.run.run_id}</strong></div>
      </div>
      <p class="muted">Exports written locally:</p>
      <ul><li>${exports.run}</li><li>${exports.attempts}</li><li>${exports.items}</li></ul>
    </section>
  `;
}

function render() {
  if (!state.module) return;
  const preVariant = variantByMode("pre_test");
  const postVariant = variantByMode("post_test");
  const preVariantId = preVariant ? preVariant.id : "full_tray";
  const postVariantId = postVariant ? postVariant.id : "full_tray";
  if (state.currentStep === "intake") renderIntake();
  if (state.currentStep === "pre") renderTraySort({ mode: "pre_test", variantId: preVariantId, title: "Pre-test tray sort", copy: "No hints. Use cards and the count sheet task to assemble the tray.", feedback: false });
  if (state.currentStep === "study") renderStudy();
  if (state.currentStep === "quiz") renderQuiz();
  if (state.currentStep === "practice") renderTraySort({ mode: "practice", variantId: preVariantId, title: "Practice tray sort", copy: "Use the same physical-card workflow. Feedback appears after submission.", feedback: true });
  if (state.currentStep === "post") renderTraySort({ mode: "post_test", variantId: postVariantId, title: "Post-test tray sort", copy: "No hints. This uses the matched post-test variant.", feedback: false });
  if (state.currentStep === "summary") renderSummary();
}

async function init() {
  state.module = await api("/api/module");
  if (localStorage.getItem("trayguard_steps_collapsed") === "true") {
    stepsNav.classList.add("collapsed");
  }
  renderSteps();
  setStep("intake");
}

init().catch((error) => {
  app.innerHTML = `<section class="panel"><h2>Startup error</h2><pre>${error}</pre></section>`;
});
