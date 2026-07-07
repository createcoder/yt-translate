# Auto-Publish Website for yt-translate

**Date:** 2026-07-07
**Status:** Approved

## Summary

Extend `yt-translate` to automatically publish translated articles to a static website hosted on GitHub Pages. After translation, the CLI builds the site and pushes to deploy. The website UI is adapted from the raja-yoga project's bilingual reader.

## Architecture

```
yt-translate <url>
    │
    ├── fetch transcript (existing)
    ├── translate via Qwen (existing)
    ├── save to articles/<slug>_zh.md
    ├── build-site:
    │     ├── scan articles/*.md
    │     ├── parse each into structured JSON
    │     └── write site/data/articles.json
    └── git commit + push (site/ + articles/)
```

## File Layout

```
yt-translate/
├── articles/              ← source of truth for translated articles
│   ├── nixon-s-revenge-..._zh.md
│   └── ...
├── site/                  ← GitHub Pages root
│   ├── index.html
│   ├── style.css
│   ├── app.js
│   └── data/
│       └── articles.json
├── src/
│   └── yt_translate/
│       ├── ...existing modules...
│       ├── build_site.py  ← parses articles/*.md → site/data/articles.json
│       └── publish.py     ← git add, commit, push
└── ...
```

## Data Format

`site/data/articles.json`:
```json
{
  "articles": [
    {
      "key": "nixon-s-revenge-trump-just-ended-the-kissinger-doctrine-and",
      "title": "Nixon's Revenge: Trump Just Ended the Kissinger Doctrine — And Britain Knows It",
      "source": "https://www.youtube.com/watch?v=gkVnOQqqBqo",
      "date": "2026-06-29",
      "paragraphs": [
        {"id": "nixon-0", "en": "Speaking at the Nixon Library...", "zh": "上周在尼克松图书馆..."}
      ]
    }
  ]
}
```

Articles are sorted by date (newest first) in the JSON.

## Website UI (adapted from raja-yoga)

### Sidebar
- Flat list of articles sorted by date (newest first)
- Each entry shows: article title + date
- Active article highlighted with accent border
- Mobile: hamburger menu toggles sidebar

### Reader
- English paragraph followed by Chinese translation below
- Click paragraph to set bookmark (accent bar indicator)
- "Resume reading" button returns to bookmarked position

### Controls
- Font size +/- buttons
- Dark mode via `prefers-color-scheme` (automatic)
- Mobile responsive (sidebar collapses)

### Styling
- Same warm color palette as raja-yoga (sepia tones)
- Serif fonts for reading comfort
- `--reading-width: 38rem` max content width

## CLI Changes

### Output path
- Default output path changes to `articles/<slug>_zh.md` (instead of repo root)
- Existing `--output / -o` flag still overrides

### New flag
- `--no-publish`: skip build + git push step (for local testing)

### New pipeline steps (after translation)
1. `build_site()`: scan `articles/*.md`, parse markdown structure, generate `articles.json`, copy static assets to `site/`
2. `publish()`: `git add site/ articles/ && git commit -m "Add: <article-title>" && git push`

## Markdown Parsing

Each `_zh.md` file has this structure:
```markdown
# Title

**Original Title:** ...
**Source:** https://youtube.com/watch?v=...
**Translated:** 2026-06-29

---

> English paragraph text

Chinese paragraph text

---

> Next English paragraph

Next Chinese paragraph
```

The parser extracts:
- Title from `# heading`
- Source URL from `**Source:**` line (normalize to full YouTube URL if only video ID is present)
- Date from `**Translated:**` line
- Paragraphs: pairs of blockquote (en) + plain text (zh) separated by `---`

## GitHub Pages Deployment

Configure GitHub Pages to serve from `site/` directory on `main` branch. Options:
- Repo Settings → Pages → Source: Deploy from branch, folder: `/site`
- Or: GitHub Actions workflow that copies `site/` to gh-pages branch

## Migration

Move existing `*_zh.md` files from repo root to `articles/` folder. Run `build_site()` once to generate initial `site/` with all existing articles.
