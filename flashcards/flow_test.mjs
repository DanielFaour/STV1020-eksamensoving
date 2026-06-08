const endpoint = process.argv[2] || "http://127.0.0.1:9223";

async function waitForPage() {
  for (let attempt = 0; attempt < 40; attempt += 1) {
    try {
      const pages = await fetch(`${endpoint}/json/list`).then((response) => response.json());
      const page = pages.find((entry) => entry.type === "page" && entry.url.includes("index.html"));
      if (page) return page;
    } catch {
      // Browser startup can take a moment.
    }
    await new Promise((resolve) => setTimeout(resolve, 250));
  }
  throw new Error("Could not connect to the test page");
}

const page = await waitForPage();
const socket = new WebSocket(page.webSocketDebuggerUrl);
await new Promise((resolve, reject) => {
  socket.addEventListener("open", resolve, { once: true });
  socket.addEventListener("error", reject, { once: true });
});

let messageId = 0;
const pending = new Map();
socket.addEventListener("message", (event) => {
  const message = JSON.parse(event.data);
  if (!pending.has(message.id)) return;
  const { resolve, reject } = pending.get(message.id);
  pending.delete(message.id);
  message.error ? reject(new Error(message.error.message)) : resolve(message.result);
});

function call(method, params = {}) {
  messageId += 1;
  socket.send(JSON.stringify({ id: messageId, method, params }));
  return new Promise((resolve, reject) => pending.set(messageId, { resolve, reject }));
}

async function evaluate(expression) {
  const result = await call("Runtime.evaluate", {
    expression,
    awaitPromise: true,
    returnByValue: true,
  });
  if (result.exceptionDetails) throw new Error(result.exceptionDetails.text);
  return result.result.value;
}

await call("Runtime.enable");
await new Promise((resolve) => setTimeout(resolve, 500));
await evaluate(`localStorage.removeItem("stv1020-exam-history"); localStorage.removeItem("stv1020-flagged-cards"); examHistory = []; flaggedCards.clear(); showFlaggedOnly = false; renderHistory(); updateFlagControls();`);

const home = await evaluate(`({
  cards: window.STV1020_DATA.flashcards.length,
  questions: window.STV1020_DATA.questions.length,
  homeActive: document.querySelector("#home-view").classList.contains("active")
})`);
if (home.cards !== 121 || home.questions !== 315 || !home.homeActive) {
  throw new Error(`Unexpected home state: ${JSON.stringify(home)}`);
}

const flippedCard = await evaluate(`(() => {
  showView("cards");
  document.querySelector("#flashcard").classList.add("flipped");
  const front = getComputedStyle(document.querySelector(".card-front"));
  const back = getComputedStyle(document.querySelector(".card-back"));
  const state = {
    frontVisibility: front.visibility,
    frontOpacity: front.opacity,
    backVisibility: back.visibility,
    backOpacity: back.opacity
  };
  document.querySelector("#flashcard").classList.remove("flipped");
  showView("home");
  return state;
})()`);
if (flippedCard.frontVisibility !== "hidden" || flippedCard.frontOpacity !== "0" || flippedCard.backVisibility !== "visible" || flippedCard.backOpacity !== "1") {
  throw new Error(`Flipped card leaks its front face: ${JSON.stringify(flippedCard)}`);
}

const flagFlow = await evaluate(`(() => {
  showView("cards");
  const initial = {
    filterDisabled: document.querySelector("#flag-filter").disabled,
    filterText: document.querySelector("#flag-filter").textContent
  };
  document.querySelector("#toggle-flagged").click();
  const afterFlag = {
    stored: JSON.parse(localStorage.getItem("stv1020-flagged-cards") || "[]").length,
    buttonText: document.querySelector("#toggle-flagged").textContent,
    filterDisabled: document.querySelector("#flag-filter").disabled,
    filterText: document.querySelector("#flag-filter").textContent
  };
  document.querySelector("#flag-filter").click();
  const filtered = {
    visible: visibleCards.length,
    active: document.querySelector("#flag-filter").classList.contains("active"),
    position: document.querySelector("#card-position").textContent
  };
  document.querySelector("#toggle-flagged").click();
  const afterUnflag = {
    stored: JSON.parse(localStorage.getItem("stv1020-flagged-cards") || "[]").length,
    visible: visibleCards.length,
    filterDisabled: document.querySelector("#flag-filter").disabled,
    filterText: document.querySelector("#flag-filter").textContent
  };
  showView("home");
  return { initial, afterFlag, filtered, afterUnflag };
})()`);
if (!flagFlow.initial.filterDisabled || flagFlow.afterFlag.stored !== 1 || flagFlow.afterFlag.filterDisabled || !flagFlow.afterFlag.buttonText.includes("Flagget") || flagFlow.filtered.visible !== 1 || !flagFlow.filtered.active || flagFlow.filtered.position !== "1 / 1" || flagFlow.afterUnflag.stored !== 0 || flagFlow.afterUnflag.visible !== 121 || !flagFlow.afterUnflag.filterDisabled) {
  throw new Error(`Flagged card flow failed: ${JSON.stringify(flagFlow)}`);
}

