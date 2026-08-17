document.addEventListener("DOMContentLoaded", () => {
  const API_BASE = "https://askyellow-staging.onrender.com";
  const BASE_PATH = "";

  const messagesDiv = document.getElementById("chatMessages");
  const chatInput = document.getElementById("chatInput");
  const sendBtn = document.getElementById("sendChat");
  const closeBtn = document.getElementById("btn-close");
  const liveAiAvatar = document.getElementById("liveAiAvatar");
  const liveUserAvatar = document.getElementById("liveUserAvatar");
  const liveAvatarDock = document.getElementById("liveAvatarDock");
  const historyBtn = document.getElementById("history-toggle");
  const historySub = document.getElementById("historySub");
  const menuToggle = document.getElementById("menuToggle");
  const appShell = document.getElementById("app-shell");
  const sidebarClose = document.getElementById("sidebarClose");

  const chatImageInput = document.getElementById("chatImageInput");
  const uploadPreview = document.getElementById("uploadPreview");
  const uploadPreviewImg = document.getElementById("uploadPreviewImg");
  const uploadPreviewText = document.getElementById("uploadPreviewText");
  const removeUploadBtn = document.getElementById("removeUploadBtn");

  const imageStore = [];
  let selectedImageFile = null;
  let historyLoadingBubble = null;
  let lastUploadedImageFile = null;
  let imageModal = null;

  const SESSION_KEY = "ay_session_id";
  const chatShell = document.getElementById("chat-shell");
  let dragDepth = 0;

  // =========================
  // SIDEBAR CONTROL
  // =========================
function closeSidebar() {
  appShell.classList.remove("sidebar-open");
}

menuToggle?.addEventListener("click", () => {
  appShell.classList.toggle("sidebar-open");
});

sidebarClose?.addEventListener("click", closeSidebar);



document.querySelectorAll(
  '.sidebar-sub-btn, .sidebar-btn[data-action="images"], .sidebar-btn[data-action="logout"]'
).forEach((btn) => {
  btn.addEventListener("click", closeSidebar);
});

["dragenter", "dragover"].forEach((eventName) => {
  window.addEventListener(eventName, (e) => {
    e.preventDefault();
    e.stopPropagation();
  });
});

["dragleave", "drop"].forEach((eventName) => {
  window.addEventListener(eventName, (e) => {
    e.preventDefault();
    e.stopPropagation();
  });
});

chatShell?.addEventListener("dragenter", (e) => {
  e.preventDefault();
  e.stopPropagation();
  dragDepth++;
  setDropzoneActive(true);
});

chatShell?.addEventListener("dragover", (e) => {
  e.preventDefault();
  e.stopPropagation();
  setDropzoneActive(true);
});

chatShell?.addEventListener("dragleave", (e) => {
  e.preventDefault();
  e.stopPropagation();

  dragDepth--;
  if (dragDepth <= 0) {
    dragDepth = 0;
    setDropzoneActive(false);
  }
});

chatShell?.addEventListener("drop", (e) => {
  e.preventDefault();
  e.stopPropagation();

  dragDepth = 0;
  setDropzoneActive(false);

  const files = e.dataTransfer?.files;
  if (!files || !files.length) return;

  handleDroppedFile(files[0]);
});

  function getSessionId() {
    let sid = localStorage.getItem(SESSION_KEY);
    if (!sid) {
      sid = crypto.randomUUID();
      localStorage.setItem(SESSION_KEY, sid);
    }
    return sid;
  }

  let CURRENT_SESSION = getSessionId();

  function isGuest() {
    return localStorage.getItem("authSession")?.startsWith("guest_");
  }

  function nowTime() {
    return new Date().toLocaleTimeString("nl-NL", {
      hour: "2-digit",
      minute: "2-digit"
    });
  }

  // avatars en realtime interractie

  const AVATAR_MEDIA = {
    yello: {
      idle: "/test/img/yello_lopend_trans.mp4",
      typing: "/test/img/yello_typen_trans.mp4",
      thinking: "/test/img/yello_denkend_trans.mp4",
      image: "/test/img/yello_image_trans.mp4"
    },
    user: {
      idle: "/test/img/yello_lopend_trans.mp4",
      typing: "/test/img/yello_typen_trans.mp4",
      sitting: "/test/img/yello_denkend_trans.mp4"
    }
  };

let currentAvatar = "yello";
let currentState = null;
let currentUserState = null;


  function parkLiveAvatars() {
    if (liveAvatarDock && liveAiAvatar) {
      liveAvatarDock.appendChild(liveAiAvatar);
    }
    if (liveAvatarDock && liveUserAvatar) {
      liveAvatarDock.appendChild(liveUserAvatar);
    }
  }

  function attachAiAvatarToMessage(messageEl) {
    if (!messageEl || !liveAiAvatar) return;
    const slot = messageEl.querySelector(".avatar-slot");
    if (!slot) return;
    slot.appendChild(liveAiAvatar);
  }

  function attachUserAvatarToMessage(messageEl) {
    if (!messageEl || !liveUserAvatar) return;
    const slot = messageEl.querySelector(".avatar-slot");
    if (!slot) return;
    slot.appendChild(liveUserAvatar);
  }

function attachAiAvatarToLastMessage() {
  const messages = document.querySelectorAll(".message.ai");
  const last = messages[messages.length - 1];
  if (!last || !liveAiAvatar) return;

  const slot = last.querySelector(".avatar-slot");
  if (!slot) return;

  slot.appendChild(liveAiAvatar);
}

function attachUserAvatarToLastMessage() {
  const messages = document.querySelectorAll(".message.user");
  const last = messages[messages.length - 1];
  if (!last) return;

  const slot = last.querySelector(".avatar-slot");
  const avatar = document.getElementById("liveUserAvatar");
  if (!slot || !avatar) return;

  slot.appendChild(avatar);
}



function setYello(state) {
  if (!AVATAR_MEDIA[currentAvatar]) return;
  if (!liveAiAvatar) return;

  if (state === currentState) return;

  const src =
    AVATAR_MEDIA[currentAvatar][state] ||
    AVATAR_MEDIA[currentAvatar].idle;

  const currentSrc = liveAiAvatar.getAttribute("src") || "";

  if (!currentSrc.includes(src)) {
    liveAiAvatar.src = src;
    liveAiAvatar.load();
    liveAiAvatar.play().catch(() => {});
  }

  currentState = state;
}

function setUserAvatar(state) {
  const userAvatar = document.getElementById("liveUserAvatar");
  if (!userAvatar || !AVATAR_MEDIA.user) {
    console.log("❌ liveUserAvatar niet gevonden of AVATAR_MEDIA.user ontbreekt");
    return;
  }

  const src = AVATAR_MEDIA.user[state] || AVATAR_MEDIA.user.idle;
  console.log("USER AVATAR STATE =", state, "SRC =", src);

  if (state === currentUserState) return;

  // alleen voor echte <video>
  if (userAvatar.tagName === "VIDEO") {
    userAvatar.pause();

    // GEEN innerHTML leegmaken
    // GEEN removeAttribute("src") meer

    userAvatar.src = src;
    userAvatar.load();
    userAvatar.play().catch((err) => {
      console.log("userAvatar play error:", err);
    });
  } else {
    userAvatar.setAttribute("src", src);
  }

  currentUserState = state;
}

// setTimeout(() => {
//   console.log("TEST 1: sitting");
//   setUserAvatar("sitting");
// }, 1000);

// setTimeout(() => {
//   console.log("TEST 2: idle");
//   setUserAvatar("idle");
// }, 4000);

function isUserImageMarker(content) {
  return typeof content === "string" && content.startsWith("[USER_IMAGE]");
}

function isAiImageMarker(content) {
  return typeof content === "string" && content.startsWith("[IMAGE]");
}

function isImageMarker(content) {
  return isAiImageMarker(content);
}

function extractImageSrc(content) {
  return content.replace("[IMAGE]", "").trim();
}

function isRenderableImageSrc(src) {
  if (!src) return false;

  return (
    src.startsWith("data:image/") ||
    src.startsWith("http://") ||
    src.startsWith("https://") ||
    src.startsWith("/uploads/") ||
    src.startsWith("/img/") ||
    src.startsWith("blob:")
  );
}
function addBubble(content, who = "ai", isHtml = false) {
  const wrapper = document.createElement("div");
  wrapper.className = "message " + (who === "user" ? "user" : "ai");

  const row = document.createElement("div");
  row.className = "message-row";

  const avatarSlot = document.createElement("div");
  avatarSlot.className = "avatar-slot";

  const contentWrap = document.createElement("div");
  contentWrap.className = "message-content";

  const div = document.createElement("div");
  div.className = "bubble " + (who === "user" ? "user" : "ai");

  if (isImageMarker(content)) {
    const src = extractImageSrc(content);

    if (isRenderableImageSrc(src)) {
      const img = document.createElement("img");
      img.src = src;
      img.className = "chat-image";
      img.style.maxWidth = "280px";
      img.style.borderRadius = "14px";
      img.style.cursor = "pointer";
      img.onclick = () => window.open(img.src, "_blank");
      div.appendChild(img);

      imageStore.push({
        url: src,
        createdAt: new Date().toISOString()
      });
    } else {
      div.textContent = src || "Geüploade afbeelding";
    }
  } else if (isHtml) {
    div.innerHTML = content;
  } else {
    div.textContent = content;
  }

  const time = document.createElement("div");
  time.className = "timestamp";
  time.textContent = nowTime();

  contentWrap.appendChild(div);
  contentWrap.appendChild(time);

  if (who === "user") {
    row.appendChild(contentWrap);
    row.appendChild(avatarSlot);
  } else {
    row.appendChild(avatarSlot);
    row.appendChild(contentWrap);
  }

  wrapper.appendChild(row);
  messagesDiv.appendChild(wrapper);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;

  return wrapper;
}

  function showGuestWelcome() {
    parkLiveAvatars();
    parkLiveAvatars();
  messagesDiv.innerHTML = "";
    addBubble(
      "👋 Welkom bij YellowMind!\n\n" +
      "Je chat nu als gast. Dit gesprek wordt niet opgeslagen.\n\n" +
      "✨ Tip: maak gratis een account aan om je gesprekken te bewaren en afbeeldingen te genereren.",
      "ai"
    );
    attachAiAvatarToLastMessage();
  }

  function formatHistoryLabel(dateStr) {
  const d = new Date(dateStr);
  const today = new Date();
  const yesterday = new Date();
  yesterday.setDate(today.getDate() - 1);

  const iso = d.toISOString().slice(0, 10);
  const todayIso = today.toISOString().slice(0, 10);
  const yesterdayIso = yesterday.toISOString().slice(0, 10);

  if (iso === todayIso) return "Vandaag";
  if (iso === yesterdayIso) return "Gisteren";

  return d.toLocaleDateString("nl-NL", {
    weekday: "long",
    day: "numeric",
    month: "long"
  });
}

  function renderHistoryButtons(days) {
    if (!historySub) return;

    historySub.innerHTML = "";

    if (!days || !days.length) {
      const empty = document.createElement("div");
      empty.className = "history-empty";
      empty.textContent = "Nog geen eerdere gesprekken";
      historySub.appendChild(empty);
      return;
    }

    days.forEach((day) => {
      const btn = document.createElement("button");
      btn.className = "sidebar-sub-btn";
      btn.dataset.action = "history";
      btn.dataset.day = day;
      btn.textContent = formatHistoryLabel(day);

      btn.addEventListener("click", () => {
        loadChatHistory(day);
        closeSidebar();
      });

      historySub.appendChild(btn);
    });
  }

  function openImageModal(url) {
  if (!imageModal) {
    imageModal = document.createElement("div");
    imageModal.className = "image-modal";
    document.body.appendChild(imageModal);
  }

  imageModal.innerHTML = `
    <div class="image-modal-inner">
      <img src="${url}" class="image-modal-img"/>
      <div class="image-modal-actions">
        <button id="downloadImageBtn">⬇️ Download</button>
        <button id="closeImageModal">✖</button>
      </div>
    </div>
  `;

  imageModal.style.display = "flex";

  document.getElementById("closeImageModal").onclick = () => {
    imageModal.style.display = "none";
  };

  document.getElementById("downloadImageBtn").onclick = async () => {
    const res = await fetch(`${API_BASE}/images/download`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        session_id: getSessionId(),
        image_url: url
      })
    });

    const data = await res.json();

    if (!data.allowed) {
      alert("⚠️ Download limiet bereikt (free account)");
      return;
    }

    const link = document.createElement("a");
    link.href = url;
    link.download = "yellowmind-image.jpg";
    link.click();
  };
}
async function loadChatHistory(day = "today") {
  if (isGuest()) return;

  const session_id = getSessionId();
  parkLiveAvatars();
  messagesDiv.innerHTML = "";
  showHistoryLoading();

  try {
    let url = `${API_BASE}/chat/history?session_id=${encodeURIComponent(session_id)}`;

    if (day) {
      url += `&day=${encodeURIComponent(day)}`;
    }

    const res = await fetch(url);
    const data = await res.json();
    removeHistoryLoading();

    let messages = [];

    if (day === "today") {
      messages = data.today || data.messages || [];
    } else if (day === "yesterday") {
      messages = data.yesterday || data.messages || [];
    } else {
      messages = data.messages || [];
    }

    if (messages.length > 0) {
      messages.forEach((msg) => {
        if (typeof msg.content === "string" && msg.content.startsWith("[USER_IMAGE]")) {
          return;
        }

        addBubble(
          msg.content || "",
          msg.role === "user" ? "user" : "ai"
        );
      });
    } else if (day === "today" && data.welcome) {
      addBubble(data.welcome, "ai");
    } else {
      addBubble("Nog geen gesprekken op deze datum.", "ai");
    }

    attachUserAvatarToLastMessage();
    attachAiAvatarToLastMessage();
  } catch (err) {
    console.error("History load failed:", err);
    removeHistoryLoading();
    addBubble("⚠️ Geschiedenis laden is mislukt.", "ai");
  }
}

