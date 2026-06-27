# yt-translate Design Spec

## Overview

A Python CLI tool that downloads YouTube video transcripts and translates them to Simplified Chinese using a local Qwen3.6-35B model, outputting a formatted Markdown file.

## Architecture

Pipeline with four stages:

```
YouTube URL → [Fetch Transcript] → [Chunk] → [Translate via Qwen] → Markdown File
```

## Components

### 1. Transcript Fetcher

- Uses `youtube-transcript-api` to fetch captions from YouTube
- Preference order: manual English captions > auto-generated English > any available language
- Extracts video title via `yt-dlp --get-title` (no video download)
- Returns: video title (str) and list of segments `[{"start": float, "duration": float, "text": str}]`

### 2. Chunker

- Groups transcript segments into chunks of ~800 words (configurable via `--chunk-size`)
- Each chunk preserves the timestamp of its first segment as the chunk timestamp
- Does not split segments mid-sentence — a segment always belongs to exactly one chunk
- If a single segment exceeds the chunk size, it becomes its own chunk

### 3. Translator

- Endpoint: `http://100.126.211.106:8000/v1/chat/completions`
- Model: `Qwen/Qwen3.6-35B-A3B-FP8`
- System prompt: "You are a professional translator. Translate the following English transcript to Simplified Chinese. Preserve the original meaning and produce natural, fluent Chinese. Do not add explanations, commentary, or annotations. Output only the translation."
- Processing: sequential (one chunk at a time to avoid overloading the single-GPU server)
- Retry: 3 attempts with exponential backoff (1s, 2s, 4s)
- Temperature: 0.3 (low creativity, high fidelity)
- Max tokens per chunk: 4096

### 4. Markdown Formatter

Output structure — article-style, no timestamps:

```markdown
# <Translated Chinese Title>

**Original Title:** <English title>
**Source:** <YouTube URL>
**Translated:** <YYYY-MM-DD>

---

<translated text for chunk 1>

<translated text for chunk 2>

...
```

- Chunks are joined as continuous prose with paragraph breaks between them
- No timestamp headers — the output reads like a natural article
- File saved as `<slugified-video-title>_zh.md` in the current directory (or `--output` path)
- Slug: lowercase, spaces to hyphens, strip special chars, max 60 chars

## CLI Interface

```bash
yt-translate <youtube-url> [--output <path>] [--chunk-size <int>] [--base-url <url>] [--model <name>]
```

### Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `youtube-url` | Yes | — | YouTube URL or video ID |
| `--output` / `-o` | No | Auto from title | Output file path |
| `--chunk-size` / `-c` | No | 800 | Words per translation chunk |
| `--base-url` | No | `http://100.126.211.106:8000/v1` | OpenAI-compatible API base URL |
| `--model` / `-m` | No | `Qwen/Qwen3.6-35B-A3B-FP8` | Model name for the API |

### Examples

```bash
# Basic usage
yt-translate "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Custom output path
yt-translate "https://youtu.be/abc123" -o my-translation.md

# Use a different model server
yt-translate "https://youtube.com/watch?v=xyz" --base-url http://localhost:8000/v1
```

## Error Handling

| Scenario | Behavior |
|----------|----------|
| No captions available | Exit with error: "No transcript available for this video. The video may not have captions enabled." |
| Invalid YouTube URL | Exit with error: "Invalid YouTube URL or video ID." |
| Model server unreachable | Exit with error: "Cannot connect to model server at <url>. Ensure the server is running." |
| Translation chunk fails after retries | Log warning, insert `[TRANSLATION FAILED]` placeholder for that chunk, continue with remaining chunks |
| Partial completion | Save whatever is translated so far, print summary of failed chunks |
| Network timeout | 30s timeout per API call, then retry |

## Progress Reporting

- Print progress to stderr: `Translating chunk 3/12...`
- On completion: `Done! Saved to <filename> (12/12 chunks translated)`
- On partial: `Saved to <filename> (10/12 chunks translated, 2 failed)`

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `youtube-transcript-api` | >=0.6.0 | Fetch YouTube captions |
| `openai` | >=1.0.0 | OpenAI-compatible API client for vLLM |
| `click` | >=8.0.0 | CLI framework |
| `yt-dlp` | >=2024.0.0 | Video title extraction |
| `python-slugify` | >=8.0.0 | Title to filename slug |

Python version: >=3.10

## Project Structure

```
yt-translate/
├── pyproject.toml
├── README.md
├── src/
│   └── yt_translate/
│       ├── __init__.py
│       ├── cli.py          # Click CLI entry point
│       ├── fetcher.py      # Transcript fetching
│       ├── chunker.py      # Text chunking logic
│       ├── translator.py   # Qwen API integration
│       └── formatter.py    # Markdown output formatting
└── tests/
    ├── test_chunker.py
    ├── test_fetcher.py
    ├── test_formatter.py
    └── test_translator.py
```

## Installation

```bash
cd yt-translate
pip install -e .
```

The `pyproject.toml` registers `yt-translate` as a console script entry point.

## Success Criteria

1. Running `yt-translate <url>` on a video with English captions produces a well-formatted Chinese markdown file
2. Translation quality is natural and fluent (leveraging Qwen3.6-35B)
3. Long videos (1+ hour) complete without crashing, with progress feedback
4. Failed chunks don't block the rest of the translation
5. The tool is installable via `pip install -e .` and usable immediately