const examStarted = await evaluate(`(() => {
  startExam("quick");
  return {
    count: examQuestions.length,
    options: document.querySelectorAll(".answer-option").length,
    sessionVisible: !document.querySelector("#exam-session").classList.contains("hidden"),
    historyHidden: document.querySelector("#history-section").classList.contains("hidden")
  };
})()`);
if (examStarted.count !== 25 || examStarted.options !== 5 || !examStarted.sessionVisible || !examStarted.historyHidden) {
  throw new Error(`Exam did not start correctly: ${JSON.stringify(examStarted)}`);
}

const perfect = await evaluate(`(() => {
  examAnswers = examQuestions.map((question) => question.correctIndex);
  submitExam();
  return {
    grade: document.querySelector("#result-grade").textContent,
    correct: document.querySelector("#correct-count").textContent,
    review: document.querySelectorAll(".review-card").length,
    historyRows: document.querySelectorAll(".history-row").length,
    latest: document.querySelector("#history-latest").textContent
  };
})()`);
if (perfect.grade !== "A" || perfect.correct !== "25" || perfect.review !== 25 || perfect.historyRows !== 1 || perfect.latest !== "100 %") {
  throw new Error(`Perfect result failed: ${JSON.stringify(perfect)}`);
}

const failed = await evaluate(`(() => {
  startExam("quick");
  examAnswers = examQuestions.map((question) => (question.correctIndex + 1) % 5);
  submitExam();
  return {
    grade: document.querySelector("#result-grade").textContent,
    wrong: document.querySelector("#wrong-count").textContent,
    review: document.querySelectorAll(".review-card").length,
    wrongBoxes: document.querySelectorAll(".review-answer-box.selected-wrong").length,
    correctBoxes: document.querySelectorAll(".review-answer-box.correct-answer").length,
    firstWrongBox: document.querySelector(".review-answer-box.selected-wrong")?.textContent || "",
    historyRows: document.querySelectorAll(".history-row").length,
    trend: document.querySelector("#history-trend").textContent,
    chartDots: document.querySelectorAll("#trend-chart circle").length,
    averageLines: document.querySelectorAll("#trend-chart .average-line").length,
    averageLabel: document.querySelector("#trend-chart .average-label")?.textContent || ""
  };
})()`);
if (failed.grade !== "F" || failed.wrong !== "25" || failed.review !== 25 || failed.wrongBoxes !== 25 || failed.correctBoxes !== 25 || !failed.firstWrongBox.includes("Ditt svar") || failed.historyRows !== 2 || failed.trend !== "↓ -100 pp" || failed.chartDots !== 2 || failed.averageLines !== 1 || !failed.averageLabel.includes("Snitt")) {
  throw new Error(`Failure result failed: ${JSON.stringify(failed)}`);
}

const fullMode = await evaluate(`(() => {
  startExam("full");
  const started = {
    count: examQuestions.length,
    options: document.querySelectorAll(".answer-option").length,
    mode: currentExamMode.key
  };
  examAnswers = examQuestions.map((question) => question.correctIndex);
  submitExam();
  return {
    ...started,
    grade: document.querySelector("#result-grade").textContent,
    correct: document.querySelector("#correct-count").textContent,
    review: document.querySelectorAll(".review-card").length,
    historyRows: document.querySelectorAll(".history-row").length,
    latestMode: examHistory.at(-1).mode
  };
})()`);
if (fullMode.count !== 70 || fullMode.options !== 5 || fullMode.mode !== "full" || fullMode.grade !== "A" || fullMode.correct !== "70" || fullMode.review !== 70 || fullMode.historyRows !== 3 || fullMode.latestMode !== "full") {
  throw new Error(`Full exam mode failed: ${JSON.stringify(fullMode)}`);
}