async function loadHistoryDays() {
  if (isGuest()) return;

  const session_id = getSessionId();

  try {
    const res = await fetch(
      `${API_BASE}/chat/history?session_id=${encodeURIComponent(session_id)}&day=list`
    );
    const data = await res.json();

    renderHistoryButtons(data.available_days || []);
  } catch (err) {
    console.error("History days load failed:", err);
    if (historySub) {
      historySub.innerHTML = `<div class="history-empty">⚠️ Datums laden mislukt</div>`;
    }
  }
}

function formatHistoryLabel(dateStr) {
  const d = new Date(dateStr);
  const today = new Date();
  const yesterday = new Date();
  yesterday.setDate(today.getDate() - 1);

  const iso = d.toISOString().slice(0, 10);
  const todayIso = today.toISOString().slice(0, 10);
  const yesterdayIso = yesterday.toISOString().slice(0, 10);

  if (iso === todayIso) return "Vandaag";
  if (iso === yesterdayIso) return "Gisteren";

  return d.toLocaleDateString("nl-NL", {
    weekday: "long",
    day: "numeric",
    month: "long"
  });
}

function renderHistoryButtons(days) {
  if (!historySub) return;

  historySub.innerHTML = "";

  if (!days.length) {
    historySub.innerHTML = `<div class="history-empty">Nog geen eerdere gesprekken</div>`;
    return;
  }

  days.forEach((day) => {
    const btn = document.createElement("button");
    btn.className = "sidebar-sub-btn";
    btn.dataset.action = "history";
    btn.dataset.day = day;
    btn.textContent = formatHistoryLabel(day);

    btn.addEventListener("click", () => {
      loadChatHistory(day);
      closeSidebar();
    });

    historySub.appendChild(btn);
  });
}

