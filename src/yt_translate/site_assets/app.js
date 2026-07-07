"use strict";

const STORAGE = {
  fontSize: "yt.fontSize",
  lastArticle: "yt.lastArticle",
};

function articleStorage(key) {
  return { bookmark: `yt.${key}.bookmark` };
}

let DATA = null;
let currentArticle = null;

// --- Data helpers ---

function findParagraph(paragraphId) {
  if (!currentArticle) return null;
  for (const para of currentArticle.paragraphs) {
    if (para.id === paragraphId) return para;
  }
  return null;
}

// --- Bookmarks ---

function loadBookmark() {
  if (!currentArticle) return null;
  const raw = localStorage.getItem(articleStorage(currentArticle.key).bookmark);
  if (!raw) return null;
  try { return JSON.parse(raw); } catch { return null; }
}

function saveBookmark(paragraphId) {
  if (!currentArticle) return;
  localStorage.setItem(
    articleStorage(currentArticle.key).bookmark,
    JSON.stringify({ paragraphId, ts: Date.now() })
  );
  refreshResumeButton();
  applyBookmarkHighlight();
}

function refreshResumeButton() {
  const button = document.getElementById("resume");
  const bookmark = loadBookmark();
  if (!bookmark) { button.hidden = true; return; }
  const found = findParagraph(bookmark.paragraphId);
  if (!found) { button.hidden = true; return; }
  button.hidden = false;
  button.textContent = "Resume reading";
}

function applyBookmarkHighlight() {
  document.querySelectorAll(".paragraph.bookmarked").forEach(el =>
    el.classList.remove("bookmarked")
  );
  const bookmark = loadBookmark();
  if (!bookmark) return;
  const el = document.querySelector(`.paragraph[data-pid="${bookmark.paragraphId}"]`);
  if (el) el.classList.add("bookmarked");
}

// --- Sidebar ---

function buildArticleNav() {
  const nav = document.getElementById("article-nav");
  nav.innerHTML = "";

  for (const article of DATA.articles) {
    const btn = document.createElement("button");
    btn.className = "article-link";
    btn.dataset.articleKey = article.key;
    const titleSpan = document.createElement("span");
    titleSpan.className = "article-title";
    titleSpan.textContent = article.title;
    const dateSpan = document.createElement("span");
    dateSpan.className = "article-date";
    dateSpan.textContent = article.date;
    btn.appendChild(titleSpan);
    btn.appendChild(dateSpan);
    btn.addEventListener("click", () => {
      selectArticle(article.key);
      closeSidebarOnMobile();
    });
    nav.appendChild(btn);
  }
}

// --- Article selection ---

function selectArticle(key) {
  const article = DATA.articles.find(a => a.key === key);
  if (!article) return;

  currentArticle = article;
  localStorage.setItem(STORAGE.lastArticle, key);

  // Mark active in sidebar
  document.querySelectorAll(".article-link.active").forEach(el => el.classList.remove("active"));
  const activeBtn = document.querySelector(`.article-link[data-article-key="${key}"]`);
  if (activeBtn) {
    activeBtn.classList.add("active");
    activeBtn.scrollIntoView({ block: "nearest" });
  }

  renderArticle();
  refreshResumeButton();
}

// --- Render ---

function renderArticle() {
  if (!currentArticle) return;

  const reader = document.getElementById("reader");
  const root = document.createElement("div");
  root.className = "article";

  // Header
  const header = document.createElement("div");
  header.className = "article-header";
  const h2 = document.createElement("h2");
  h2.textContent = currentArticle.title;
  header.appendChild(h2);
  const meta = document.createElement("div");
  meta.className = "meta";
  meta.textContent = `${currentArticle.date} · `;
  const ytLink = document.createElement("a");
  ytLink.textContent = "YouTube";
  ytLink.rel = "noopener";
  ytLink.target = "_blank";
  // Only allow https:// URLs to prevent javascript: injection
  const src = currentArticle.source || "";
  ytLink.href = src.startsWith("https://") ? src : "#";
  meta.appendChild(ytLink);
  header.appendChild(meta);
  root.appendChild(header);

  // Paragraphs
  for (const para of currentArticle.paragraphs) {
    const block = document.createElement("div");
    block.className = "paragraph";
    block.dataset.pid = para.id;

    if (para.en) {
      const en = document.createElement("p");
      en.className = "en";
      en.textContent = para.en;
      block.appendChild(en);
    }

    if (para.zh) {
      const zh = document.createElement("p");
      zh.className = "zh";
      zh.textContent = para.zh;
      block.appendChild(zh);
    }

    block.addEventListener("click", () => saveBookmark(para.id));
    root.appendChild(block);
  }

  reader.innerHTML = "";
  reader.appendChild(root);
  applyBookmarkHighlight();
  window.scrollTo({ top: 0, behavior: "instant" });
}

// --- Navigation ---

function jumpToBookmark() {
  const bookmark = loadBookmark();
  if (!bookmark) return;
  const el = document.querySelector(`.paragraph[data-pid="${bookmark.paragraphId}"]`);
  if (el) el.scrollIntoView({ behavior: "smooth", block: "center" });
}

// --- Font size ---

function setFontSize(px) {
  const clamped = Math.max(13, Math.min(24, px));
  document.documentElement.style.setProperty("--base-font", clamped + "px");
  localStorage.setItem(STORAGE.fontSize, String(clamped));
}

function loadFontSize() {
  const raw = localStorage.getItem(STORAGE.fontSize);
  if (raw) setFontSize(parseInt(raw, 10));
}

function currentFontSize() {
  const raw = localStorage.getItem(STORAGE.fontSize);
  return raw ? parseInt(raw, 10) : 17;
}

// --- Mobile ---

function closeSidebarOnMobile() {
  if (window.matchMedia("(max-width: 768px)").matches) {
    document.getElementById("sidebar").classList.remove("open");
  }
}

// --- Init ---

function setupControls() {
  document.getElementById("resume").addEventListener("click", jumpToBookmark);
  document.getElementById("font-up").addEventListener("click", () => setFontSize(currentFontSize() + 1));
  document.getElementById("font-down").addEventListener("click", () => setFontSize(currentFontSize() - 1));
  document.getElementById("menu-toggle").addEventListener("click", () => {
    document.getElementById("sidebar").classList.toggle("open");
  });
}

async function main() {
  loadFontSize();
  setupControls();

  try {
    const resp = await fetch("data/articles.json");
    DATA = await resp.json();
  } catch {
    document.getElementById("reader").innerHTML =
      `<p style="color: var(--muted)">Failed to load articles.</p>`;
    return;
  }

  if (DATA.articles.length === 0) {
    document.getElementById("reader").innerHTML =
      `<p style="color: var(--muted)">No articles yet.</p>`;
    return;
  }

  buildArticleNav();

  // Restore last article or default to first
  const last = localStorage.getItem(STORAGE.lastArticle);
  const initial = DATA.articles.find(a => a.key === last) ? last : DATA.articles[0].key;
  selectArticle(initial);
}

main();
