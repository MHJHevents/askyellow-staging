const API_BASE = "https://askyellow-staging.onrender.com";

const searchInput = document.getElementById("searchInput");
const answerBox = document.getElementById("answerBox");
const answerText = document.getElementById("answerText");
const webBlock = document.getElementById("webResults");
const webList = document.getElementById("webList");
const shopSection = document.getElementById("shopResults");
const kbSection = document.getElementById("kbResults");
const affiliateBox = document.getElementById("affiliateBox");
const searchActions = document.getElementById("searchActions");
const btnRefine = document.getElementById("btnRefine");
const btnNewSearch = document.getElementById("btnNewSearch");
const searchCloseBtn = document.getElementById("searchCloseBtn");

function getOrCreateFlowId() {
  let flowId = sessionStorage.getItem("shopper_flow_id");
  if (!flowId) {
    flowId = crypto.randomUUID();
    sessionStorage.setItem("shopper_flow_id", flowId);
  }
  return flowId;
}

function resetFlow() {
  const flowId = crypto.randomUUID();
  sessionStorage.setItem("shopper_flow_id", flowId);
  return flowId;
}

function clearResults() {
  if (answerText) answerText.textContent = "";
  if (answerBox) answerBox.style.display = "none";
  if (webBlock) webBlock.style.display = "none";
  if (webList) webList.innerHTML = "";
  if (shopSection) shopSection.style.display = "none";
  if (kbSection) kbSection.style.display = "none";
  if (affiliateBox) affiliateBox.style.display = "none";
  if (searchActions) searchActions.style.display = "none";
}

function showAnswer(text) {
  if (answerBox) answerBox.style.display = "block";
  if (answerText) answerText.textContent = text;
}

function showActions() {
  if (searchActions) searchActions.style.display = "flex";
}

function renderWebResults(results) {
  if (!webBlock || !webList) return;

  webBlock.style.display = "block";
  webList.innerHTML = "";

  if (!Array.isArray(results) || results.length === 0) {
    const empty = document.createElement("div");
    empty.className = "web-item";
    empty.textContent = "Geen actuele webresultaten gevonden.";
    webList.appendChild(empty);
    return;
  }

  results.forEach((result) => {
    const item = document.createElement("div");
    item.className = "web-item";

    const title = document.createElement("a");
    title.className = "web-title";
    title.textContent = result.title || "Resultaat";
    title.href = result.url || "#";
    title.target = "_blank";
    title.rel = "noopener noreferrer";

    const snippet = document.createElement("div");
    snippet.className = "result-snippet";
    snippet.textContent = result.snippet || "";

    const url = document.createElement("div");
    url.className = "result-url";
    url.textContent = result.url || "";

    item.appendChild(title);
    if (result.snippet) item.appendChild(snippet);
    if (result.url) item.appendChild(url);
    webList.appendChild(item);
  });
}

async function callShopper(query) {
  const response = await fetch(`${API_BASE}/shopper/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      session_id: getOrCreateFlowId(),
      query
    })
  });

  if (!response.ok) {
    throw new Error(`Shopper analyze failed: ${response.status}`);
  }

  return await response.json();
}

async function fetchRealWebResults(query) {
  const response = await fetch(`${API_BASE}/tool/websearch`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query })
  });

  if (!response.ok) {
    throw new Error(`Websearch failed: ${response.status}`);
  }

  return await response.json();
}

async function runSearch() {
  const query = (searchInput?.value || "").trim();
  if (!query) return;

  if (answerBox) answerBox.style.display = "block";
  if (answerText) answerText.textContent = "Even kijken…";
  if (webBlock) webBlock.style.display = "none";
  if (searchActions) searchActions.style.display = "none";

  try {
    const decision = await callShopper(query);

    if (decision.action === "ask") {
      showAnswer(decision.question || "Kun je één belangrijk detail toevoegen?");
      if (searchInput) {
        searchInput.value = "";
        searchInput.focus();
      }
      return;
    }

    if (decision.action === "search") {
      const searchQuery = decision.query || query;
      showAnswer(`Ik zoek nu gericht naar: ${searchQuery}`);

      const webData = await fetchRealWebResults(searchQuery);
      renderWebResults(webData.results || []);
      showActions();

      if (searchInput) {
        searchInput.value = "";
        searchInput.focus();
      }
      return;
    }

    showAnswer("Ik kan deze zoekopdracht nog niet goed verwerken.");
  } catch (error) {
    console.error("Shopper flow error:", error);
    showAnswer("Oeps, het zoeken ging even mis. Probeer het nog eens.");
  }
}

btnRefine?.addEventListener("click", () => {
  if (searchActions) searchActions.style.display = "none";
  if (searchInput) {
    searchInput.placeholder = "Waar wil je verder op verfijnen?";
    searchInput.focus();
  }
});

btnNewSearch?.addEventListener("click", () => {
  resetFlow();
  clearResults();
  if (searchInput) {
    searchInput.value = "";
    searchInput.placeholder = "Waar ben je naar op zoek?";
    searchInput.focus();
  }
});

searchCloseBtn?.addEventListener("click", () => {
  resetFlow();
  clearResults();
  if (searchInput) {
    searchInput.value = "";
    searchInput.focus();
  }
});

window.runSearch = runSearch;

const initialQuery = new URLSearchParams(window.location.search).get("q");
if (initialQuery && searchInput) {
  searchInput.value = initialQuery;
  runSearch();
}