function showHistoryLoading(text = "🕘 Geschiedenis wordt opgehaald, moment geduld…") {
  historyLoadingBubble = document.createElement("div");
  historyLoadingBubble.className = "message ai message-loading";

  const row = document.createElement("div");
  row.className = "message-row";

  const avatarSlot = document.createElement("div");
  avatarSlot.className = "avatar-slot";

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;

  row.appendChild(avatarSlot);
  row.appendChild(bubble);

  historyLoadingBubble.appendChild(row);
  messagesDiv.appendChild(historyLoadingBubble);

  attachAiAvatarToMessage(historyLoadingBubble);
}

  function removeHistoryLoading() {
    if (historyLoadingBubble) {
      historyLoadingBubble.remove();
      historyLoadingBubble = null;
    }
  }

  function isRememberedImageQuestion(text) {
  const q = (text || "").toLowerCase().trim();

    if (!lastUploadedImageFile) return false;
    if (!q) return false;

    // Eerst text-to-image uitsluiten
    if (isTextToImagePrompt(q)) return false;

    // Analyse / verwijzing naar bestaande afbeelding
    const analysisSignals = [
      "genereer een afbeelding",
    "genereer afbeelding",
    "afbeelding genereren",
    "afbeeldingen genereren",
    "kun je een afbeelding maken",
    "kun je afbeeldingen maken",
    "maak een afbeelding",
    "maak afbeelding",
    "maak een plaatje",
    "maak een foto",
    "laat een afbeelding zien",
    "laat eens zien",
    "teken",
    "illustratie",
    "genereer een",
    "afbeelding van",
    "plaatje van",
    "foto van",
    "logo maken",
    "banner maken",
    "avatar maken"
    ];

    if (analysisSignals.some(t => q.includes(t))) {
      return true;
    }

    // Editvragen op bestaande afbeelding
    if (isUploadEditPrompt(q)) {
      return true;
    }

    return false;
  }



