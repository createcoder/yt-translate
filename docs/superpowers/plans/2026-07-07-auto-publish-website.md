# Auto-Publish Website Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend yt-translate to auto-publish translated articles to a static website on GitHub Pages after each translation run.

**Architecture:** A markdown parser converts `articles/*.md` files into `site/data/articles.json`. The site is a single-page app (HTML/CSS/JS, no framework) adapted from the raja-yoga project. The CLI gains a build+publish step after translation.

**Tech Stack:** Python 3.10+, Click CLI, static HTML/CSS/JS (no build tools), GitHub Pages

## Global Constraints

- Python >= 3.10, no new runtime dependencies (uses stdlib only for build/publish)
- Site must work as a static file (no server required for reading)
- All existing tests must continue to pass
- Commit style: `feat:`, `fix:`, `chore:` prefixes

---

### Task 1: Markdown Article Parser

**Files:**
- Create: `src/yt_translate/parser.py`
- Test: `tests/test_parser.py`

**Interfaces:**
- Consumes: Markdown file content (string) — the `_zh.md` format produced by `formatter.py`
- Produces: `parse_article(text: str) -> dict` returning `{"title": str, "source": str, "date": str, "paragraphs": [{"id": str, "en": str, "zh": str}]}`

- [ ] **Step 1: Write the failing tests**

```python
"""Tests for the article markdown parser."""

import pytest
from yt_translate.parser import parse_article


SAMPLE_ARTICLE = """\
# Test Article Title

**Original Title:** Test Article Title
**Source:** https://www.youtube.com/watch?v=abc123
**Translated:** 2026-06-29

---

> First English paragraph.

第一段中文翻译。

---

> Second English paragraph.

第二段中文翻译。
"""

SAMPLE_BARE_ID = """\
# Another Article

**Original Title:** Another Article
**Source:** eg096o07w9o
**Translated:** 2026-07-07

---

> Hello world.

你好世界。
"""


class TestParseArticle:
    def test_extracts_title(self):
        result = parse_article(SAMPLE_ARTICLE)
        assert result["title"] == "Test Article Title"

    def test_extracts_source_url(self):
        result = parse_article(SAMPLE_ARTICLE)
        assert result["source"] == "https://www.youtube.com/watch?v=abc123"

    def test_extracts_date(self):
        result = parse_article(SAMPLE_ARTICLE)
        assert result["date"] == "2026-06-29"

    def test_extracts_paragraphs(self):
        result = parse_article(SAMPLE_ARTICLE)
        assert len(result["paragraphs"]) == 2
        assert result["paragraphs"][0]["en"] == "First English paragraph."
        assert result["paragraphs"][0]["zh"] == "第一段中文翻译。"
        assert result["paragraphs"][1]["en"] == "Second English paragraph."
        assert result["paragraphs"][1]["zh"] == "第二段中文翻译。"

    def test_paragraph_ids_are_sequential(self):
        result = parse_article(SAMPLE_ARTICLE)
        assert result["paragraphs"][0]["id"].endswith("-0")
        assert result["paragraphs"][1]["id"].endswith("-1")

    def test_normalizes_bare_video_id_to_url(self):
        result = parse_article(SAMPLE_BARE_ID)
        assert result["source"] == "https://www.youtube.com/watch?v=eg096o07w9o"

    def test_multiline_english_paragraph(self):
        text = """\
# Multi

**Original Title:** Multi
**Source:** https://www.youtube.com/watch?v=x
**Translated:** 2026-01-01

---

> Line one of the paragraph.
> Line two of the paragraph.

多行翻译内容。
"""
        result = parse_article(text)
        assert result["paragraphs"][0]["en"] == "Line one of the paragraph. Line two of the paragraph."
        assert result["paragraphs"][0]["zh"] == "多行翻译内容。"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/sunnyyang/Projects/yt-translate && python -m pytest tests/test_parser.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'yt_translate.parser'`

- [ ] **Step 3: Implement the parser**

