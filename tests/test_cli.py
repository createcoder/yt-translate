"""Integration tests for the CLI."""

from pathlib import Path
from unittest.mock import patch, MagicMock
from click.testing import CliRunner

from yt_translate.cli import main


@patch("yt_translate.cli.publish")
@patch("yt_translate.cli.build_site")
@patch("yt_translate.cli.fetch_transcript")
@patch("yt_translate.cli.translate_chunks")
def test_full_pipeline(mock_translate, mock_fetch, mock_build, mock_publish, tmp_path):
    """Test the full CLI pipeline with mocked external calls."""
    mock_fetch.return_value = ("Test Video", [
        {"start": 0.0, "duration": 5.0, "text": "Hello world this is a test video."},
    ])
    mock_translate.return_value = [
        {"start": 0.0, "original": "Hello world this is a test video.", "text": "你好世界，这是一个测试视频。", "success": True},
    ]
    mock_build.return_value = 1
    mock_publish.return_value = True

    output_file = tmp_path / "output.md"
    runner = CliRunner()
    result = runner.invoke(main, [
        "https://www.youtube.com/watch?v=abc123",
        "--output", str(output_file),
    ])

    assert result.exit_code == 0
    content = output_file.read_text()
    assert "Test Video" in content
    assert "你好世界，这是一个测试视频。" in content


@patch("yt_translate.cli.fetch_transcript")
def test_invalid_url(mock_fetch):
    """Test error handling for invalid URLs."""
    mock_fetch.side_effect = SystemExit(1)

    runner = CliRunner()
    result = runner.invoke(main, ["https://example.com/not-youtube"])

    assert result.exit_code == 1


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
