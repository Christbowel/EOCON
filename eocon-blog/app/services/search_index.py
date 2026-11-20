from app.db import get_db


def rebuild_index():
    db = get_db()
    posts = db.execute(
        "SELECT id, title, body FROM posts WHERE status = 'published'"
    ).fetchall()

    index = {}
    for post in posts:
        words = set()
        for field in [post["title"], post["body"]]:
            tokens = field.lower().split()
            for token in tokens:
                cleaned = "".join(c for c in token if c.isalnum())
                if len(cleaned) > 2:
                    words.add(cleaned)
        for word in words:
            if word not in index:
                index[word] = []
            index[word].append(post["id"])

    return index


def search_index(query):
    index = rebuild_index()
    terms = query.lower().split()
    results = set()
    for term in terms:
        cleaned = "".join(c for c in term if c.isalnum())
        if cleaned in index:
            results.update(index[cleaned])
    return list(results)
