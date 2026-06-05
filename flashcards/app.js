const { flashcards, questions } = window.STV1020_DATA;

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];
const shuffle = (items) => {
  const copy = [...items];
  for (let index = copy.length - 1; index > 0; index -= 1) {
    const swap = Math.floor(Math.random() * (index + 1));
    [copy[index], copy[swap]] = [copy[swap], copy[index]];
  }
  return copy;
};
const escapeHTML = (value) => String(value).replace(/[&<>"']/g, (character) => ({
  "&": "&amp;",
  "<": "&lt;",
  ">": "&gt;",
  '"': "&quot;",
  "'": "&#039;",
})[character]);

const learned = new Set(JSON.parse(localStorage.getItem("stv1020-learned") || "[]"));
let examHistory = JSON.parse(localStorage.getItem("stv1020-exam-history") || "[]");
const EXAM_MODES = {
  quick: { key: "quick", size: 25, label: "Kort prøve" },
  full: { key: "full", size: 70, label: "Full eksamenssimulator" },
};
let visibleCards = [...flashcards];
let cardIndex = 0;
let examQuestions = [];
let examAnswers = [];
let examIndex = 0;
let currentExamMode = EXAM_MODES.quick;

function showView(view, updateHash = true) {
  if (!["home", "cards", "exam"].includes(view)) view = "home";
  $$(".view").forEach((element) => element.classList.toggle("active", element.id === `${view}-view`));
  $$(".nav-button").forEach((button) => button.classList.toggle("active", button.dataset.view === view));
  if (updateHash && window.location.hash !== `#${view}`) history.replaceState(null, "", `#${view}`);
  window.scrollTo({ top: 0, behavior: "smooth" });
}

$$("[data-view]").forEach((button) => button.addEventListener("click", () => showView(button.dataset.view)));
$$("[data-go]").forEach((button) => button.addEventListener("click", () => showView(button.dataset.go)));

function saveLearned() {
  localStorage.setItem("stv1020-learned", JSON.stringify([...learned]));
  updateProgress();
}

function updateProgress() {
  const percent = Math.round((learned.size / flashcards.length) * 100);
  $("#learned-count").textContent = learned.size;
  $("#total-card-count").textContent = flashcards.length;
  $("#home-card-count").textContent = flashcards.length;
  $("#home-learned-count").textContent = learned.size;
  $("#home-progress-label").textContent = `${percent} %`;
  $("#home-progress-bar").style.width = `${percent}%`;
  $$(".question-bank-count").forEach((element) => {
    element.textContent = questions.length;
  });
}

function renderCard() {
  const card = visibleCards[cardIndex];
  $("#flashcard").classList.remove("flipped");
  $("#card-topic").textContent = card.topic;
  $("#card-topic-back").textContent = card.topic;
  $("#card-position").textContent = `${cardIndex + 1} / ${visibleCards.length}`;
  $("#card-term").textContent = card.term;
  $("#card-term-back").textContent = card.term;
  $("#card-definition").textContent = card.definition;
  const isLearned = learned.has(card.id);
  $("#toggle-learned").classList.toggle("learned", isLearned);
  $("#toggle-learned").textContent = isLearned ? "Lært ✓" : "Marker som lært";
}

function changeCard(direction) {
  cardIndex = (cardIndex + direction + visibleCards.length) % visibleCards.length;
  renderCard();
}

function initializeCards() {
  const topics = ["Alle temaer", ...new Set(flashcards.map((card) => card.topic))];
  $("#topic-filter").innerHTML = topics.map((topic) => `<option value="${escapeHTML(topic)}">${escapeHTML(topic)}</option>`).join("");
  $("#topic-filter").addEventListener("change", (event) => {
    visibleCards = event.target.value === "Alle temaer"
      ? [...flashcards]
      : flashcards.filter((card) => card.topic === event.target.value);
    cardIndex = 0;
    renderCard();
  });
  $("#flashcard").addEventListener("click", () => $("#flashcard").classList.toggle("flipped"));
  $("#flashcard").addEventListener("keydown", (event) => {
    if (event.key === "Enter") $("#flashcard").classList.toggle("flipped");
  });
  $("#prev-card").addEventListener("click", () => changeCard(-1));
  $("#next-card").addEventListener("click", () => changeCard(1));
  $("#shuffle-cards").addEventListener("click", () => {
    visibleCards = shuffle(visibleCards);
    cardIndex = 0;
    renderCard();
  });
  $("#toggle-learned").addEventListener("click", () => {
    const id = visibleCards[cardIndex].id;
    learned.has(id) ? learned.delete(id) : learned.add(id);
    saveLearned();
    renderCard();
  });
  $("#reset-cards").addEventListener("click", () => {
    if (confirm("Vil du nullstille alle kort som er markert som lært?")) {
      learned.clear();
      saveLearned();
      renderCard();
    }
  });
  document.addEventListener("keydown", (event) => {
    if (!$("#cards-view").classList.contains("active") || ["SELECT", "BUTTON"].includes(document.activeElement.tagName)) return;
    if (event.key === "ArrowLeft") changeCard(-1);
    if (event.key === "ArrowRight") changeCard(1);
    if (event.code === "Space") {
      event.preventDefault();
      $("#flashcard").classList.toggle("flipped");
    }
  });
  renderCard();
}

