# yt-translate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Python CLI tool that fetches YouTube transcripts and translates them to Simplified Chinese via a local Qwen model, outputting article-style Markdown.

**Architecture:** Four-stage pipeline — fetch transcript via `youtube-transcript-api`, chunk into ~800-word blocks, translate each chunk sequentially via OpenAI-compatible API to local Qwen3.6-35B, format as continuous-prose Markdown.

**Tech Stack:** Python 3.10+, click, youtube-transcript-api, openai, yt-dlp, python-slugify

## Global Constraints

- Python >= 3.10
- All dependencies pinned with minimum versions: youtube-transcript-api>=0.6.0, openai>=1.0.0, click>=8.0.0, yt-dlp>=2024.0.0, python-slugify>=8.0.0
- Default model server: `http://100.126.211.106:8000/v1`
- Default model: `Qwen/Qwen3.6-35B-A3B-FP8`
- Output format: article-style Markdown, no timestamps
- Sequential translation (one chunk at a time)
- Progress to stderr, output file to disk

---

### Task 1: Project Scaffolding & pyproject.toml

**Files:**
- Create: `pyproject.toml`
- Create: `src/yt_translate/__init__.py`
- Create: `src/yt_translate/cli.py` (stub)

**Interfaces:**
- Consumes: nothing
- Produces: installable package with `yt-translate` console script entry point

- [ ] **Step 1: Create pyproject.toml**

```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "yt-translate"
version = "0.1.0"
description = "Download YouTube transcripts and translate to Chinese"
requires-python = ">=3.10"
dependencies = [
    "youtube-transcript-api>=0.6.0",
    "openai>=1.0.0",
    "click>=8.0.0",
    "yt-dlp>=2024.0.0",
    "python-slugify>=8.0.0",
]

[project.scripts]
yt-translate = "yt_translate.cli:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

- [ ] **Step 2: Create src/yt_translate/__init__.py**

```python
"""yt-translate: YouTube transcript downloader and Chinese translator."""
```

- [ ] **Step 3: Create src/yt_translate/cli.py stub**

```python
"""CLI entry point for yt-translate."""

import click


@click.command()
@click.argument("youtube_url")
@click.option("--output", "-o", default=None, help="Output file path")
@click.option("--chunk-size", "-c", default=800, help="Words per translation chunk")
@click.option(
    "--base-url",
    default="http://100.126.211.106:8000/v1",
    help="OpenAI-compatible API base URL",
)
@click.option(
    "--model",
    "-m",
    default="Qwen/Qwen3.6-35B-A3B-FP8",
    help="Model name for the API",
)
def main(youtube_url: str, output: str | None, chunk_size: int, base_url: str, model: str) -> None:
    """Translate a YouTube video transcript to Chinese.

    YOUTUBE_URL: A YouTube video URL or video ID.
    """
    click.echo("yt-translate: not yet implemented", err=True)
    raise SystemExit(1)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Install in dev mode and verify CLI entry point**

```bash
cd /Users/sunnyyang/Projects/yt-translate
pip install -e .
yt-translate --help
```

Expected: help text showing `YOUTUBE_URL` argument and all options.

- [ ] **Step 5: Commit**

```bash
git init
git add pyproject.toml src/
git commit -m "feat: project scaffolding with CLI stub"
```

---

### Task 2: Chunker Module

**Files:**
- Create: `src/yt_translate/chunker.py`
- Create: `tests/test_chunker.py`

**Interfaces:**
- Consumes: list of transcript segments `list[dict]` where each dict has keys `"start"` (float), `"duration"` (float), `"text"` (str)
- Produces: `chunk_segments(segments: list[dict], chunk_size: int = 800) -> list[dict]` returning `[{"start": float, "text": str}]` — each item is a merged chunk with combined text and the start time of the first segment in that chunk

- [ ] **Step 1: Write failing tests**

