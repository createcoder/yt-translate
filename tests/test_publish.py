"""Tests for the publish module."""

import subprocess
from unittest.mock import patch

import pytest
from yt_translate.publish import PublishOutcome, publish


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
            mock_push.return_value = subprocess.CompletedProcess(
                args=["git", "push"], returncode=0, stdout="", stderr=""
            )
            result = publish(git_repo, "New Article")

        assert result.outcome == PublishOutcome.PUBLISHED
        assert result.ok

        # Verify commit was made
        log = subprocess.run(
            ["git", "log", "--oneline", "-1"],
            cwd=git_repo, capture_output=True, text=True
        )
        assert "Add: New Article" in log.stdout

    def test_no_changes_returns_no_changes_outcome(self, git_repo):
        with patch("yt_translate.publish._git_push") as mock_push:
            result = publish(git_repo, "Nothing")

        assert result.outcome == PublishOutcome.NO_CHANGES
        assert not result.ok
        mock_push.assert_not_called()

    def test_push_failure_surfaces_git_stderr(self, git_repo):
        (git_repo / "articles" / "fail_zh.md").write_text("# Fail")

        with patch("yt_translate.publish._git_push") as mock_push:
            mock_push.return_value = subprocess.CompletedProcess(
                args=["git", "push"],
                returncode=1,
                stdout="",
                stderr="fatal: 'origin' does not appear to be a git repository\n",
            )
            result = publish(git_repo, "Fail Article")

        assert result.outcome == PublishOutcome.PUSH_FAILED
        assert not result.ok
        assert "origin" in result.detail
        assert "does not appear to be a git repository" in result.detail

    def test_commit_failure_surfaces_git_stderr(self, git_repo, monkeypatch):
        # Force `git commit` to fail by breaking committer identity so it
        # aborts with an actionable error message that must reach the user.
        (git_repo / "articles" / "fail_zh.md").write_text("# Fail")
        subprocess.run(["git", "config", "--unset", "user.email"], cwd=git_repo, capture_output=True)
        subprocess.run(["git", "config", "--unset", "user.name"], cwd=git_repo, capture_output=True)
        # Prevent git from picking up ambient identity from the environment
        monkeypatch.setenv("GIT_AUTHOR_NAME", "")
        monkeypatch.setenv("GIT_AUTHOR_EMAIL", "")
        monkeypatch.setenv("GIT_COMMITTER_NAME", "")
        monkeypatch.setenv("GIT_COMMITTER_EMAIL", "")
        monkeypatch.setenv("HOME", str(git_repo))  # ignore ~/.gitconfig

        with patch("yt_translate.publish._git_push") as mock_push:
            result = publish(git_repo, "Fail Article")

        assert result.outcome == PublishOutcome.COMMIT_FAILED
        assert not result.ok
        assert result.detail  # non-empty stderr from git
        mock_push.assert_not_called()