```python
"""Parse translated article markdown into structured data."""

import re
from pathlib import Path


def parse_article(text: str) -> dict:
    """Parse a _zh.md file into structured article data.

    Args:
        text: Full markdown content of a translated article.

    Returns:
        Dict with keys: title, source, date, paragraphs.
        Each paragraph has: id, en, zh.
    """
    lines = text.strip().split("\n")

    title = ""
    source = ""
    date_str = ""

    # Parse header
    for line in lines:
        if line.startswith("# ") and not title:
            title = line[2:].strip()
        elif line.startswith("**Source:**"):
            source = line.replace("**Source:**", "").strip()
        elif line.startswith("**Translated:**"):
            date_str = line.replace("**Translated:**", "").strip()

    # Normalize bare video ID to full URL
    if source and re.match(r"^[A-Za-z0-9_-]{11}$", source):
        source = f"https://www.youtube.com/watch?v={source}"

    # Parse paragraphs: split by --- separators
    # Find the first --- after the header to start paragraph parsing
    content = text.strip()
    # Split on --- lines (with optional surrounding whitespace)
    sections = re.split(r"\n---\n", content)

    # First section is the header, skip it
    paragraphs = []
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:30]

    for i, section in enumerate(sections[1:]):
        section = section.strip()
        if not section:
            continue

        # Extract English (blockquote lines) and Chinese (non-blockquote)
        en_lines = []
        zh_lines = []

        for line in section.split("\n"):
            if line.startswith("> "):
                en_lines.append(line[2:])
            elif line.startswith(">"):
                en_lines.append(line[1:])
            elif line.strip():
                zh_lines.append(line.strip())

        en_text = " ".join(en_lines).strip()
        zh_text = "\n".join(zh_lines).strip()

        if en_text or zh_text:
            paragraphs.append({
                "id": f"{slug}-{i}",
                "en": en_text,
                "zh": zh_text,
            })

    return {
        "title": title,
        "source": source,
        "date": date_str,
        "paragraphs": paragraphs,
    }
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/sunnyyang/Projects/yt-translate && python -m pytest tests/test_parser.py -v`
Expected: All 7 tests PASS

- [ ] **Step 5: Commit**

```bash
cd /Users/sunnyyang/Projects/yt-translate
git add src/yt_translate/parser.py tests/test_parser.py
git commit -m "feat: add markdown article parser for site builder"
```

---

### Task 2: Site Builder (articles → JSON)

**Files:**
- Create: `src/yt_translate/build_site.py`
- Test: `tests/test_build_site.py`

**Interfaces:**
- Consumes: `parse_article(text: str) -> dict` from `parser.py`
- Produces: `build_site(articles_dir: Path, site_dir: Path) -> int` — returns count of articles built; writes `site/data/articles.json` and copies static assets

- [ ] **Step 1: Write the failing tests**

```python
"""Tests for the site builder."""

import json
from pathlib import Path

import pytest
from yt_translate.build_site import build_site


@pytest.fixture
def workspace(tmp_path):
    """Create articles dir with sample files and an empty site dir."""
    articles = tmp_path / "articles"
    articles.mkdir()

    (articles / "first-article_zh.md").write_text("""\
# First Article

**Original Title:** First Article
**Source:** https://www.youtube.com/watch?v=aaa
**Translated:** 2026-07-01

---

> Hello.

你好。
""", encoding="utf-8")

    (articles / "second-article_zh.md").write_text("""\
# Second Article

**Original Title:** Second Article
**Source:** https://www.youtube.com/watch?v=bbb
**Translated:** 2026-07-05

---

> World.

世界。
""", encoding="utf-8")

    site = tmp_path / "site"
    return articles, site


class TestBuildSite:
    def test_creates_articles_json(self, workspace):
        articles, site = workspace
        build_site(articles, site)
        data_file = site / "data" / "articles.json"
        assert data_file.exists()

    def test_articles_sorted_newest_first(self, workspace):
        articles, site = workspace
        build_site(articles, site)
        data = json.loads((site / "data" / "articles.json").read_text())
        dates = [a["date"] for a in data["articles"]]
        assert dates == sorted(dates, reverse=True)

    def test_article_structure(self, workspace):
        articles, site = workspace
        build_site(articles, site)
        data = json.loads((site / "data" / "articles.json").read_text())
        article = data["articles"][0]
        assert "key" in article
        assert "title" in article
        assert "source" in article
        assert "date" in article
        assert "paragraphs" in article
        assert len(article["paragraphs"]) > 0

    def test_copies_static_assets(self, workspace):
        articles, site = workspace
        build_site(articles, site)
        assert (site / "index.html").exists()
        assert (site / "style.css").exists()
        assert (site / "app.js").exists()

    def test_returns_article_count(self, workspace):
        articles, site = workspace
        count = build_site(articles, site)
        assert count == 2

    def test_ignores_non_zh_md_files(self, workspace):
        articles, site = workspace
        (articles / "notes.txt").write_text("not an article")
        count = build_site(articles, site)
        assert count == 2

    def test_empty_articles_dir(self, tmp_path):
        articles = tmp_path / "articles"
        articles.mkdir()
        site = tmp_path / "site"
        count = build_site(articles, site)
        assert count == 0
        data = json.loads((site / "data" / "articles.json").read_text())
        assert data["articles"] == []
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/sunnyyang/Projects/yt-translate && python -m pytest tests/test_build_site.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'yt_translate.build_site'`

