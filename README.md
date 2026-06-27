# yt-translate

CLI tool that downloads YouTube video transcripts and translates them to Simplified Chinese, outputting a dual-language Markdown file for easy learning.

## Features

- Fetches transcripts from YouTube (manual or auto-generated captions)
- Translates to Simplified Chinese via a local Qwen3.6-35B model (OpenAI-compatible API)
- **Dual-language output** — English in blockquotes, Chinese translation below, paragraph by paragraph
- **Sentence-aware chunking** — never cuts mid-sentence; handles abbreviations (Mr., Dr., U.S.) correctly
- Retry logic with exponential backoff
- Progress reporting to stderr

## Output Format

```markdown
# Video Title

**Original Title:** Video Title
**Source:** https://youtube.com/watch?v=...
**Translated:** 2025-06-27

---

> This week, three candidates backed by New York City Mayor swept to victory.

本周，三位由纽约市长支持的候选人取得了压倒性胜利。

---

> But nobody is going to show you what I'm going to tell you in this video.

但没有人会向你展示我在这个视频中要告诉你的内容。
```

## Installation

```bash
git clone https://github.com/createcoder/yt-translate.git
cd yt-translate
pip install -e .
```

Requires Python 3.10+ and `yt-dlp` installed on your system.

## Usage

```bash
# Basic usage (outputs <video-title>_zh.md in current directory)
yt-translate "https://www.youtube.com/watch?v=VIDEO_ID"

# Custom output path
yt-translate "https://youtu.be/VIDEO_ID" -o my-translation.md

# Fewer sentences per paragraph (default: 4)
yt-translate "https://youtube.com/watch?v=VIDEO_ID" --chunk-size 3

# Use a different model server
yt-translate "https://youtube.com/watch?v=VIDEO_ID" --base-url http://localhost:8000/v1

# Use a different model
yt-translate "https://youtube.com/watch?v=VIDEO_ID" -m "Qwen/Qwen2.5-72B"
```

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--output` / `-o` | Auto from title | Output file path |
| `--chunk-size` / `-c` | 4 | Sentences per paragraph |
| `--base-url` | `http://100.126.211.106:8000/v1` | OpenAI-compatible API base URL |
| `--model` / `-m` | `Qwen/Qwen3.6-35B-A3B-FP8` | Model name |

## Requirements

- Python >= 3.10
- A running OpenAI-compatible model server (e.g., vLLM with Qwen)
- `yt-dlp` (for video title extraction)

## Dependencies

- `youtube-transcript-api` — fetch YouTube captions
- `openai` — OpenAI-compatible API client
- `click` — CLI framework
- `yt-dlp` — video title extraction
- `python-slugify` — filename generation

## Running Tests

```bash
pip install pytest
pytest tests/ -v
```

## License

MIT