if (process.argv[3]) {
  await call("Emulation.setDeviceMetricsOverride", {
    width: 1440,
    height: 1000,
    deviceScaleFactor: 1,
    mobile: false,
  });
  await evaluate(`(() => {
    showView("exam");
    document.querySelector("#exam-start").classList.add("hidden");
    document.querySelector("#exam-result").classList.add("hidden");
    document.querySelector("#history-section").classList.remove("hidden");
    document.querySelector("#history-section").scrollIntoView();
  })()`);
  await new Promise((resolve) => setTimeout(resolve, 500));
  const screenshot = await call("Page.captureScreenshot", { format: "png" });
  const { writeFile } = await import("node:fs/promises");
  await writeFile(process.argv[3], Buffer.from(screenshot.data, "base64"));
}

if (process.argv[4]) {
  await call("Emulation.setDeviceMetricsOverride", {
    width: 1200,
    height: 800,
    deviceScaleFactor: 1,
    mobile: false,
  });
  await evaluate(`(() => {
    showView("cards");
    document.querySelector("#flashcard").classList.add("flipped");
    document.querySelector("#flashcard").scrollIntoView({ block: "center" });
  })()`);
  await new Promise((resolve) => setTimeout(resolve, 700));
  const flippedScreenshot = await call("Page.captureScreenshot", { format: "png" });
  const { writeFile } = await import("node:fs/promises");
  await writeFile(process.argv[4], Buffer.from(flippedScreenshot.data, "base64"));
}

const thresholds = await evaluate(`({
  below: gradeFor(39),
  pass: gradeFor(40),
  tenOfTwentyFive: gradeFor(10 / 25 * 100)
})`);
if (thresholds.below !== "F" || thresholds.pass !== "E" || thresholds.tenOfTwentyFive !== "E") {
  throw new Error(`Pass threshold failed: ${JSON.stringify(thresholds)}`);
}

await call("Emulation.setDeviceMetricsOverride", {
  width: 390,
  height: 844,
  deviceScaleFactor: 1,
  mobile: true,
});
const mobileHistory = await evaluate(`(() => {
  showView("exam");
  document.querySelector("#exam-start").classList.add("hidden");
  document.querySelector("#exam-result").classList.add("hidden");
  document.querySelector("#history-section").classList.remove("hidden");
  return {
    scrollWidth: document.documentElement.scrollWidth,
    historyWidth: Math.round(document.querySelector("#history-section").getBoundingClientRect().width),
    statColumns: getComputedStyle(document.querySelector(".history-stats")).gridTemplateColumns.split(" ").length
  };
})()`);
if (mobileHistory.scrollWidth > 390 || mobileHistory.historyWidth > 362 || mobileHistory.statColumns !== 2) {
  throw new Error(`Mobile history layout overflows: ${JSON.stringify(mobileHistory)}`);
}

const mobileExamDots = await evaluate(`(() => {
  showView("exam");
  startExam("full");
  const dots = [...document.querySelectorAll(".question-dot")].map((dot) => {
    const rect = dot.getBoundingClientRect();
    return { width: Math.round(rect.width), height: Math.round(rect.height) };
  });
  const container = document.querySelector("#question-dots").getBoundingClientRect();
  return {
    count: dots.length,
    maxWidth: Math.max(...dots.map((dot) => dot.width)),
    minWidth: Math.min(...dots.map((dot) => dot.width)),
    maxHeight: Math.max(...dots.map((dot) => dot.height)),
    containerWidth: Math.round(container.width),
    scrollWidth: document.documentElement.scrollWidth
  };
})()`);
if (mobileExamDots.count !== 70 || mobileExamDots.maxWidth > 12 || mobileExamDots.minWidth < 6 || mobileExamDots.maxHeight > 12 || mobileExamDots.scrollWidth > 390) {
  throw new Error(`Mobile exam dots layout failed: ${JSON.stringify(mobileExamDots)}`);
}

const mobile = await evaluate(`(() => {
  showView("cards");
  return {
    innerWidth: window.innerWidth,
    scrollWidth: document.documentElement.scrollWidth,
    cardWidth: Math.round(document.querySelector("#flashcard").getBoundingClientRect().width)
  };
})()`);
if (mobile.innerWidth !== 390 || mobile.scrollWidth > 390 || mobile.cardWidth > 362) {
  throw new Error(`Mobile layout overflows: ${JSON.stringify(mobile)}`);
}

socket.close();
console.log("Passed browser flow: flagged flashcards, 25/70 question modes, five options, wrong-answer explanations, exam dots, history trend chart with average line, 40% pass threshold, review rendering, and 390px mobile layout.");
