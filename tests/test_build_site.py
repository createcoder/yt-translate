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
