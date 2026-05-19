# ChatGPTRepo — Claude API Demo & Tutorial Production Kit

Build a streaming AI chatbot with the Claude API in 50 lines of Python. This repo contains the working source code plus a complete production package: tutorial, voiceover copy, visual prompts, publishing assets, and a sellable kit template.

## Quick Start

```bash
pip install -r src/requirements.txt
export ANTHROPIC_API_KEY=sk-ant-your-key-here

# Basic chatbot
python src/chatbot.py

# Streaming + prompt caching
python src/chatbot_streaming.py
```

## Repo Structure

```
src/
  chatbot.py               # Basic multi-turn chatbot
  chatbot_streaming.py     # Streaming + prompt caching version
  requirements.txt

demo/
  raw/
    logs/execution_log.md  # Execution log and simulation notes
  working/
    script/                # Full tutorial script (10-min video)
    voiceover/             # Long-form + 60-second voiceover copy
    visuals/               # Image/video generation prompts
  final/
    tutorial/              # Step-by-step written tutorial
    publishing/            # Titles, descriptions, captions, tags
    sellable/              # Sellable asset package breakdown
    performance_log.md     # Repeatable performance tracking template
```

## Get Your API Key

[console.anthropic.com](https://console.anthropic.com) — free tier available.

## License

Code: MIT. Tutorial text: CC BY 4.0.
