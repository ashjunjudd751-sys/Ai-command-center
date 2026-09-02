from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    conversation_id: str | None = None
    agent_id: str = "general"

class ChatResponse(BaseModel):
    conversation_id: str
    message: str
    agent_id: str
    usage: dict

class AgentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    instructions: str = Field(min_length=1)
    model: str | None = None

class AgentOut(AgentCreate):
    id: str