function clearSelectedImage() {
  selectedImageFile = null;

  if (chatImageInput) chatImageInput.value = "";
  if (uploadPreview) uploadPreview.style.display = "none";
  if (uploadPreviewImg) uploadPreviewImg.src = "";
  if (uploadPreviewText) uploadPreviewText.textContent = "Afbeelding geselecteerd";
}

    function showSelectedImagePreview(file) {
    console.log("🖼️ showSelectedImagePreview called:", file);

    if (!file) return;

    const objectUrl = URL.createObjectURL(file);
    console.log("🔗 preview objectUrl:", objectUrl);
    console.log("uploadPreview =", uploadPreview);
    console.log("uploadPreviewImg =", uploadPreviewImg);
    console.log("uploadPreviewText =", uploadPreviewText);

    if (uploadPreviewImg) {
        uploadPreviewImg.src = objectUrl;
    }

    if (uploadPreviewText) {
        uploadPreviewText.textContent = file.name;
    }

    if (uploadPreview) {
        uploadPreview.style.display = "flex";
        uploadPreview.style.alignItems = "center";
        uploadPreview.style.gap = "12px";
    }
    }

    function setDropzoneActive(active) {
    if (!chatShell) return;
    chatShell.classList.toggle("drag-active", active);
  }

    function handleDroppedFile(file) {
    console.log("📥 handleDroppedFile called:", file);

    if (!file) {
        console.log("⛔ geen file ontvangen");
        return;
    }

    const allowed = ["image/jpeg", "image/png", "image/webp"];
    if (!allowed.includes(file.type)) {
        console.log("⛔ ongeldig filetype:", file.type);
        alert("Alleen JPG, PNG en WEBP zijn toegestaan.");
        clearSelectedImage();
        return;
    }

    selectedImageFile = file;
    lastUploadedImageFile = file;

    console.log("✅ selectedImageFile gezet:", selectedImageFile);
    console.log("✅ lastUploadedImageFile gezet:", lastUploadedImageFile);

    showSelectedImagePreview(file);
    }


    function isUploadEditPrompt(text) {
    const q = (text || "").toLowerCase();
    const triggers = [
        "karikatuur",
        "cartoon",
        "anime",
        "ghibli",
        "bewerk",
        "bewerken",
        "edit",
        "verander",
        "veranderen",
        "transformeer",
        "transformeren",
        "stijl",
        "pas aan",
        "achtergrond",
        "verwijder",
        "weghalen",
        "haal",
        "eruit halen",
        "uitknippen",
        "losmaken",
        "apart zetten",
        "apart in een afbeelding",
        "vrijstaand",
        "maak hiervan",
        "maak hier",
        "van maken"
    ];
    
    return triggers.some(t => q.includes(t));
    }

