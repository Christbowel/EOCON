import json
from app.db import get_db


def export_posts(fmt="json"):
    db = get_db()
    posts = db.execute(
        "SELECT p.id, p.title, p.slug, p.body, p.status, p.created_at, "
        "u.username as author FROM posts p JOIN users u ON p.author_id = u.id"
    ).fetchall()

    result = []
    for p in posts:
        result.append({
            "id": p["id"],
            "title": p["title"],
            "slug": p["slug"],
            "body": p["body"],
            "status": p["status"],
            "created_at": p["created_at"],
            "author": p["author"],
        })

    if fmt == "json":
        return json.dumps({"posts": result}, indent=2)

    lines = []
    for p in result:
        lines.append("---")
        lines.append("title: {}".format(p["title"]))
        lines.append("slug: {}".format(p["slug"]))
        lines.append("author: {}".format(p["author"]))
        lines.append("status: {}".format(p["status"]))
        lines.append("---")
        lines.append(p["body"])
        lines.append("")
    return "\n".join(lines)


def export_comments():
    db = get_db()
    comments = db.execute(
        "SELECT * FROM comments ORDER BY post_id, created_at"
    ).fetchall()
    return json.dumps({"comments": [dict(c) for c in comments]}, indent=2)