```python
"""Tests for the chunker module."""

from yt_translate.chunker import chunk_segments


def test_single_short_segment():
    """A single short segment becomes one chunk."""
    segments = [{"start": 0.0, "duration": 5.0, "text": "Hello world"}]
    result = chunk_segments(segments, chunk_size=800)
    assert len(result) == 1
    assert result[0]["start"] == 0.0
    assert result[0]["text"] == "Hello world"


def test_multiple_segments_under_limit():
    """Multiple segments that fit within chunk_size are merged."""
    segments = [
        {"start": 0.0, "duration": 3.0, "text": "First sentence."},
        {"start": 3.0, "duration": 3.0, "text": "Second sentence."},
        {"start": 6.0, "duration": 3.0, "text": "Third sentence."},
    ]
    result = chunk_segments(segments, chunk_size=800)
    assert len(result) == 1
    assert result[0]["start"] == 0.0
    assert "First sentence." in result[0]["text"]
    assert "Third sentence." in result[0]["text"]


def test_segments_split_at_chunk_boundary():
    """Segments are split into multiple chunks when exceeding chunk_size."""
    # Each segment has 10 words
    segments = [
        {"start": float(i * 10), "duration": 10.0, "text": " ".join(["word"] * 10)}
        for i in range(20)
    ]
    # chunk_size=50 means ~5 segments per chunk
    result = chunk_segments(segments, chunk_size=50)
    assert len(result) == 4
    assert result[0]["start"] == 0.0
    assert result[1]["start"] == 50.0


def test_oversized_single_segment():
    """A single segment exceeding chunk_size becomes its own chunk."""
    big_text = " ".join(["word"] * 1000)
    segments = [
        {"start": 0.0, "duration": 5.0, "text": "Short intro."},
        {"start": 5.0, "duration": 60.0, "text": big_text},
        {"start": 65.0, "duration": 5.0, "text": "Short outro."},
    ]
    result = chunk_segments(segments, chunk_size=800)
    assert len(result) == 3
    assert result[1]["text"] == big_text


def test_empty_segments():
    """Empty input returns empty output."""
    result = chunk_segments([], chunk_size=800)
    assert result == []
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd /Users/sunnyyang/Projects/yt-translate
pytest tests/test_chunker.py -v
```

Expected: FAIL with `ModuleNotFoundError` or `ImportError`

- [ ] **Step 3: Implement chunker**

```python
"""Chunk transcript segments into groups of approximately N words."""


def chunk_segments(segments: list[dict], chunk_size: int = 800) -> list[dict]:
    """Group transcript segments into chunks of approximately chunk_size words.

    Args:
        segments: List of dicts with keys "start", "duration", "text".
        chunk_size: Target number of words per chunk.

    Returns:
        List of dicts with keys "start" (float) and "text" (str).
        Each dict represents a merged chunk.
    """
    if not segments:
        return []

    chunks: list[dict] = []
    current_texts: list[str] = []
    current_word_count = 0
    current_start = segments[0]["start"]

    for segment in segments:
        segment_word_count = len(segment["text"].split())

        # If adding this segment would exceed the limit and we already have content,
        # finalize the current chunk first
        if current_texts and current_word_count + segment_word_count > chunk_size:
            chunks.append({
                "start": current_start,
                "text": " ".join(current_texts),
            })
            current_texts = []
            current_word_count = 0
            current_start = segment["start"]

        current_texts.append(segment["text"])
        current_word_count += segment_word_count

    # Don't forget the last chunk
    if current_texts:
        chunks.append({
            "start": current_start,
            "text": " ".join(current_texts),
        })

    return chunks
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_chunker.py -v
```

Expected: all 5 tests PASS

- [ ] **Step 5: Commit**

```bash
git add src/yt_translate/chunker.py tests/test_chunker.py
git commit -m "feat: add chunker module with tests"
```

---

### Task 3: Transcript Fetcher Module

**Files:**
- Create: `src/yt_translate/fetcher.py`
- Create: `tests/test_fetcher.py`

**Interfaces:**
- Consumes: YouTube URL or video ID (str)
- Produces: `fetch_transcript(url: str) -> tuple[str, list[dict]]` returning `(video_title, segments)` where segments match the format consumed by `chunk_segments`

- [ ] **Step 1: Write failing tests**

