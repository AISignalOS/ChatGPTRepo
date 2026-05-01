# Voiceover Copy — Claude AI Chatbot Tutorial

**Tone:** Direct, confident, slightly fast-paced. No filler words. Developer-to-developer.  
**Delivery notes:** Pause 0.5 s after code blocks. Emphasize numbers (14 lines, 90% off, 5 minutes).

---

## Long-Form Voiceover (8–10 min video)

### Hook
"What if you could build your own AI chatbot — with streaming, multi-turn memory, and cost optimization — in under 50 lines of Python? That's exactly what we're doing today using the Claude API."

### Setup
"Start by grabbing a free API key from Anthropic. Then: `pip install anthropic`. That's your entire dependency list. One package."

"Create `chatbot.py`. Import Anthropic, instantiate the client, and always load your API key from an environment variable — never paste it into code."

### Core chatbot explanation
"Here's the most important thing to understand about Claude's API: it's stateless. Every request is independent. You send the full conversation history each time. This feels weird at first, but it means you control memory completely — no hidden state, no session magic."

"We build a simple loop. User types. We append their message to history. We call `client.messages.create`. We print the reply. We append it to history. Fourteen lines. Done."

"Let me show you this running."

### Demo narration
"I'll ask it something real. [pause] And there's the answer. Now I'll ask a follow-up that references the first answer. [pause] See — it remembers the context because we're passing history. This is a proper multi-turn conversation."

### Streaming upgrade
"The one complaint about the basic version: you wait for the full response before seeing anything. Fix: use `client.messages.stream` instead of `create`. It returns a context manager. You iterate over `stream.text_stream`. Tokens come in real time — same as ChatGPT."

"Watch how different this feels."

### Prompt caching explanation
"Now the bonus feature that most people miss: prompt caching. If your system prompt is long — a knowledge base, a persona, instructions — Claude charges you full input price on the first call. But add one field — `cache_control: ephemeral` — and every call in the next five minutes costs 90% less for that cached section."

"At scale, with thousands of daily conversations, this pays for itself in hours. Add it now, thank yourself later."

### Outro
"Fifty lines. Streaming. Caching. Multi-turn memory. The full source code is linked in the description — fork it, star it, make it yours."

"Next: we wrap this in a FastAPI server and build a React chat UI on top. Subscribe and hit the bell so you catch that one."

---

## Short-Form Voiceover (60-second cut — TikTok / Reels / Shorts)

"Build a real AI chatbot in 60 seconds. `pip install anthropic` — one dependency. Create the client. Build a message loop. Pass history on every call — that's how you get memory. Call `messages.create`. Print the reply."

"Want streaming? Swap `create` for `stream`. Tokens appear in real time."

"Want to cut costs 90%? Add `cache_control: ephemeral` to your system prompt."

"That's it. Fourteen lines for a chatbot. Three more for streaming. One field for caching. Full code in bio."

---

## Captions / On-Screen Text Overlays

| Timestamp (short) | Overlay text                          |
|-------------------|---------------------------------------|
| 0:05              | `pip install anthropic`               |
| 0:15              | "14 lines = working chatbot"          |
| 0:30              | "Streaming: swap create → stream"     |
| 0:45              | "Prompt caching = 90% cost savings"   |
| 0:58              | "Full code → link in bio"             |
