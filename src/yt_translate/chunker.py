"""Chunk transcript segments into natural paragraphs."""

import re


def chunk_segments(segments: list[dict], chunk_size: int = 4) -> list[dict]:
    """Group transcript segments into natural paragraphs.

    Merges all segments into continuous text, splits into sentences,
    then groups sentences into paragraphs. This ensures no sentence
    is ever cut mid-way, which is critical for poetry, philosophy,
    and religious content.

    Args:
        segments: List of dicts with keys "start", "duration", "text".
        chunk_size: Number of sentences per paragraph (default: 4).

    Returns:
        List of dicts with keys "start" (float) and "text" (str).
        Each dict represents one paragraph.
    """
    if not segments:
        return []

    # Step 1: Merge all segment text into one continuous string
    full_text = " ".join(seg["text"] for seg in segments)

    # Step 2: Split into sentences using punctuation boundaries
    # Handles: period, exclamation, question mark — followed by space or end
    # Preserves the punctuation with the sentence
    sentences = _split_sentences(full_text)

    if not sentences:
        return [{"start": segments[0]["start"], "text": full_text}]

    # Step 3: Group sentences into paragraphs of chunk_size sentences each
    chunks: list[dict] = []
    for i in range(0, len(sentences), chunk_size):
        paragraph_sentences = sentences[i : i + chunk_size]
        paragraph_text = " ".join(paragraph_sentences)

        # Estimate the start time based on position in the full text
        start_time = _estimate_start_time(
            paragraph_sentences[0], full_text, segments
        )

        chunks.append({"start": start_time, "text": paragraph_text})

    return chunks


def _split_sentences(text: str) -> list[str]:
    """Split text into sentences at sentence-ending punctuation.

    Handles common abbreviations and edge cases like:
    - Mr. Mrs. Dr. St. etc. (not sentence endings)
    - Quoted speech ending with punctuation
    - Ellipsis (...)
    - Single-letter abbreviations like U.S., i.e., e.g.

    Args:
        text: Continuous text string.

    Returns:
        List of sentence strings, each stripped of leading/trailing whitespace.
    """
    # Common abbreviations that should NOT trigger a sentence split
    abbreviations = {
        "Mr", "Mrs", "Ms", "Dr", "Prof", "Sr", "Jr", "St", "Rev", "Gen",
        "Sgt", "Cpl", "Pvt", "Lt", "Col", "Maj", "Capt", "Cmdr", "Adm",
        "Gov", "Sen", "Rep", "Pres", "Dept", "Univ", "Assn", "Bros",
        "Inc", "Ltd", "Co", "Corp", "vs", "etc", "approx", "appt",
        "est", "dept", "avg", "Vol", "No", "Fig", "eq",
    }

    # Strategy: use regex to find potential split points, then filter out
    # those that follow known abbreviations
    # Find all positions where ". " or "! " or "? " occurs before an uppercase letter
    sentences: list[str] = []
    current_pos = 0

    # Find candidate split points
    for match in re.finditer(r'([.!?])\s+(?=[A-Z"])', text):
        split_pos = match.end()
        punct_pos = match.start()

        # Check if this period follows an abbreviation
        if match.group(1) == ".":
            # Look back to find the word before the period
            before = text[:punct_pos]
            word_match = re.search(r'(\b[A-Za-z]+)$', before)
            if word_match:
                word = word_match.group(1)
                # Skip if it's a known abbreviation or single letter (like U.S.A)
                if word in abbreviations or len(word) == 1:
                    continue

        sentences.append(text[current_pos:split_pos].strip())
        current_pos = split_pos

    # Don't forget the last sentence
    remaining = text[current_pos:].strip()
    if remaining:
        sentences.append(remaining)

    return [s for s in sentences if s]


def _estimate_start_time(
    first_sentence: str, full_text: str, segments: list[dict]
) -> float:
    """Estimate the start time of a paragraph based on text position.

    Finds where the paragraph starts in the full text, calculates the
    character ratio, and maps it to the timeline.

    Args:
        first_sentence: The first sentence of the paragraph.
        full_text: The complete merged transcript text.
        segments: Original segments with timing info.

    Returns:
        Estimated start time in seconds.
    """
    # Find position of this sentence in the full text
    pos = full_text.find(first_sentence[:50])  # Use first 50 chars to find position
    if pos <= 0:
        return segments[0]["start"]

    # Calculate character ratio through the text
    ratio = pos / len(full_text)

    # Map to timeline
    total_duration = segments[-1]["start"] + segments[-1]["duration"] - segments[0]["start"]
    return segments[0]["start"] + ratio * total_duration
