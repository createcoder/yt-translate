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
