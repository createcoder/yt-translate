"""Integration tests for the CLI."""

from unittest.mock import patch
from click.testing import CliRunner

from yt_translate.cli import main


@patch("yt_translate.cli.fetch_transcript")
@patch("yt_translate.cli.translate_chunks")
def test_full_pipeline(mock_translate, mock_fetch, tmp_path):
    """Test the full CLI pipeline with mocked external calls."""
    mock_fetch.return_value = ("Test Video", [
        {"start": 0.0, "duration": 5.0, "text": "Hello world this is a test video."},
    ])
    mock_translate.return_value = [
        {"start": 0.0, "text": "你好世界，这是一个测试视频。", "success": True},
    ]

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
