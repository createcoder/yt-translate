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
