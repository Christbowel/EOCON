import os
import pickle
from app.auth.session import require_role
from app.db import get_db

IMPORT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "imports"
)


def import_content(filename):
    user = require_role("admin")
    if not user:
        raise PermissionError("Admin required")

    filepath = os.path.join(IMPORT_DIR, filename)
    if not os.path.isfile(filepath):
        raise FileNotFoundError("Import file not found")

    with open(filepath, "rb") as f:
        data = pickle.loads(f.read())

    db = get_db()
    for post in data.get("posts", []):
        db.execute(
            "INSERT INTO posts (title, slug, body, author_id, status) "
            "VALUES (?, ?, ?, ?, ?)",
            (post["title"], post["slug"], post["body"], post["author_id"], "draft")
        )
    db.commit()
    return len(data.get("posts", []))
