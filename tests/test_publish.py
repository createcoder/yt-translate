"""Tests for the publish module."""

import subprocess
from pathlib import Path
from unittest.mock import patch, call

import pytest
from yt_translate.publish import publish


@pytest.fixture
def git_repo(tmp_path):
    """Create a temporary git repo with articles/ and site/ dirs."""
    subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=tmp_path, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp_path, capture_output=True)

    (tmp_path / "articles").mkdir()
    (tmp_path / "site").mkdir()
    (tmp_path / "articles" / "test_zh.md").write_text("# Test")
    (tmp_path / "site" / "index.html").write_text("<html>")

    subprocess.run(["git", "add", "."], cwd=tmp_path, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=tmp_path, capture_output=True)
    return tmp_path


class TestPublish:
    def test_commits_articles_and_site(self, git_repo):
        (git_repo / "articles" / "new_zh.md").write_text("# New")
        (git_repo / "site" / "data").mkdir()
        (git_repo / "site" / "data" / "articles.json").write_text("{}")

        with patch("yt_translate.publish._git_push") as mock_push:
            mock_push.return_value = True
            result = publish(git_repo, "New Article")

        assert result is True

        # Verify commit was made
        log = subprocess.run(
            ["git", "log", "--oneline", "-1"],
            cwd=git_repo, capture_output=True, text=True
        )
        assert "Add: New Article" in log.stdout

    def test_no_changes_returns_false(self, git_repo):
        with patch("yt_translate.publish._git_push") as mock_push:
            result = publish(git_repo, "Nothing")

        assert result is False
        mock_push.assert_not_called()

    def test_push_failure_returns_false(self, git_repo):
        (git_repo / "articles" / "fail_zh.md").write_text("# Fail")

        with patch("yt_translate.publish._git_push") as mock_push:
            mock_push.return_value = False
            result = publish(git_repo, "Fail Article")

        assert result is False