function prepareQuestion(question) {
  const choices = question.choices.map((text, index) => ({ text, correct: index === question.correctIndex }));
  const randomizedChoices = shuffle(choices);
  return {
    ...question,
    choices: randomizedChoices.map((choice) => choice.text),
    correctIndex: randomizedChoices.findIndex((choice) => choice.correct),
  };
}

function startExam(modeKey = currentExamMode.key) {
  currentExamMode = EXAM_MODES[modeKey] || EXAM_MODES.quick;
  const size = Math.min(currentExamMode.size, questions.length);
  examQuestions = shuffle(questions).slice(0, size).map(prepareQuestion);
  examAnswers = Array(size).fill(null);
  examIndex = 0;
  $("#exam-start").classList.add("hidden");
  $("#exam-result").classList.add("hidden");
  $("#history-section").classList.add("hidden");
  $("#exam-session").classList.remove("hidden");
  renderExamQuestion();
}

function renderExamQuestion() {
  const question = examQuestions[examIndex];
  const total = examQuestions.length;
  $("#exam-topic").textContent = question.topic;
  $("#exam-progress-label").textContent = `${currentExamMode.label}: spørsmål ${examIndex + 1} av ${total}`;
  $("#exam-progress-bar").style.width = `${((examIndex + 1) / total) * 100}%`;
  $("#answered-label").textContent = `${examAnswers.filter((answer) => answer !== null).length} besvart`;
  $("#question-number").textContent = `Oppgave ${examIndex + 1}`;
  $("#question-text").textContent = question.question;
  $("#answer-options").innerHTML = question.choices.map((choice, index) => `
    <button class="answer-option ${examAnswers[examIndex] === index ? "selected" : ""}" data-answer="${index}">
      <span class="option-letter">${"ABCDE"[index]}</span><span>${escapeHTML(choice)}</span>
    </button>
  `).join("");
  $$(".answer-option").forEach((button) => button.addEventListener("click", () => {
    examAnswers[examIndex] = Number(button.dataset.answer);
    renderExamQuestion();
  }));

  $("#question-dots").innerHTML = examQuestions.map((_, index) => `
    <button aria-label="Gå til spørsmål ${index + 1}" data-question="${index}" class="question-dot ${examAnswers[index] !== null ? "answered" : ""} ${index === examIndex ? "current" : ""}"></button>
  `).join("");
  $$(".question-dot").forEach((dot) => dot.addEventListener("click", () => {
    examIndex = Number(dot.dataset.question);
    renderExamQuestion();
  }));

  $("#exam-prev").disabled = examIndex === 0;
  $("#exam-prev").style.opacity = examIndex === 0 ? ".35" : "1";
  $("#exam-next").classList.toggle("hidden", examIndex === total - 1);
  $("#submit-exam").classList.toggle("hidden", examIndex !== total - 1);
}

function gradeFor(percent) {
  if (percent >= 90) return "A";
  if (percent >= 80) return "B";
  if (percent >= 65) return "C";
  if (percent >= 55) return "D";
  if (percent >= 40) return "E";
  return "F";
}

function saveExamResult(correct, total, percent, grade) {
  examHistory.push({
    id: `${Date.now()}-${Math.random().toString(16).slice(2)}`,
    date: new Date().toISOString(),
    correct,
    total,
    percent,
    grade,
    mode: currentExamMode.key,
    modeLabel: currentExamMode.label,
  });
  examHistory = examHistory.slice(-100);
  localStorage.setItem("stv1020-exam-history", JSON.stringify(examHistory));
}

