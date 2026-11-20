from app.db import get_db


def get_all_tags():
    db = get_db()
    return db.execute("SELECT * FROM tags ORDER BY name").fetchall()


def get_tag_by_slug(slug):
    db = get_db()
    return db.execute(
        "SELECT * FROM tags WHERE slug = ?", (slug,)
    ).fetchone()


def create_tag(name, slug):
    db = get_db()
    db.execute("INSERT INTO tags (name, slug) VALUES (?, ?)", (name, slug))
    db.commit()


def get_posts_by_tag(tag_id):
    db = get_db()
    return db.execute(
        "SELECT p.*, u.username as author_name FROM posts p "
        "JOIN users u ON p.author_id = u.id "
        "JOIN post_tags pt ON p.id = pt.post_id "
        "WHERE pt.tag_id = ? AND p.status = 'published' "
        "ORDER BY p.created_at DESC",
        (tag_id,)
    ).fetchall()


def get_tags_for_post(post_id):
    db = get_db()
    return db.execute(
        "SELECT t.* FROM tags t "
        "JOIN post_tags pt ON t.id = pt.tag_id "
        "WHERE pt.post_id = ?",
        (post_id,)
    ).fetchall()


def get_all_categories():
    db = get_db()
    return db.execute("SELECT * FROM categories ORDER BY name").fetchall()


def get_category_by_slug(slug):
    db = get_db()
    return db.execute(
        "SELECT * FROM categories WHERE slug = ?", (slug,)
    ).fetchone()


def get_posts_by_category(category_id):
    db = get_db()
    return db.execute(
        "SELECT p.*, u.username as author_name FROM posts p "
        "JOIN users u ON p.author_id = u.id "
        "JOIN post_categories pc ON p.id = pc.post_id "
        "WHERE pc.category_id = ? AND p.status = 'published' "
        "ORDER BY p.created_at DESC",
        (category_id,)
    ).fetchall()
