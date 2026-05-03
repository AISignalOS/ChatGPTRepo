"""
Multi-provider AI service for generating Signal Summaries.

Set MODEL_PROVIDER to one of the supported providers below.
Set MODEL_NAME to override the default model for any provider.

Supported providers
───────────────────
Frontier / cloud (OpenAI-compatible API):
  openai      — GPT-4o, o1, o3, etc.
  google      — Gemini 2.0 Flash, Pro, Ultra, etc.
  xai         — Grok 3, Grok 2, etc.
  mistral     — Mistral Large, Codestral, etc.
  groq        — Llama 3.3, Mixtral, Gemma, etc. (fast inference)
  deepseek    — DeepSeek V3, R1, etc.
  together    — 200+ open models via Together AI
  perplexity  — Sonar, Sonar Pro, etc.
  cohere      — Command R+, Command R, etc.

Aggregators (access many models with one key):
  openrouter  — Any model on OpenRouter (300+ models)

Local / self-hosted:
  ollama      — Any model running locally via Ollama

Anthropic (special — uses prompt caching):
  anthropic   — Claude (default)

Escape hatch for any other OpenAI-compatible endpoint:
  custom      — Set CUSTOM_BASE_URL + CUSTOM_API_KEY + MODEL_NAME
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

# Registry of all OpenAI-compatible providers.
# Keys:
#   base_url        — static endpoint URL
#   base_url_env    — env var holding the endpoint (dynamic/self-hosted providers)
#   default_base_url— fallback when base_url_env is unset
#   append_v1       — append "/v1" to the resolved base URL (e.g. Ollama)
#   api_key_env     — env var holding the API key
#   api_key         — static API key (for providers that don't require one)
#   default_model   — used when MODEL_NAME env var is not set
_REGISTRY: dict[str, dict] = {
    "openai": {
        "base_url":     "https://api.openai.com/v1",
        "api_key_env":  "OPENAI_API_KEY",
        "default_model": "gpt-4o",
    },
    "google": {
        # Gemini via its OpenAI-compatible endpoint
        "base_url":     "https://generativelanguage.googleapis.com/v1beta/openai/",
        "api_key_env":  "GOOGLE_API_KEY",
        "default_model": "gemini-2.0-flash",
    },
    "xai": {
        # Grok models
        "base_url":     "https://api.x.ai/v1",
        "api_key_env":  "XAI_API_KEY",
        "default_model": "grok-3",
    },
    "mistral": {
        "base_url":     "https://api.mistral.ai/v1",
        "api_key_env":  "MISTRAL_API_KEY",
        "default_model": "mistral-large-latest",
    },
    "groq": {
        "base_url":     "https://api.groq.com/openai/v1",
        "api_key_env":  "GROQ_API_KEY",
        "default_model": "llama-3.3-70b-versatile",
    },
    "deepseek": {
        "base_url":     "https://api.deepseek.com/v1",
        "api_key_env":  "DEEPSEEK_API_KEY",
        "default_model": "deepseek-chat",
    },
    "together": {
        "base_url":     "https://api.together.xyz/v1",
        "api_key_env":  "TOGETHER_API_KEY",
        "default_model": "meta-llama/Llama-3.3-70b-instruct-turbo",
    },
    "perplexity": {
        "base_url":     "https://api.perplexity.ai",
        "api_key_env":  "PERPLEXITY_API_KEY",
        "default_model": "sonar-pro",
    },
    "cohere": {
        "base_url":     "https://api.cohere.com/compatibility/v1",
        "api_key_env":  "COHERE_API_KEY",
        "default_model": "command-r-plus",
    },
    "openrouter": {
        "base_url":     "https://openrouter.ai/api/v1",
        "api_key_env":  "OPENROUTER_API_KEY",
        "default_model": "mistralai/mistral-7b-instruct",
    },
    "ollama": {
        "base_url_env":     "OLLAMA_BASE_URL",
        "default_base_url": "http://localhost:11434",
        "append_v1":        True,
        "api_key":          "ollama",
        "default_model":    "llama3.2",
    },
    "custom": {
        "base_url_env":  "CUSTOM_BASE_URL",
        "api_key_env":   "CUSTOM_API_KEY",
        "default_model": "",
    },
}

_ALL_PROVIDERS = sorted(["anthropic"] + list(_REGISTRY))


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


def _resolve_config(provider: str) -> tuple[str, str, str]:
    """Return (base_url, api_key, model) for a registry provider."""
    cfg = _REGISTRY[provider]

    # base_url
    if "base_url_env" in cfg:
        raw = os.getenv(cfg["base_url_env"], cfg.get("default_base_url", ""))
        if not raw:
            raise ValueError(
                f"MODEL_PROVIDER={provider!r} requires {cfg['base_url_env']} to be set."
            )
        base_url = raw.rstrip("/")
        if cfg.get("append_v1") and not base_url.endswith("/v1"):
            base_url += "/v1"
    else:
        base_url = cfg["base_url"]

    # api_key
    if "api_key" in cfg:
        api_key = cfg["api_key"]
    else:
        key_env = cfg["api_key_env"]
        api_key = os.environ.get(key_env, "")
        if not api_key:
            raise ValueError(
                f"MODEL_PROVIDER={provider!r} requires {key_env} to be set."
            )

    # model
    default_model = cfg["default_model"]
    model = os.getenv("MODEL_NAME", default_model)
    if not model:
        raise ValueError(
            f"MODEL_PROVIDER={provider!r} requires MODEL_NAME to be set."
        )

    return base_url, api_key, model


def generate_signal_summary(raw_content: str, tool_name: str, tool_url: str) -> dict:
    provider = os.getenv("MODEL_PROVIDER", "anthropic").lower()

    if provider == "anthropic":
        return _generate_anthropic(raw_content, tool_name, tool_url)

    if provider not in _REGISTRY:
        raise ValueError(
            f"Unknown MODEL_PROVIDER: {provider!r}. "
            f"Valid options: {_ALL_PROVIDERS}"
        )

    base_url, api_key, model = _resolve_config(provider)
    return _generate_openai_compat(
        raw_content, tool_name, tool_url, base_url, api_key, model
    )