- [ ] **Step 3: Implement the site builder**

```python
"""Build the static site from translated articles."""

import json
import shutil
from pathlib import Path

from yt_translate.parser import parse_article

ASSETS_DIR = Path(__file__).parent / "site_assets"


def build_site(articles_dir: Path, site_dir: Path) -> int:
    """Build the static site from all articles in articles_dir.

    Args:
        articles_dir: Directory containing *_zh.md files.
        site_dir: Output directory for the static site.

    Returns:
        Number of articles processed.
    """
    site_dir.mkdir(parents=True, exist_ok=True)
    data_dir = site_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    # Parse all articles
    articles = []
    for md_file in sorted(articles_dir.glob("*_zh.md")):
        text = md_file.read_text(encoding="utf-8")
        article = parse_article(text)
        article["key"] = md_file.stem.replace("_zh", "")
        articles.append(article)

    # Sort by date, newest first
    articles.sort(key=lambda a: a["date"], reverse=True)

    # Write articles.json
    (data_dir / "articles.json").write_text(
        json.dumps({"articles": articles}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # Copy static assets
    for asset in ("index.html", "style.css", "app.js"):
        src = ASSETS_DIR / asset
        if src.exists():
            shutil.copy2(src, site_dir / asset)

    return len(articles)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/sunnyyang/Projects/yt-translate && python -m pytest tests/test_build_site.py -v`
Expected: `test_copies_static_assets` will fail because `site_assets/` doesn't exist yet. That's expected — we'll create the assets in Task 3. The other tests should pass.

- [ ] **Step 5: Commit**

```bash
cd /Users/sunnyyang/Projects/yt-translate
git add src/yt_translate/build_site.py tests/test_build_site.py
git commit -m "feat: add site builder (articles/*.md → articles.json)"
```

---

### Task 3: Static Site Assets (HTML/CSS/JS)

**Files:**
- Create: `src/yt_translate/site_assets/index.html`
- Create: `src/yt_translate/site_assets/style.css`
- Create: `src/yt_translate/site_assets/app.js`

**Interfaces:**
- Consumes: `site/data/articles.json` at runtime (loaded by `app.js` via fetch)
- Produces: A working static site when served from `site/`

- [ ] **Step 1: Create `index.html`**

```html
<!doctype html>
<html lang="zh">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>YT Translate</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <button id="menu-toggle" aria-label="Toggle sidebar">☰</button>

  <aside id="sidebar" aria-label="Navigation">
    <div id="sidebar-header">
      <h1>YT Translate</h1>
    </div>
    <nav id="article-nav"></nav>
    <div class="controls">
      <button id="resume" hidden>Resume reading</button>
      <div class="font-controls">
        <span>Aa</span>
        <button id="font-down" aria-label="Smaller text">−</button>
        <button id="font-up" aria-label="Larger text">+</button>
      </div>
    </div>
  </aside>

  <main id="reader">
    <div id="loading">Loading…</div>
  </main>

  <script src="app.js"></script>
</body>
</html>
```

