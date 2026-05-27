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
  state.currentStep = step;
  modeStatus.textContent = steps.find(([id]) => id === step)?.[1] || step;
  renderSteps();
  render();
}

function renderSteps() {
  stepsNav.innerHTML = "";
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
    state.run = await api("/api/runs", {
      method: "POST",
      body: JSON.stringify({
        learner_id: document.querySelector("#learnerId").value,
        participant_group: document.querySelector("#participantGroup").value,
        prior_experience_level: document.querySelector("#priorExperience").value,
      }),
    });
    setStep("pre");
  };
}

function renderTraySort({ mode, variantId, title, copy, feedback }) {
  const startedAt = new Date();
  const variant = state.module.assessment_variants[variantId];
  const template = document.querySelector("#tray-sort-template").content.cloneNode(true);
  template.querySelector("[data-title]").textContent = title;
  template.querySelector("[data-copy]").textContent = variant?.photo_view ? `${copy} Photo set: ${variant.photo_view}.` : copy;
  const controls = template.querySelector("#manualControls");
  for (const instrument of instrumentsForVariant(variantId)) {
    const row = document.createElement("div");
    row.className = "manual-row";
    row.innerHTML = `<span>${instrument.display_name}</span><input type="number" min="0" value="0" data-instrument-id="${instrument.id}">`;
    controls.appendChild(row);
  }
  app.innerHTML = "";
  app.appendChild(template);
  document.querySelector("#startCamera").onclick = startCamera;
  document.querySelector("#detectCards").onclick = detectCards;
  document.querySelector("#submitSort").onclick = async () => {
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
        not_sure: document.querySelector("#notSure").checked,
      }),
    });
    state.attempts[mode] = result;
    renderAttemptResult(result, feedback, mode);
  };
}

async function startCamera() {
  const video = document.querySelector("#video");
  const summary = document.querySelector("#detectionSummary");
  summary.textContent = "Requesting camera access...";
  if (!navigator.mediaDevices?.getUserMedia) {
    summary.textContent = "Camera API is not available in this browser. Use Chrome/Safari on http://127.0.0.1 or use manual fallback.";
    return false;
  }
  try {
    if (state.stream) {
      state.stream.getTracks().forEach((track) => track.stop());
    }
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
  await video.play();
  summary.textContent = "Camera is live. Place cards in view, then detect visible cards.";
  return true;
}

async function detectCards() {
  const video = document.querySelector("#video");
  if (!video.srcObject) {
    const started = await startCamera();
    if (!started) return;
  }
  const canvas = document.querySelector("#snapshotCanvas");
  canvas.width = video.videoWidth || 1280;
  canvas.height = video.videoHeight || 720;
  canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);
  const image = canvas.toDataURL("image/png");
  const result = await api("/api/detect-cards", { method: "POST", body: JSON.stringify({ image }) });
  setManualCounts(result.selected_counts);
  document.querySelector("#detectionSummary").textContent = `${result.detections.length} marker(s) detected. Review quantities before submitting.`;
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

function renderStudy() {
  const cards = instrumentsForTray();
  const instrument = cards[state.studyIndex % cards.length];
  const required = state.module.required_items[instrument.id];
  app.innerHTML = `
    <section class="panel study-card">
      <h2>Study card ${state.studyIndex + 1} of ${cards.length}</h2>
      <p class="muted">Prompt before reveal: identify the instrument and its key distinguishing features.</p>
      <div class="card">
        <h3>${instrument.display_name}</h3>
        <p><strong>Family:</strong> ${instrument.family}</p>
        <p><strong>Required count:</strong> ${required ? required.quantity : "Distractor"}</p>
        <p><strong>Aliases:</strong> ${instrument.aliases.join(", ") || "-"}</p>
        <ul class="feature-list">${instrument.distinguishing_features.map((feature) => `<li>${feature}</li>`).join("")}</ul>
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
    state.quizItems = cards.flatMap((item) => (item.study_prompts || []).map((prompt) => ({ instrument: item, prompt }))).slice(0, 12);
    state.quizIndex = 0;
    setStep("quiz");
  };
}

function renderQuiz() {
  if (!state.quizItems.length) {
    state.quizItems = instrumentsForTray().flatMap((item) => (item.study_prompts || []).map((prompt) => ({ instrument: item, prompt }))).slice(0, 12);
  }
  if (state.quizIndex >= state.quizItems.length) {
    setStep("practice");
    return;
  }
  const item = state.quizItems[state.quizIndex];
  app.innerHTML = `
    <section class="panel">
      <h2>Quiz ${state.quizIndex + 1} of ${state.quizItems.length}</h2>
      <p class="muted">${item.prompt.prompt}</p>
      <label>Your answer <input id="quizAnswer" autocomplete="off"></label>
      <label>Confidence <input id="quizConfidence" type="range" min="1" max="5" value="3"></label>
      <label class="check"><input id="quizNotSure" type="checkbox"> Not sure</label>
      <div class="button-row"><button class="primary" id="submitQuiz">Submit</button></div>
      <div id="quizFeedback"></div>
    </section>
  `;
  document.querySelector("#submitQuiz").onclick = async () => {
    const answer = document.querySelector("#quizAnswer").value;
    const correct = answer.trim().length > 0 && item.prompt.answer.toLowerCase().includes(answer.trim().toLowerCase());
    await api(`/api/runs/${state.run.run_id}/quiz`, {
      method: "POST",
      body: JSON.stringify({
        prompt_id: item.prompt.id,
        instrument_id: item.instrument.id,
        answer,
        correct,
        confidence: Number.parseInt(document.querySelector("#quizConfidence").value, 10),
        not_sure: document.querySelector("#quizNotSure").checked,
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
  if (state.currentStep === "intake") renderIntake();
  if (state.currentStep === "pre") renderTraySort({ mode: "pre_test", variantId: preVariant.id, title: "Pre-test tray sort", copy: "No hints. Use cards and the count sheet task to assemble the tray.", feedback: false });
  if (state.currentStep === "study") renderStudy();
  if (state.currentStep === "quiz") renderQuiz();
  if (state.currentStep === "practice") renderTraySort({ mode: "practice", variantId: preVariant.id, title: "Practice tray sort", copy: "Use the same physical-card workflow. Feedback appears after submission.", feedback: true });
  if (state.currentStep === "post") renderTraySort({ mode: "post_test", variantId: postVariant.id, title: "Post-test tray sort", copy: "No hints. This uses the matched post-test variant.", feedback: false });
  if (state.currentStep === "summary") renderSummary();
}

async function init() {
  state.module = await api("/api/module");
  renderSteps();
  setStep("intake");
}

init().catch((error) => {
  app.innerHTML = `<section class="panel"><h2>Startup error</h2><pre>${error}</pre></section>`;
});
