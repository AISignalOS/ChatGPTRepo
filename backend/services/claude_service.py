import json
import os
import anthropic
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


def generate_signal_summary(raw_content: str, tool_name: str, tool_url: str) -> dict:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    response = client.messages.create(
        model="claude-sonnet-4-6",
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

    text = response.content[0].text.strip()

    # Strip markdown fences if present
    if text.startswith("```"):
        parts = text.split("```")
        text = parts[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()

    return json.loads(text)
