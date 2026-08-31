"""Fetch YouTube video transcript and title."""

import json
import re
import subprocess
import tempfile
from pathlib import Path
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


def fetch_transcript(url: str, prefer_ytdlp: bool = False) -> tuple[str, list[dict]]:
    """Fetch transcript and title for a YouTube video.

    Args:
        url: YouTube URL or video ID.
        prefer_ytdlp: Try yt-dlp captions before the transcript API. Useful for
            batch jobs where avoiding a potentially slow API request matters.

    Returns:
        Tuple of (video_title, segments) where segments is a list of dicts
        with keys "start", "duration", "text".

    Raises:
        SystemExit: If no transcript is available.
    """
    video_id = extract_video_id(url)
    if prefer_ytdlp:
        # Batch jobs must be bounded: yt-dlp already covers manual and auto
        # captions, and failures are persisted per video by playlist_cli.
        return _get_video_title(video_id), _fetch_transcript_with_ytdlp(video_id)
    api = YouTubeTranscriptApi()

    try:
        fetched = api.fetch(video_id, languages=["en"])
        segments = fetched.to_raw_data()
    except (TranscriptsDisabled, NoTranscriptFound) as primary_error:
        try:
            # Fallback: try listing available transcripts
            transcript_list = api.list(video_id)
            try:
                transcript = transcript_list.find_transcript(["en"])
            except NoTranscriptFound:
                # Last resort: pick the first available transcript
                available = list(transcript_list)
                if not available:
                    raise
                transcript = available[0]
            fetched = transcript.fetch()
            segments = fetched.to_raw_data()
        except Exception as list_error:
            segments = _fetch_with_fallback(video_id, primary_error, list_error)
    except Exception as e:
        # youtube-transcript-api is sometimes blocked by YouTube even when
        # captions are available.  yt-dlp can retrieve auto-generated VTT
        # captions in that case.
        segments = _fetch_with_fallback(video_id, e)

    title = _get_video_title(video_id)

    return title, segments


def _fetch_with_fallback(video_id: str, primary_error: Exception, secondary_error: Exception | None = None) -> list[dict]:
    """Try yt-dlp captions and retain the original failure in the error message."""
    try:
        return _fetch_transcript_with_ytdlp(video_id)
    except Exception as fallback_error:
        extra = f"; transcript selection failed: {secondary_error}" if secondary_error else ""
        click.echo(
            f"Error: Failed to fetch transcript: {primary_error}{extra}. "
            f"yt-dlp fallback also failed: {fallback_error}",
            err=True,
        )
        raise SystemExit(1)


def _fetch_transcript_with_ytdlp(video_id: str) -> list[dict]:
    """Download English manual or auto captions with yt-dlp and parse VTT."""
    with tempfile.TemporaryDirectory(prefix="yt-captions-") as directory:
        output_template = str(Path(directory) / "captions.%(ext)s")
        result = subprocess.run(
            [
                "yt-dlp", "--skip-download", "--write-subs", "--write-auto-subs",
                "--sub-langs", "en.*,en", "--sub-format", "vtt",
                "--socket-timeout", "20",
                "-o", output_template, f"https://www.youtube.com/watch?v={video_id}",
            ],
            capture_output=True,
            text=True,
            timeout=45,
        )
        caption_files = list(Path(directory).glob("*.vtt"))
        if result.returncode != 0 or not caption_files:
            raise RuntimeError(result.stderr.strip() or "no English VTT captions found")
        return _parse_vtt(caption_files[0].read_text(encoding="utf-8", errors="replace"))


def _parse_vtt(vtt: str) -> list[dict]:
    """Convert a WebVTT caption file into the segment shape used by this app."""
    segments: list[dict] = []
    seen: set[tuple[float, str]] = set()
    for block in re.split(r"\n\s*\n", vtt.replace("\r\n", "\n")):
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        timing = next((line for line in lines if "-->" in line), None)
        if not timing:
            continue
        start_text, end_text = (part.strip().split(" ")[0] for part in timing.split("-->", 1))
        try:
            start = _vtt_seconds(start_text)
            end = _vtt_seconds(end_text)
        except ValueError:
            continue
        text_lines = lines[lines.index(timing) + 1:]
        text = re.sub(r"<[^>]+>", "", " ".join(text_lines))
        text = re.sub(r"\s+", " ", text).strip()
        key = (start, text)
        if text and key not in seen:
            seen.add(key)
            segments.append({"start": start, "duration": max(0, end - start), "text": text})
    if not segments:
        raise RuntimeError("caption file did not contain usable cues")
    return segments


def _vtt_seconds(value: str) -> float:
    """Parse a WebVTT timestamp (HH:MM:SS.mmm or MM:SS.mmm)."""
    parts = value.replace(",", ".").split(":")
    if len(parts) == 2:
        minutes, seconds = parts
        return int(minutes) * 60 + float(seconds)
    if len(parts) == 3:
        hours, minutes, seconds = parts
        return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
    raise ValueError(f"Invalid VTT timestamp: {value}")


def fetch_playlist(url_or_id: str) -> list[dict]:
    """Return public playlist entries using yt-dlp without downloading videos.

    Each item contains its video ID, title, and canonical watch URL.
    """
    playlist_url = (
        url_or_id if url_or_id.startswith(("http://", "https://"))
        else f"https://www.youtube.com/playlist?list={url_or_id}"
    )
    result = subprocess.run(
        ["yt-dlp", "--flat-playlist", "--dump-single-json", playlist_url],
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "yt-dlp could not read playlist")
    data = json.loads(result.stdout)
    entries = []
    for entry in data.get("entries") or []:
        video_id = entry.get("id")
        if video_id:
            entries.append({
                "id": video_id,
                "title": entry.get("title") or "Untitled",
                "url": f"https://www.youtube.com/watch?v={video_id}",
            })
    if not entries:
        raise RuntimeError("playlist contains no accessible videos")
    return entries
