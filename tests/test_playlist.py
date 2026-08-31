"""Tests for playlist enumeration, durable output, and VTT parsing."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from yt_translate.fetcher import _parse_vtt, fetch_playlist
from yt_translate.playlist_cli import main


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
    result = CliRunner().invoke(main, ["PLtest", "--output-dir", str(tmp_path)])
    assert result.exit_code == 0
    video = next((tmp_path / "PLtest").glob("[0-9]*.md"))
    content = video.read_text()
    assert "https://youtube.com/watch?v=dQw4w9WgXcQ" in content
    assert "Useful detail" in content
    assert "Technical transcript" in content
    assert "Video title" in (tmp_path / "PLtest" / "README.md").read_text()
    _transcript.assert_called_once_with("https://youtube.com/watch?v=dQw4w9WgXcQ", prefer_ytdlp=True)
