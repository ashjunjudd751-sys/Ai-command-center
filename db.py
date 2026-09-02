import sqlite3
from pathlib import Path
from .config import DATABASE_PATH

def connect():
    path = Path(DATABASE_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect() as db:
        db.executescript('''
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            agent_id TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS agents (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            instructions TEXT NOT NULL,
            model TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        db.execute(
            "INSERT OR IGNORE INTO agents(id,name,instructions,model) VALUES(?,?,?,?)",
            ("general", "General Assistant",
             "You are the primary assistant for an AI command center. Be useful, accurate, clear, and honest about uncertainty.", None)
        )
        db.execute(
            "INSERT OR IGNORE INTO agents(id,name,instructions,model) VALUES(?,?,?,?)",
            ("research", "Research Agent",
             "You are a research specialist. Separate facts from assumptions and clearly state uncertainty.", None)
        )
        db.execute(
            "INSERT OR IGNORE INTO agents(id,name,instructions,model) VALUES(?,?,?,?)",
            ("coding", "Coding Agent",
             "You are a senior software engineer. Produce maintainable code and explain important implementation choices.", None)
        )
        db.commit()
