"""Git commit and push for auto-publishing.

Every git step's stderr is captured and returned so callers can show the
user the actual failure (auth error, no upstream, hook rejection, …)
instead of collapsing every outcome into a single boolean.
"""

import subprocess
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class PublishOutcome(Enum):
    PUBLISHED = "published"
    NO_CHANGES = "no_changes"
    COMMIT_FAILED = "commit_failed"
    PUSH_FAILED = "push_failed"


@dataclass
class PublishResult:
    outcome: PublishOutcome
    detail: str = ""  # git stderr (or stdout) from the failing step

    @property
    def ok(self) -> bool:
        return self.outcome == PublishOutcome.PUBLISHED


def _run_git(repo_dir: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=repo_dir,
        capture_output=True,
        text=True,
    )


def _git_push(repo_dir: Path) -> subprocess.CompletedProcess:
    return _run_git(repo_dir, "push")


def _detail(result: subprocess.CompletedProcess) -> str:
    return (result.stderr or result.stdout or "").strip()


def publish(repo_dir: Path, article_title: str) -> PublishResult:
    """Commit articles/ and site/ changes and push to origin.

    Returns a PublishResult; on failure, ``result.detail`` holds the
    stderr of the git step that failed.
    """
    _run_git(repo_dir, "add", "articles/", "site/")

    status = _run_git(repo_dir, "diff", "--cached", "--quiet")
    if status.returncode == 0:
        return PublishResult(PublishOutcome.NO_CHANGES)

    commit = _run_git(repo_dir, "commit", "-m", f"Add: {article_title}")
    if commit.returncode != 0:
        return PublishResult(PublishOutcome.COMMIT_FAILED, detail=_detail(commit))

    push = _git_push(repo_dir)
    if push.returncode != 0:
        return PublishResult(PublishOutcome.PUSH_FAILED, detail=_detail(push))

    return PublishResult(PublishOutcome.PUBLISHED)