- [ ] **Step 2: Create `style.css`**

Adapt from raja-yoga with these changes:
- Remove book-list styling (replaced by article-nav)
- Remove section-title / chapter hierarchy styling
- Add article-specific styles (date display)

```css
:root {
  --bg: #faf7f2;
  --fg: #2a2926;
  --fg-zh: #5a4a3a;
  --muted: #8a8275;
  --accent: #a4540a;
  --rule: #e6dfd2;
  --sidebar-bg: #f1ebde;
  --reading-width: 38rem;
  --base-font: 17px;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: #1c1a17;
    --fg: #e9e4d8;
    --fg-zh: #cabd9f;
    --muted: #8a8275;
    --accent: #d6862e;
    --rule: #3a352d;
    --sidebar-bg: #221f1a;
  }
}

* { box-sizing: border-box; }

html {
  font-size: var(--base-font);
}

body {
  margin: 0;
  background: var(--bg);
  color: var(--fg);
  font-family: Georgia, "Iowan Old Style", "Source Serif Pro", serif;
  line-height: 1.65;
  -webkit-font-smoothing: antialiased;
}

/* --- Menu toggle (mobile) --- */

#menu-toggle {
  position: fixed;
  top: 0.6rem;
  left: 0.6rem;
  z-index: 20;
  width: 2.4rem;
  height: 2.4rem;
  border: 1px solid var(--rule);
  background: var(--bg);
  color: var(--fg);
  border-radius: 4px;
  font-size: 1.2rem;
  cursor: pointer;
  display: none;
}

/* --- Sidebar --- */

#sidebar {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  width: 18rem;
  padding: 1.2rem 1rem;
  background: var(--sidebar-bg);
  border-right: 1px solid var(--rule);
  overflow-y: auto;
  z-index: 10;
  display: flex;
  flex-direction: column;
}

#sidebar-header {
  padding-bottom: 0.8rem;
  margin-bottom: 0.8rem;
  border-bottom: 1px solid var(--rule);
}

#sidebar-header h1 {
  font-size: 1rem;
  font-weight: 600;
  color: var(--accent);
  margin: 0;
  letter-spacing: 0.02em;
}

/* --- Article nav --- */

#article-nav {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
  flex: 1;
  overflow-y: auto;
  margin-bottom: 0.8rem;
}

.article-link {
  display: flex;
  flex-direction: column;
  padding: 0.5rem 0.6rem;
  border-radius: 4px;
  cursor: pointer;
  border: none;
  background: none;
  text-align: left;
  font-family: inherit;
  width: 100%;
}

.article-link:hover {
  background: var(--rule);
}

.article-link.active {
  background: var(--rule);
  border-left: 3px solid var(--accent);
  padding-left: calc(0.6rem - 3px);
}

.article-link .article-title {
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--fg);
  line-height: 1.3;
}

.article-link.active .article-title {
  color: var(--accent);
}

.article-link .article-date {
  font-size: 0.72rem;
  color: var(--muted);
  margin-top: 0.15rem;
}

/* --- Controls --- */

.controls {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  padding-top: 0.8rem;
  border-top: 1px solid var(--rule);
  flex-shrink: 0;
}

#resume {
  padding: 0.5rem;
  border: 1px solid var(--accent);
  background: transparent;
  color: var(--accent);
  border-radius: 4px;
  cursor: pointer;
  font-family: inherit;
  font-size: 0.85rem;
}

#resume:hover {
  background: var(--accent);
  color: var(--bg);
}

.font-controls {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.85rem;
  color: var(--muted);
}

.font-controls button {
  flex: 1;
  padding: 0.3rem 0.6rem;
  border: 1px solid var(--rule);
  background: transparent;
  color: var(--fg);
  border-radius: 3px;
  cursor: pointer;
  font-family: inherit;
}

.font-controls button:hover {
  background: var(--rule);
}

/* --- Reader --- */

#reader {
  margin-left: 18rem;
  padding: 3rem 2rem 6rem;
  display: flex;
  justify-content: center;
}

.article {
  width: 100%;
  max-width: var(--reading-width);
}

.article-header {
  margin-bottom: 2.5rem;
  padding-bottom: 1.2rem;
  border-bottom: 1px solid var(--rule);
}

.article-header h2 {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0 0 0.4rem;
  letter-spacing: 0.01em;
}

.article-header .meta {
  font-size: 0.8rem;
  color: var(--muted);
}

.article-header .meta a {
  color: var(--accent);
  text-decoration: none;
}

.article-header .meta a:hover {
  text-decoration: underline;
}

.paragraph {
  position: relative;
  margin: 0 0 1.6rem;
  padding: 0.4rem 0.6rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.12s;
}

.paragraph:hover {
  background: var(--rule);
}

.paragraph.bookmarked {
  background: transparent;
}

.paragraph.bookmarked::before {
  content: "";
  position: absolute;
  left: -0.6rem;
  top: 0.4rem;
  bottom: 0.4rem;
  width: 3px;
  background: var(--accent);
  border-radius: 2px;
}

.paragraph .en {
  margin: 0;
}

.paragraph .zh {
  margin: 0.6rem 0 0;
  color: var(--fg-zh);
  font-family: "PingFang SC", "Hiragino Sans GB", "Songti SC", "Noto Serif CJK SC",
               "Source Han Serif SC", serif;
  line-height: 1.8;
}

#loading {
  color: var(--muted);
  font-style: italic;
}

/* --- Mobile --- */

@media (max-width: 768px) {
  :root { --base-font: 16px; }
  #menu-toggle { display: block; }
  #sidebar {
    transform: translateX(-100%);
    transition: transform 0.2s;
    width: 20rem;
    max-width: 85vw;
    box-shadow: 2px 0 16px rgba(0, 0, 0, 0.2);
  }
  #sidebar.open { transform: translateX(0); }
  #reader { margin-left: 0; padding: 4rem 1.2rem 4rem; }
}
```

