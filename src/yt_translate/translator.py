"""Translate text chunks using an OpenAI-compatible API."""

import time

import click
from openai import OpenAI

SYSTEM_PROMPT = (
    "You are a professional translator. Translate the following English transcript "
    "to Simplified Chinese. Preserve the original meaning and produce natural, fluent "
    "Chinese. Do not add explanations, commentary, or annotations. Output only the "
    "translation."
)

MAX_RETRIES = 3
RETRY_DELAYS = [1, 2, 4]  # seconds
TEMPERATURE = 0.3
MAX_TOKENS = 4096
TIMEOUT = 30


def translate_single_chunk(
    text: str,
    base_url: str,
    model: str,
) -> str | None:
    """Translate a single text chunk to Chinese.

    Args:
        text: English text to translate.
        base_url: OpenAI-compatible API base URL.
        model: Model name to use.

    Returns:
        Translated Chinese text, or None if all retries failed.
    """
    client = OpenAI(base_url=base_url, api_key="not-needed")

    for attempt in range(MAX_RETRIES):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": text},
                ],
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
                timeout=TIMEOUT,
            )
            content = response.choices[0].message.content
            if content:
                return content.strip()
            return None
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAYS[attempt])
            else:
                click.echo(
                    f"  Warning: Translation failed after {MAX_RETRIES} attempts: {e}",
                    err=True,
                )
                return None

    return None


def translate_chunks(
    chunks: list[dict],
    base_url: str,
    model: str,
) -> list[dict]:
    """Translate all chunks sequentially.

    Args:
        chunks: List of dicts with keys "start" and "text".
        base_url: OpenAI-compatible API base URL.
        model: Model name to use.

    Returns:
        List of dicts with keys "start", "text" (translated), and "success" (bool).
    """
    results: list[dict] = []
    total = len(chunks)

    for i, chunk in enumerate(chunks, 1):
        click.echo(f"Translating chunk {i}/{total}...", err=True)

        translated = translate_single_chunk(chunk["text"], base_url, model)

        if translated:
            results.append({"start": chunk["start"], "text": translated, "success": True})
        else:
            results.append(
                {"start": chunk["start"], "text": "[TRANSLATION FAILED]", "success": False}
            )

    return results
