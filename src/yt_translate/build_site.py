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

    # Playlist briefs are deliberately stored outside articles/ because they
    # contain a full source transcript. Include them as a separate reader type.
    playlist_dir = articles_dir.parent / "playlist-summaries"
    if playlist_dir.exists():
        for md_file in sorted(playlist_dir.glob("**/[0-9]*.md")):
            brief = _parse_playlist_brief(md_file.read_text(encoding="utf-8"))
            if brief:
                brief["key"] = f"playlist-{md_file.parent.name}-{md_file.stem}"
                articles.append(brief)

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


def _parse_playlist_brief(text: str) -> dict | None:
    """Parse the durable Markdown shape emitted by playlist_cli."""
    lines = text.splitlines()
    if not lines or not lines[0].startswith("# "):
        return None
    title = lines[0][2:].strip()
    source = next((line.removeprefix("- **Video:** ") for line in lines if line.startswith("- **Video:** ")), "")
    generated = next((line.removeprefix("- **Generated:** ") for line in lines if line.startswith("- **Generated:** ")), "")
    status = next((line.removeprefix("- **Status:** ") for line in lines if line.startswith("- **Status:** ")), "")
    try:
        summary = text.split("## Technical brief\n", 1)[1].split("\n## Full transcript\n", 1)[0].strip()
        transcript = text.split("\n## Full transcript\n", 1)[1].strip()
    except IndexError:
        return None
    return {
        "type": "playlist_brief",
        "title": title,
        "source": source,
        "date": generated[:10],
        "status": status,
        "summary": summary,
        "transcript": transcript,
        "paragraphs": [],
    }