function formatHistoryDate(value) {
  return new Intl.DateTimeFormat("nb-NO", {
    day: "numeric",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(value));
}

function trendDetails() {
  if (examHistory.length < 2) {
    return { difference: null, direction: "neutral", label: "Trenger minst to prøver", message: "Første resultat er registrert" };
  }
  const latest = examHistory.at(-1).percent;
  const previous = examHistory.at(-2).percent;
  const difference = latest - previous;
  if (difference > 0) return { difference, direction: "up", label: "Bedre enn sist", message: `Du gikk opp ${difference} prosentpoeng fra forrige prøve.` };
  if (difference < 0) return { difference, direction: "down", label: "Lavere enn sist", message: `Du gikk ned ${Math.abs(difference)} prosentpoeng fra forrige prøve.` };
  return { difference, direction: "neutral", label: "Samme som sist", message: "Resultatet er uendret fra forrige prøve." };
}

function buildTrendChart() {
  const width = 900;
  const height = 250;
  const padding = { left: 38, right: 18, top: 25, bottom: 30 };
  const chartWidth = width - padding.left - padding.right;
  const chartHeight = height - padding.top - padding.bottom;
  const entries = examHistory.slice(-20);
  const x = (index) => padding.left + (entries.length === 1 ? chartWidth / 2 : (index / (entries.length - 1)) * chartWidth);
  const y = (percent) => padding.top + chartHeight - (percent / 100) * chartHeight;
  const points = entries.map((entry, index) => `${x(index)},${y(entry.percent)}`).join(" ");
  const areaPoints = `${x(0)},${y(0)} ${points} ${x(entries.length - 1)},${y(0)}`;

  const grid = [0, 40, 60, 80, 100].map((value) => `
    <line x1="${padding.left}" y1="${y(value)}" x2="${width - padding.right}" y2="${y(value)}" class="${value === 40 ? "pass-line" : "grid-line"}"></line>
    <text x="${padding.left - 8}" y="${y(value) + 4}" text-anchor="end">${value}</text>
  `).join("");
  const labels = entries.map((entry, index) => `
    <text x="${x(index)}" y="${height - 8}" text-anchor="middle">${examHistory.length - entries.length + index + 1}</text>
  `).join("");
  const dots = entries.map((entry, index) => `
    <circle cx="${x(index)}" cy="${y(entry.percent)}" r="5" data-index="${index}">
        <title>Prøve ${examHistory.length - entries.length + index + 1}: ${entry.percent} %, karakter ${entry.grade}${entry.modeLabel ? `, ${entry.modeLabel}` : ""}</title>
    </circle>
  `).join("");

  return `
    <svg viewBox="0 0 ${width} ${height}" aria-hidden="true">
      ${grid}
      <polygon points="${areaPoints}" class="trend-area"></polygon>
      ${entries.length > 1 ? `<polyline points="${points}" class="trend-line"></polyline>` : ""}
      ${dots}
      ${labels}
    </svg>
  `;
}

function renderHistory() {
  const hasHistory = examHistory.length > 0;
  $("#history-empty").classList.toggle("hidden", hasHistory);
  $("#history-content").classList.toggle("hidden", !hasHistory);
  $("#clear-history").classList.toggle("hidden", !hasHistory);
  if (!hasHistory) return;

  const latest = examHistory.at(-1);
  const best = examHistory.reduce((current, entry) => entry.percent > current.percent ? entry : current, examHistory[0]);
  const average = Math.round(examHistory.reduce((sum, entry) => sum + entry.percent, 0) / examHistory.length);
  const trend = trendDetails();

  $("#history-latest").textContent = `${latest.percent} %`;
  $("#history-latest-grade").textContent = `Karakter ${latest.grade}`;
  $("#history-best").textContent = `${best.percent} %`;
  $("#history-best-grade").textContent = `Karakter ${best.grade}`;
  $("#history-average").textContent = `${average} %`;
  $("#history-test-count").textContent = `${examHistory.length} ${examHistory.length === 1 ? "prøve" : "prøver"}`;
  $("#history-trend").textContent = trend.difference === null ? "–" : `${trend.difference > 0 ? "↑ +" : trend.difference < 0 ? "↓ " : "→ "}${trend.difference} pp`;
  $("#history-trend-label").textContent = trend.label;
  $("#history-trend-card").dataset.direction = trend.direction;
  $("#trend-message").textContent = trend.message;
  $("#trend-chart").innerHTML = buildTrendChart();

  $("#history-list").innerHTML = [...examHistory].reverse().map((entry, reverseIndex) => {
    const index = examHistory.length - 1 - reverseIndex;
    const previous = index > 0 ? examHistory[index - 1] : null;
    const difference = previous ? entry.percent - previous.percent : null;
    const direction = difference > 0 ? "up" : difference < 0 ? "down" : "neutral";
    const change = difference === null ? "Første prøve" : difference === 0 ? "→ Uendret" : `${difference > 0 ? "↑ +" : "↓ "}${difference} pp`;
    return `
      <article class="history-row">
        <div class="history-grade grade-${entry.grade.toLowerCase()}">${entry.grade}</div>
        <div class="history-result"><strong>${entry.percent} %</strong><span>${entry.correct} av ${entry.total} riktige · ${escapeHTML(entry.modeLabel || "Prøve")}</span></div>
        <time datetime="${entry.date}">${escapeHTML(formatHistoryDate(entry.date))}</time>
        <span class="history-change ${direction}">${change}</span>
      </article>
    `;
  }).join("");
}

function submitExam() {
  const unanswered = examAnswers.filter((answer) => answer === null).length;
  if (unanswered && !confirm(`Du har ${unanswered} ubesvarte spørsmål. Vil du levere likevel?`)) return;

  const results = examQuestions.map((question, index) => ({
    question,
    selected: examAnswers[index],
    correct: examAnswers[index] === question.correctIndex,
  }));
  const correct = results.filter((result) => result.correct).length;
  const total = examQuestions.length;
  const percent = Math.round((correct / total) * 100);
  const grade = gradeFor(percent);
  const incorrect = results.filter((result) => !result.correct);
  saveExamResult(correct, total, percent, grade);
  renderHistory();

  $("#exam-session").classList.add("hidden");
  $("#exam-result").classList.remove("hidden");
  $("#history-section").classList.remove("hidden");
  $("#result-grade").textContent = grade;
  $("#result-heading").textContent = grade === "A" ? "Svært solid." : grade === "F" ? "Her er det mye å hente." : "Prøven er gjennomført.";
  $("#result-summary").textContent = `${currentExamMode.label}: Du fikk ${correct} av ${total} riktige og karakter ${grade}. ${incorrect.length ? "Gjennomgå feilene nedenfor før neste forsøk." : "Du besvarte alt riktig."}`;
  $("#correct-count").textContent = correct;
  $("#wrong-count").textContent = total - correct;
  $("#result-percent").textContent = `${percent} %`;
  $("#review-heading").textContent = incorrect.length ? "Spørsmål du bør se på" : "Alle spørsmål var riktige";

  const reviewResults = incorrect.length ? incorrect : results;
  $("#review-list").innerHTML = reviewResults.map((result) => {
    const selectedText = result.selected === null ? "Ikke besvart" : `${"ABCDE"[result.selected]}. ${result.question.choices[result.selected]}`;
    const correctText = `${"ABCDE"[result.question.correctIndex]}. ${result.question.choices[result.question.correctIndex]}`;
    return `
      <article class="review-card ${result.correct ? "correct-review" : ""}">
        <span class="review-meta">${escapeHTML(result.question.topic)} · Oppgave fra spørsmålsbanken #${result.question.id}</span>
        <h3>${escapeHTML(result.question.question)}</h3>
        <div class="review-answer"><span>Ditt svar</span><strong>${escapeHTML(selectedText)}</strong></div>
        <div class="review-answer"><span>Riktig svar</span><strong>${escapeHTML(correctText)}</strong></div>
        <p class="review-explanation">${escapeHTML(result.question.explanation)}</p>
      </article>
    `;
  }).join("");
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function initializeExam() {
  $$("[data-exam-mode]").forEach((button) => button.addEventListener("click", () => startExam(button.dataset.examMode)));
  $("#restart-exam").addEventListener("click", () => startExam(currentExamMode.key));
  $("#exam-prev").addEventListener("click", () => {
    if (examIndex > 0) {
      examIndex -= 1;
      renderExamQuestion();
    }
  });
  $("#exam-next").addEventListener("click", () => {
    if (examIndex < examQuestions.length - 1) {
      examIndex += 1;
      renderExamQuestion();
    }
  });
  $("#submit-exam").addEventListener("click", submitExam);
  $("#clear-history").addEventListener("click", () => {
    if (!confirm("Vil du slette hele testhistorikken?")) return;
    examHistory = [];
    localStorage.removeItem("stv1020-exam-history");
    renderHistory();
  });
}

initializeCards();
initializeExam();
updateProgress();
renderHistory();
showView(window.location.hash.slice(1) || "home", false);
window.addEventListener("hashchange", () => showView(window.location.hash.slice(1), false));