- [ ] **Step 3: Create `app.js`**

Adapted from raja-yoga — simplified for flat article list (no book/chapter hierarchy).

```javascript
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
    btn.innerHTML = `<span class="article-title">${article.title}</span><span class="article-date">${article.date}</span>`;
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
  meta.innerHTML = `${currentArticle.date} · <a href="${currentArticle.source}" target="_blank" rel="noopener">YouTube</a>`;
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
```

- [ ] **Step 4: Create the `site_assets` directory and write files**

```bash
mkdir -p /Users/sunnyyang/Projects/yt-translate/src/yt_translate/site_assets
```

Write the three files above to:
- `src/yt_translate/site_assets/index.html`
- `src/yt_translate/site_assets/style.css`
- `src/yt_translate/site_assets/app.js`

- [ ] **Step 5: Verify build_site tests now pass**

Run: `cd /Users/sunnyyang/Projects/yt-translate && python -m pytest tests/test_build_site.py -v`
Expected: All 7 tests PASS

- [ ] **Step 6: Commit**

```bash
cd /Users/sunnyyang/Projects/yt-translate
git add src/yt_translate/site_assets/
git commit -m "feat: add static site assets (HTML/CSS/JS) adapted from raja-yoga"
```

---

### Task 4: Publish Function (git commit + push)

**Files:**
- Create: `src/yt_translate/publish.py`
- Test: `tests/test_publish.py`

**Interfaces:**
- Consumes: article title (str) for commit message
- Produces: `publish(repo_dir: Path, article_title: str) -> bool` — commits `site/` and `articles/`, pushes, returns True on success

- [ ] **Step 1: Write the failing tests**