async function showImagesView() {
  parkLiveAvatars();
  messagesDiv.innerHTML = "";
  showHistoryLoading("🖼️ Afbeeldingen worden opgehaald, moment geduld…");

  try {
    const res = await fetch(
      `${API_BASE}/images/library?session_id=${getSessionId()}`
    );

    const data = await res.json();
    const images = data.images || [];

    removeHistoryLoading();

    const block = document.createElement("div");
    block.className = "images-view";

    const grid = document.createElement("div");
    grid.className = "images-grid";

    if (!images.length) {
      grid.innerHTML = "<div>Geen afbeeldingen</div>";
    } else {
      images.forEach(imgObj => {
        const img = document.createElement("img");
        img.src = imgObj.url;
        img.className = "image-thumb";
        img.onclick = () => openImageModal(imgObj.url);
        grid.appendChild(img);
      });
    }

    block.appendChild(grid);
    messagesDiv.appendChild(block);
  } catch (err) {
    console.error("Images load failed:", err);
    removeHistoryLoading();
    addBubble("⚠️ Afbeeldingen laden mislukt.", "ai");
  }
}


function openImageModal(url) {
  if (!imageModal) {
    imageModal = document.createElement("div");
    imageModal.className = "image-modal";
    document.body.appendChild(imageModal);
  }

  imageModal.innerHTML = `
    <div class="image-modal-inner">
      <img src="${url}" class="image-modal-img"/>
      <div class="image-modal-actions">
        <button id="downloadBtn">⬇️ Download</button>
        <button id="closeBtn">✖</button>
      </div>
    </div>
  `;

  imageModal.style.display = "flex";

  document.getElementById("closeBtn").onclick = () => {
    imageModal.style.display = "none";
  };

  document.getElementById("downloadBtn").onclick = async () => {
    const res = await fetch(`${API_BASE}/images/download`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        session_id: getSessionId(),
        image_url: url
      })
    });

    const data = await res.json();

    if (!data.allowed) {
      alert("⚠️ Free limiet bereikt");
      return;
    }

    const a = document.createElement("a");
    a.href = url;
    a.download = "yellowmind.jpg";
    a.click();
  };
}


  function isTextToImagePrompt(text) {
    const q = (text || "").toLowerCase();
    const triggers = [
      "genereer",
      "maak een afbeelding",
      "maak een plaatje",
      "teken",
      "illustratie",
      "genereer een"
    ];
    return triggers.some(t => q.includes(t));
  }

  async function sendPlainChat(text) {
    const res = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: text,
        session_id: CURRENT_SESSION,
        language: "nl",
        wants_image: isTextToImagePrompt(text)
      })
    });

    return await res.json();
  }

  async function sendImageChat(text, file) {
    const formData = new FormData();
    formData.append("session_id", CURRENT_SESSION);
    formData.append("message", text || "");
    formData.append("file", file);

    const res = await fetch(`${API_BASE}/chat/image`, {
      method: "POST",
      body: formData
    });

    return await res.json();
  }

