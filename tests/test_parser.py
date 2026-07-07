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