```python
"""Tests for the publish module."""

import subprocess
from pathlib import Path
from unittest.mock import patch, call

import pytest
from yt_translate.publish import publish


@pytest.fixture
def git_repo(tmp_path):
    """Create a temporary git repo with articles/ and site/ dirs."""
    subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=tmp_path, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp_path, capture_output=True)

    (tmp_path / "articles").mkdir()
    (tmp_path / "site").mkdir()
    (tmp_path / "articles" / "test_zh.md").write_text("# Test")
    (tmp_path / "site" / "index.html").write_text("<html>")

    subprocess.run(["git", "add", "."], cwd=tmp_path, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=tmp_path, capture_output=True)
    return tmp_path


class TestPublish:
    def test_commits_articles_and_site(self, git_repo):
        (git_repo / "articles" / "new_zh.md").write_text("# New")
        (git_repo / "site" / "data").mkdir()
        (git_repo / "site" / "data" / "articles.json").write_text("{}")

        with patch("yt_translate.publish._git_push") as mock_push:
            mock_push.return_value = True
            result = publish(git_repo, "New Article")

        assert result is True

        # Verify commit was made
        log = subprocess.run(
            ["git", "log", "--oneline", "-1"],
            cwd=git_repo, capture_output=True, text=True
        )
        assert "Add: New Article" in log.stdout

    def test_no_changes_returns_false(self, git_repo):
        with patch("yt_translate.publish._git_push") as mock_push:
            result = publish(git_repo, "Nothing")

        assert result is False
        mock_push.assert_not_called()

    def test_push_failure_returns_false(self, git_repo):
        (git_repo / "articles" / "fail_zh.md").write_text("# Fail")

        with patch("yt_translate.publish._git_push") as mock_push:
            mock_push.return_value = False
            result = publish(git_repo, "Fail Article")

        assert result is False
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/sunnyyang/Projects/yt-translate && python -m pytest tests/test_publish.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'yt_translate.publish'`

- [ ] **Step 3: Implement the publish module**

```python
"""Git commit and push for auto-publishing."""

import subprocess
from pathlib import Path


def _git_push(repo_dir: Path) -> bool:
    """Push to origin. Returns True on success."""
    result = subprocess.run(
        ["git", "push"],
        cwd=repo_dir,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def publish(repo_dir: Path, article_title: str) -> bool:
    """Commit site/ and articles/ changes and push.

    Args:
        repo_dir: Root of the git repository.
        article_title: Title for the commit message.

    Returns:
        True if changes were committed and pushed successfully.
        False if there were no changes or push failed.
    """
    # Stage articles/ and site/
    subprocess.run(
        ["git", "add", "articles/", "site/"],
        cwd=repo_dir,
        capture_output=True,
    )

    # Check if there's anything to commit
    status = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=repo_dir,
        capture_output=True,
    )
    if status.returncode == 0:
        return False

    # Commit
    subprocess.run(
        ["git", "commit", "-m", f"Add: {article_title}"],
        cwd=repo_dir,
        capture_output=True,
    )

    # Push
    return _git_push(repo_dir)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/sunnyyang/Projects/yt-translate && python -m pytest tests/test_publish.py -v`
Expected: All 3 tests PASS

- [ ] **Step 5: Commit**

```bash
cd /Users/sunnyyang/Projects/yt-translate
git add src/yt_translate/publish.py tests/test_publish.py
git commit -m "feat: add publish module (git commit + push)"
```

---

### Task 5: Integrate into CLI

**Files:**
- Modify: `src/yt_translate/cli.py`
- Test: `tests/test_cli.py` (add new tests)

**Interfaces:**
- Consumes: `build_site(articles_dir, site_dir)` from `build_site.py`, `publish(repo_dir, title)` from `publish.py`
- Produces: Updated CLI that outputs to `articles/`, builds site, and publishes unless `--no-publish` is passed

- [ ] **Step 1: Write a failing integration test**

Add to `tests/test_cli.py`:

