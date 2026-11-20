from app.db import get_db


def get_published_posts(limit=10, offset=0):
    db = get_db()
    return db.execute(
        "SELECT p.*, u.username as author_name FROM posts p "
        "JOIN users u ON p.author_id = u.id "
        "WHERE p.status = 'published' ORDER BY p.created_at DESC "
        "LIMIT ? OFFSET ?",
        (limit, offset)
    ).fetchall()


def get_post_by_slug(slug):
    db = get_db()
    return db.execute(
        "SELECT p.*, u.username as author_name FROM posts p "
        "JOIN users u ON p.author_id = u.id WHERE p.slug = ?",
        (slug,)
    ).fetchone()


def get_post_by_id(post_id):
    db = get_db()
    return db.execute(
        "SELECT * FROM posts WHERE id = ?", (post_id,)
    ).fetchone()


def create_post(title, slug, body, author_id, status="draft"):
    db = get_db()
    db.execute(
        "INSERT INTO posts (title, slug, body, author_id, status) "
        "VALUES (?, ?, ?, ?, ?)",
        (title, slug, body, author_id, status)
    )
    db.commit()


def update_post(post_id, title, body, status):
    db = get_db()
    db.execute(
        "UPDATE posts SET title = ?, body = ?, status = ?, "
        "updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (title, body, status, post_id)
    )
    db.commit()


def delete_post(post_id):
    db = get_db()
    db.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    db.commit()


def count_published_posts():
    db = get_db()
    row = db.execute(
        "SELECT COUNT(*) FROM posts WHERE status = 'published'"
    ).fetchone()
    return row[0]


def search_posts(query):
    db = get_db()
    pattern = "%{}%".format(query)
    return db.execute(
        "SELECT p.*, u.username as author_name FROM posts p "
        "JOIN users u ON p.author_id = u.id "
        "WHERE p.status = 'published' AND (p.title LIKE ? OR p.body LIKE ?) "
        "ORDER BY p.created_at DESC",
        (pattern, pattern)
    ).fetchall()
