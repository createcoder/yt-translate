"""Technical, work-focused transcript summarization."""

import re
from openai import OpenAI

SUMMARY_PROMPT = """You summarize YouTube material for a Technical Product Owner at Superior Propane.
Their remit includes AI infrastructure, Databricks, Azure cloud, and Azure AI Foundry.
Write a detailed but efficient technical brief. Capture specific architectures, products,
implementation steps, limitations, security/governance, costs, operational trade-offs,
and concrete implications for that role. Distinguish speaker claims from established facts.
Do not invent details and say when a topic is not relevant. Use clear Markdown headings and bullets.
For a full transcript, organize it as: Executive takeaway; Technical details; Potential
applications for Superior Propane; Risks and validation questions; Action items."""


def transcript_text(segments: list[dict]) -> str:
    """Turn timed caption segments into readable transcript text."""
    return "\n".join(
        f"[{int(item.get('start', 0)) // 60:02d}:{int(item.get('start', 0)) % 60:02d}] {item.get('text', '').strip()}"
        for item in segments if item.get("text", "").strip()
    )


def summarize_transcript(text: str, base_url: str, model: str) -> str:
    """Produce a map/reduce summary so lengthy videos retain technical details."""
    # The CLI records a durable transcript before this call. Avoid SDK retries
    # that would otherwise keep an unavailable model request alive for minutes.
    client = OpenAI(base_url=base_url, api_key="not-needed", max_retries=0)
    chunks = _split_text(text, 18000)
    partials = [_complete(client, f"Transcript section {i}/{len(chunks)}:\n{chunk}", model)
                for i, chunk in enumerate(chunks, 1)]
    if len(partials) == 1:
        return partials[0]
    combined = "\n\n".join(f"## Section {i}\n{item}" for i, item in enumerate(partials, 1))
    return _complete(
        client,
        "Consolidate these section summaries into one non-redundant technical brief. "
        "Preserve useful specifics and include: Executive takeaway, Technical details, "
        "Potential applications for Superior Propane, Risks/validation questions, and Action items.\n\n" + combined,
        model,
    )


def _complete(client: OpenAI, content: str, model: str) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": SUMMARY_PROMPT}, {"role": "user", "content": content}],
        temperature=0.2,
        max_tokens=4000,
        timeout=120,
    )
    answer = response.choices[0].message.content or ""
    answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL).strip()
    if not answer:
        raise RuntimeError("model returned an empty summary")
    return answer


def _split_text(text: str, limit: int) -> list[str]:
    lines = text.splitlines()
    chunks: list[str] = []
    current: list[str] = []
    length = 0
    for line in lines:
        if current and length + len(line) + 1 > limit:
            chunks.append("\n".join(current))
            current, length = [], 0
        current.append(line)
        length += len(line) + 1
    if current:
        chunks.append("\n".join(current))
    return chunks or [""]
