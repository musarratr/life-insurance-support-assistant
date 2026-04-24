import sqlite3
from pathlib import Path
from typing import Dict, List

from app.config import DATABASE_PATH


def get_connection(database_path: Path = DATABASE_PATH) -> sqlite3.Connection:
    database_path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(database_path)


def init_db(database_path: Path = DATABASE_PATH) -> None:
    with get_connection(database_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_messages_session_time
            ON messages (session_id, timestamp)
            """
        )


def save_message(
    session_id: str,
    role: str,
    content: str,
    database_path: Path = DATABASE_PATH,
) -> None:
    with get_connection(database_path) as connection:
        connection.execute(
            """
            INSERT INTO messages (session_id, role, content)
            VALUES (?, ?, ?)
            """,
            (session_id, role, content),
        )


def load_recent_history(
    session_id: str,
    limit: int = 10,
    database_path: Path = DATABASE_PATH,
) -> List[Dict[str, str]]:
    with get_connection(database_path) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            """
            SELECT role, content, timestamp
            FROM messages
            WHERE session_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (session_id, limit),
        ).fetchall()

    return [
        {
            "role": row["role"],
            "content": row["content"],
            "timestamp": row["timestamp"],
        }
        for row in reversed(rows)
    ]


def clear_session(session_id: str, database_path: Path = DATABASE_PATH) -> None:
    with get_connection(database_path) as connection:
        connection.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
