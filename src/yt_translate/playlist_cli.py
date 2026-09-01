"""CLI for producing durable technical briefs from a YouTube playlist."""

from datetime import datetime, timezone
import os
from pathlib import Path
import re

import click
from slugify import slugify

from yt_translate.fetcher import fetch_playlist, fetch_transcript
from yt_translate.summarizer import summarize_transcript, transcript_text
from yt_translate.build_site import build_site as build_static_site


def _load_dotenv(path: Path | None = None) -> None:
    """Load a project-local .env without overriding explicitly set variables."""
    env_path = path or Path.cwd() / ".env"
    if not env_path.is_file():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.removeprefix("export ").strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


_load_dotenv()


@click.command()
@click.argument("playlist")
@click.option("--output-dir", default="playlist-summaries", show_default=True, type=click.Path(path_type=Path))
@click.option("--base-url", default=lambda: os.getenv("LITELLM_BASE_URL", "http://192.168.150.100:4004/v1"), show_default=True)
@click.option("--model", "-m", default=lambda: os.getenv("LITELLM_MODEL", "gpt-5.6-terra"), show_default=True)
@click.option("--api-key", envvar="LITELLM_API_KEY", default=None, help="LiteLLM API key (or set LITELLM_API_KEY).")
@click.option("--limit", type=click.IntRange(min=1), default=None, help="Process only the first N videos.")
@click.option("--build-site/--no-build-site", default=True, show_default=True, help="Rebuild the local static site when finished.")
def main(playlist: str, output_dir: Path, base_url: str, model: str, api_key: str | None, limit: int | None, build_site: bool) -> None:
    """Save transcripts and technical summaries for every video in PLAYLIST."""
    try:
        videos = fetch_playlist(playlist)
    except Exception as error:
        raise click.ClickException(f"Could not load playlist: {error}") from error
    if limit:
        videos = videos[:limit]
    playlist_id = _playlist_id(playlist)
    destination = output_dir / playlist_id
    destination.mkdir(parents=True, exist_ok=True)
    completed = _completed_videos(destination)
    index = [f"# Playlist technical summaries\n\n**Playlist:** {playlist}\n", "## Videos\n"]
    successes = 0
    skipped = 0
    for number, video in enumerate(videos, 1):
        filename = f"{number:03d}-{slugify(video['title'], max_length=70) or video['id']}.md"
        output_file = destination / filename
        if video["id"] in completed:
            existing = completed[video["id"]]
            click.echo(f"[{number}/{len(videos)}] Skipping completed video: {video['title']}", err=True)
            index.append(f"- [{number:03d}. {video['title']}]({existing.name}) — Skipped (already completed)")
            skipped += 1
            continue
        if not api_key:
            raise click.ClickException("Set LITELLM_API_KEY or pass --api-key to generate summaries.")
        click.echo(f"[{number}/{len(videos)}] {video['title']}", err=True)
        try:
            title, segments = fetch_transcript(video["url"], prefer_ytdlp=True)
            transcript = transcript_text(segments)
        except Exception as error:
            title = video["title"]
            transcript = "Transcript was not retrieved."
            summary = f"Summary was not produced. Error: `{error}`"
            status = "Failed"
            click.echo(f"  Warning: {error}", err=True)
        else:
            # Preserve the source immediately. This is particularly important
            # when a downstream model service is slow or unavailable.
            output_file.write_text(
                _document(title, video["url"], "Transcript captured — summary in progress", "Summary is being generated.", transcript),
                encoding="utf-8",
            )
            if build_site:
                repo_root = Path.cwd()
                build_static_site(repo_root / "articles", repo_root / "site")
            try:
                summary = summarize_transcript(transcript, base_url, model, api_key)
                status = "Completed"
                successes += 1
            except Exception as error:
                summary = f"Summary was not produced. Error: `{error}`"
                status = "Failed"
                click.echo(f"  Warning: {error}", err=True)
        output_file.write_text(_document(title, video["url"], status, summary, transcript), encoding="utf-8")
        index.append(f"- [{number:03d}. {title}]({filename}) — {status}")
    (destination / "README.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    if build_site:
        repo_root = Path.cwd()
        count = build_static_site(repo_root / "articles", repo_root / "site")
        click.echo(f"Rebuilt site with {count} readable items", err=True)
    click.echo(
        f"Saved {successes} new briefs; skipped {skipped} completed videos; "
        f"processed {len(videos)} playlist videos in {destination}",
        err=True,
    )


def _completed_videos(destination: Path) -> dict[str, Path]:
    """Return successfully summarized videos already saved for this playlist."""
    completed: dict[str, Path] = {}
    for path in destination.glob("*.md"):
        if path.name == "README.md":
            continue
        text = path.read_text(encoding="utf-8")
        if "- **Status:** Completed" not in text:
            continue
        source = next((line for line in text.splitlines() if line.startswith("- **Video:** ")), "")
        match = re.search(r"[?&]v=([A-Za-z0-9_-]{11})", source)
        if match:
            completed[match.group(1)] = path
    return completed


def _playlist_id(value: str) -> str:
    if "list=" in value:
        return value.split("list=", 1)[1].split("&", 1)[0]
    return value


def _document(title: str, url: str, status: str, summary: str, transcript: str) -> str:
    created = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return f"# {title}\n\n- **Video:** {url}\n- **Generated:** {created}\n- **Status:** {status}\n\n## Technical brief\n\n{summary}\n\n## Full transcript\n\n{transcript}\n"


if __name__ == "__main__":
    main()
