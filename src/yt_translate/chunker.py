"""Chunk transcript segments into groups of approximately N words."""


def chunk_segments(segments: list[dict], chunk_size: int = 150) -> list[dict]:
    """Group transcript segments into chunks of approximately chunk_size words.

    Default chunk_size is 150 words (paragraph-sized) for dual-language output.

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