```python
"""Tests for CLI integration with build and publish."""

from pathlib import Path
from unittest.mock import patch, MagicMock
from click.testing import CliRunner

from yt_translate.cli import main


class TestCliPublishIntegration:
    @patch("yt_translate.cli.publish")
    @patch("yt_translate.cli.build_site")
    @patch("yt_translate.cli.translate_chunks")
    @patch("yt_translate.cli.chunk_segments")
    @patch("yt_translate.cli.fetch_transcript")
    def test_default_output_to_articles_dir(
        self, mock_fetch, mock_chunk, mock_translate, mock_build, mock_publish, tmp_path, monkeypatch
    ):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "articles").mkdir()

        mock_fetch.return_value = ("Test Video", [{"text": "hello", "start": 0, "duration": 1}])
        mock_chunk.return_value = [["hello"]]
        mock_translate.return_value = [{"original": "hello", "text": "你好", "success": True}]
        mock_build.return_value = 1
        mock_publish.return_value = True

        runner = CliRunner()
        result = runner.invoke(main, ["https://www.youtube.com/watch?v=abc123"])

        assert result.exit_code == 0
        # Output should be in articles/ directory
        articles = list((tmp_path / "articles").glob("*_zh.md"))
        assert len(articles) == 1

    @patch("yt_translate.cli.publish")
    @patch("yt_translate.cli.build_site")
    @patch("yt_translate.cli.translate_chunks")
    @patch("yt_translate.cli.chunk_segments")
    @patch("yt_translate.cli.fetch_transcript")
    def test_no_publish_flag_skips_publish(
        self, mock_fetch, mock_chunk, mock_translate, mock_build, mock_publish, tmp_path, monkeypatch
    ):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "articles").mkdir()

        mock_fetch.return_value = ("Test Video", [{"text": "hello", "start": 0, "duration": 1}])
        mock_chunk.return_value = [["hello"]]
        mock_translate.return_value = [{"original": "hello", "text": "你好", "success": True}]

        runner = CliRunner()
        result = runner.invoke(main, ["https://www.youtube.com/watch?v=abc123", "--no-publish"])

        assert result.exit_code == 0
        mock_build.assert_called_once()
        mock_publish.assert_not_called()
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd /Users/sunnyyang/Projects/yt-translate && python -m pytest tests/test_cli.py::TestCliPublishIntegration -v`
Expected: FAIL (missing `--no-publish` option, missing imports)

- [ ] **Step 3: Update `cli.py`**

