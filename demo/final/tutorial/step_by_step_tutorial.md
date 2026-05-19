# Step-by-Step Tutorial — Build a Claude AI Chatbot with Python

**Difficulty:** Beginner-friendly  
**Time:** 15 minutes  
**Prerequisites:** Python 3.10+, pip, Anthropic API key (free tier available)

---

## What You'll Build

A terminal chatbot powered by Claude that:
- Remembers conversation history (multi-turn)
- Streams responses token-by-token
- Uses prompt caching to cut costs by up to 90%

---

## Step 1 — Get Your API Key

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up for a free account
3. Navigate to **API Keys** → **Create Key**
4. Copy the key — it starts with `sk-ant-`

**Never commit your API key to git.** Always load it from an environment variable.

---

## Step 2 — Install the SDK

```bash
pip install anthropic
```

That's your only dependency.

---

## Step 3 — Build the Basic Chatbot

Create `src/chatbot.py`:

```python
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
        user_input = input("You: ").strip()
        if user_input.lower() in {"quit", "exit"}:
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
        print("Error: set ANTHROPIC_API_KEY", file=sys.stderr)
        sys.exit(1)
    chat()
```

**Run it:**
```bash
export ANTHROPIC_API_KEY=sk-ant-your-key-here
python src/chatbot.py
```

### Why pass history every time?

Claude's API is stateless — each request is independent. By appending both user and assistant messages to `history` and sending the list every call, you recreate multi-turn memory. You control exactly what the model "remembers."

---

## Step 4 — Add Streaming

Streaming makes responses appear token-by-token instead of all at once. It feels more natural and responsive.

Replace the `client.messages.create(...)` block with:

```python
print("Claude: ", end="", flush=True)
reply_parts = []

with client.messages.stream(
    model=MODEL,
    max_tokens=1024,
    system=SYSTEM_PROMPT,
    messages=history,
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
        reply_parts.append(text)

print("\n")
history.append({"role": "assistant", "content": "".join(reply_parts)})
```

See `src/chatbot_streaming.py` for the full version.

---

## Step 5 — Add Prompt Caching (Cost Optimization)

If your system prompt is long — a persona, knowledge base, or set of rules — prompt caching saves you up to 90% on input tokens after the first call.

Change the `system` parameter from a string to a list:

```python
system=[
    {
        "type": "text",
        "text": SYSTEM_PROMPT,
        "cache_control": {"type": "ephemeral"},
    }
]
```

**How it works:**
- First call: full token cost (prompt is cached on Anthropic's side)
- Subsequent calls within 5 minutes: cached section costs ~10% of normal
- Available on: `claude-sonnet-4-6`, `claude-haiku-4-5`

---

## Step 6 — Test It

```
==================================================
  Claude AI Chatbot  (type 'quit' to exit)
==================================================

You: What is Python?
Claude: Python is a high-level, interpreted programming language...

You: What was my first question?
Claude: Your first question was "What is Python?"

You: quit
Goodbye!
```

Multi-turn memory works. Streaming works. Caching works.

---

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `AuthenticationError` | Bad or missing API key | Check `ANTHROPIC_API_KEY` env var |
| `RateLimitError` | Too many requests | Add `time.sleep(1)` between calls |
| `overloaded_error` | API overloaded | Retry with exponential backoff |
| `ModuleNotFoundError: anthropic` | SDK not installed | `pip install anthropic` |

---

## Next Steps

- [ ] Wrap in a **FastAPI** web server (next tutorial)
- [ ] Add a **React frontend** for a real chat UI
- [ ] Persist conversation history to **SQLite** or **Redis**
- [ ] Add **tool use** so Claude can call external APIs
- [ ] Deploy to **Railway**, **Fly.io**, or **AWS Lambda**

---

## Full Source Code

- `src/chatbot.py` — basic version
- `src/chatbot_streaming.py` — streaming + caching version
- `src/requirements.txt` — dependencies
