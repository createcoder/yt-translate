"""CLI for producing durable technical briefs from a YouTube playlist."""

from datetime import datetime, timezone
from pathlib import Path

import click
from slugify import slugify

from yt_translate.fetcher import fetch_playlist, fetch_transcript
from yt_translate.summarizer import summarize_transcript, transcript_text
from yt_translate.build_site import build_site as build_static_site


@click.command()
@click.argument("playlist")
@click.option("--output-dir", default="playlist-summaries", show_default=True, type=click.Path(path_type=Path))
@click.option("--base-url", default="http://100.126.211.106:8000/v1", show_default=True)
@click.option("--model", "-m", default="Qwen/Qwen3.6-35B-A3B-FP8", show_default=True)
@click.option("--limit", type=click.IntRange(min=1), default=None, help="Process only the first N videos.")
@click.option("--build-site/--no-build-site", default=True, show_default=True, help="Rebuild the local static site when finished.")
def main(playlist: str, output_dir: Path, base_url: str, model: str, limit: int | None, build_site: bool) -> None:
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
    index = [f"# Playlist technical summaries\n\n**Playlist:** {playlist}\n", "## Videos\n"]
    successes = 0
    for number, video in enumerate(videos, 1):
        click.echo(f"[{number}/{len(videos)}] {video['title']}", err=True)
        filename = f"{number:03d}-{slugify(video['title'], max_length=70) or video['id']}.md"
        output_file = destination / filename
        try:
            title, segments = fetch_transcript(video["url"], prefer_ytdlp=True)
            transcript = transcript_text(segments)
            # Preserve the source immediately. This is particularly important
            # when a downstream model service is slow or unavailable.
            output_file.write_text(
                _document(title, video["url"], "Transcript captured — summary in progress", "Summary is being generated.", transcript),
                encoding="utf-8",
            )
            if build_site:
                repo_root = Path.cwd()
                build_static_site(repo_root / "articles", repo_root / "site")
            summary = summarize_transcript(transcript, base_url, model)
            status = "Completed"
            successes += 1
        except Exception as error:
            title = video["title"]
            transcript = "Transcript was not retrieved."
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
    click.echo(f"Saved {successes}/{len(videos)} completed video briefs to {destination}", err=True)


def _playlist_id(value: str) -> str:
    if "list=" in value:
        return value.split("list=", 1)[1].split("&", 1)[0]
    return value


def _document(title: str, url: str, status: str, summary: str, transcript: str) -> str:
    created = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return f"# {title}\n\n- **Video:** {url}\n- **Generated:** {created}\n- **Status:** {status}\n\n## Technical brief\n\n{summary}\n\n## Full transcript\n\n{transcript}\n"


if __name__ == "__main__":
    main()