async function loadImages() {
  if (isGuest()) return;

  const session_id = getSessionId();
  messagesDiv.innerHTML = "";
  showHistoryLoading();

  try {
    const res = await fetch(
      `${API_BASE}/chat/history?session_id=${encodeURIComponent(session_id)}&day=images`
    );
    const data = await res.json();
    removeHistoryLoading();

    const images = data.images || [];
    let renderedCount = 0;

    if (!images.length) {
      addBubble("Nog geen afbeeldingen gevonden.", "ai");
      return;
    }

    images.forEach((img) => {
      const raw = (img.content || "").replace("[USER_IMAGE]", "").trim();

      const isUsableImage =
        raw.startsWith("http") ||
        raw.startsWith("/") ||
        raw.startsWith("data:image/");

      if (!isUsableImage) {
        return;
      }

      const url =
        raw.startsWith("http") || raw.startsWith("data:image/")
          ? raw
          : `${API_BASE}${raw}`;

      const wrapper = document.createElement("div");
      wrapper.className = "image-history-item";

      const image = document.createElement("img");
      image.src = url;
      image.className = "chat-image";
      image.alt = "Opgeslagen afbeelding";

      wrapper.appendChild(image);
      messagesDiv.appendChild(wrapper);
      renderedCount++;
    });

    if (renderedCount === 0) {
      addBubble("Er zijn afbeeldings-items gevonden, maar geen toonbare afbeeldingen.", "ai");
    }
  } catch (err) {
    console.error("Image load failed:", err);
    removeHistoryLoading();
    addBubble("⚠️ Afbeeldingen laden mislukt.", "ai");
  }
}

