"""Tests for the translator module."""

from unittest.mock import patch, MagicMock

from yt_translate.translator import translate_chunks, translate_single_chunk


class TestTranslateSingleChunk:
    """Tests for single chunk translation."""

    @patch("yt_translate.translator.time.sleep")
    @patch("yt_translate.translator.OpenAI")
    def test_successful_translation(self, mock_openai_cls, mock_sleep):
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "你好世界"
        mock_client.chat.completions.create.return_value = mock_response

        result = translate_single_chunk(
            "Hello world",
            base_url="http://localhost:8000/v1",
            model="test-model",
        )

        assert result == "你好世界"

    @patch("yt_translate.translator.time.sleep")
    @patch("yt_translate.translator.OpenAI")
    def test_retry_on_failure(self, mock_openai_cls, mock_sleep):
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_client.chat.completions.create.side_effect = [
            Exception("Connection error"),
            Exception("Connection error"),
            MagicMock(choices=[MagicMock(message=MagicMock(content="翻译结果"))]),
        ]

        result = translate_single_chunk(
            "Test text",
            base_url="http://localhost:8000/v1",
            model="test-model",
        )

        assert result == "翻译结果"
        assert mock_client.chat.completions.create.call_count == 3
        assert mock_sleep.call_count == 2

    @patch("yt_translate.translator.time.sleep")
    @patch("yt_translate.translator.OpenAI")
    def test_failure_after_retries(self, mock_openai_cls, mock_sleep):
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("Server down")

        result = translate_single_chunk(
            "Test text",
            base_url="http://localhost:8000/v1",
            model="test-model",
        )

        assert result is None
        assert mock_client.chat.completions.create.call_count == 3

    @patch("yt_translate.translator.time.sleep")
    @patch("yt_translate.translator.OpenAI")
    def test_empty_content_returns_none(self, mock_openai_cls, mock_sleep):
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = ""
        mock_client.chat.completions.create.return_value = mock_response

        result = translate_single_chunk(
            "Test text",
            base_url="http://localhost:8000/v1",
            model="test-model",
        )

        assert result is None


class TestTranslateChunks:
    """Tests for batch chunk translation."""

    @patch("yt_translate.translator.translate_single_chunk")
    def test_all_chunks_succeed(self, mock_translate):
        mock_translate.side_effect = ["第一段", "第二段"]
        chunks = [
            {"start": 0.0, "text": "First paragraph"},
            {"start": 60.0, "text": "Second paragraph"},
        ]

        result = translate_chunks(chunks, base_url="http://x/v1", model="m")

        assert len(result) == 2
        assert result[0]["text"] == "第一段"
        assert result[0]["original"] == "First paragraph"
        assert result[0]["success"] is True
        assert result[0]["start"] == 0.0
        assert result[1]["text"] == "第二段"
        assert result[1]["original"] == "Second paragraph"
        assert result[1]["success"] is True
        assert result[1]["start"] == 60.0

    @patch("yt_translate.translator.translate_single_chunk")
    def test_partial_failure(self, mock_translate):
        mock_translate.side_effect = ["第一段", None]
        chunks = [
            {"start": 0.0, "text": "First paragraph"},
            {"start": 60.0, "text": "Second paragraph"},
        ]

        result = translate_chunks(chunks, base_url="http://x/v1", model="m")

        assert result[0]["success"] is True
        assert result[0]["original"] == "First paragraph"
        assert result[1]["success"] is False
        assert result[1]["original"] == "Second paragraph"
        assert result[1]["text"] == "[TRANSLATION FAILED]"

    @patch("yt_translate.translator.translate_single_chunk")
    def test_empty_chunks_list(self, mock_translate):
        result = translate_chunks([], base_url="http://x/v1", model="m")

        assert result == []
        mock_translate.assert_not_called()
