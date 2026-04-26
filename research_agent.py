import anthropic
from typing import Generator

MODEL = "claude-opus-4-7"
MAX_CONTINUATION_TURNS = 5

SYSTEM_PROMPT = """You are a context-aware research assistant with access to web search and web fetch tools.

Your role:
- Research topics thoroughly using current web information
- Maintain and leverage the full conversation history for context-aware, connected responses
- Build progressively deeper understanding across multiple turns
- Synthesize information from multiple sources with clear source citations
- Make explicit connections between new research and prior conversation context

When researching:
1. Search multiple sources for comprehensive and balanced coverage
2. Prioritize recent, authoritative sources
3. Always include source URLs when citing information
4. Reference earlier topics in our conversation when relevant
5. Note important nuances, debates, or uncertainties in the field"""


class ResearchAgent:
    def __init__(self) -> None:
        self.client = anthropic.Anthropic()
        self._sessions: dict[str, list] = {}

    def get_or_create_session(self, session_id: str) -> list:
        return self._sessions.setdefault(session_id, [])

    def clear_session(self, session_id: str) -> bool:
        return self._sessions.pop(session_id, None) is not None

    def get_context_info(self, session_id: str) -> dict:
        messages = self._sessions.get(session_id, [])
        user_turns = [m for m in messages if m["role"] == "user"]
        return {
            "session_id": session_id,
            "turn_count": len(user_turns),
            "has_context": bool(user_turns),
        }

    def research_stream(self, session_id: str, query: str) -> Generator[str, None, None]:
        """Stream Claude's research response, maintaining conversation context."""
        messages = self.get_or_create_session(session_id)
        messages.append({"role": "user", "content": query})

        tools = [
            {"type": "web_search_20260209", "name": "web_search"},
            {"type": "web_fetch_20260209", "name": "web_fetch"},
        ]

        continuations = 0
        while continuations <= MAX_CONTINUATION_TURNS:
            with self.client.messages.stream(
                model=MODEL,
                max_tokens=8192,
                system=SYSTEM_PROMPT,
                thinking={"type": "adaptive"},
                tools=tools,
                messages=messages,
            ) as stream:
                for event in stream:
                    if (
                        event.type == "content_block_delta"
                        and event.delta.type == "text_delta"
                    ):
                        yield event.delta.text

                final = stream.get_final_message()

            messages.append({"role": "assistant", "content": final.content})

            if final.stop_reason != "pause_turn":
                break

            # pause_turn means server-side tool loop hit its limit; re-send to continue
            continuations += 1
