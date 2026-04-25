"""
Multi-provider AI service for generating Signal Summaries.

Supported providers (set via MODEL_PROVIDER env var):
  anthropic   — Claude via Anthropic SDK (default); uses prompt caching
  ollama      — Any local model via Ollama's OpenAI-compatible API
  openrouter  — Any model via OpenRouter's OpenAI-compatible API

Model is selected via MODEL_NAME env var; each provider has a sensible default.
"""

import json
import os

from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """You are a research analyst specializing in AI productivity tools.
Your job is to analyze raw webpage content and extract structured intelligence about AI tools.

Always respond with a valid JSON object containing exactly these fields:
- signal_summary: string (2-3 sentences summarizing what the tool does and who it's for)
- use_cases: array of strings (3-5 specific use case tags chosen from or similar to: content-writing, code-generation, image-generation, data-analysis, customer-support, productivity, research, audio-generation, video-generation, automation, writing-assistance, design, marketing, sales, education)
- price_tier: one of "free" | "freemium" | "paid" | "enterprise"
- target_audience: string (short description of primary users, e.g. "developers", "marketers", "content creators")

Be concise and factual. Do not invent features not present in the content.
If pricing information is unclear, default to "freemium".
Respond with raw JSON only — no markdown fences, no explanation."""


def _strip_json(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        parts = text.split("```")
        text = parts[1]
        if text.startswith("json"):
            text = text[4:]
    return text.strip()


def _generate_anthropic(raw_content: str, tool_name: str, tool_url: str) -> dict:
    import anthropic

    model = os.getenv("MODEL_NAME", "claude-sonnet-4-6")
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    response = client.messages.create(
        model=model,
        max_tokens=1024,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[
            {
                "role": "user",
                "content": (
                    f"Tool Name: {tool_name}\n"
                    f"URL: {tool_url}\n\n"
                    f"Raw page content:\n{raw_content[:8000]}"
                ),
            }
        ],
    )
    return json.loads(_strip_json(response.content[0].text))


def _generate_openai_compat(
    raw_content: str,
    tool_name: str,
    tool_url: str,
    base_url: str,
    api_key: str,
    model: str,
) -> dict:
    from openai import OpenAI

    client = OpenAI(base_url=base_url, api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        max_tokens=1024,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Tool Name: {tool_name}\n"
                    f"URL: {tool_url}\n\n"
                    f"Raw page content:\n{raw_content[:8000]}"
                ),
            },
        ],
    )
    return json.loads(_strip_json(response.choices[0].message.content))


def generate_signal_summary(raw_content: str, tool_name: str, tool_url: str) -> dict:
    provider = os.getenv("MODEL_PROVIDER", "anthropic").lower()

    if provider == "anthropic":
        return _generate_anthropic(raw_content, tool_name, tool_url)

    if provider == "ollama":
        model = os.getenv("MODEL_NAME", "llama3.2")
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/") + "/v1"
        return _generate_openai_compat(
            raw_content, tool_name, tool_url,
            base_url=base_url,
            api_key="ollama",
            model=model,
        )

    if provider == "openrouter":
        model = os.getenv("MODEL_NAME", "mistralai/mistral-7b-instruct")
        return _generate_openai_compat(
            raw_content, tool_name, tool_url,
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["OPENROUTER_API_KEY"],
            model=model,
        )

    raise ValueError(
        f"Unknown MODEL_PROVIDER: {provider!r}. "
        "Valid options: 'anthropic', 'ollama', 'openrouter'."
    )
