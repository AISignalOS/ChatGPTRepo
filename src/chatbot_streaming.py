"""
Claude-powered streaming chatbot — advanced version with prompt caching.
Requires: pip install anthropic
Run:      ANTHROPIC_API_KEY=sk-... python src/chatbot_streaming.py
"""

import os
import sys
from anthropic import Anthropic

MODEL = "claude-sonnet-4-6"
SYSTEM_PROMPT = (
    "You are a helpful, concise AI assistant. "
    "Answer clearly and accurately. "
    "If you don't know something, say so."
)


def chat():
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    history = []

    print(f"\n{'='*54}")
    print("  Claude AI Chatbot — Streaming  (type 'quit' to exit)")
    print(f"{'='*54}\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in {"quit", "exit", "bye"}:
            print("Goodbye!")
            break

        history.append({"role": "user", "content": user_input})

        print("Claude: ", end="", flush=True)
        reply_parts = []

        with client.messages.stream(
            model=MODEL,
            max_tokens=1024,
            system=[
                {
                    "type": "text",
                    "text": SYSTEM_PROMPT,
                    # Cache the system prompt — saves tokens on long sessions
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=history,
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
                reply_parts.append(text)

        print("\n")
        history.append({"role": "assistant", "content": "".join(reply_parts)})


if __name__ == "__main__":
    if "ANTHROPIC_API_KEY" not in os.environ:
        print("Error: set ANTHROPIC_API_KEY before running.", file=sys.stderr)
        sys.exit(1)
    chat()
