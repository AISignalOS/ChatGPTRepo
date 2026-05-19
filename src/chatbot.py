"""
Claude-powered terminal chatbot — demo app for the AI Demo Agent tutorial.
Requires: pip install anthropic
Run:      ANTHROPIC_API_KEY=sk-... python src/chatbot.py
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

    print(f"\n{'='*50}")
    print("  Claude AI Chatbot  (type 'quit' to exit)")
    print(f"{'='*50}\n")

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

        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=history,
        )

        reply = response.content[0].text
        history.append({"role": "assistant", "content": reply})

        print(f"\nClaude: {reply}\n")


if __name__ == "__main__":
    if "ANTHROPIC_API_KEY" not in os.environ:
        print("Error: set ANTHROPIC_API_KEY before running.", file=sys.stderr)
        sys.exit(1)
    chat()
