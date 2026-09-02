# AI Command Center V2 — Real Application Architecture

This is the first real application architecture for the AI dashboard.

## Stack
- Frontend: plain HTML/CSS/JS (easy to replace with React/Next later)
- Backend: FastAPI
- AI orchestration: OpenAI Agents SDK
- Persistence: SQLite
- Sessions: SQLite-backed agent session memory
- API: REST endpoints
- Environment secrets: `.env`

## Features in this architecture
- Health endpoint
- Conversations
- Persistent chat messages
- Agent registry
- Custom agent creation
- Agent selection
- Real AI execution through the Agents SDK
- Session memory per conversation
- Usage metadata
- Basic tool architecture
- CORS for local frontend development

## Run

1. Install Python 3.11+.
2. From the project folder:

   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate

3. Install:
   pip install -r backend/requirements.txt

4. Create `.env` from `.env.example` and add your API key.

5. Start backend:
   uvicorn backend.app.main:app --reload --port 8000

6. Open `frontend/index.html` in your browser.

The frontend expects the API at http://localhost:8000.

IMPORTANT: Never put your API key in frontend JavaScript.

## Architecture

frontend/
  index.html

backend/
  app/
    main.py       API entrypoint
    db.py         SQLite schema and access
    models.py     Pydantic request/response models
    agents.py     Agent factory + orchestration
    memory.py     Session management
    tools.py      Tool definitions
    config.py     Environment configuration

## Next V3 targets
- Authentication/users
- PostgreSQL
- Vector-store knowledge
- Web search
- File uploads
- Streaming responses
- Agent handoffs
- Tool permissions/approvals
- Project workspaces
- Background jobs
- Observability dashboard
