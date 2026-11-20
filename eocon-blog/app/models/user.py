from app.db import get_db


def find_user_by_username(username):
    db = get_db()
    return db.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()


def find_user_by_id(user_id):
    db = get_db()
    return db.execute(
        "SELECT * FROM users WHERE id = ?", (user_id,)
    ).fetchone()


def find_user_by_token(token):
    db = get_db()
    return db.execute(
        "SELECT * FROM users WHERE api_token = ?", (token,)
    ).fetchone()


def create_user(username, email, password_hash, role="reader"):
    db = get_db()
    db.execute(
        "INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
        (username, email, password_hash, role)
    )
    db.commit()


def list_users():
    db = get_db()
    return db.execute(
        "SELECT id, username, email, role, created_at FROM users"
    ).fetchall()