function formatHistoryLabel(dateStr) {
  const d = new Date(dateStr);
  const today = new Date();
  const yesterday = new Date();
  yesterday.setDate(today.getDate() - 1);

  const iso = d.toISOString().slice(0, 10);
  const todayIso = today.toISOString().slice(0, 10);
  const yesterdayIso = yesterday.toISOString().slice(0, 10);

  if (iso === todayIso) return "Vandaag";
  if (iso === yesterdayIso) return "Gisteren";

  return d.toLocaleDateString("nl-NL", {
    weekday: "long",
    day: "numeric",
    month: "long"
  });
}

function renderHistoryButtons(days) {
  if (!historySub) return;

  historySub.innerHTML = "";

  if (!days.length) {
    historySub.innerHTML = `<div class="history-empty">Nog geen eerdere gesprekken</div>`;
    return;
  }

  days.forEach((day) => {
    const btn = document.createElement("button");
    btn.className = "sidebar-sub-btn";
    btn.dataset.action = "history";
    btn.dataset.day = day;
    btn.textContent = formatHistoryLabel(day);

    btn.addEventListener("click", () => {
      loadChatHistory(day);
      closeSidebar();
    });

    historySub.appendChild(btn);
  });
}  

async function sendChatMessage() {
  const text = chatInput.value.trim();
  console.log("📨 sendChatMessage text =", text);
  console.log("📨 selectedImageFile =", selectedImageFile);
  console.log("📨 lastUploadedImageFile =", lastUploadedImageFile);

  const hasFreshUpload = !!selectedImageFile;
  const wantsNewGeneratedImage = isTextToImagePrompt(text);
  const wantsRememberedImage = isRememberedImageQuestion(text);

  const imageFileForRequest = hasFreshUpload
    ? selectedImageFile
    : (wantsRememberedImage ? lastUploadedImageFile : null);

  if (!text && !imageFileForRequest) return;

  const userTextBubble = addBubble(text || "🖼️ Afbeelding geüpload", "user");
  attachUserAvatarToMessage(userTextBubble);
  chatInput.value = "";

  if (selectedImageFile) {
    const previewUrl = URL.createObjectURL(selectedImageFile);
    const userImageBubble = addBubble("[IMAGE]" + previewUrl, "user");
    attachUserAvatarToMessage(userImageBubble);
  }

  setYello(imageFileForRequest || wantsNewGeneratedImage ? "image" : "thinking");
  setUserAvatar("sitting");
  attachUserAvatarToLastMessage();

  const thinkingText = imageFileForRequest
    ? (selectedImageFile
        ? (isUploadEditPrompt(text)
            ? "🖼️ Ik ben je afbeelding aan het bewerken…"
            : "👀 Ik kijk even naar je afbeelding…")
        : (isUploadEditPrompt(text)
            ? "🖼️ Ik gebruik je laatst geüploade afbeelding en ga hem bewerken…"
            : "👀 Ik gebruik je laatst geüploade afbeelding…"))
    : (wantsNewGeneratedImage
        ? "🖼️ Ik ben een afbeelding voor je aan het maken…"
        : "Aan het denken…");

  const thinkingBubble = addBubble(thinkingText, "ai");
  attachAiAvatarToMessage(thinkingBubble);

  try {
    let data;

    if (imageFileForRequest) {
      console.log("🚀 sendImageChat()");
      data = await sendImageChat(text, imageFileForRequest);
    } else {
      console.log("🚀 sendPlainChat()");
      data = await sendPlainChat(text);
    }

    thinkingBubble.remove();

    setYello("typing");

    if (data.type === "image" && data.url) {
      if (data.reply) {
        const replyBubble = addBubble(data.reply, "ai");
        attachAiAvatarToMessage(replyBubble);
      }
      const imageBubble = addBubble("[IMAGE]" + data.url, "ai");
      attachAiAvatarToMessage(imageBubble);
    } else if (data.type === "vision") {
      const replyBubble = addBubble(data.reply || "⚠️ Geen analyse teruggekregen.", "ai");
      attachAiAvatarToMessage(replyBubble);
    } else if (data.type === "search") {
      const searchBubble = addBubble("🔍 Ik ga dit voor je opzoeken…", "ai");
      attachAiAvatarToMessage(searchBubble);
      window.location.href = `${BASE_PATH}/search.html?q=${encodeURIComponent(data.query)}`;
      return;
    } else {
      const replyBubble = addBubble(data.reply || "⚠️ Geen antwoord", "ai");
      attachAiAvatarToMessage(replyBubble);
    }
  } catch (err) {
    console.error(err);
    thinkingBubble.remove();
    const errorBubble = addBubble("⚠️ Er ging iets mis.", "ai");
    attachAiAvatarToMessage(errorBubble);
  } finally {
    clearSelectedImage();

    setTimeout(() => {
      setYello("idle");
      setUserAvatar("idle");
    }, 1200);

    chatInput.focus();
  }
}

  chatImageInput?.addEventListener("change", (e) => {
    const file = e.target.files?.[0];
    handleDroppedFile(file);
  });

  removeUploadBtn?.addEventListener("click", () => {
    clearSelectedImage();
  });

  sendBtn?.addEventListener("click", sendChatMessage);

