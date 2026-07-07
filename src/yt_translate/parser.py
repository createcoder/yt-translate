"""Parse translated article markdown into structured data."""

import re
from pathlib import Path


def parse_article(text: str) -> dict:
    """Parse a _zh.md file into structured article data.

    Args:
        text: Full markdown content of a translated article.

    Returns:
        Dict with keys: title, source, date, paragraphs.
        Each paragraph has: id, en, zh.
    """
    lines = text.strip().split("\n")

    title = ""
    source = ""
    date_str = ""

    # Parse header
    for line in lines:
        if line.startswith("# ") and not title:
            title = line[2:].strip()
        elif line.startswith("**Source:**"):
            source = line.replace("**Source:**", "").strip()
        elif line.startswith("**Translated:**"):
            date_str = line.replace("**Translated:**", "").strip()

    # Normalize bare video ID to full URL
    if source and re.match(r"^[A-Za-z0-9_-]{11}$", source):
        source = f"https://www.youtube.com/watch?v={source}"

    # Parse paragraphs: split by --- separators
    # Find the first --- after the header to start paragraph parsing
    content = text.strip()
    # Split on --- lines (with optional surrounding whitespace)
    sections = re.split(r"\n---\n", content)

    # First section is the header, skip it
    paragraphs = []
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:30]

    for i, section in enumerate(sections[1:]):
        section = section.strip()
        if not section:
            continue

        # Extract English (blockquote lines) and Chinese (non-blockquote)
        en_lines = []
        zh_lines = []

        for line in section.split("\n"):
            if line.startswith("> "):
                en_lines.append(line[2:])
            elif line.startswith(">"):
                en_lines.append(line[1:])
            elif line.strip():
                zh_lines.append(line.strip())

        en_text = " ".join(en_lines).strip()
        zh_text = "\n".join(zh_lines).strip()

        if en_text or zh_text:
            paragraphs.append({
                "id": f"{slug}-{i}",
                "en": en_text,
                "zh": zh_text,
            })

    return {
        "title": title,
        "source": source,
        "date": date_str,
        "paragraphs": paragraphs,
    }
