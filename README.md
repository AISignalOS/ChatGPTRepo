# Research Agent — Context-Aware AI Tool Directory

A compound productivity loop: browse the web, automatically catalogue AI tools you encounter, and surface what's trending — powered by your choice of any major language model.

```
Chrome Extension  ──►  FastAPI Backend  ──►  SQLite DB
      │                      │
      │               Claude / GPT-4o /        React Directory
      │               Gemini / Grok /     ◄──  (with analytics)
      │               Ollama / ...
      │
      └──────────────────────────────────────►  CLI Tool
```

**The compounding loop:**
1. Extension detects AI tool pages as you browse and sends content to the backend
2. Backend generates a "Signal Summary" via an LLM (use case tags, price tier, audience)
3. Summaries auto-populate the Tool Directory website
4. Click analytics surface which tools get the most attention
5. Trending data informs your next deep-dive research

---

## Components

| Component | Location | Stack |
|---|---|---|
| API backend | `backend/` | Python, FastAPI, SQLAlchemy, SQLite |
| Chrome extension | `extension/` | Manifest V3, vanilla JS |
| Tool directory | `frontend/` | React 18, Vite, Recharts |
| CLI | `cli/` | Python, Click, Rich |

---

## Quick Start

### 1. Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp ../.env.example .env
# Edit .env — set MODEL_PROVIDER and the matching API key
```

```bash
uvicorn main:app --reload --port 8000
# API docs: http://localhost:8000/docs
# Health:   http://localhost:8000/health
```

The SQLite database (`research_agent.db`) is created automatically on first run.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev      # http://localhost:5173
```

### 3. Chrome Extension

1. Open `chrome://extensions` in Chrome
2. Enable **Developer mode** (top-right toggle)
3. Click **Load unpacked** → select the `extension/` folder
4. Visit an AI tool site — it will be detected and submitted automatically
5. Click the extension icon to see recent captures
6. Use the **Options** page to change the backend API URL if needed (default: `http://localhost:8000`)

### 4. CLI

```bash
cd cli
pip install -e .

research-agent --help
research-agent add https://cursor.com
research-agent list --price-tier freemium
research-agent trending
research-agent summary cursor
```

---

## Configuration

All configuration is via environment variables in `backend/.env`.

### Choosing a provider

Set `MODEL_PROVIDER` to one of the values below. Set `MODEL_NAME` to override the default model.

#### Frontier / cloud

| `MODEL_PROVIDER` | Default model | API key env var |
|---|---|---|
| `anthropic` **(default)** | `claude-sonnet-4-6` | `ANTHROPIC_API_KEY` |
| `openai` | `gpt-4o` | `OPENAI_API_KEY` |
| `google` | `gemini-2.0-flash` | `GOOGLE_API_KEY` |
| `xai` | `grok-3` | `XAI_API_KEY` |
| `mistral` | `mistral-large-latest` | `MISTRAL_API_KEY` |
| `groq` | `llama-3.3-70b-versatile` | `GROQ_API_KEY` |
| `deepseek` | `deepseek-chat` | `DEEPSEEK_API_KEY` |
| `together` | `meta-llama/Llama-3.3-70b-instruct-turbo` | `TOGETHER_API_KEY` |
| `perplexity` | `sonar-pro` | `PERPLEXITY_API_KEY` |
| `cohere` | `command-r-plus` | `COHERE_API_KEY` |

#### Aggregators (one key, many models)

| `MODEL_PROVIDER` | Default model | API key env var |
|---|---|---|
| `openrouter` | `mistralai/mistral-7b-instruct` | `OPENROUTER_API_KEY` |

With OpenRouter you can set `MODEL_NAME` to any model slug, e.g. `openai/gpt-4o`, `google/gemini-2.0-flash`, `meta-llama/llama-3.3-70b`.

#### Local / self-hosted

| `MODEL_PROVIDER` | Default model | Config |
|---|---|---|
| `ollama` | `llama3.2` | `OLLAMA_BASE_URL` (default: `http://localhost:11434`) |

#### Custom OpenAI-compatible endpoint

```env
MODEL_PROVIDER=custom
CUSTOM_BASE_URL=https://your-endpoint.example.com/v1
CUSTOM_API_KEY=your-key
MODEL_NAME=your-model-name
```

Works with any provider that exposes an OpenAI-compatible chat completions API.

### Example `.env` files

**Anthropic (default):**
```env
MODEL_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
```

**GPT-4o:**
```env
MODEL_PROVIDER=openai
OPENAI_API_KEY=sk-...
MODEL_NAME=gpt-4o
```

**Gemini 2.0 Flash:**
```env
MODEL_PROVIDER=google
GOOGLE_API_KEY=AIza...
```

**Grok 3:**
```env
MODEL_PROVIDER=xai
XAI_API_KEY=xai-...
```

**Local Llama via Ollama:**
```env
MODEL_PROVIDER=ollama
MODEL_NAME=llama3.2
```

