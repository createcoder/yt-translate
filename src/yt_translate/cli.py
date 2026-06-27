"""CLI entry point for yt-translate."""

from pathlib import Path

import click

from yt_translate.fetcher import fetch_transcript
from yt_translate.chunker import chunk_segments
from yt_translate.translator import translate_chunks
from yt_translate.formatter import format_markdown, generate_filename


@click.command()
@click.argument("youtube_url")
@click.option("--output", "-o", default=None, help="Output file path")
@click.option("--chunk-size", "-c", default=800, help="Words per translation chunk")
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
def main(youtube_url: str, output: str | None, chunk_size: int, base_url: str, model: str) -> None:
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
        output_path = Path(generate_filename(title))

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


if __name__ == "__main__":
    main()
