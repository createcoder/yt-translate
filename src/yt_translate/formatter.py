"""Format translated chunks into dual-language Markdown."""

import re
from datetime import date

from slugify import slugify


_LINE_LEADING_MARKER = re.compile(r"^(>\s+)?>>\s*(.*)$")
_INLINE_MARKER = re.compile(r"\s*>>\s*")


def strip_speaker_markers(text: str) -> str:
    """Remove ">>" speaker-change markers injected by YouTube captions.

    YouTube uses ">>" to signal a speaker change. Preserving the marker
    clutters the raw markdown; the site's dual-language rendering already
    handles speaker turns. Line-leading ">>" is stripped (dropping the
    line if that's all it contained); inline ">>" collapses to a single
    space. Idempotent.
    """
    out_lines = []
    for line in text.split("\n"):
        m = _LINE_LEADING_MARKER.match(line)
        if m:
            prefix, rest = m.groups()
            if not rest.strip():
                continue  # entire line was just the marker
            line = (prefix or "") + rest
        line = _INLINE_MARKER.sub(" ", line)
        out_lines.append(line)
    return "\n".join(out_lines)


def format_markdown(title: str, url: str, chunks: list[dict]) -> str:
    """Format translated chunks as dual-language Markdown.

    Each paragraph shows the original English (in blockquote) followed by
    the Chinese translation, making it easy to learn from.

    Args:
        title: Original video title (English).
        url: Source YouTube URL.
        chunks: List of dicts with keys "original", "text", "success".

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

    paragraphs = []
    for chunk in chunks:
        original = strip_speaker_markers(chunk.get("original", ""))
        translated = strip_speaker_markers(chunk["text"])
        # Format original as blockquote
        quoted_original = "\n".join(f"> {line}" for line in original.split("\n"))
        paragraphs.append(f"{quoted_original}\n\n{translated}")

    body = "\n\n---\n\n".join(paragraphs)

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
