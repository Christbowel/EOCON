from app.db import get_db


def get_comments_for_post(post_id):
    db = get_db()
    return db.execute(
        "SELECT * FROM comments WHERE post_id = ? ORDER BY created_at ASC",
        (post_id,)
    ).fetchall()


def create_comment(post_id, author_name, body):
    db = get_db()
    db.execute(
        "INSERT INTO comments (post_id, author_name, body) VALUES (?, ?, ?)",
        (post_id, author_name, body)
    )
    db.commit()


def delete_comment(comment_id):
    db = get_db()
    db.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
    db.commit()
