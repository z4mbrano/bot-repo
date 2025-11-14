import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).parent / "data.db"

CREATE_USERS = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    username TEXT,
    password_hash TEXT NOT NULL
);
"""

CREATE_CHAT_HISTORY = """
CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    bot_name TEXT NOT NULL,
    title TEXT NOT NULL,
    messages TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
"""


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(CREATE_USERS)
    cur.execute(CREATE_CHAT_HISTORY)
    # Commit creation of tables
    conn.commit()

    # Ensure existing DB has the username column in users table
    cur.execute("PRAGMA table_info(users)")
    cols = [r[1] for r in cur.fetchall()]
    if 'username' not in cols:
        try:
            cur.execute("ALTER TABLE users ADD COLUMN username TEXT")
            conn.commit()
        except Exception:
            # If alter fails, ignore (older SQLite versions or other edge cases)
            pass
    conn.close()


# User helpers
def create_user(email: str, password_hash: str, username: str = None):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (email, username, password_hash) VALUES (?, ?, ?)", (email, username, password_hash))
        conn.commit()
        user_id = cur.lastrowid
    except sqlite3.IntegrityError:
        conn.close()
        return None
    conn.close()
    return user_id


def get_user_by_email(email: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, email, username, password_hash FROM users WHERE email = ?", (email,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def get_user_by_id(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, email FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


# Chat helpers
def create_chat(user_id: int, bot_name: str, title: str, messages: list):
    messages_blob = json.dumps(messages, ensure_ascii=False)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO chat_history (user_id, bot_name, title, messages) VALUES (?, ?, ?, ?)",
        (user_id, bot_name, title, messages_blob),
    )
    conn.commit()
    chat_id = cur.lastrowid
    conn.close()
    return chat_id


def update_chat(chat_id: int, user_id: int, messages: list):
    messages_blob = json.dumps(messages, ensure_ascii=False)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE chat_history SET messages = ? WHERE id = ? AND user_id = ?",
        (messages_blob, chat_id, user_id),
    )
    conn.commit()
    updated = cur.rowcount
    conn.close()
    return updated > 0


def list_chats_for_user(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, bot_name, title, created_at FROM chat_history WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,),
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_chat_messages(chat_id: int, user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, messages FROM chat_history WHERE id = ? AND user_id = ?", (chat_id, user_id))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    # messages stored as JSON string
    try:
        messages = json.loads(row["messages"]) if row["messages"] else []
    except Exception:
        messages = []
    return {"id": row["id"], "messages": messages}


def delete_chat(chat_id: int, user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM chat_history WHERE id = ? AND user_id = ?", (chat_id, user_id))
    conn.commit()
    deleted = cur.rowcount
    conn.close()
    return deleted > 0