```python
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
    def test_successful_fetch(self, mock_api, mock_title):
        mock_title.return_value = "Test Video Title"
        mock_transcript = [
            {"start": 0.0, "duration": 5.0, "text": "Hello world"},
            {"start": 5.0, "duration": 3.0, "text": "This is a test"},
        ]
        mock_api.get_transcript.return_value = mock_transcript

        title, segments = fetch_transcript("https://www.youtube.com/watch?v=abc123")

        assert title == "Test Video Title"
        assert len(segments) == 2
        assert segments[0]["text"] == "Hello world"

    @patch("yt_translate.fetcher._get_video_title")
    @patch("yt_translate.fetcher.YouTubeTranscriptApi")
    def test_no_transcript_available(self, mock_api, mock_title):
        from youtube_transcript_api._errors import TranscriptsDisabled

        mock_api.get_transcript.side_effect = TranscriptsDisabled("abc123")

        with pytest.raises(SystemExit):
            fetch_transcript("https://www.youtube.com/watch?v=abc123")
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_fetcher.py -v
```

Expected: FAIL with `ImportError`

- [ ] **Step 3: Implement fetcher**

```python
"""Fetch YouTube video transcript and title."""

import re
import subprocess
import sys
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

    try:
        segments = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
    except (TranscriptsDisabled, NoTranscriptFound):
        try:
            # Fallback: try any available language
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            transcript = transcript_list.find_transcript(["en"])
            segments = transcript.fetch()
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
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_fetcher.py -v
```

Expected: all tests PASS

- [ ] **Step 5: Commit**

```bash
git add src/yt_translate/fetcher.py tests/test_fetcher.py
git commit -m "feat: add transcript fetcher with URL parsing"
```

---

### Task 4: Translator Module

**Files:**
- Create: `src/yt_translate/translator.py`
- Create: `tests/test_translator.py`

**Interfaces:**
- Consumes: list of chunk dicts `[{"start": float, "text": str}]`, base_url (str), model (str)
- Produces: `translate_chunks(chunks: list[dict], base_url: str, model: str) -> list[dict]` returning `[{"start": float, "text": str, "success": bool}]` where `text` is the translated Chinese text (or `[TRANSLATION FAILED]` on failure)

- [ ] **Step 1: Write failing tests**

```python
"""Tests for the translator module."""

from unittest.mock import patch, MagicMock

from yt_translate.translator import translate_chunks, translate_single_chunk


class TestTranslateSingleChunk:
    """Tests for single chunk translation."""

    @patch("yt_translate.translator.OpenAI")
    def test_successful_translation(self, mock_openai_cls):
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

    @patch("yt_translate.translator.OpenAI")
    def test_retry_on_failure(self, mock_openai_cls):
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

    @patch("yt_translate.translator.OpenAI")
    def test_failure_after_retries(self, mock_openai_cls):
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("Server down")

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
        assert result[0]["success"] is True
        assert result[1]["text"] == "第二段"

    @patch("yt_translate.translator.translate_single_chunk")
    def test_partial_failure(self, mock_translate):
        mock_translate.side_effect = ["第一段", None]
        chunks = [
            {"start": 0.0, "text": "First paragraph"},
            {"start": 60.0, "text": "Second paragraph"},
        ]

        result = translate_chunks(chunks, base_url="http://x/v1", model="m")

        assert result[0]["success"] is True
        assert result[1]["success"] is False
        assert result[1]["text"] == "[TRANSLATION FAILED]"
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_translator.py -v
```

Expected: FAIL with `ImportError`

- [ ] **Step 3: Implement translator**

