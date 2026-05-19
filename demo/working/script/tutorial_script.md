# Tutorial Script — Build a ChatGPT-Style AI Chatbot with Claude API

**Format:** Screen-recorded coding tutorial  
**Target length:** 8–12 minutes (short-form cut: 60 s)  
**Audience:** Developers who want to build AI apps without stitching together OpenAI wrappers  
**Deliverable:** Working Python chatbot + streaming upgrade + prompt-caching bonus

---

## SECTION 0 — Hook (0:00–0:20)

**[SCREEN: Terminal window, chatbot already running, user types a question, Claude answers in real time]**

> "In the next ten minutes you're going to build your own AI chatbot — from zero lines of code to a fully streaming, multi-turn conversation — using the Claude API. No boilerplate, no wrapper hell. Let's go."

---

## SECTION 1 — Setup (0:20–1:30)

**[SCREEN: Empty project folder in VS Code / terminal]**

> "First, grab your Anthropic API key from console.anthropic.com. It's free to start. Then install the SDK:"

```bash
pip install anthropic
```

> "That's the only dependency. One package. Create a file called chatbot.py."

**[SCREEN: New file opens — src/chatbot.py]**

---

## SECTION 2 — Core Chatbot (1:30–4:00)

**[SCREEN: Live-type or fast-cut paste the code with syntax highlighting]**

> "Import Anthropic, instantiate the client, and drop in your API key from the environment — never hardcode it."

```python
from anthropic import Anthropic
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
```

> "Now the key insight: Claude's API is *stateless*. You pass the entire conversation history on every call. That's actually a superpower — you control memory completely."

```python
history = []
history.append({"role": "user", "content": user_input})

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system=SYSTEM_PROMPT,
    messages=history,
)

reply = response.content[0].text
history.append({"role": "assistant", "content": reply})
```

> "Fourteen lines and you have a working multi-turn AI chatbot. Let's run it."

**[SCREEN: Terminal — python src/chatbot.py — live demo Q&A]**

---

## SECTION 3 — Streaming Upgrade (4:00–7:00)

**[SCREEN: Duplicate file → chatbot_streaming.py]**

> "The basic version waits for the full response. Streaming makes it feel *alive* — tokens appear as Claude generates them, exactly like ChatGPT."

> "Swap `client.messages.create` for `client.messages.stream`:"

```python
with client.messages.stream(
    model=MODEL,
    max_tokens=1024,
    system=SYSTEM_PROMPT,
    messages=history,
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

> "Three lines changed. Now watch."

**[SCREEN: Terminal — streaming chatbot running, text appears token-by-token]**

---

## SECTION 4 — Prompt Caching Bonus (7:00–9:30)

**[SCREEN: System prompt section, add cache_control]**

> "Here's the pro move: prompt caching. If you have a long system prompt — say, a 10,000-token knowledge base — Claude charges you full price the first call, then *90% off* every call after that, for up to 5 minutes."

```python
system=[
    {
        "type": "text",
        "text": SYSTEM_PROMPT,
        "cache_control": {"type": "ephemeral"},
    }
]
```

> "One dict field. Massive cost savings at scale. This is available on Claude Sonnet and Haiku."

---

## SECTION 5 — Recap & CTA (9:30–10:30)

**[SCREEN: Split — terminal chatbot + code side by side]**

> "So what did we build? A fully working terminal chatbot, streaming output, with prompt caching — in under 50 lines of Python."

> "The full code is linked in the description. Next video: we wrap this in a FastAPI web server and add a React frontend. Subscribe so you don't miss it."

**[SCREEN: Outro card with GitHub link and subscribe button]**

---

## B-Roll Notes

| Timestamp | B-Roll                                    |
|-----------|-------------------------------------------|
| 0:00      | Terminal chatbot answering in real time   |
| 1:00      | console.anthropic.com API key page        |
| 2:30      | Code editor with syntax highlighting      |
| 4:30      | Side-by-side: non-streaming vs streaming  |
| 7:30      | Token cost calculator / pricing page      |
| 9:30      | GitHub repo page with star count          |
