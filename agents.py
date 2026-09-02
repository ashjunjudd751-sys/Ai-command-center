from agents import Agent, Runner
from .config import OPENAI_API_KEY, OPENAI_MODEL
from .db import connect
from .memory import get_session
from .tools import get_system_status

def get_agent_config(agent_id: str):
    with connect() as db:
        row = db.execute("SELECT * FROM agents WHERE id=?", (agent_id,)).fetchone()
    if not row:
        raise ValueError("Agent not found")
    return dict(row)

async def run_agent(agent_id: str, conversation_id: str, user_message: str):
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not configured on the server.")

    cfg = get_agent_config(agent_id)
    agent = Agent(
        name=cfg["name"],
        instructions=cfg["instructions"],
        model=cfg["model"] or OPENAI_MODEL,
        tools=[get_system_status],
    )
    session = get_session(conversation_id)
    result = await Runner.run(agent, user_message, session=session)
    usage = result.context_wrapper.usage
    return result.final_output, {
        "requests": usage.requests,
        "input_tokens": usage.input_tokens,
        "output_tokens": usage.output_tokens,
        "total_tokens": usage.total_tokens,
    }
