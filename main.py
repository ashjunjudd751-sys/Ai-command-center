import uuid
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .config import FRONTEND_ORIGIN
from .db import init_db, connect
from .models import ChatRequest, ChatResponse, AgentCreate, AgentOut
from .agents import run_agent

app = FastAPI(title="AI Command Center API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if FRONTEND_ORIGIN == "*" else [FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/api/health")
def health():
    return {"ok": True, "service": "ai-command-center", "version": "2.0.0"}

@app.get("/api/agents", response_model=list[AgentOut])
def list_agents():
    with connect() as db:
        rows = db.execute("SELECT id,name,instructions,model FROM agents ORDER BY created_at").fetchall()
    return [dict(r) for r in rows]

@app.post("/api/agents", response_model=AgentOut)
def create_agent(body: AgentCreate):
    agent_id = uuid.uuid4().hex[:12]
    with connect() as db:
        db.execute(
            "INSERT INTO agents(id,name,instructions,model) VALUES(?,?,?,?)",
            (agent_id, body.name, body.instructions, body.model)
        )
        db.commit()
    return {"id": agent_id, **body.model_dump()}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(body: ChatRequest):
    conversation_id = body.conversation_id or uuid.uuid4().hex
    now = datetime.now(timezone.utc).isoformat()

    with connect() as db:
        exists = db.execute("SELECT id FROM conversations WHERE id=?", (conversation_id,)).fetchone()
        if not exists:
            db.execute(
                "INSERT INTO conversations(id,title,agent_id,created_at,updated_at) VALUES(?,?,?,?,?)",
                (conversation_id, body.message[:60], body.agent_id, now, now)
            )
        db.execute(
            "INSERT INTO messages(conversation_id,role,content) VALUES(?,?,?)",
            (conversation_id, "user", body.message)
        )
        db.commit()

    try:
        answer, usage = await run_agent(body.agent_id, conversation_id, body.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    with connect() as db:
        db.execute(
            "INSERT INTO messages(conversation_id,role,content) VALUES(?,?,?)",
            (conversation_id, "assistant", answer)
        )
        db.execute(
            "UPDATE conversations SET updated_at=?, agent_id=? WHERE id=?",
            (now, body.agent_id, conversation_id)
        )
        db.commit()

    return ChatResponse(
        conversation_id=conversation_id,
        message=answer,
        agent_id=body.agent_id,
        usage=usage
    )

@app.get("/api/conversations/{conversation_id}/messages")
def conversation_messages(conversation_id: str):
    with connect() as db:
        rows = db.execute(
            "SELECT role,content,created_at FROM messages WHERE conversation_id=? ORDER BY id",
            (conversation_id,)
        ).fetchall()
    return [dict(r) for r in rows]


app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
