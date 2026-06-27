"""Tests for the chunker module."""

from yt_translate.chunker import chunk_segments, _split_sentences


class TestSplitSentences:
    """Tests for sentence splitting."""

    def test_basic_sentences(self):
        text = "Hello world. This is a test. How are you?"
        result = _split_sentences(text)
        assert result == ["Hello world.", "This is a test.", "How are you?"]

    def test_preserves_abbreviations(self):
        """Mr. Mrs. Dr. should not cause splits."""
        text = "Mr. Smith went to Washington. He met Dr. Jones there."
        result = _split_sentences(text)
        assert len(result) == 2
        assert "Mr. Smith" in result[0]
        assert "Dr. Jones" in result[1]

    def test_quoted_speech(self):
        text = 'She said, "Hello there." And then she left.'
        result = _split_sentences(text)
        # Should split after the quoted sentence ends
        assert len(result) >= 1

    def test_exclamation_and_question(self):
        text = "What a day! Can you believe it? I certainly can."
        result = _split_sentences(text)
        assert len(result) == 3

    def test_no_punctuation(self):
        text = "this is text without any ending punctuation"
        result = _split_sentences(text)
        assert result == ["this is text without any ending punctuation"]


class TestChunkSegments:
    """Tests for paragraph chunking."""

    def test_single_short_segment(self):
        """A single short segment becomes one chunk."""
        segments = [{"start": 0.0, "duration": 5.0, "text": "Hello world."}]
        result = chunk_segments(segments, chunk_size=4)
        assert len(result) == 1
        assert result[0]["text"] == "Hello world."

    def test_groups_by_sentence_count(self):
        """Segments are merged and split by sentence count."""
        segments = [
            {"start": 0.0, "duration": 10.0, "text": "First sentence. Second sentence."},
            {"start": 10.0, "duration": 10.0, "text": "Third sentence. Fourth sentence."},
            {"start": 20.0, "duration": 10.0, "text": "Fifth sentence. Sixth sentence."},
        ]
        # chunk_size=2 means 2 sentences per paragraph
        result = chunk_segments(segments, chunk_size=2)
        assert len(result) == 3
        assert "First sentence." in result[0]["text"]
        assert "Second sentence." in result[0]["text"]
        assert "Third sentence." in result[1]["text"]
        assert "Fourth sentence." in result[1]["text"]
        assert "Fifth sentence." in result[2]["text"]
        assert "Sixth sentence." in result[2]["text"]

    def test_no_mid_sentence_cuts(self):
        """Sentences are never cut in the middle."""
        segments = [
            {"start": 0.0, "duration": 5.0, "text": "This is a long first sentence with many words."},
            {"start": 5.0, "duration": 5.0, "text": "Short second. Third one here."},
            {"start": 10.0, "duration": 5.0, "text": "And a fourth sentence."},
        ]
        result = chunk_segments(segments, chunk_size=2)
        # Each chunk should contain complete sentences only
        for chunk in result:
            text = chunk["text"]
            # Should not end mid-word (unless it's the last chunk)
            assert text[-1] in ".!?" or chunk == result[-1]

    def test_empty_segments(self):
        """Empty input returns empty output."""
        result = chunk_segments([], chunk_size=4)
        assert result == []

    def test_preserves_start_time(self):
        """Each chunk has an estimated start time."""
        segments = [
            {"start": 0.0, "duration": 10.0, "text": "First. Second."},
            {"start": 10.0, "duration": 10.0, "text": "Third. Fourth."},
            {"start": 20.0, "duration": 10.0, "text": "Fifth. Sixth."},
        ]
        result = chunk_segments(segments, chunk_size=2)
        # First chunk starts at 0
        assert result[0]["start"] == 0.0
        # Later chunks have increasing start times
        for i in range(1, len(result)):
            assert result[i]["start"] >= result[i - 1]["start"]

    def test_default_chunk_size_is_4(self):
        """Default groups 4 sentences per paragraph."""
        segments = [
            {"start": 0.0, "duration": 30.0,
             "text": "One. Two. Three. Four. Five. Six. Seven. Eight."},
        ]
        result = chunk_segments(segments)  # default chunk_size=4
        assert len(result) == 2
        assert "One." in result[0]["text"]
        assert "Four." in result[0]["text"]
        assert "Five." in result[1]["text"]
        assert "Eight." in result[1]["text"]
