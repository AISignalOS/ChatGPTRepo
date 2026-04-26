import asyncio
import json
import queue
import threading
import uuid

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel

from research_agent import ResearchAgent

app = FastAPI(title="Context-Aware Research Agent")
agent = ResearchAgent()


class ResearchQuery(BaseModel):
    query: str
    session_id: str | None = None


@app.get("/", response_class=HTMLResponse)
async def serve_ui() -> str:
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()


@app.post("/api/research")
async def research(req: ResearchQuery) -> StreamingResponse:
    session_id = req.session_id or str(uuid.uuid4())
    q: queue.Queue = queue.Queue()
    sentinel = object()

    def run_sync() -> None:
        try:
            for chunk in agent.research_stream(session_id, req.query):
                q.put(chunk)
        except Exception as exc:
            q.put(exc)
        finally:
            q.put(sentinel)

    threading.Thread(target=run_sync, daemon=True).start()

    async def event_stream():
        yield f"data: {json.dumps({'type': 'session', 'session_id': session_id})}\n\n"
        loop = asyncio.get_event_loop()

        while True:
            item = await loop.run_in_executor(None, q.get)

            if item is sentinel:
                yield f"data: {json.dumps({'type': 'done'})}\n\n"
                break
            if isinstance(item, Exception):
                yield f"data: {json.dumps({'type': 'error', 'message': str(item)})}\n\n"
                break
            if isinstance(item, str):
                yield f"data: {json.dumps({'type': 'text', 'content': item})}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.get("/api/context/{session_id}")
async def get_context(session_id: str) -> dict:
    return agent.get_context_info(session_id)


@app.delete("/api/sessions/{session_id}")
async def clear_session(session_id: str) -> dict:
    cleared = agent.clear_session(session_id)
    return {"cleared": cleared, "session_id": session_id}