**DeepSeek R1:**
```env
MODEL_PROVIDER=deepseek
DEEPSEEK_API_KEY=sk-...
MODEL_NAME=deepseek-reasoner
```

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/api/tools` | Submit a tool (triggers LLM summarisation) |
| `GET` | `/api/tools` | List tools — supports `?use_case=`, `?price_tier=`, `?search=`, `?limit=` |
| `GET` | `/api/tools/{id}` | Get a single tool (increments view count) |
| `POST` | `/api/tools/{id}/click` | Track a click (increments click count) |
| `GET` | `/api/analytics` | Top tools by click count — supports `?limit=` |

Interactive docs available at `http://localhost:8000/docs` when the backend is running.

---

## CLI Reference

```
research-agent [--api-url URL] COMMAND

Commands:
  add <url>               Scrape a URL, generate a Signal Summary, and store it
  list                    List tools in the directory
    --use-case TEXT       Filter by use case tag
    --price-tier CHOICE   Filter by price tier (free|freemium|paid|enterprise)
    --search TEXT         Full-text search across name and summary
  trending [--limit N]    Show most-clicked tools
  summary <query>         Show the Signal Summary for a tool by name or URL

Environment:
  RESEARCH_AGENT_API_URL  Backend URL (default: http://localhost:8000)
```

---

## Project Structure

```
ChatGPTRepo/
├── .env.example                    # All config options with documentation
├── .gitignore
│
├── backend/
│   ├── requirements.txt
│   ├── main.py                     # FastAPI app entry point
│   ├── database.py                 # SQLAlchemy engine + session
│   ├── models.py                   # Tool, AnalyticsEvent ORM models
│   ├── schemas.py                  # Pydantic request/response schemas
│   ├── routers/
│   │   ├── tools.py                # POST /api/tools, GET /api/tools
│   │   ├── analytics.py            # POST /api/tools/{id}/click, GET /api/analytics
│   │   └── health.py               # GET /health
│   └── services/
│       ├── ai_service.py           # Multi-provider LLM abstraction
│       ├── claude_service.py       # Original Anthropic-only implementation
│       └── tool_service.py         # Upsert logic + URL normalisation
│
├── extension/
│   ├── manifest.json               # Chrome Manifest V3
│   ├── background/
│   │   └── service_worker.js       # Receives page data, POSTs to API
│   ├── content/
│   │   └── detector.js             # Heuristic AI tool detection + scraping
│   ├── popup/                      # Extension popup (recent captures)
│   └── options/                    # Settings page (API URL)
│
├── frontend/
│   ├── package.json                # React 18, Vite, Recharts
│   ├── vite.config.js              # Dev proxy: /api → localhost:8000
│   └── src/
│       ├── App.jsx
│       ├── api.js                  # Fetch wrappers
│       └── components/
│           ├── ToolCard.jsx        # Tool card with summary, tags, price badge
│           ├── FilterBar.jsx       # Use case / price / search filters
│           ├── ToolGrid.jsx        # Responsive card grid
│           └── AnalyticsDashboard.jsx  # Recharts bar chart of top tools
│
└── cli/
    ├── setup.py
    ├── requirements.txt            # click, httpx, rich, beautifulsoup4
    └── research_agent/
        └── cli.py                  # add, list, trending, summary commands
```

---

## How the Extension Works

The content script (`extension/content/detector.js`) runs on every page and scores it for AI tool signals:

- **+2 points** per AI keyword found (`"llm"`, `"generative ai"`, `"claude"`, etc.)
- **+1 point** per pricing indicator (`"per month"`, `"free plan"`, etc.)
- **+1 point** per structural element (`[class*='pricing']`, `[class*='hero']`, etc.)

Pages scoring **≥ 4** are submitted to the backend. The service worker deduplicates submissions within a browser session using `chrome.storage.session`.

---

## Signal Summary Format

Every tool stored in the directory has a structured Signal Summary generated by the configured LLM:

```json
{
  "signal_summary": "Cursor is an AI-first code editor built on VS Code that integrates LLM assistance directly into the editing workflow. It offers inline code generation, multi-file context awareness, and chat-based refactoring for developers.",
  "use_cases": ["code-generation", "productivity", "writing-assistance"],
  "price_tier": "freemium",
  "target_audience": "software developers"
}
```

The Anthropic provider additionally uses **prompt caching** (`cache_control: ephemeral`) on the system prompt, reducing latency and token cost on repeated calls.

---

## Development Notes

- The Vite dev proxy (`/api → http://localhost:8000`) means the frontend never directly hits the backend from the browser, avoiding CORS issues during development.
- The backend uses `allow_origins=["*"]` so the Chrome extension (which has no fixed origin) can POST directly to `http://localhost:8000`.
- `click_count` updates use a SQL-level `UPDATE ... SET click_count = click_count + 1` to avoid race conditions under concurrent requests.
- URL normalisation (lowercase host, strip query params and fragments) prevents duplicate entries when the same tool is visited with different tracking parameters.
