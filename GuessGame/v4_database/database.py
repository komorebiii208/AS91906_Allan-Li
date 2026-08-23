"""
database.py
SQLite persistence layer for the Ranui Family Clothing Allowance App.
"""


import sqlite3
import os
from datetime import datetime


db_path = os.path.join(os.path.dirname(__file__), "data", "guess_game.db")


def get_connection():
    """Get connection to database"""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return sqlite3.connect(db_path)


def init_db():
    """Create tables if they don't exist."""
    with get_connection() as conn:
        cur = conn.cursor()


        # Create users table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id              INTEGER     PRIMARY KEY AUTOINCREMENT,
                username        TEXT        NOT NULL UNIQUE,
                password        TEXT        NOT NULL,
                highest_score   INTEGER     NOT NULL DEFAULT 0,
                total_score     INTEGER     NOT NULL DEFAULT 0
            )
        """)

        # Create game_records table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS game_records (
                id              INTEGER     PRIMARY KEY AUTOINCREMENT,
                username        TEXT        NOT NULL,
                game_id         INTEGER     NOT NULL,
                score           INTEGER     NOT NULL,
                timestamp       TEXT        NOT NULL
            )
        """)

        # Create games table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS games (
                id              INTEGER     PRIMARY KEY AUTOINCREMENT,
                title           TEXT        NOT NULL,
                cover_color     TEXT        NOT NULL DEFAULT '#1a6fa1'
            )
        """)

        # Create questions table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id              INTEGER     PRIMARY KEY AUTOINCREMENT,
                game_id         INTEGER     NOT NULL,
                question_text   TEXT        NOT NULL,
                option_a        TEXT        NOT NULL,
                option_b        TEXT        NOT NULL,
                option_c        TEXT        NOT NULL,
                option_d        TEXT        NOT NULL,
                correct_answer  TEXT        NOT NULL,
                FOREIGN KEY (game_id) REFERENCES games (id)
            )
        """)



        cur.execute("SELECT COUNT(*) FROM users")
        if cur.fetchone()[0] == 0:
            cur.execute(
                "INSERT INTO users (username, password, highest_score, total_score)"
                "VALUES (?, ?, ?, ?)",
                ("Default User", "123456", 0, 0)
            )

        conn.commit()



# ── User ────────────────────────────────────────────────

def get_user(username: str) -> dict:
    """Obtain user info"""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT username, password, highest_score, total_score FROM users WHERE username=?",
            (username,)
        )
        row = cur.fetchone()
        if row:
            return {
                "username": row[0],
                "password": row[1],
                "highest_score": row[2],
                "total_score": row[3]
            }
        return None

def verify_user(username: str, password: str) -> bool:
    """Verify user credentials"""
    user = get_user(username)
    if user and user["password"] == password:
        return True
    return False

def register_user(username: str, password: str) -> bool:
    """Register a new user"""
    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO users (username, password, highest_score, total_score) VALUES (?, ?, 0, 0)",
                (username, password)
            )
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False



# ── Game ──────────────────────────────────────────────────────────

def get_all_games() -> list[dict]:
    """Get all games"""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, title, cover_color FROM games")
        return [
            {"id": row[0], "title": row[1], "cover_colour": row[2]}
            for row in cur.fetchall()
        ]


def get_questions_by_game_id(game_id: int) -> list[dict]:
    """Get all questions for a specific game"""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT question_text, option_a, option_b, option_c, option_d, correct_answer "
            "FROM questions WHERE game_id=?",
            (game_id,)
        )
        return [
            {
                "question": row[0],
                "options": [row[1], row[2], row[3], row[4]],
                "correct_answer": row[5]
            }
            for row in cur.fetchall()
        ]

# ── Update user scores ────────────────────────────────────────────

def update_user_score_in_db(username: str, new_score: int, game_id: int = 1):
    """Update user's score"""
    user = get_user(username)
    if not user:
        return

    # Calculate new highest and total scores
    highest = max(user["highest_score"], new_score)
    total = user["total_score"] + new_score

    with get_connection() as conn:
        conn.execute(
            "UPDATE users SET highest_score=?, total_score=? WHERE username=?",
            (highest, total, username)
        )

        conn.execute(
            "INSERT INTO game_records (username, game_id, score, timestamp) VALUES (?, ?, ?, ?)",
            (username, game_id, new_score, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )

        conn.commit()

    return {"highest_score": highest, "total_score": total}


def get_game_history(username: str = None) -> list[dict]:
    """Get game history"""
    with get_connection() as conn:
        cur = conn.cursor()
        if username:
            cur.execute(
                "SELECT username, game_id, score, timestamp"
                "FROM game_records"
                "WHERE username=?"
                "ORDER BY timestamp DESC",
                (username,)
            )
        else:
            cur.execute(
                "SELECT username, game_id, score, timestamp"
                "FROM game_records"
                "ORDER BY timestamp DESC"
            )

        cols = ["username", "game_id", "score", "timestamp"]
        return [dict(zip(cols, row)) for row in cur.fetchall()]
