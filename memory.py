from agents import SQLiteSession

_sessions: dict[str, SQLiteSession] = {}

def get_session(conversation_id: str) -> SQLiteSession:
    if conversation_id not in _sessions:
        _sessions[conversation_id] = SQLiteSession(
            f"conversation_{conversation_id}",
            db_path="./data/agent_sessions.db"
        )
    return _sessions[conversation_id]