```python
"""Translate text chunks using an OpenAI-compatible API."""

import sys
import time

import click
from openai import OpenAI

SYSTEM_PROMPT = (
    "You are a professional translator. Translate the following English transcript "
    "to Simplified Chinese. Preserve the original meaning and produce natural, fluent "
    "Chinese. Do not add explanations, commentary, or annotations. Output only the "
    "translation."
)

MAX_RETRIES = 3
RETRY_DELAYS = [1, 2, 4]  # seconds
TEMPERATURE = 0.3
MAX_TOKENS = 4096
TIMEOUT = 30


def translate_single_chunk(
    text: str,
    base_url: str,
    model: str,
) -> str | None:
    """Translate a single text chunk to Chinese.

    Args:
        text: English text to translate.
        base_url: OpenAI-compatible API base URL.
        model: Model name to use.

    Returns:
        Translated Chinese text, or None if all retries failed.
    """
    client = OpenAI(base_url=base_url, api_key="not-needed")

    for attempt in range(MAX_RETRIES):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": text},
                ],
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
                timeout=TIMEOUT,
            )
            content = response.choices[0].message.content
            if content:
                return content.strip()
            return None
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAYS[attempt])
            else:
                click.echo(f"  Warning: Translation failed after {MAX_RETRIES} attempts: {e}", err=True)
                return None

    return None


def translate_chunks(
    chunks: list[dict],
    base_url: str,
    model: str,
) -> list[dict]:
    """Translate all chunks sequentially.

    Args:
        chunks: List of dicts with keys "start" and "text".
        base_url: OpenAI-compatible API base URL.
        model: Model name to use.

    Returns:
        List of dicts with keys "start", "text" (translated), and "success" (bool).
    """
    results: list[dict] = []
    total = len(chunks)

    for i, chunk in enumerate(chunks, 1):
        click.echo(f"Translating chunk {i}/{total}...", err=True)

        translated = translate_single_chunk(chunk["text"], base_url, model)

        if translated:
            results.append({"start": chunk["start"], "text": translated, "success": True})
        else:
            results.append({"start": chunk["start"], "text": "[TRANSLATION FAILED]", "success": False})

    return results
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_translator.py -v
```

Expected: all tests PASS

- [ ] **Step 5: Commit**

```bash
git add src/yt_translate/translator.py tests/test_translator.py
git commit -m "feat: add translator module with retry logic"
```

---

### Task 5: Markdown Formatter Module

**Files:**
- Create: `src/yt_translate/formatter.py`
- Create: `tests/test_formatter.py`

**Interfaces:**
- Consumes: video title (str), youtube URL (str), translated chunks `list[dict]` with keys "start", "text", "success"
- Produces: `format_markdown(title: str, url: str, chunks: list[dict]) -> str` returning the complete Markdown string; `generate_filename(title: str) -> str` returning the slugified filename

- [ ] **Step 1: Write failing tests**

```python
"""Tests for the formatter module."""

from yt_translate.formatter import format_markdown, generate_filename


class TestFormatMarkdown:
    """Tests for Markdown output formatting."""

    def test_basic_output(self):
        chunks = [
            {"start": 0.0, "text": "第一段翻译内容。", "success": True},
            {"start": 60.0, "text": "第二段翻译内容。", "success": True},
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

    def test_article_style_continuous_prose(self):
        chunks = [
            {"start": 0.0, "text": "第一段。", "success": True},
            {"start": 30.0, "text": "第二段。", "success": True},
        ]
        result = format_markdown("Title", "http://url", chunks)

        # Chunks separated by double newline (paragraph break)
        assert "第一段。\n\n第二段。" in result

    def test_failed_chunk_placeholder(self):
        chunks = [
            {"start": 0.0, "text": "成功翻译。", "success": True},
            {"start": 30.0, "text": "[TRANSLATION FAILED]", "success": False},
        ]
        result = format_markdown("Title", "http://url", chunks)
        assert "[TRANSLATION FAILED]" in result


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
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_formatter.py -v
```

Expected: FAIL with `ImportError`

- [ ] **Step 3: Implement formatter**

```python
"""Format translated chunks into article-style Markdown."""

from datetime import date

from slugify import slugify


def format_markdown(title: str, url: str, chunks: list[dict]) -> str:
    """Format translated chunks as article-style Markdown.

    Args:
        title: Original video title (English).
        url: Source YouTube URL.
        chunks: List of dicts with keys "start", "text", "success".

    Returns:
        Complete Markdown string.
    """
    today = date.today().isoformat()

    header = f"""# {title}

**Original Title:** {title}
**Source:** {url}
**Translated:** {today}

---

"""

    body = "\n\n".join(chunk["text"] for chunk in chunks)

    return header + body + "\n"


def generate_filename(title: str) -> str:
    """Generate a slugified filename from the video title.

    Args:
        title: Video title string.

    Returns:
        Filename like "video-title_zh.md".
    """
    if not title.strip():
        return "untitled_zh.md"

    slug = slugify(title, max_length=60)

    if not slug:
        return "untitled_zh.md"

    return f"{slug}_zh.md"
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_formatter.py -v
```

