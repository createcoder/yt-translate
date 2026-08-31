from pathlib import Path

from yt_translate.build_site import build_site


def test_build_site_includes_playlist_brief(tmp_path: Path):
    articles = tmp_path / "articles"
    playlist = tmp_path / "playlist-summaries" / "PLtest"
    articles.mkdir()
    playlist.mkdir(parents=True)
    (playlist / "001-video.md").write_text(
        "# Video\n\n- **Video:** https://youtube.com/watch?v=abc\n- **Generated:** 2026-08-31 12:00 UTC\n- **Status:** Completed\n\n## Technical brief\n\n## Executive takeaway\n\nUseful\n\n## Full transcript\n\n[00:00] Source text\n",
        encoding="utf-8",
    )
    assert build_site(articles, tmp_path / "site") == 1
    data = (tmp_path / "site" / "data" / "articles.json").read_text(encoding="utf-8")
    assert '"type": "playlist_brief"' in data
    assert "Source text" in data
