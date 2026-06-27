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
