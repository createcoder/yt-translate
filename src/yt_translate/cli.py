"""CLI entry point for yt-translate."""

import click


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
    click.echo("yt-translate: not yet implemented", err=True)
    raise SystemExit(1)


if __name__ == "__main__":
    main()
