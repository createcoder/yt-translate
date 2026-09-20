"""Tests for the formatter module."""

from yt_translate.formatter import format_markdown, generate_filename, strip_speaker_markers


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


class TestStripSpeakerMarkers:
    """Tests for removing YouTube caption speaker-change markers."""

    def test_leaves_plain_text_alone(self):
        assert strip_speaker_markers("Hello world.") == "Hello world."
        assert strip_speaker_markers("你好世界。") == "你好世界。"

    def test_strips_line_leading_marker(self):
        assert strip_speaker_markers(">> Hello world.") == "Hello world."
        assert strip_speaker_markers(">> 你好世界。") == "你好世界。"

    def test_strips_marker_without_trailing_space(self):
        assert strip_speaker_markers(">>Hello") == "Hello"

    def test_collapses_inline_marker_to_single_space(self):
        assert strip_speaker_markers("Todd Blanche >> Yeah. It's okay.") == "Todd Blanche Yeah. It's okay."
        assert strip_speaker_markers("EU last week. >> No, laughable.") == "EU last week. No, laughable."

    def test_drops_line_that_was_only_the_marker(self):
        assert strip_speaker_markers("line one\n>>\nline two") == "line one\nline two"

    def test_preserves_blockquote_prefix(self):
        assert strip_speaker_markers("> >> Something") == "> Something"

    def test_strips_marker_from_middle_of_blockquote_line(self):
        # Real English caption pattern from articles/
        line = "> Todd Blanche >> Yeah. It's okay."
        assert strip_speaker_markers(line) == "> Todd Blanche Yeah. It's okay."

    def test_multiline_mixed(self):
        text = (
            "> Here's the President. >> No, laughable.\n"
            "\n"
            "以下是特朗普的讲话。\n"
            ">> 不，我觉得这很可笑。\n"
        )
        expected = (
            "> Here's the President. No, laughable.\n"
            "\n"
            "以下是特朗普的讲话。\n"
            "不，我觉得这很可笑。\n"
        )
        assert strip_speaker_markers(text) == expected

    def test_idempotent(self):
        text = ">> foo >> bar\n>> baz"
        once = strip_speaker_markers(text)
        twice = strip_speaker_markers(once)
        assert once == twice
