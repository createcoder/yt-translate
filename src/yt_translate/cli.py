"""CLI entry point for yt-translate."""

from pathlib import Path

import click

from yt_translate.fetcher import fetch_transcript
from yt_translate.chunker import chunk_segments
from yt_translate.translator import translate_chunks
from yt_translate.formatter import format_markdown, generate_filename
from yt_translate.build_site import build_site
from yt_translate.publish import publish


@click.command()
@click.argument("youtube_url")
@click.option("--output", "-o", default=None, help="Output file path")
@click.option("--chunk-size", "-c", default=4, help="Sentences per paragraph (default: 4)")
@click.option(
    "--base-url",
    default="http://100.126.211.106:8000/v1",
    help="OpenAI-compatible API base URL",
)
@click.option(
    "--model",
    "-m",
    default="Qwen/Qwen3.6-35B-A3B-FP8",
    help="Model name for the API",
)
@click.option(
    "--no-publish",
    is_flag=True,
    default=False,
    help="Skip building the site and pushing to git",
)
def main(youtube_url: str, output: str | None, chunk_size: int, base_url: str, model: str, no_publish: bool) -> None:
    """Translate a YouTube video transcript to Chinese.

    YOUTUBE_URL: A YouTube video URL or video ID.
    """
    # Step 1: Fetch transcript
    click.echo("Fetching transcript...", err=True)
    title, segments = fetch_transcript(youtube_url)
    click.echo(f"Got transcript: \"{title}\" ({len(segments)} segments)", err=True)

    # Step 2: Chunk
    chunks = chunk_segments(segments, chunk_size=chunk_size)
    click.echo(f"Split into {len(chunks)} chunks for translation", err=True)

    # Step 3: Translate
    translated = translate_chunks(chunks, base_url=base_url, model=model)

    # Step 4: Format and save
    markdown = format_markdown(title, youtube_url, translated)

    if output:
        output_path = Path(output)
    else:
        repo_root = Path.cwd()
        articles_dir = repo_root / "articles"
        articles_dir.mkdir(exist_ok=True)
        output_path = articles_dir / generate_filename(title)

    output_path.write_text(markdown, encoding="utf-8")

    # Summary
    success_count = sum(1 for c in translated if c["success"])
    total_count = len(translated)

    if success_count == total_count:
        click.echo(f"Done! Saved to {output_path} ({success_count}/{total_count} chunks translated)", err=True)
    else:
        failed = total_count - success_count
        click.echo(
            f"Saved to {output_path} ({success_count}/{total_count} chunks translated, {failed} failed)",
            err=True,
        )

    # Step 5: Build site and publish
    repo_root = Path.cwd()
    articles_dir = repo_root / "articles"
    site_dir = repo_root / "site"

    click.echo("Building site...", err=True)
    count = build_site(articles_dir, site_dir)
    click.echo(f"Site built with {count} articles", err=True)

    if not no_publish:
        click.echo("Publishing...", err=True)
        if publish(repo_root, title):
            click.echo("Published successfully!", err=True)
        else:
            click.echo("Nothing to publish (no changes or push failed)", err=True)


if __name__ == "__main__":
    main()
