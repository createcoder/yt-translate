"""Tests for the fetcher module."""

import pytest
from unittest.mock import patch, MagicMock

from yt_translate.fetcher import fetch_transcript, extract_video_id


class TestExtractVideoId:
    """Tests for URL parsing."""

    def test_standard_url(self):
        assert extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == "dQw4w9WgXcQ"

    def test_short_url(self):
        assert extract_video_id("https://youtu.be/dQw4w9WgXcQ") == "dQw4w9WgXcQ"

    def test_bare_video_id(self):
        assert extract_video_id("dQw4w9WgXcQ") == "dQw4w9WgXcQ"

    def test_url_with_extra_params(self):
        assert extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=120") == "dQw4w9WgXcQ"

    def test_invalid_url(self):
        with pytest.raises(ValueError, match="Invalid YouTube URL"):
            extract_video_id("https://example.com/not-youtube")


class TestFetchTranscript:
    """Tests for transcript fetching (mocked)."""

    @patch("yt_translate.fetcher._get_video_title")
    @patch("yt_translate.fetcher.YouTubeTranscriptApi")
    def test_successful_fetch(self, mock_api_cls, mock_title):
        mock_title.return_value = "Test Video Title"

        # Mock the instance and its fetch method
        mock_instance = MagicMock()
        mock_api_cls.return_value = mock_instance

        mock_fetched = MagicMock()
        mock_fetched.to_raw_data.return_value = [
            {"start": 0.0, "duration": 5.0, "text": "Hello world"},
            {"start": 5.0, "duration": 3.0, "text": "This is a test"},
        ]
        mock_instance.fetch.return_value = mock_fetched

        title, segments = fetch_transcript("https://www.youtube.com/watch?v=abc123abcd")

        assert title == "Test Video Title"
        assert len(segments) == 2
        assert segments[0]["text"] == "Hello world"
        assert segments[0]["start"] == 0.0
        assert segments[1]["text"] == "This is a test"

    @patch("yt_translate.fetcher._get_video_title")
    @patch("yt_translate.fetcher.YouTubeTranscriptApi")
    def test_no_transcript_available(self, mock_api_cls, mock_title):
        from youtube_transcript_api._errors import TranscriptsDisabled

        mock_instance = MagicMock()
        mock_api_cls.return_value = mock_instance
        mock_instance.fetch.side_effect = TranscriptsDisabled("abc123abcde")

        # Also make the fallback fail
        mock_instance.list.side_effect = Exception("No transcripts")

        with pytest.raises(SystemExit):
            fetch_transcript("https://www.youtube.com/watch?v=abc123abcde")

    @patch("yt_translate.fetcher._get_video_title")
    @patch("yt_translate.fetcher.YouTubeTranscriptApi")
    def test_fallback_to_list_transcripts(self, mock_api_cls, mock_title):
        """When fetch() fails with NoTranscriptFound, fall back to list()."""
        from youtube_transcript_api._errors import NoTranscriptFound

        mock_title.return_value = "Fallback Video"
        mock_instance = MagicMock()
        mock_api_cls.return_value = mock_instance

        mock_instance.fetch.side_effect = NoTranscriptFound(
            "abc123abcde", ["en"], {"en": "English"}
        )

        # Fallback: list transcripts -> find -> fetch
        mock_transcript = MagicMock()
        mock_fetched = MagicMock()
        mock_fetched.to_raw_data.return_value = [
            {"start": 0.0, "duration": 4.0, "text": "Fallback text"},
        ]
        mock_transcript.fetch.return_value = mock_fetched

        mock_transcript_list = MagicMock()
        mock_transcript_list.find_transcript.return_value = mock_transcript
        mock_instance.list.return_value = mock_transcript_list

        title, segments = fetch_transcript("https://www.youtube.com/watch?v=abc123abcde")

        assert title == "Fallback Video"
        assert len(segments) == 1
        assert segments[0]["text"] == "Fallback text"