```python
"""CLI entry point for yt-translate."""

from pathlib import Path

import click

from yt_translate.fetcher import fetch_transcript
from yt_translate.chunker import chunk_segments
from yt_translate.translator import translate_chunks
from yt_translate.formatter import format_markdown, generate_filename
from yt_translate.build_site import build_site
from yt_translate.publish import publish


@click.command()
@click.argument("youtube_url")
@click.option("--output", "-o", default=None, help="Output file path")
@click.option("--chunk-size", "-c", default=4, help="Sentences per paragraph (default: 4)")
@click.option(
    "--base-url",
    default="http://100.126.211.106:8000/v1",
    help="OpenAI-compatible API base URL",
)
@click.option(
    "--model",
    "-m",
    default="Qwen/Qwen3.6-35B-A3B-FP8",
    help="Model name for the API",
)
@click.option(
    "--no-publish",
    is_flag=True,
    default=False,
    help="Skip building the site and pushing to git",
)
def main(youtube_url: str, output: str | None, chunk_size: int, base_url: str, model: str, no_publish: bool) -> None:
    """Translate a YouTube video transcript to Chinese.

    YOUTUBE_URL: A YouTube video URL or video ID.
    """
    # Step 1: Fetch transcript
    click.echo("Fetching transcript...", err=True)
    title, segments = fetch_transcript(youtube_url)
    click.echo(f"Got transcript: \"{title}\" ({len(segments)} segments)", err=True)

    # Step 2: Chunk
    chunks = chunk_segments(segments, chunk_size=chunk_size)
    click.echo(f"Split into {len(chunks)} chunks for translation", err=True)

    # Step 3: Translate
    translated = translate_chunks(chunks, base_url=base_url, model=model)

    # Step 4: Format and save
    markdown = format_markdown(title, youtube_url, translated)

    if output:
        output_path = Path(output)
    else:
        repo_root = Path.cwd()
        articles_dir = repo_root / "articles"
        articles_dir.mkdir(exist_ok=True)
        output_path = articles_dir / generate_filename(title)

    output_path.write_text(markdown, encoding="utf-8")

    # Summary
    success_count = sum(1 for c in translated if c["success"])
    total_count = len(translated)

    if success_count == total_count:
        click.echo(f"Done! Saved to {output_path} ({success_count}/{total_count} chunks translated)", err=True)
    else:
        failed = total_count - success_count
        click.echo(
            f"Saved to {output_path} ({success_count}/{total_count} chunks translated, {failed} failed)",
            err=True,
        )

    # Step 5: Build site and publish
    repo_root = Path.cwd()
    articles_dir = repo_root / "articles"
    site_dir = repo_root / "site"

    click.echo("Building site...", err=True)
    count = build_site(articles_dir, site_dir)
    click.echo(f"Site built with {count} articles", err=True)

    if not no_publish:
        click.echo("Publishing...", err=True)
        if publish(repo_root, title):
            click.echo("Published successfully!", err=True)
        else:
            click.echo("Nothing to publish (no changes or push failed)", err=True)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run all tests**

Run: `cd /Users/sunnyyang/Projects/yt-translate && python -m pytest tests/ -v`
Expected: All tests PASS (existing + new)

- [ ] **Step 5: Commit**

```bash
cd /Users/sunnyyang/Projects/yt-translate
git add src/yt_translate/cli.py tests/test_cli.py
git commit -m "feat: integrate build + publish into CLI pipeline"
```

---

### Task 6: Migration & Deployment Setup

**Files:**
- Create: `articles/` directory with existing markdown files moved in
- Modify: `.gitignore` (stop ignoring `*_zh.md` in `articles/`)
- Create: `.github/workflows/pages.yml` (optional, for GitHub Pages)

**Interfaces:**
- Consumes: Existing `*_zh.md` files in repo root
- Produces: Working site in `site/` directory, GitHub Pages configured

- [ ] **Step 1: Create articles directory and move existing files**

```bash
cd /Users/sunnyyang/Projects/yt-translate
mkdir -p articles
mv *_zh.md articles/ 2>/dev/null || true
```

- [ ] **Step 2: Update `.gitignore`**

Remove the `*_zh.md` line and add rules to track articles but not the site build output (site/ should be tracked for GitHub Pages):

Replace the existing `.gitignore` content with:

```
.superpowers/
.venv/
__pycache__/
*.egg-info/
dist/
build/
.DS_Store
*.swp
```

- [ ] **Step 3: Build the site for the first time**

```bash
cd /Users/sunnyyang/Projects/yt-translate
python -c "from yt_translate.build_site import build_site; from pathlib import Path; build_site(Path('articles'), Path('site'))"
```

- [ ] **Step 4: Verify the site works locally**

```bash
cd /Users/sunnyyang/Projects/yt-translate/site
python3 -m http.server 8000
```

Open http://localhost:8000 in a browser. Verify:
- Article list appears in sidebar (sorted by date, newest first)
- Clicking an article renders paragraphs (English + Chinese)
- Font size controls work
- Dark mode works (toggle system preference)
- Mobile responsive (resize window)

- [ ] **Step 5: Commit everything**

```bash
cd /Users/sunnyyang/Projects/yt-translate
git add articles/ site/ .gitignore
git commit -m "feat: initial site build with existing articles"
```

- [ ] **Step 6: Configure GitHub Pages**

Push and configure Pages via GitHub settings:
- Go to repo Settings → Pages
- Source: "Deploy from a branch"
- Branch: `main`, folder: `/site`
- Save

Or create `.github/workflows/pages.yml`:

```yaml
name: Deploy to Pages

on:
  push:
    branches: [main]
    paths: [site/**]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: site
      - id: deployment
        uses: actions/deploy-pages@v4
```

```bash
cd /Users/sunnyyang/Projects/yt-translate
mkdir -p .github/workflows
# Write the workflow file above
git add .github/workflows/pages.yml
git commit -m "chore: add GitHub Pages deployment workflow"
git push
```