Expected: all tests PASS

- [ ] **Step 5: Commit**

```bash
git add src/yt_translate/formatter.py tests/test_formatter.py
git commit -m "feat: add markdown formatter for article-style output"
```

---

### Task 6: Wire Up CLI (Integration)

**Files:**
- Modify: `src/yt_translate/cli.py`

**Interfaces:**
- Consumes: `fetch_transcript`, `chunk_segments`, `translate_chunks`, `format_markdown`, `generate_filename`
- Produces: complete working CLI that orchestrates the full pipeline

- [ ] **Step 1: Write an integration test**

Create `tests/test_cli.py`:

```python
"""Integration tests for the CLI."""

from unittest.mock import patch, MagicMock
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
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_cli.py -v
```

Expected: FAIL (cli.py doesn't import or call the modules yet)

- [ ] **Step 3: Implement the full CLI**

Replace `src/yt_translate/cli.py` with:

```python
"""CLI entry point for yt-translate."""

import sys
from pathlib import Path

import click

from yt_translate.fetcher import fetch_transcript
from yt_translate.chunker import chunk_segments
from yt_translate.translator import translate_chunks
from yt_translate.formatter import format_markdown, generate_filename


@click.command()
@click.argument("youtube_url")
@click.option("--output", "-o", default=None, help="Output file path")
@click.option("--chunk-size", "-c", default=800, help="Words per translation chunk")
@click.option(
    "--base-url",
    default="http://100.126.211.106:8000/v1",
    help="OpenAI-compatible API base URL",
)
@click.option(
    "--model",
    "-m",
    default="Qwen/Qwen3.6-35B-A3B-FP8",
    help="Model name for the API",
)
def main(youtube_url: str, output: str | None, chunk_size: int, base_url: str, model: str) -> None:
    """Translate a YouTube video transcript to Chinese.

    YOUTUBE_URL: A YouTube video URL or video ID.
    """
    # Step 1: Fetch transcript
    click.echo("Fetching transcript...", err=True)
    title, segments = fetch_transcript(youtube_url)
    click.echo(f"Got transcript: \"{title}\" ({len(segments)} segments)", err=True)

    # Step 2: Chunk
    chunks = chunk_segments(segments, chunk_size=chunk_size)
    click.echo(f"Split into {len(chunks)} chunks for translation", err=True)

    # Step 3: Translate
    translated = translate_chunks(chunks, base_url=base_url, model=model)

    # Step 4: Format and save
    markdown = format_markdown(title, youtube_url, translated)

    if output:
        output_path = Path(output)
    else:
        output_path = Path(generate_filename(title))

    output_path.write_text(markdown, encoding="utf-8")

    # Summary
    success_count = sum(1 for c in translated if c["success"])
    total_count = len(translated)

    if success_count == total_count:
        click.echo(f"Done! Saved to {output_path} ({success_count}/{total_count} chunks translated)", err=True)
    else:
        failed = total_count - success_count
        click.echo(
            f"Saved to {output_path} ({success_count}/{total_count} chunks translated, {failed} failed)",
            err=True,
        )


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run all tests**

```bash
pytest tests/ -v
```

Expected: all tests PASS

- [ ] **Step 5: Manual smoke test (optional, requires network)**

```bash
yt-translate "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -o test_output.md
```

- [ ] **Step 6: Commit**

```bash
git add src/yt_translate/cli.py tests/test_cli.py
git commit -m "feat: wire up CLI with full translation pipeline"
```

---

### Task 7: Final Polish

**Files:**
- Create: `tests/__init__.py`
- Verify all tests pass together

**Interfaces:**
- Consumes: all modules
- Produces: fully working, tested project

- [ ] **Step 1: Create tests/__init__.py**

```python
```

(Empty file to make tests a proper package)

- [ ] **Step 2: Run full test suite**

```bash
cd /Users/sunnyyang/Projects/yt-translate
pytest tests/ -v --tb=short
```

Expected: all tests PASS

- [ ] **Step 3: Verify installation**

```bash
pip install -e .
yt-translate --help
```

Expected: clean help output with all options

- [ ] **Step 4: Commit any remaining files**

```bash
git add tests/__init__.py
git commit -m "chore: finalize test structure"
```
