"""Fetch YouTube video transcript and title."""

import re
import subprocess
from urllib.parse import urlparse, parse_qs

import click
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound


def extract_video_id(url: str) -> str:
    """Extract YouTube video ID from a URL or bare ID.

    Args:
        url: YouTube URL (various formats) or an 11-char video ID.

    Returns:
        The video ID string.

    Raises:
        ValueError: If the URL cannot be parsed as a YouTube video.
    """
    # Bare video ID (11 alphanumeric + hyphen/underscore chars)
    if re.match(r"^[A-Za-z0-9_-]{11}$", url):
        return url

    parsed = urlparse(url)

    # youtu.be/VIDEO_ID
    if parsed.hostname in ("youtu.be",):
        video_id = parsed.path.lstrip("/")
        if video_id:
            return video_id

    # youtube.com/watch?v=VIDEO_ID
    if parsed.hostname in ("www.youtube.com", "youtube.com", "m.youtube.com"):
        qs = parse_qs(parsed.query)
        if "v" in qs:
            return qs["v"][0]

    raise ValueError(f"Invalid YouTube URL or video ID: {url}")


def _get_video_title(video_id: str) -> str:
    """Get video title using yt-dlp.

    Args:
        video_id: YouTube video ID.

    Returns:
        The video title string, or "Untitled" on failure.
    """
    try:
        result = subprocess.run(
            ["yt-dlp", "--get-title", f"https://www.youtube.com/watch?v={video_id}"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return "Untitled"


def fetch_transcript(url: str) -> tuple[str, list[dict]]:
    """Fetch transcript and title for a YouTube video.

    Args:
        url: YouTube URL or video ID.

    Returns:
        Tuple of (video_title, segments) where segments is a list of dicts
        with keys "start", "duration", "text".

    Raises:
        SystemExit: If no transcript is available.
    """
    video_id = extract_video_id(url)
    api = YouTubeTranscriptApi()

    try:
        fetched = api.fetch(video_id, languages=["en"])
        segments = fetched.to_raw_data()
    except (TranscriptsDisabled, NoTranscriptFound):
        try:
            # Fallback: try listing available transcripts
            transcript_list = api.list(video_id)
            transcript = transcript_list.find_transcript(["en"])
            fetched = transcript.fetch()
            segments = fetched.to_raw_data()
        except Exception:
            click.echo(
                "Error: No transcript available for this video. "
                "The video may not have captions enabled.",
                err=True,
            )
            raise SystemExit(1)
    except Exception as e:
        click.echo(f"Error: Failed to fetch transcript: {e}", err=True)
        raise SystemExit(1)

    title = _get_video_title(video_id)

    return title, segments