chatInput?.addEventListener("input", () => {
  const hasText = chatInput.value.trim().length > 0;

  if (hasText) {
    setUserAvatar("typing");
  } else {
    setUserAvatar("idle");
  }
});


  chatInput?.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      sendChatMessage();
    }
  });

  closeBtn?.addEventListener("click", () => {
    window.location.href = `${BASE_PATH}/index.html`;
  });

historyBtn?.addEventListener("click", async (e) => {
  e.stopPropagation();

  const willOpen = !historySub.classList.contains("open");

  if (willOpen) {
    await loadHistoryDays();
  }

  historySub.classList.toggle("open");
});

  document.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-action]");
    if (!btn) return;

    const action = btn.dataset.action;

    if (action === "images") {
      e.preventDefault();
      showImagesView();
      closeSidebar();
      return;
    }

    const accountBtn = document.querySelector('.sidebar-btn[data-action="account"]');
    const session = localStorage.getItem("authSession");

    if (accountBtn) {
      if (!session || session.startsWith("guest_")) {
        accountBtn.querySelector("span").textContent = "Inloggen";
      } else {
        const name = localStorage.getItem("authUserName");
        if (name) {
          accountBtn.querySelector("span").textContent = name;
        }
      }
    }

    if (action === "logout") {
      e.preventDefault();

      fetch(`${API_BASE}/auth/logout`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: getSessionId() })
      }).finally(() => {
        localStorage.clear();
        window.location.href = `${BASE_PATH}/index.html`;
      });
    }
  });

  if (isGuest()) {
    showGuestWelcome();
    setYello("idle");
    setUserAvatar("idle");
  } else {
    loadChatHistory("today");
    setYello("idle");
    setUserAvatar("idle");
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const accountBtn = document.querySelector('.sidebar-btn[data-action="account"]');

  if (accountBtn) {
    accountBtn.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();

      const session = localStorage.getItem("authSession");

      if (!session || session.startsWith("guest_")) {
        window.location.href = "/test/login.html";
        return;
      }

      window.location.href = "/test/account.html";
    });
  }
});
