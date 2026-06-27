"""Format translated chunks into dual-language Markdown."""

from datetime import date

from slugify import slugify


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
        original = chunk.get("original", "")
        translated = chunk["text"]
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
