"""Tests for the formatter module."""

from yt_translate.formatter import format_markdown, generate_filename


class TestFormatMarkdown:
    """Tests for dual-language Markdown output formatting."""

    def test_basic_output(self):
        chunks = [
            {"start": 0.0, "original": "First paragraph.", "text": "第一段翻译内容。", "success": True},
            {"start": 60.0, "original": "Second paragraph.", "text": "第二段翻译内容。", "success": True},
        ]
        result = format_markdown("Test Video", "https://youtube.com/watch?v=abc", chunks)

        assert "# Test Video" in result
        assert "**Original Title:** Test Video" in result
        assert "**Source:** https://youtube.com/watch?v=abc" in result
        assert "第一段翻译内容。" in result
        assert "第二段翻译内容。" in result
        # No timestamps in output
        assert "[00:00:00]" not in result
        assert "[00:01:00]" not in result

    def test_dual_language_format(self):
        chunks = [
            {"start": 0.0, "original": "Hello world.", "text": "你好世界。", "success": True},
            {"start": 30.0, "original": "Goodbye.", "text": "再见。", "success": True},
        ]
        result = format_markdown("Title", "http://url", chunks)

        # Original in blockquote, translation below
        assert "> Hello world." in result
        assert "你好世界。" in result
        assert "> Goodbye." in result
        assert "再见。" in result
        # Paragraphs separated by ---
        assert "---" in result

    def test_failed_chunk_placeholder(self):
        chunks = [
            {"start": 0.0, "original": "Success text.", "text": "成功翻译。", "success": True},
            {"start": 30.0, "original": "Failed text.", "text": "[TRANSLATION FAILED]", "success": False},
        ]
        result = format_markdown("Title", "http://url", chunks)
        assert "[TRANSLATION FAILED]" in result
        assert "> Failed text." in result


class TestGenerateFilename:
    """Tests for filename generation."""

    def test_basic_slug(self):
        assert generate_filename("Hello World Video") == "hello-world-video_zh.md"

    def test_special_characters(self):
        result = generate_filename("What's the Deal? (2024) | Episode #5")
        assert "/" not in result
        assert "?" not in result
        assert result.endswith("_zh.md")

    def test_long_title_truncated(self):
        long_title = "A" * 100
        result = generate_filename(long_title)
        # Slug part (before _zh.md) should be max 60 chars
        slug_part = result.replace("_zh.md", "")
        assert len(slug_part) <= 60

    def test_empty_title(self):
        result = generate_filename("")
        assert result == "untitled_zh.md"
