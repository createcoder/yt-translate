"""Git commit and push for auto-publishing."""

import subprocess
from pathlib import Path


def _git_push(repo_dir: Path) -> bool:
    """Push to origin. Returns True on success."""
    result = subprocess.run(
        ["git", "push"],
        cwd=repo_dir,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def publish(repo_dir: Path, article_title: str) -> bool:
    """Commit site/ and articles/ changes and push.

    Args:
        repo_dir: Root of the git repository.
        article_title: Title for the commit message.

    Returns:
        True if changes were committed and pushed successfully.
        False if there were no changes or push failed.
    """
    # Stage articles/ and site/
    subprocess.run(
        ["git", "add", "articles/", "site/"],
        cwd=repo_dir,
        capture_output=True,
    )

    # Check if there's anything to commit
    status = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=repo_dir,
        capture_output=True,
    )
    if status.returncode == 0:
        return False

    # Commit
    subprocess.run(
        ["git", "commit", "-m", f"Add: {article_title}"],
        cwd=repo_dir,
        capture_output=True,
    )

    # Push
    return _git_push(repo_dir)
