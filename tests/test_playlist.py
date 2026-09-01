"""Tests for playlist enumeration, durable output, and VTT parsing."""

import json
import os
from pathlib import Path
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from yt_translate.fetcher import _parse_vtt, fetch_playlist
from yt_translate.playlist_cli import _load_dotenv, main


def test_parse_vtt_removes_markup_and_keeps_timing():
    result = _parse_vtt("WEBVTT\n\n00:00:01.000 --> 00:00:03.500\n<c>Hello</c> world\n")
    assert result == [{"start": 1.0, "duration": 2.5, "text": "Hello world"}]


@patch("yt_translate.fetcher.subprocess.run")
def test_fetch_playlist_uses_flat_ytdlp_data(mock_run):
    mock_run.return_value = MagicMock(
        returncode=0,
        stdout=json.dumps({"entries": [{"id": "dQw4w9WgXcQ", "title": "Example"}]}),
    )
    assert fetch_playlist("PLexample") == [{
        "id": "dQw4w9WgXcQ", "title": "Example", "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    }]
    assert "--flat-playlist" in mock_run.call_args.args[0]


@patch("yt_translate.playlist_cli.summarize_transcript", return_value="## Executive takeaway\nUseful detail")
@patch("yt_translate.playlist_cli.fetch_transcript", return_value=("Video title", [{"start": 0, "text": "Technical transcript"}]))
@patch("yt_translate.playlist_cli.fetch_playlist", return_value=[{"id": "dQw4w9WgXcQ", "title": "Video title", "url": "https://youtube.com/watch?v=dQw4w9WgXcQ"}])
def test_playlist_cli_saves_summary_transcript_and_index(_playlist, _transcript, _summary, tmp_path: Path):
    result = CliRunner().invoke(main, ["PLtest", "--output-dir", str(tmp_path), "--api-key", "test-key"])
    assert result.exit_code == 0
    video = next((tmp_path / "PLtest").glob("[0-9]*.md"))
    content = video.read_text()
    assert "https://youtube.com/watch?v=dQw4w9WgXcQ" in content
    assert "Useful detail" in content
    assert "Technical transcript" in content
    assert "Video title" in (tmp_path / "PLtest" / "README.md").read_text()
    _transcript.assert_called_once_with("https://youtube.com/watch?v=dQw4w9WgXcQ", prefer_ytdlp=True)


@patch("yt_translate.playlist_cli.fetch_transcript")
@patch("yt_translate.playlist_cli.fetch_playlist", return_value=[{"id": "dQw4w9WgXcQ", "title": "Existing", "url": "https://youtube.com/watch?v=dQw4w9WgXcQ"}])
def test_playlist_cli_skips_completed_video(_playlist, mock_transcript, tmp_path: Path):
    destination = tmp_path / "PLtest"
    destination.mkdir()
    (destination / "001-existing.md").write_text(
        "# Existing\n\n- **Video:** https://youtube.com/watch?v=dQw4w9WgXcQ\n- **Status:** Completed\n",
        encoding="utf-8",
    )
    result = CliRunner().invoke(main, ["PLtest", "--output-dir", str(tmp_path)])
    assert result.exit_code == 0
    mock_transcript.assert_not_called()
    assert "Skipped (already completed)" in (destination / "README.md").read_text()


@patch("yt_translate.playlist_cli.summarize_transcript", side_effect=RuntimeError("model unavailable"))
@patch("yt_translate.playlist_cli.fetch_transcript", return_value=("Video", [{"start": 0, "text": "Preserved transcript"}]))
@patch("yt_translate.playlist_cli.fetch_playlist", return_value=[{"id": "dQw4w9WgXcQ", "title": "Video", "url": "https://youtube.com/watch?v=dQw4w9WgXcQ"}])
def test_playlist_cli_preserves_transcript_when_summary_fails(_playlist, _transcript, _summary, tmp_path: Path):
    result = CliRunner().invoke(main, ["PLtest", "--output-dir", str(tmp_path), "--api-key", "test-key"])
    assert result.exit_code == 0
    content = next((tmp_path / "PLtest").glob("[0-9]*.md")).read_text()
    assert "Preserved transcript" in content
    assert "model unavailable" in content


def test_load_dotenv_sets_missing_values_without_overriding_environment(tmp_path: Path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("LITELLM_BASE_URL=http://example.test/v1\nLITELLM_API_KEY=example-key\n", encoding="utf-8")
    monkeypatch.delenv("LITELLM_BASE_URL", raising=False)
    monkeypatch.setenv("LITELLM_API_KEY", "environment-key")
    _load_dotenv(env_file)
    assert os.environ["LITELLM_BASE_URL"] == "http://example.test/v1"
    assert os.environ["LITELLM_API_KEY"] == "environment-key"
